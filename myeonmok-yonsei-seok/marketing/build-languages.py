#!/usr/bin/env python3
"""Render the clinic's translated pages, language links and subtitle tracks."""
import argparse
import json
import posixpath
import re
from datetime import date, datetime
from html import escape
from pathlib import Path
from string import Template
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
COPY = ROOT / "marketing" / "languages"
BASE = "https://starichdog-collab.github.io/myeonmok-yonsei-seok/"
OFFICIAL = "https://www.xn--vb0bn4ecstcd77y.com/"
MAP = "https://map.naver.com/p/entry/place/1648448794?placePath=%2Fhome"
LANGS = {"ko": ("", "한국어"), "zh-Hans": ("zh", "简体中文"),
         "mn": ("mn", "Монгол"), "en": ("en", "English")}
OG = {"zh-Hans": "zh_CN", "mn": "mn_MN", "en": "en_US"}
TOPICS = ("home", "myeonmok-internal-medicine", "chronic-care", "jungnang-dialysis",
          "dialysis-consultation", "visit", "video")
GLOBE = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/></svg>'
ARROW = '<span aria-hidden="true">↗</span>'


def route(lang, topic):
    parts = [LANGS[lang][0], "" if topic == "home" else topic]
    return "".join(part + "/" for part in parts if part)


def relative(current, target):
    path = posixpath.relpath(target or ".", current or ".")
    return path + "/"


def alternates(topic):
    pairs = [(lang, route(lang, topic)) for lang in LANGS]
    pairs.append(("x-default", route("ko", topic)))
    return "\n".join(f'  <link rel="alternate" hreflang="{lang}" href="{BASE}{path}">' for lang, path in pairs)


def switcher(lang, topic, label):
    current = route(lang, topic)
    links = []
    for code, (_, native_name) in LANGS.items():
        url = relative(current, route(code, topic))
        selected = ' aria-current="page"' if code == lang else ''
        links.append(f'<li><a href="{url}" hreflang="{code}" lang="{code}"{selected}>{native_name}</a></li>')
    return (f'<nav class="clinic-language" aria-label="{label}"><div class="container">'
            f'<span class="language-label">{GLOBE}{label}</span><ul>{"".join(links)}</ul></div></nav>')


def caption_tracks(root, current_lang):
    tracks = []
    for lang, (folder, label) in LANGS.items():
        kind = "captions" if lang == "ko" else "subtitles"
        default = " default" if lang == current_lang and lang != "ko" else ""
        tracks.append(f'<track kind="{kind}" src="{root}assets/clinic-film-{folder or lang}.vtt" '
                      f'srclang="{lang}" label="{label}"{default}>')
    return "\n".join(tracks)


def contact_panel(u):
    return f'''<aside class="guide-aside" aria-labelledby="clinic-contact">
          <h2 id="clinic-contact">{u["phone"]}</h2>
          <a class="local-phone" href="tel:+8224370808">02-437-0808</a><span class="international">+82 2 437 0808</span>
          <p>{u["phoneNote"]}</p>
          <p class="address-line"><strong>{u["address"]}</strong>{u["addressLocal"]}</p>
          <p>{u["station"]}</p>
          <p><strong>{u["floorLabel"]}</strong>{u["floor"]}</p>
          <p><strong>{u["addressNative"]}</strong><span class="map-address" lang="ko">서울특별시 중랑구 면목로 398 스마트빌딩</span></p>
          <a class="guide-map" href="{MAP}">{u["map"]} {ARROW}</a>
        </aside>'''


def hours_table(u):
    rows = [(u["weekdays"], "08:30–20:00"), (u["saturday"], "08:30–16:00"),
            (u["lunch"], "13:00–14:00"), (u["closedDays"], u["closed"])]
    body = "\n".join(f'<tr><th scope="row">{label}</th><td>{when}</td></tr>' for label, when in rows)
    return (f'<section class="guide-section guide-hours"><h2 id="outpatient-hours">{u["hours"]}</h2>'
            f'<table aria-labelledby="outpatient-hours"><tbody>{body}</tbody></table><p>{u["hoursNote"]}</p></section>')


def checklist(u, items, assets, folder):
    rows = "\n".join(f'<label><input type="checkbox"><span>{escape(item)}</span></label>' for item in items)
    return (f'<section class="guide-section guide-check"><h2>{u["checklist"]}</h2>{rows}'
            f'<div class="guide-actions"><button type="button" onclick="window.print()">{u["print"]}</button>'
            f'<a class="guide-body-link" href="{assets}arrival-card-{folder}.pdf">{u["arrivalCard"]}</a>'
            f'<a class="guide-body-link" href="{assets}myeonmok-visit-guide.pdf">{u["pdf"]}</a></div></section>')


