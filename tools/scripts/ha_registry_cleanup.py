#!/usr/bin/env python3
import argparse
import asyncio
import json
import sys
import urllib.request
from pathlib import Path
from typing import Any

import websockets

DEFAULT_BASE_URLS = [
    "http://192.168.4.141:8123",
    "https://evcjv8cnjndmqevolt32uwvhs94papom.ui.nabu.casa",
]

# Tuya device IDs that exist in both cloud and local integrations.
TUYA_SHARED_IDS = [
    "eb091e364d198b733eb49o",
    "eb0bb2197162ccb50c7qyx",
    "eb0f5ddc2c9008be0ahhe2",
    "eb14ff2bbc715ae70bcxag",
    "eb399baf125748a73ct36d",
    "eb464489cfc5a591acfcn2",
    "eb4a1d55b2bd137a6cbd9h",
    "eb59b5cb8a02b5c58doeh4",
    "eb795ac41154770a9bwhel",
    "ebb9bd800dd8c3e5afd3s9",
    "ebcb920c5cd08f54bbahnr",
    "ebe5ac0c9b1ad9b4f6wpvz",
    "ebf729d83efcdab9a8pskm",
    "ebf7e0ad003f674b2dwffk",
]

# Staircase bulbs (local Tuya) to rename 1-8.
STAIRCASE_BULBS = [
    "eb091e364d198b733eb49o",
    "eb0bb2197162ccb50c7qyx",
    "eb399baf125748a73ct36d",
    "eb4a1d55b2bd137a6cbd9h",
    "ebb9bd800dd8c3e5afd3s9",
    "ebcb920c5cd08f54bbahnr",
    "ebe5ac0c9b1ad9b4f6wpvz",
    "ebf729d83efcdab9a8pskm",
]


def load_token() -> str:
    token_path = Path.home() / ".ha_token"
    return token_path.read_text().strip()


def request_json(base_url: str, path: str, method: str = "GET", body=None, timeout: int = 10):
    url = base_url.rstrip("/") + path
    headers = {
        "Authorization": f"Bearer {load_token()}",
        "Content-Type": "application/json",
    }
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, headers=headers, data=data, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        payload = json.loads(resp.read())
        return resp.status, payload


def pick_base_url(base_urls: list[str]) -> str:
    for base_url in base_urls:
        try:
            request_json(base_url, "/api/config", timeout=5)
            return base_url
        except Exception:
            continue
    raise RuntimeError("No reachable HA base URL")


def to_ws_url(base_url: str) -> str:
    if base_url.startswith("https://"):
        return "wss://" + base_url[len("https://") :].rstrip("/") + "/api/websocket"
    if base_url.startswith("http://"):
        return "ws://" + base_url[len("http://") :].rstrip("/") + "/api/websocket"
    return base_url.rstrip("/") + "/api/websocket"


async def ws_request(ws, msg_id: int, payload: dict[str, Any]) -> Any:
    await ws.send(json.dumps({"id": msg_id, **payload}))
    while True:
        response = json.loads(await ws.recv())
        if response.get("id") != msg_id:
            continue
        if not response.get("success"):
            raise RuntimeError(f"Request failed: {response}")
        return response.get("result")


async def fetch_registries(base_url: str) -> dict[str, Any]:
    ws_url = to_ws_url(base_url)
    token = load_token()
    async with websockets.connect(ws_url, max_size=None) as ws:
        auth_msg = json.loads(await ws.recv())
        if auth_msg.get("type") != "auth_required":
            raise RuntimeError(f"Unexpected auth message: {auth_msg}")
        await ws.send(json.dumps({"type": "auth", "access_token": token}))
        auth_resp = json.loads(await ws.recv())
        if auth_resp.get("type") != "auth_ok":
            raise RuntimeError(f"Auth failed: {auth_resp}")

        registries = {}
        msg_id = 1
        for label, req_type in (
            ("areas", "config/area_registry/list"),
            ("devices", "config/device_registry/list"),
            ("entities", "config/entity_registry/list"),
        ):
            registries[label] = await ws_request(ws, msg_id, {"type": req_type})
            msg_id += 1
        return registries


