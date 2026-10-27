#!/usr/bin/env python3
"""Notify Naver after deployment. No request is sent without --submit."""
import argparse
import json
from pathlib import Path
import re
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ENDPOINT = "https://searchadvisor.naver.com/indexnow"


def payload():
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [e.text for e in ET.parse(ROOT / "sitemap.xml").findall("s:url/s:loc", ns)]
    base = urls[0]
    host = urlsplit(base).netloc
    if not all(url.startswith(base) and urlsplit(url).netloc == host for url in urls):
        raise ValueError("Only this clinic's pages may be submitted")
    keys = [p for p in ROOT.glob("*.txt") if re.fullmatch(r"[a-fA-F0-9-]{8,128}", p.stem)]
    if len(keys) != 1:
        raise ValueError("Expected one public IndexNow key file")
    key = keys[0].read_text(encoding="utf-8").strip()
    if key != keys[0].stem:
        raise ValueError("The public key file must contain its own filename stem")
    return {"host": host, "key": key, "keyLocation": base + keys[0].name, "urlList": urls}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--submit", action="store_true", help="Send one batch to Naver after checking the published key")
    args = parser.parse_args()
    data = payload()
    if not args.submit:
        print(json.dumps({"endpoint": ENDPOINT, "request": data, "submitted": False}, ensure_ascii=False, indent=2))
        return
    with urlopen(data["keyLocation"], timeout=25) as response:
        if response.status != 200 or response.read().decode("utf-8").strip() != data["key"]:
            raise ValueError("Published key verification failed; no IndexNow request sent")
    request = Request(ENDPOINT, data=json.dumps(data).encode("utf-8"), headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
    try:
        with urlopen(request, timeout=25) as response:
            status, body = response.status, response.read().decode("utf-8", errors="replace")
    except HTTPError as error:
        status, body = error.code, error.read().decode("utf-8", errors="replace")
    print(json.dumps({"endpoint": ENDPOINT, "http_status": status, "url_count": len(data["urlList"]), "response": body, "indexing_confirmed": False}, ensure_ascii=False, indent=2))
    if status not in (200, 202):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