def structured_data(lang, topic, page, home_name, captions):
    url = BASE + route(lang, topic)
    clinic = {"@type": "MedicalClinic", "@id": OFFICIAL + "#clinic", "name": "면목연세석내과의원",
              "alternateName": ["면목연세석내과", "Myeonmok Yonsei Seok Internal Medicine"],
              "url": OFFICIAL, "telephone": "+82-2-437-0808", "hasMap": MAP,
              "address": {"@type": "PostalAddress", "streetAddress": "면목로 398 스마트빌딩",
                          "addressLocality": "중랑구", "addressRegion": "서울특별시", "addressCountry": "KR"}}
    web = {"@type": "WebPage", "@id": url, "url": url, "name": page["title"],
           "description": page["description"], "inLanguage": lang, "about": clinic,
           "isPartOf": {"@id": BASE + "#website"}}
    graph = [web]
    if topic != "home":
        crumb = {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": home_name, "item": BASE + route(lang, "home")},
            {"@type": "ListItem", "position": 2, "name": page["label"], "item": url}]}
        web["breadcrumb"] = {"@id": crumb["@id"]}
        graph.append(crumb)
    if topic == "video":
        video = {"@type": "VideoObject", "@id": url + "#film", "name": page["h1"], "description": page["intro"],
                 "inLanguage": "ko", "contentUrl": BASE + "assets/myeonmok-yonsei-seok-dialysis-30s.mp4",
                 "thumbnailUrl": BASE + "assets/dialysis-room-1280.webp",
                 "uploadDate": "2026-10-27T06:51:08+00:00", "duration": "PT30S", "transcript": " ".join(captions)}
        web["mainEntity"] = {"@id": video["@id"]}
        graph.append(video)
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False,
                      separators=(",", ":")).replace("<", "\\u003c")


def render(lang, topic, data, template):
    page, pages = data["pages"][topic], data["pages"]
    u = {key: escape(value) for key, value in data["ui"].items()}
    current = route(lang, topic)
    link = lambda slug: relative(current, route(lang, slug))
    root = relative(current, "")
    assets = root + "assets/"
    home = escape(pages["home"]["label"])
    visit = escape(pages["visit"]["label"])
    section_html = []
    for s in page["sections"]:
        section_html.append(f'<section class="guide-section"><h2>{escape(s["heading"])}</h2><p>{escape(s["text"])}</p></section>')
    official_services = {
        "myeonmok-internal-medicine": ("15", "officialMedicine"),
        "chronic-care": ("15", "officialMedicine"),
        "jungnang-dialysis": ("18", "officialDialysis"),
    }
    if topic in official_services:
        path, label = official_services[topic]
        section_html.append(f'<p><a class="guide-body-link" href="{OFFICIAL}{path}" hreflang="ko">{u[label]} {ARROW}</a></p>')
    topic_links = []
    for other in TOPICS:
        if topic != other:
            topic_links.append(f'<a href="{link(other)}">{escape(pages[other]["label"])} <span aria-hidden="true">→</span></a>')
    breadcrumb = ""
    if topic != "home":
        breadcrumb = (f'<nav class="guide-crumb" aria-label="{u["nav"]}"><a href="{link("home")}">{home}</a>'
                      f'<span aria-hidden="true">/</span><span aria-current="page">{escape(page["label"])}</span></nav>')
    photo, actions = "", ""
    if topic in ("home", "jungnang-dialysis"):
        photo = (f'<figure class="guide-photo"><img src="{assets}dialysis-room-1280.webp" '
                 f'srcset="{assets}dialysis-room-640.webp 640w, {assets}dialysis-room-1280.webp 1280w" '
                 f'sizes="(max-width: 800px) 92vw, 560px" width="1280" height="720" fetchpriority="high" '
                 f'alt="{u["photoAlt"]}"><figcaption>{u["photoCaption"]}</figcaption></figure>')
        target = "jungnang-dialysis" if topic == "home" else "dialysis-consultation"
        actions = (f'<div class="guide-actions"><a class="guide-primary" href="{link(target)}">'
                   f'{escape(pages[target]["label"])} <span aria-hidden="true">→</span></a>'
                   f'<a class="guide-body-link" href="{link("visit")}">{visit}</a></div>')
    form = ""
    if topic in ("visit", "dialysis-consultation"):
        items = data["visitChecklist"] if topic == "visit" else data["consultQuestions"]
        form = checklist(u, items, assets, LANGS[lang][0])
    player, transcript = "", ""
    if topic == "video":
        player = (f'<figure class="guide-player"><video controls playsinline preload="metadata" width="1280" height="720" '
                  f'poster="{assets}dialysis-room-1280.webp" aria-label="{u["film"]}">'
                  f'<source src="{assets}myeonmok-yonsei-seok-dialysis-30s.mp4" type="video/mp4">'
                  f'{caption_tracks(root, lang)}</video></figure>')
        lines = "".join(f'<li>{escape(line).replace(chr(10), " ")}</li>' for line in data["captions"])
        transcript = f'<section class="guide-section guide-transcript"><h2>{u["transcript"]}</h2><ol>{lines}</ol></section>'
    details = {key: escape(page[key]) for key in ("title", "description", "h1", "intro")}
    result = template.substitute(u, **details, language=lang, canonical=BASE+current, alternates=alternates(topic),
        assets=assets, root=root, og_locale=OG[lang], share_image=BASE+"assets/dialysis-room-1280.webp",
        schema=structured_data(lang, topic, page, pages["home"]["label"], data["captions"]),
        switcher=switcher(lang, topic, u["language"]), home=link("home"), visit=link("visit"), visit_label=visit,
        breadcrumb=breadcrumb, hero_class="with-photo" if photo else "", hero_actions=actions, hero_picture=photo,
        player=player, hours_table=hours_table(u) if topic == "visit" else "", sections="\n".join(section_html),
        checklist_panel=form, transcript_panel=transcript, contact_card=contact_panel(u),
        directory="\n".join(topic_links), official_url=OFFICIAL)
    return "\n".join(line.rstrip() for line in result.splitlines() if line.strip()) + "\n"


