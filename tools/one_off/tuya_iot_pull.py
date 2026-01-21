#!/usr/bin/env python3
import argparse
import json
import os
import sys
from pathlib import Path

try:
    from tuya_iot import TuyaOpenAPI
    from tuya_iot.asset import TuyaAssetManager
    from tuya_iot.openapi import TuyaTokenInfo
except Exception as exc:
    print(
        "tuya-iot-py-sdk is not available. Install deps in a venv and re-run.",
        file=sys.stderr,
    )
    print(f"Import error: {exc}", file=sys.stderr)
    sys.exit(1)


DATA_CENTER_ENDPOINTS = {
    "us": "https://openapi.tuyaus.com",
    "eu": "https://openapi.tuyaeu.com",
    "cn": "https://openapi.tuyacn.com",
    "in": "https://openapi.tuyain.com",
}


def load_env(path: Path) -> dict:
    if not path.exists():
        return {}
    env = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip()
    return env


def get_endpoint(data_center: str) -> str:
    return DATA_CENTER_ENDPOINTS.get(data_center, data_center)


def chunked(items: list[str], size: int) -> list[list[str]]:
    return [items[i : i + size] for i in range(0, len(items), size)]


def fetch_device_ids_from_assets(openapi: TuyaOpenAPI, root_asset_id: str) -> list[str]:
    assets = TuyaAssetManager(openapi)
    device_ids = []
    for asset in assets.get_asset_list(root_asset_id):
        asset_id = asset.get("asset_id")
        if not asset_id:
            continue
        device_ids.extend(assets.get_device_list(asset_id))
    return list(dict.fromkeys(device_ids))


def fetch_devices_by_ids(openapi: TuyaOpenAPI, device_ids: list[str]) -> list[dict]:
    devices = []
    for batch in chunked(device_ids, 20):
        resp = openapi.get("/v1.0/iot-03/devices", {"device_ids": ",".join(batch)})
        if not resp or not resp.get("success"):
            raise RuntimeError(resp)
        devices.extend(resp.get("result", {}).get("list", []))
    return devices


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Pull device inventory from Tuya IoT Cloud using Access ID/Secret.",
    )
    parser.add_argument(
        "--env",
        default=".env",
        help="Path to .env containing TUYA_ACCESS_ID/TUYA_ACCESS_SECRET.",
    )
    parser.add_argument(
        "--out",
        default="tuya_iot_devices.json",
        help="Output JSON file for device inventory",
    )
    parser.add_argument(
        "--page-size",
        type=int,
        default=100,
        help="Devices page size",
    )
    parser.add_argument(
        "--asset-id",
        default="-1",
        help="Root asset id to enumerate devices from (default: -1)",
    )
    parser.add_argument(
        "--auth-check",
        action="store_true",
        help="Only test authentication and print token response",
    )
    args = parser.parse_args()

    env = {**os.environ, **load_env(Path(args.env))}
    access_id = env.get("TUYA_ACCESS_ID")
    access_secret = env.get("TUYA_ACCESS_SECRET")
    data_center = env.get("TUYA_DATA_CENTER", "us")

    if not access_id or not access_secret:
        print("Missing TUYA_ACCESS_ID or TUYA_ACCESS_SECRET.", file=sys.stderr)
        return 1

    endpoint = get_endpoint(data_center)
    openapi = TuyaOpenAPI(endpoint, access_id, access_secret)
    token_resp = openapi.get("/v1.0/token", {"grant_type": 1})
    if args.auth_check:
        print(json.dumps(token_resp, indent=2))
        return 0 if token_resp and token_resp.get("success") else 1

    if not token_resp or not token_resp.get("success"):
        print(json.dumps(token_resp, indent=2), file=sys.stderr)
        return 1

    openapi.token_info = TuyaTokenInfo(token_resp)

    device_ids = fetch_device_ids_from_assets(openapi, args.asset_id)
    if not device_ids:
        print(
            "No device ids found via assets. This usually means the project has no assets "
            "or uses Smart Home authorization instead of Industry/Asset APIs.",
            file=sys.stderr,
        )
        print(
            "If this is a Smart Home project, you need a user-authorized token "
            "(username/password + country code + app schema) to list devices.",
            file=sys.stderr,
        )
        return 1
    devices = fetch_devices_by_ids(openapi, device_ids)
    Path(args.out).write_text(json.dumps({"devices": devices}, indent=2))
    print(f"Wrote {len(devices)} devices to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
