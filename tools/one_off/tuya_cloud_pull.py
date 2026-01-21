#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

try:
    import segno
except Exception:
    segno = None

try:
    from tuya_sharing import LoginControl, Manager, SharingTokenListener
except Exception as exc:
    print(
        "tuya_sharing is not available. Install deps in a venv and re-run.",
        file=sys.stderr,
    )
    print(f"Import error: {exc}", file=sys.stderr)
    sys.exit(1)

# Constants mirrored from tuya_local to avoid importing Home Assistant.
TUYA_CLIENT_ID = "HA_3y9q4ak7g4ephrvke"
TUYA_SCHEMA = "haauthorize"
TUYA_RESPONSE_SUCCESS = "success"
TUYA_RESPONSE_RESULT = "result"
TUYA_RESPONSE_QR_CODE = "qrcode"


class TokenListener(SharingTokenListener):
    def update_token(self, token_info):
        # Token refresh callback; not needed for one-shot pulls.
        return None


def load_json(path: Path, default=None):
    if not path.exists():
        return default
    return json.loads(path.read_text())


def save_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True))


def generate_qr(user_code: str, qr_state: Path, qr_png: Path | None) -> int:
    login = LoginControl()
    response = login.qr_code(TUYA_CLIENT_ID, TUYA_SCHEMA, user_code)
    if not response.get(TUYA_RESPONSE_SUCCESS):
        print(f"QR request failed: {response}", file=sys.stderr)
        return 1

    qr_code = response[TUYA_RESPONSE_RESULT][TUYA_RESPONSE_QR_CODE]
    qr_data = f"tuyaSmart--qrLogin?token={qr_code}"
    save_json(
        qr_state,
        {
            "user_code": user_code,
            "qr_code": qr_code,
            "qr_data": qr_data,
        },
    )
    print(f"Saved QR state to {qr_state}")
    print(f"QR data: {qr_data}")

    if qr_png:
        if segno is None:
            print("segno not installed; cannot render QR PNG.", file=sys.stderr)
        else:
            segno.make(qr_data).save(str(qr_png), scale=5)
            print(f"Wrote QR PNG to {qr_png}")
    return 0


def device_to_dict(device):
    return {
        "category": device.category,
        "id": device.id,
        "ip": device.ip,
        "local_key": device.local_key if hasattr(device, "local_key") else "",
        "name": device.name,
        "node_id": device.node_id if hasattr(device, "node_id") else "",
        "online": device.online,
        "product_id": device.product_id,
        "product_name": device.product_name,
        "support_local": device.support_local,
        "uid": device.uid,
        "uuid": device.uuid,
    }


def fetch_datamodel(manager: Manager, device_id: str, include_nonlocal: bool):
    response = manager.customer_api.get(
        f"/v1.0/m/life/devices/{device_id}/status",
    )
    if response.get("result"):
        response = response["result"]
    transform = []
    for entry in response.get("dpStatusRelationDTOS", []):
        if not include_nonlocal and not entry.get("supportLocal"):
            continue
        transform.append(
            {
                "id": entry.get("dpId"),
                "name": entry.get("dpCode"),
                "type": entry.get("valueType"),
                "format": entry.get("valueDesc"),
                "enumMap": entry.get("enumMappingMap"),
                "supportLocal": entry.get("supportLocal"),
            }
        )
    return transform, response


