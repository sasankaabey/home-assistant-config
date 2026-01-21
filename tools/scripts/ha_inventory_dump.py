#!/usr/bin/env python3
"""
ha_inventory_dump.py — Inventory dump utility

Purpose:
  Dumps Home Assistant entities/devices/services to a file for auditing and cleanup work.

Usage:
  python3 tools/scripts/ha_inventory_dump.py [args]

Notes:
  Useful before refactors and registry cleanups.
"""

import argparse
import asyncio
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import websockets

DEFAULT_BASE_URLS = [
    "http://192.168.4.141:8123",
    "https://evcjv8cnjndmqevolt32uwvhs94papom.ui.nabu.casa",
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

        requests = [
            ("areas", "config/area_registry/list"),
            ("devices", "config/device_registry/list"),
            ("entities", "config/entity_registry/list"),
        ]

        results: dict[str, Any] = {}
        msg_id = 1
        for label, req_type in requests:
            await ws.send(json.dumps({"id": msg_id, "type": req_type}))
            while True:
                response = json.loads(await ws.recv())
                if response.get("id") != msg_id:
                    continue
                if not response.get("success"):
                    raise RuntimeError(f"{req_type} failed: {response}")
                results[label] = response.get("result")
                break
            msg_id += 1
        return results


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Dump HA registries (areas/devices/entities) and optional states",
    )
    parser.add_argument(
        "--base-url",
        help="Override HA base URL (defaults to probing known URLs)",
    )
    parser.add_argument(
        "--out",
        default="ha_inventory.json",
        help="Output JSON file",
    )
    parser.add_argument(
        "--include-states",
        action="store_true",
        help="Include /api/states in output (can be large)",
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

    payload: dict[str, Any] = {
        "base_url": base_url,
        "areas": registries.get("areas", []),
        "devices": registries.get("devices", []),
        "entities": registries.get("entities", []),
    }

    if args.include_states:
        try:
            _, states = request_json(base_url, "/api/states")
            payload["states"] = states
        except Exception as exc:
            print(f"Failed to fetch states: {exc}", file=sys.stderr)
            return 1

    Path(args.out).write_text(json.dumps(payload, indent=2))
    print(f"Wrote inventory to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