async def apply_actions(base_url: str, actions: list[dict[str, Any]]) -> None:
    ws_url = to_ws_url(base_url)
    token = load_token()
    async with websockets.connect(ws_url, max_size=None) as ws:
        auth_msg = json.loads(await ws.recv())
        if auth_msg.get("type") != "auth_required":
            raise RuntimeError(f"Unexpected auth message: {auth_msg}")
        await ws.send(json.dumps({"type": "auth", "access_token": token}))
        auth_resp = json.loads(await ws.recv())
        if auth_resp.get("type") != "auth_ok":
            raise RuntimeError(f"Auth failed: {auth_resp}")

        msg_id = 1
        for action in actions:
            await ws_request(ws, msg_id, action)
            msg_id += 1


def build_identifier_map(devices: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    lookup = {}
    for dev in devices:
        for ident in dev.get("identifiers", []) or []:
            if isinstance(ident, (list, tuple)) and len(ident) == 2:
                lookup[(ident[0], ident[1])] = dev
    return lookup


def build_actions(registries: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    devices = registries.get("devices", [])
    entities = registries.get("entities", [])
    areas = registries.get("areas", [])

    area_by_name = {a.get("name", "").lower(): a.get("area_id") for a in areas}
    dining_room_area = area_by_name.get("dining room")

    identifier_map = build_identifier_map(devices)

    actions: list[dict[str, Any]] = []
    warnings: list[str] = []

    # Rename staircase bulbs (local Tuya) to Staircase Bulb 1-8.
    for idx, tuya_id in enumerate(sorted(STAIRCASE_BULBS), start=1):
        dev = identifier_map.get(("tuya_local", tuya_id))
        if not dev:
            warnings.append(f"Missing local device for staircase bulb {tuya_id}")
            continue
        target_name = f"Staircase Bulb {idx}"
        if dev.get("name_by_user") != target_name:
            actions.append(
                {
                    "type": "config/device_registry/update",
                    "device_id": dev["id"],
                    "name_by_user": target_name,
                }
            )

    # Set smoke detector area (local Tuya) to Dining Room.
    smoke_local = identifier_map.get(("tuya_local", "eb14ff2bbc715ae70bcxag"))
    if smoke_local:
        if dining_room_area and smoke_local.get("area_id") != dining_room_area:
            actions.append(
                {
                    "type": "config/device_registry/update",
                    "device_id": smoke_local["id"],
                    "area_id": dining_room_area,
                }
            )
    else:
        warnings.append("Missing local smoke detector device for eb14ff2bbc715ae70bcxag")

    # Disable cloud Tuya devices/entities that are duplicated by local.
    cloud_device_ids = []
    for tuya_id in TUYA_SHARED_IDS:
        dev = identifier_map.get(("tuya", tuya_id))
        if not dev:
            warnings.append(f"Missing cloud Tuya device for {tuya_id}")
            continue
        cloud_device_ids.append(dev["id"])
        if dev.get("disabled_by") != "user":
            actions.append(
                {
                    "type": "config/device_registry/update",
                    "device_id": dev["id"],
                    "disabled_by": "user",
                }
            )

    # Disable entities attached to cloud devices.
    for ent in entities:
        if ent.get("device_id") not in cloud_device_ids:
            continue
        if ent.get("disabled_by") == "user":
            continue
        actions.append(
            {
                "type": "config/entity_registry/update",
                "entity_id": ent["entity_id"],
                "disabled_by": "user",
            }
        )

    return actions, warnings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Cleanup HA registry for Tuya cloud/local duplicates.",
    )
    parser.add_argument(
        "--base-url",
        help="Override HA base URL (defaults to probing known URLs)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply changes (default is dry-run)",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    base_url = args.base_url or pick_base_url(DEFAULT_BASE_URLS)

    try:
        registries = asyncio.run(fetch_registries(base_url))
    except Exception as exc:
        print(f"Failed to fetch registries: {exc}", file=sys.stderr)
        return 1

    actions, warnings = build_actions(registries)
    if warnings:
        print("Warnings:")
        for item in warnings:
            print(f"- {item}")

    if not actions:
        print("No changes needed.")
        return 0

    print(f"Planned changes: {len(actions)}")
    if not args.apply:
        print("Dry-run only. Re-run with --apply to execute.")
        return 0

    try:
        asyncio.run(apply_actions(base_url, actions))
    except Exception as exc:
        print(f"Failed to apply updates: {exc}", file=sys.stderr)
        return 1

    print("Registry updates applied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
