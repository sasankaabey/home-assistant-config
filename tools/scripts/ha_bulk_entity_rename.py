#!/usr/bin/env python3
import argparse
import asyncio
import json
import re
import unicodedata
from pathlib import Path
from typing import Any

import websockets

DEFAULT_INVENTORY = "ha_inventory.json"
DEFAULT_MAP = "entity_rename_map.json"
DEFAULT_ACTIONS = "entity_rename_actions.json"

TARGET_DOMAINS = {
    "alarm_control_panel",
    "binary_sensor",
    "climate",
    "cover",
    "fan",
    "humidifier",
    "light",
    "lock",
    "media_player",
    "sensor",
    "siren",
    "switch",
    "vacuum",
    "valve",
    "water_heater",
}

OVERRIDES = {
    "light.basement_lights": "basement_lights",
    "light.living_room_lamps_group": "living_room_lamps",
    "light.downstairs_lights": "basement_lights",
    "light.office_ct_lights": "upstairs_hallway_lights",
}

BASE_URLS = [
    "http://192.168.4.141:8123",
    "https://evcjv8cnjndmqevolt32uwvhs94papom.ui.nabu.casa",
]


def slugify(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    lowered = ascii_text.lower()
    collapsed = re.sub(r"[^a-z0-9]+", "_", lowered).strip("_")
    collapsed = re.sub(r"_+", "_", collapsed)
    return re.sub(r"([a-z])_s(\b|_)", r"\1s\2", collapsed)


def compute_base_slug(friendly: str, area_slug: str | None) -> str:
    base = slugify(friendly)
    if not base:
        return base
    if not area_slug:
        return base
    if base.startswith(area_slug + "_"):
        return base
    if area_slug.endswith("_room"):
        room_prefix = area_slug[: -len("_room")]
        if room_prefix and base.startswith(room_prefix + "_"):
            return area_slug + base[len(room_prefix) :]
    last_token = area_slug.split("_")[-1]
    if base.startswith(last_token + "_"):
        return area_slug + "_" + base[len(last_token) + 1 :]
    if area_slug in base:
        return base
    return area_slug + "_" + base


def load_inventory(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def build_mapping(inventory: dict[str, Any]) -> dict[str, str]:
    areas = inventory.get("areas", [])
    devices = inventory.get("devices", [])
    entities = inventory.get("entities", [])
    states = inventory.get("states", [])

    area_slug_by_id = {}
    for area in areas:
        name = area.get("name") or ""
        area_id = area.get("area_id")
        if area_id:
            area_slug_by_id[area_id] = slugify(name)

    device_area_by_id = {dev.get("id"): dev.get("area_id") for dev in devices}
    state_by_id = {state.get("entity_id"): state for state in states}

    existing_ids = {ent.get("entity_id") for ent in entities if ent.get("entity_id")}

    desired_map: dict[str, str] = {}

    for ent in entities:
        entity_id = ent.get("entity_id")
        if not entity_id:
            continue
        domain, _, object_id = entity_id.partition(".")
        if domain not in TARGET_DOMAINS:
            continue

        if entity_id in OVERRIDES:
            new_object_id = OVERRIDES[entity_id]
            desired_map[entity_id] = f"{domain}.{new_object_id}"
            continue

        state = state_by_id.get(entity_id, {})
        friendly = (
            state.get("attributes", {}).get("friendly_name")
            or ent.get("name")
            or ent.get("original_name")
        )
        if not friendly:
            continue

        area_id = ent.get("area_id") or device_area_by_id.get(ent.get("device_id"))
        area_slug = area_slug_by_id.get(area_id) if area_id else None
        base = compute_base_slug(str(friendly), area_slug)
        if not base:
            continue
        if object_id == base or re.fullmatch(rf"{re.escape(base)}_\d+", object_id):
            desired_map[entity_id] = entity_id
            continue
        if ent.get("disabled_by") == "user" and ent.get("platform") == "hue" and not base.startswith("hue_"):
            base = f"hue_{base}"
        desired_map[entity_id] = f"{domain}.{base}"

    rename_candidates = {k: v for k, v in desired_map.items() if v != k}
    return resolve_collisions(rename_candidates, existing_ids)


def resolve_collisions(mapping: dict[str, str], existing_ids: set[str]) -> dict[str, str]:
    pending = dict(mapping)

    while True:
        reserved = set(existing_ids) - set(pending.keys())
        assigned: set[str] = set()
        resolved: dict[str, str] = {}
        dropped: set[str] = set()

        for old_id in sorted(pending.keys()):
            desired = pending[old_id]
            domain, _, base = desired.partition(".")
            new_id = desired
            if new_id in reserved or new_id in assigned:
                idx = 2
                while True:
                    candidate = f"{domain}.{base}_{idx}"
                    if candidate not in reserved and candidate not in assigned:
                        new_id = candidate
                        break
                    idx += 1
            if new_id == old_id:
                dropped.add(old_id)
                continue
            resolved[old_id] = new_id
            assigned.add(new_id)

        if not dropped:
            return resolved
        for old_id in dropped:
            pending.pop(old_id, None)


def plan_actions(mapping: dict[str, str], existing_ids: set[str]) -> list[tuple[str, str]]:
    pending = dict(mapping)
    current = set(existing_ids)
    actions: list[tuple[str, str]] = []

    while pending:
        progress = False
        for old_id, new_id in list(pending.items()):
            if new_id not in current:
                actions.append((old_id, new_id))
                current.remove(old_id)
                current.add(new_id)
                del pending[old_id]
                progress = True
        if progress:
            continue

        old_id, new_id = next(iter(pending.items()))
        temp_id = f"{old_id}_tmp"
        while temp_id in current or temp_id in pending or temp_id in mapping.values():
            temp_id += "_tmp"
        actions.append((old_id, temp_id))
        current.remove(old_id)
        current.add(temp_id)
        del pending[old_id]
        pending[temp_id] = new_id

    return actions


def load_token() -> str:
    return Path.home().joinpath(".ha_token").read_text().strip()


def to_ws_url(base_url: str) -> str:
    if base_url.startswith("https://"):
        return "wss://" + base_url[len("https://") :].rstrip("/") + "/api/websocket"
    if base_url.startswith("http://"):
        return "ws://" + base_url[len("http://") :].rstrip("/") + "/api/websocket"
    return base_url.rstrip("/") + "/api/websocket"


def request_json(base_url: str, path: str, method: str = "GET", body=None, timeout: int = 10):
    import urllib.request

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


async def ws_request(ws, msg_id: int, payload: dict[str, Any]) -> Any:
    await ws.send(json.dumps({"id": msg_id, **payload}))
    while True:
        response = json.loads(await ws.recv())
        if response.get("id") != msg_id:
            continue
        if not response.get("success"):
            raise RuntimeError(f"Request failed: {response}")
        return response.get("result")


async def apply_actions(base_url: str, actions: list[tuple[str, str]]) -> None:
    if not actions:
        return
    ws_url = to_ws_url(base_url)
    token = load_token()
    async with websockets.connect(ws_url, max_size=None) as ws:
        await ws.recv()
        await ws.send(json.dumps({"type": "auth", "access_token": token}))
        await ws.recv()
        msg_id = 1
        for old_id, new_id in actions:
            await ws_request(
                ws,
                msg_id,
                {
                    "type": "config/entity_registry/update",
                    "entity_id": old_id,
                    "new_entity_id": new_id,
                },
            )
            msg_id += 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Bulk rename HA entities with area-aware slugs.")
    parser.add_argument("--inventory", default=DEFAULT_INVENTORY, help="Path to ha_inventory.json")
    parser.add_argument("--write-map", default=DEFAULT_MAP, help="Write mapping JSON file")
    parser.add_argument("--write-actions", default=DEFAULT_ACTIONS, help="Write actions JSON file")
    parser.add_argument("--apply", action="store_true", help="Apply renames to Home Assistant")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    inventory_path = Path(args.inventory)
    inventory = load_inventory(inventory_path)

    mapping = build_mapping(inventory)
    entities = inventory.get("entities", [])
    existing_ids = {ent.get("entity_id") for ent in entities if ent.get("entity_id")}
    actions = plan_actions(mapping, existing_ids)

    Path(args.write_map).write_text(json.dumps(mapping, indent=2, sort_keys=True))
    Path(args.write_actions).write_text(
        json.dumps({"actions": actions}, indent=2)
    )

    if args.apply:
        base_url = pick_base_url(BASE_URLS)
        asyncio.run(apply_actions(base_url, actions))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