def replace_block(source, name, markup, before):
    start, end = f"<!-- {name} -->", f"<!-- /{name} -->"
    block = f"{start}\n{markup}\n{end}\n"
    if start in source:
        a = source.index(start)
        b = source.index(end, a) + len(end)
        return source[:a] + block.rstrip("\n") + source[b:]
    offset = source.index(before)
    return source[:offset] + block + source[offset:]


def korean_page(topic, source):
    root = relative(route("ko", topic), "")
    head = alternates(topic) + f'\n  <link rel="stylesheet" href="{root}language-menu.css">'
    source = replace_block(source, "language-pages", head, "</head>")
    source = replace_block(source, "language-menu", switcher("ko", topic, "언어 선택"), "<header")
    if topic == "video":
        source, count = re.subn(r'(<source [^>]+>)(?:\s*<track\b[^>]*>)+',
                                lambda m: m[1]+caption_tracks(root, "ko"), source, count=1)
        if count != 1:
            raise ValueError("Could not locate the Korean film tracks")
    if topic == "home":
        website_language = r'("@type":\s*"WebSite"[^{}]*?"inLanguage":\s*)"ko-KR"'
        source = re.sub(website_language, lambda m: m[1] + '["ko", "zh-Hans", "mn", "en"]', source, count=1)
    return source


def write_changed(path, text):
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return True


def update_sitemap(path, all_urls, changed, when):
    text = path.read_text(encoding="utf-8")
    existing = set(re.findall(r"<loc>([^<]+)</loc>", text))
    def update(match):
        block = match[0]
        url = re.search(r"<loc>([^<]+)</loc>", block)[1]
        if url in changed:
            return re.sub(r"<lastmod>[^<]+</lastmod>", f"<lastmod>{when}</lastmod>", block)
        return block
    text = re.sub(r"<url>.*?</url>", update, text, flags=re.S)
    extra = "".join(f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{when}</lastmod>\n  </url>\n"
                    for url in all_urls if url not in existing)
    write_changed(path, text.replace("</urlset>", extra+"</urlset>"))


def build(when):
    template = Template((COPY / "page.html.in").read_text(encoding="utf-8"))
    all_urls, changed = [], set()
    for lang, (folder, _) in LANGS.items():
        data = None
        if lang != "ko":
            data = json.loads((COPY / (lang+".json")).read_text(encoding="utf-8"))
            if set(data["pages"]) != set(TOPICS) or len(data["captions"]) != 6:
                raise ValueError(f"Incomplete translation: {lang}")
            vtt = ["WEBVTT", ""]
            for i, caption in enumerate(data["captions"]):
                vtt.extend([f"00:{i*5:02}.000 --> 00:{(i+1)*5:02}.000", caption, ""])
            write_changed(ROOT / "assets" / f"clinic-film-{folder}.vtt", "\n".join(vtt))
        for topic in TOPICS:
            path = ROOT / route(lang, topic) / "index.html"
            url = BASE + route(lang, topic)
            all_urls.append(url)
            if lang == "ko":
                source = path.read_text(encoding="utf-8")
                result = korean_page(topic, source)
                if result != source:
                    result = re.sub(r'("dateModified"\s*:\s*")[^"]+(")', lambda m: m[1]+when+m[2], result)
            else:
                result = render(lang, topic, data, template)
            if write_changed(path, result):
                changed.add(url)
    cards = [BASE + f"assets/arrival-card-{folder}.pdf" for folder, _ in LANGS.values() if folder]
    for sitemap in (ROOT / "sitemap.xml", ROOT.parent / "sitemap.xml"):
        update_sitemap(sitemap, all_urls + cards, changed, when)
    print(f"{len(all_urls)} pages in {len(LANGS)} languages; {len(changed)} page(s) changed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", type=date.fromisoformat, default=datetime.now(ZoneInfo("Asia/Seoul")).date())
    build(parser.parse_args().date.isoformat())