def fetch_devices(
    user_code: str,
    qr_state: Path,
    snapshot_path: Path | None,
    out_devices: Path,
    out_datamodels: Path,
    include_all: bool,
    include_nonlocal: bool,
    raw_datamodels: bool,
) -> int:
    state = load_json(qr_state)
    if not state:
        print(f"QR state not found at {qr_state}", file=sys.stderr)
        return 1
    if state.get("user_code") != user_code:
        print(
            "User code mismatch with saved QR state. Re-run --action qr.",
            file=sys.stderr,
        )
        return 1

    login = LoginControl()
    success, info = login.login_result(state["qr_code"], TUYA_CLIENT_ID, user_code)
    if not success:
        print(f"Login failed: {info}", file=sys.stderr)
        return 1

    token_info = {
        "t": info["t"],
        "uid": info["uid"],
        "expire_time": info["expire_time"],
        "access_token": info["access_token"],
        "refresh_token": info["refresh_token"],
    }

    manager = Manager(
        TUYA_CLIENT_ID,
        user_code,
        info["terminal_id"],
        info["endpoint"],
        token_info,
        TokenListener(),
    )

    manager.update_device_cache()

    snapshot_by_id = {}
    if snapshot_path and snapshot_path.exists():
        snapshot = load_json(snapshot_path, {})
        for device in snapshot.get("devices", []):
            dev_id = device.get("id")
            if dev_id:
                snapshot_by_id[dev_id] = device

    devices = []
    datamodels = {}
    raw = {} if raw_datamodels else None
    for device in manager.device_map.values():
        info = device_to_dict(device)
        snap = snapshot_by_id.get(device.id)
        if snap:
            info["snapshot"] = {
                "ip": snap.get("ip"),
                "productKey": snap.get("productKey"),
                "ver": snap.get("ver"),
            }
        devices.append(info)

    target_ids = set(snapshot_by_id.keys()) if snapshot_by_id else set()
    if include_all or not target_ids:
        target_ids = {d["id"] for d in devices}

    for dev_id in sorted(target_ids):
        try:
            model, raw_resp = fetch_datamodel(manager, dev_id, include_nonlocal)
            datamodels[dev_id] = model
            if raw_datamodels:
                raw[dev_id] = raw_resp
        except Exception as exc:
            datamodels[dev_id] = {"error": str(exc)}
            if raw_datamodels:
                raw[dev_id] = {"error": str(exc)}

    save_json(out_devices, {"devices": devices})
    save_json(out_datamodels, {"datamodels": datamodels})
    if raw_datamodels:
        save_json(Path("tuya_cloud_datamodels_raw.json"), {"raw": raw})

    print(f"Wrote devices to {out_devices}")
    print(f"Wrote datamodels to {out_datamodels}")
    return 0


def build_parser():
    parser = argparse.ArgumentParser(
        description="Pull Tuya cloud device info and datamodels for tuya_local.",
    )
    parser.add_argument("--user-code", required=True, help="Tuya/Smart Life user code")
    parser.add_argument(
        "--action",
        choices=["qr", "fetch"],
        required=True,
        help="Generate QR or fetch devices/datamodels after scan.",
    )
    parser.add_argument(
        "--qr-state",
        default=".tuya_qr.json",
        help="Path to save/load QR state",
    )
    parser.add_argument(
        "--qr-png",
        default="tuya_qr.png",
        help="Path to write QR PNG (action=qr)",
    )
    parser.add_argument(
        "--snapshot",
        default="snapshot.json",
        help="Path to snapshot.json for device matching",
    )
    parser.add_argument(
        "--out-devices",
        default="tuya_cloud_devices.json",
        help="Output file for device list",
    )
    parser.add_argument(
        "--out-datamodels",
        default="tuya_cloud_datamodels.json",
        help="Output file for datamodels",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Fetch datamodels for all devices, not just snapshot matches",
    )
    parser.add_argument(
        "--include-nonlocal",
        action="store_true",
        help="Include DPs that are not marked as local in the cloud model",
    )
    parser.add_argument(
        "--raw-datamodels",
        action="store_true",
        help="Write raw datamodel responses for inspection",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    qr_state = Path(args.qr_state)
    qr_png = Path(args.qr_png) if args.qr_png else None
    snapshot_path = Path(args.snapshot) if args.snapshot else None

    if args.action == "qr":
        return generate_qr(args.user_code, qr_state, qr_png)

    return fetch_devices(
        args.user_code,
        qr_state,
        snapshot_path,
        Path(args.out_devices),
        Path(args.out_datamodels),
        args.all,
        args.include_nonlocal,
        args.raw_datamodels,
    )


if __name__ == "__main__":
    raise SystemExit(main())
