#!/usr/bin/env python3
"""Build bilingual arrival cards. See --help for the three embeddable font inputs."""
import argparse
import json
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.graphics import renderPDF
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://starichdog-collab.github.io/myeonmok-yonsei-seok/"
OFFICIAL = "https://www.xn--vb0bn4ecstcd77y.com/"
MAP = "https://map.naver.com/p/entry/place/1648448794?placePath=%2Fhome"
WIDTH, HEIGHT = A4
MARGIN = 39
BODY = WIDTH - 2 * MARGIN
INK, MUTED, ACCENT = map(HexColor, ("#193f40", "#4e635b", "#366659"))
LIGHT, LINE, PAPER = map(HexColor, ("#eaf1e5", "#c4d2c5", "#fcfcf7"))
KOREAN = [
    "내과 외래 접수는 어디에서 하나요?",
    "혈액투석 상담은 언제 받을 수 있나요?",
    "다른 병원에서 투석을 받고 있습니다. 어떤 기록을 준비해야 하나요?",
    "통역이 필요하면 방문 전에 어떻게 준비하면 될까요?",
]
COPY = {
    "en": {
        "label": "English / 한국어", "title": "Visit card", "instruction": "Show the address to your driver. At reception, point to the question you want to ask.",
        "questions": "Questions for reception", "lines": [
            "Where do I check in for an internal medicine appointment?",
            "When is a hemodialysis consultation available?",
            "I receive dialysis at another clinic. Which records should I bring?",
            "If I need an interpreter, what should I arrange before my visit?"
        ], "visit": "Map and outpatient hours", "consult": "Dialysis consultation guide",
        "source": "Clinic website (Korean)", "map": "Open map",
        "note": "Call the clinic to confirm appointments, dialysis times and language support."
    },
    "zh": {
        "label": "简体中文 / 한국어", "title": "就诊沟通卡", "instruction": "乘车时可向司机出示韩文地址。在挂号处，可指给工作人员看您想问的那句话。",
        "questions": "在挂号处可以这样问", "lines": [
            "请问内科门诊在哪里挂号？", "什么时候可以咨询血液透析？",
            "我目前在其他医院做透析。需要准备哪些病历或检查资料？",
            "如果需要口译，我应该在就诊前做哪些准备？"
        ], "visit": "交通路线和门诊时间", "consult": "血液透析咨询指南",
        "source": "诊所官网（韩文）", "map": "查看地图",
        "note": "挂号、透析时段及口译安排，请提前致电诊所确认。"
    },
    "mn": {
        "label": "Монгол / 한국어", "title": "Эмнэлэгт үзүүлэх карт", "instruction": "Жолоочид солонгос хаягийг үзүүлээрэй. Бүртгэл дээр асуух өгүүлбэрээ зааж болно.",
        "questions": "Бүртгэл дээр асуух зүйлс", "lines": [
            "Дотрын эмчид үзүүлэхийн тулд хаана бүртгүүлэх вэ?",
            "Гемодиализын талаар хэзээ зөвлөгөө авч болох вэ?",
            "Би одоо өөр эмнэлэгт диализ хийлгэдэг. Ямар баримт бичиг авчрах вэ?",
            "Хэлмэрч хэрэгтэй бол очихоосоо өмнө хэрхэн зохицуулах вэ?"
        ], "visit": "Хаяг, үзлэгийн цаг", "consult": "Диализын зөвлөгөө",
        "source": "Эмнэлгийн сайт (солонгос хэлээр)", "map": "Газрын зураг",
        "note": "Үзлэг, диализын цаг болон хэлмэрчийн талаар эмнэлгээс утсаар лавлаарай."
    },
}


