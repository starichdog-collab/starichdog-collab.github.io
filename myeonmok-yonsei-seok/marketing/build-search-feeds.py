#!/usr/bin/env python3
"""Build a full-content RSS feed from the clinic's canonical HTML pages."""
from datetime import datetime, timezone
from email.utils import format_datetime
from html import escape, unescape
from pathlib import Path
from urllib.parse import urljoin, urlsplit
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def full_content(source, page_url):
    content = re.search(r"<main\b[^>]*>(.*?)</main>", source, re.S).group(1)
    # The feed exposes readable content, not interactive UI or inline icons.
    content = re.sub(r"<(button|svg|script)\b[^>]*>.*?</\1>", "", content, flags=re.S)
    content = re.sub(r"<input\b[^>]*>", "", content)
    content = re.sub(r"<output\b[^>]*>.*?</output>", "", content, flags=re.S)
    def absolute(match):
        return f'{match[1]}="{escape(urljoin(page_url, unescape(match[2])), quote=True)}"'
    content = re.sub(r'(href|src|poster)="([^"]*)"', absolute, content)
    def absolute_srcset(match):
        candidates = []
        for candidate in unescape(match[1]).split(","):
            parts = candidate.strip().split()
            if parts:
                parts[0] = urljoin(page_url, parts[0])
                candidates.append(" ".join(parts))
        return 'srcset="' + escape(", ".join(candidates), quote=True) + '"'
    return re.sub(r'srcset="([^"]*)"', absolute_srcset, content)


def build():
    urls = [e.text for e in ET.parse(ROOT / "sitemap.xml").findall("s:url/s:loc", NS)]
    base = urls[0]
    if not all(url.startswith(base) and urlsplit(url).netloc == urlsplit(base).netloc for url in urls):
        raise ValueError("The feed must contain only clinic URLs under its base directory")
    rss = ET.Element("rss", {"version": "2.0"})
    channel = ET.SubElement(rss, "channel")
    for name, value in {
        "title": "면목연세석내과 진료·방문 안내",
        "link": base,
        "description": "중랑구 면목동 면목연세석내과의 내과 진료, 신장투석, 방문 준비 및 병원 소개 안내.",
        "language": "ko-kr",
        "lastBuildDate": format_datetime(datetime.now(timezone.utc)),
    }.items():
        ET.SubElement(channel, name).text = value
    for url in urls:
        relative = url[len(base):]
        page = ROOT / relative / "index.html"
        source = page.read_text(encoding="utf-8")
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = unescape(re.search(r"<title>(.*?)</title>", source, re.S).group(1))
        ET.SubElement(item, "link").text = url
        ET.SubElement(item, "guid", {"isPermaLink": "true"}).text = url
        ET.SubElement(item, "description").text = full_content(source, url)
    ET.indent(rss)
    ET.ElementTree(rss).write(ROOT / "feed.xml", encoding="utf-8", xml_declaration=True)
    print(f"Built feed.xml with {len(urls)} complete pages")


if __name__ == "__main__":
    build()
