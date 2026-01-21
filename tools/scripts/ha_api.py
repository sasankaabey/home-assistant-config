#!/usr/bin/env python3
"""
ha_api.py — Home Assistant API helper

Purpose:
  Small helper for calling the Home Assistant REST API from the command line.

Usage:
  python3 tools/scripts/ha_api.py [args]

Auth:
  Expects a long-lived access token in: ~/.ha_token

Notes:
  - Keeps tokens out of git by reading from your home directory.
  - Default base URLs are defined in DEFAULT_BASE_URLS.
"""
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_BASE_URLS = [
    "http://192.168.4.141:8123",
    "https://evcjv8cnjndmqevolt32uwvhs94papom.ui.nabu.casa",
]


def load_token():
    token_path = Path.home() / ".ha_token"
    return token_path.read_text().strip()


def request_json(base_url, path, method="GET", body=None, timeout=10):
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


def pick_base_url(base_urls):
    for base_url in base_urls:
        try:
            request_json(base_url, "/api/config", timeout=5)
            return base_url
        except Exception:
            continue
    raise RuntimeError("No reachable HA base URL")


def main():
    base_urls = DEFAULT_BASE_URLS
    path = "/api/config"
    method = "GET"
    body = None

    if len(sys.argv) > 1:
        path = sys.argv[1]
    if len(sys.argv) > 2:
        method = sys.argv[2].upper()
    if len(sys.argv) > 3:
        body = json.loads(sys.argv[3])

    base_url = pick_base_url(base_urls)
    status, payload = request_json(base_url, path, method=method, body=body)
    print(json.dumps({"base_url": base_url, "status": status, "payload": payload}, indent=2))


if __name__ == "__main__":
    main()