def card(code, copy):
    locale = "zh-Hans" if code == "zh" else code
    ui = json.loads((ROOT / "marketing/languages" / (locale + ".json")).read_text())["ui"]
    font = "CJK" if code == "zh" else "Sans"
    emphasis = "CJK" if code == "zh" else "SansBold"
    out = ROOT / "assets" / f"arrival-card-{code}.pdf"
    c = Canvas(str(out), pagesize=A4, pageCompression=1)
    c.setTitle(f'{copy["title"]} | 면목연세석내과')
    c.setAuthor("면목연세석내과 홍보 안내 사이트")
    c.setSubject(ui["address"] + " / 면목로 398, 외래 접수와 혈액투석 상담 질문")
    c.setFillColor(PAPER)
    c.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)

    def line(text, x, top, face, size, color=INK):
        c.setFont(face, size)
        c.setFillColor(color)
        c.drawString(x, HEIGHT - top - size, text)

    def para(text, x, top, width, face, size, leading, color=INK):
        style = ParagraphStyle("body", fontName=face, fontSize=size, leading=leading,
                               textColor=color, wordWrap="CJK" if face == "CJK" else None)
        item = Paragraph(escape(text), style)
        _, height = item.wrap(width, HEIGHT)
        item.drawOn(c, x, HEIGHT - top - height)
        return height

    def hot_link(label, url, x, top, face, size):
        line(label, x, top, face, size, ACCENT)
        width = pdfmetrics.stringWidth(label, face, size)
        baseline = HEIGHT - top - size
        c.setStrokeColor(ACCENT)
        c.setLineWidth(.5)
        c.line(x, baseline - 2, x + width, baseline - 2)
        c.linkURL(url, (x, baseline - 5, x + width, baseline + size + 2), relative=0)

    def qr(url, x, top):
        widget = QrCodeWidget(url, barLevel="M", barBorder=4, barFillColor=INK)
        bounds = widget.getBounds()
        side = 74
        glyph = Drawing(side, side, transform=[side/(bounds[2]-bounds[0]), 0, 0,
                                               side/(bounds[3]-bounds[1]), 0, 0])
        glyph.add(widget)
        c.setFillColor(HexColor("#ffffff"))
        c.rect(x, HEIGHT-top-side, side, side, fill=1, stroke=0)
        renderPDF.draw(glyph, c, x, HEIGHT-top-side)
        c.linkURL(url, (x, HEIGHT-top-side, x+side, HEIGHT-top), relative=0)

    line("MYEONMOK YONSEI SEOK", MARGIN, 30, "SansBold", 9, ACCENT)
    native = copy["label"].split(" / ")[0].upper()
    badge_face = "CJK" if code == "zh" else "SansBold"
    right = WIDTH - MARGIN
    # Draw the two scripts separately so every glyph uses an embedded font.
    ko_suffix = "  /  한국어"
    ko_width = pdfmetrics.stringWidth(ko_suffix, "CJK", 9)
    line(native, right-ko_width-pdfmetrics.stringWidth(native, badge_face, 9), 30, badge_face, 9, ACCENT)
    line(ko_suffix, right-ko_width, 30, "CJK", 9, ACCENT)
    line(copy["title"], MARGIN, 52, emphasis, 29)
    line("면목연세석내과", MARGIN, 94, "CJK", 15)
    description_h = para(copy["instruction"], MARGIN, 119, BODY, font, 12, 17, MUTED)
    top = 119 + description_h + 18
    c.setFillColor(LIGHT)
    c.roundRect(MARGIN, HEIGHT-top-153, BODY, 153, 8, fill=1, stroke=0)
    line("목적지  /  면목역 2번 출구 인근", MARGIN+15, top+10, "CJK", 10, ACCENT)
    line("서울특별시 중랑구 면목로 398 스마트빌딩", MARGIN+15, top+30, "CJK", 18)
    line("외래 2층   ·   인공신장실 5·6층", MARGIN+15, top+59, "CJK", 13)
    floor_h = para(ui["floor"], MARGIN+15, top+81, BODY-30, font, 11.5, 15, MUTED)
    if floor_h > 32:
        raise ValueError(f"{code}: floor description does not fit")
    hot_link("02-437-0808", "tel:+8224370808", MARGIN+15, top+117, "SansBold", 14)
    hot_link(copy["map"], MAP, MARGIN+210, top+120, font, 11)
    top += 172
    top += para(copy["questions"], MARGIN, top, BODY, emphasis, 20, 26) + 10
    for i, (question, translation) in enumerate(zip(KOREAN, copy["lines"]), 1):
        c.setStrokeColor(LINE)
        c.setLineWidth(.65)
        c.line(MARGIN, HEIGHT-top, right, HEIGHT-top)
        line(f"{i:02}", MARGIN, top+12, "SansBold", 10, ACCENT)
        top += 9 + para(question, MARGIN+34, top+9, BODY-34, "CJK", 13.6, 18)
        top += 4 + para(translation, MARGIN+34, top+4, BODY-34, font, 12.5, 17.5, MUTED) + 11
    panel_top = 665
    if top > panel_top-8:
        raise ValueError(f"{code}: questions overlap the links ({top})")
    c.setStrokeColor(LINE)
    c.line(MARGIN, HEIGHT-panel_top, right, HEIGHT-panel_top)
    destinations = [(copy["visit"], BASE+code+"/visit/"), (copy["consult"], BASE+code+"/dialysis-consultation/")]
    for i, (label, url) in enumerate(destinations):
        x = MARGIN + i*(BODY/2+5)
        qr(url, x, panel_top+12)
        text_x=x+77
        label_h=para(label, text_x, panel_top+24, BODY/2-85, emphasis, 11.5, 16, ACCENT)
        c.linkURL(url, (text_x, HEIGHT-panel_top-28-label_h, x+BODY/2-4, HEIGHT-panel_top-20), relative=0)
    note_top = panel_top+93
    note_h = para(copy["note"], MARGIN, note_top, BODY, font, 10.3, 14.5, MUTED)
    if note_top+note_h>799:
        raise ValueError(f"{code}: footer overflow")
    hot_link(copy["source"], OFFICIAL, MARGIN, 800, font, 9.5)
    line("2026.11.04", right-52, 800, "Sans", 9.5, MUTED)
    c.showPage()
    c.save()
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cjk_ttf", type=Path, help="A Korean and simplified Chinese TrueType font, e.g. Droid Sans Fallback.")
    parser.add_argument("sans_ttf", type=Path, help="Latin and Mongolian Cyrillic TrueType, e.g. DejaVu Sans.")
    parser.add_argument("bold_ttf", type=Path, help="Bold counterpart of sans_ttf.")
    args = parser.parse_args()
    for face, path in (("CJK", args.cjk_ttf), ("Sans", args.sans_ttf), ("SansBold", args.bold_ttf)):
        pdfmetrics.registerFont(TTFont(face, str(path)))
    for lang, content in COPY.items():
        print(card(lang, content))
