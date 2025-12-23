#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

import tinytuya


def load_json(path: Path, default=None):
    if not path.exists():
        return default
    return json.loads(path.read_text())


def save_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True))


def build_targets(snapshot_path: Path, cloud_path: Path, device_ids: list[str] | None):
    snapshot = load_json(snapshot_path, {})
    cloud = load_json(cloud_path, {})

    snap_by_id = {d.get("id"): d for d in snapshot.get("devices", []) if d.get("id")}
    cloud_by_id = {d.get("id"): d for d in cloud.get("devices", []) if d.get("id")}

    targets = []
    for dev_id, snap in snap_by_id.items():
        if device_ids and dev_id not in device_ids:
            continue
        cloud_info = cloud_by_id.get(dev_id, {})
        local_key = cloud_info.get("local_key") or ""
        if not local_key:
            targets.append(
                {
                    "id": dev_id,
                    "name": cloud_info.get("name"),
                    "ip": snap.get("ip"),
                    "version": snap.get("ver"),
                    "product_id": cloud_info.get("product_id")
                    or snap.get("productKey"),
                    "skip_reason": "missing_local_key",
                }
            )
            continue

        targets.append(
            {
                "id": dev_id,
                "name": cloud_info.get("name"),
                "ip": snap.get("ip"),
                "version": snap.get("ver"),
                "product_id": cloud_info.get("product_id") or snap.get("productKey"),
                "local_key": local_key,
            }
        )

    return targets


def parse_extra_dps(extra_dps: str | None) -> list[int]:
    if not extra_dps:
        return []
    items = []
    for part in extra_dps.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            try:
                start = int(start_s.strip())
                end = int(end_s.strip())
            except ValueError:
                continue
            if end < start:
                start, end = end, start
            items.extend(range(start, end + 1))
        else:
            try:
                items.append(int(part))
            except ValueError:
                continue
    return sorted(set(items))


def probe_device(device_info, timeout, detect_dps, fetch_status, extra_dps):
    result = {
        "id": device_info["id"],
        "name": device_info.get("name"),
        "ip": device_info.get("ip"),
        "version": device_info.get("version"),
        "product_id": device_info.get("product_id"),
        "status": None,
        "dps": None,
        "available_dps": None,
    }

    if device_info.get("skip_reason"):
        result["error"] = device_info["skip_reason"]
        return result

    try:
        device = tinytuya.Device(
            device_info["id"],
            device_info["ip"],
            device_info["local_key"],
        )
        if device_info.get("version"):
            try:
                device.set_version(float(device_info["version"]))
            except ValueError:
                pass
        device.set_socketTimeout(timeout)

        if fetch_status:
            if extra_dps:
                device.dps_to_request = {"1": None}
                device.add_dps_to_request(extra_dps)
            status = device.status()
            result["status"] = status
            if isinstance(status, dict):
                result["dps"] = status.get("dps")

        if detect_dps:
            try:
                result["available_dps"] = sorted(device.detect_available_dps())
            except Exception as exc:
                result["available_dps"] = {"error": str(exc)}
            if extra_dps:
                try:
                    device.dps_to_request = {"1": None}
                    device.add_dps_to_request(extra_dps)
                    data = device.status()
                    if isinstance(data, dict) and "dps" in data:
                        extra_found = sorted(data["dps"].keys())
                        if isinstance(result["available_dps"], list):
                            result["available_dps"] = sorted(
                                set(result["available_dps"]) | set(extra_found)
                            )
                except Exception as exc:
                    if isinstance(result["available_dps"], list):
                        result["available_dps"] = {
                            "error": str(exc),
                            "partial": result["available_dps"],
                        }

    except Exception as exc:
        result["error"] = str(exc)

    return result


def build_parser():
    parser = argparse.ArgumentParser(
        description="Probe Tuya local devices for DPS/status using tinytuya.",
    )
    parser.add_argument(
        "--snapshot",
        default="snapshot.json",
        help="Path to snapshot.json",
    )
    parser.add_argument(
        "--cloud-devices",
        default="tuya_cloud_devices.json",
        help="Path to tuya_cloud_devices.json",
    )
    parser.add_argument(
        "--out",
        default="tuya_local_dps.json",
        help="Output file for DPS/status info",
    )
    parser.add_argument(
        "--device-id",
        action="append",
        dest="device_ids",
        help="Limit probing to specific device ID(s)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="Socket timeout seconds",
    )
    parser.add_argument(
        "--detect-dps",
        action="store_true",
        help="Call detect_available_dps for each device",
    )
    parser.add_argument(
        "--no-status",
        action="store_true",
        help="Skip device status query",
    )
    parser.add_argument(
        "--extra-dps",
        help="Comma separated DPS ids or ranges to request (e.g. 201-210,1,2)",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    snapshot_path = Path(args.snapshot)
    cloud_path = Path(args.cloud_devices)
    targets = build_targets(snapshot_path, cloud_path, args.device_ids)

    extra_dps = parse_extra_dps(args.extra_dps)
    results = []
    for info in targets:
        results.append(
            probe_device(
                info,
                timeout=args.timeout,
                detect_dps=args.detect_dps,
                fetch_status=not args.no_status,
                extra_dps=extra_dps,
            )
        )

    save_json(Path(args.out), {"devices": results})
    print(f"Wrote probe results to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
