#!/usr/bin/env python3
"""Create the clinic's one-page sharing leaflet with embedded Korean fonts.

Usage: python build-visit-leaflet.py REGULAR_TTF BOLD_TTF
Requires reportlab and Pillow. Nanum Gothic is available under SIL OFL at
https://github.com/google/fonts/tree/main/ofl/nanumgothic
"""
from pathlib import Path
import sys
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/myeonmok-visit-guide.pdf'
BASE='https://starichdog-collab.github.io/myeonmok-yonsei-seok/'
OFFICIAL='https://www.xn--vb0bn4ecstcd77y.com/'
pdfmetrics.registerFont(TTFont('Nanum',sys.argv[1]))
pdfmetrics.registerFont(TTFont('NanumBold',sys.argv[2]))
W,H=595.28,841.89
INK=HexColor('#163f43'); MUTED=HexColor('#526563'); CREAM=HexColor('#f7f8f2'); LINE=HexColor('#d9e1d3')
c=canvas.Canvas(str(OUT),pagesize=(W,H),pageCompression=1)
c.setTitle('면목연세석내과 방문·혈액투석 상담 준비 안내')
c.setAuthor('면목연세석내과 홍보 안내 사이트')
c.setSubject('면목로 398 위치, 연락처, 첫 상담·전원 준비와 공식 안내 링크')
c.setKeywords('면목연세석내과, 방문 안내, 혈액투석 상담 준비, 중랑구 면목동')
c.setFillColor(CREAM);c.rect(0,0,W,H,fill=1,stroke=0)

def text(txt,x,top,size=11,bold=False,color=INK):
    c.setFillColor(color);c.setFont('NanumBold' if bold else 'Nanum',size);c.drawString(x,H-top-size,txt)

def para(txt,x,top,width,size=10.5,color=MUTED,bold=False,leading=None):
    style=ParagraphStyle('body',fontName='NanumBold' if bold else 'Nanum',fontSize=size,leading=leading or size*1.55,textColor=color,wordWrap='CJK')
    p=Paragraph(txt,style);_,height=p.wrap(width,H);p.drawOn(c,x,H-top-height);return height

def rule(top):
    c.setStrokeColor(LINE);c.setLineWidth(.8);c.line(36,H-top,W-36,H-top)

def link(label,url,x,top,size=10):
    text(label,x,top,size,True);width=pdfmetrics.stringWidth(label,'NanumBold',size)
    c.linkURL(url,(x,H-top-size-3,x+width,H-top+2),relative=0)
    c.setStrokeColor(INK);c.setLineWidth(.4);c.line(x,H-top-size-2,x+width,H-top-size-2)

text('VISIT GUIDE  |  2026.10',36,30,9,True,MUTED)
text('면목연세석내과',36,55,27,True)
text('방문과 혈액투석 상담을 준비하는 한 장 안내',36,96,12)
rule(129)

c.drawImage(ImageReader(str(ROOT/'assets/dialysis-room.jpg')),36,H-290,width=260,height=140,preserveAspectRatio=True,anchor='c',mask='auto')
text('인공신장실 실제 사진 · 출처: 병원 공식 홈페이지',36,298,8,color=MUTED)
text('찾아오시는 곳',316,149,12,True)
para('서울 중랑구 면목로 398<br/>스마트빌딩',316,177,243,11,color=INK)
para('외래 2층<br/>인공신장실 5·6층<br/>면목역 인근 · 면목본동 주민센터 맞은편',316,218,243,10)

c.setFillColor(INK);c.roundRect(36,H-380,523,51,7,fill=1,stroke=0)
text('상담·일정 문의',51,342,10,True,HexColor('#ffffff'))
text('02-437-0808',307,339,21,True,HexColor('#ffffff'))
c.linkURL('tel:024370808',(36,H-380,559,H-329),relative=0)

text('전화하기 전에, 네 가지를 확인하세요',36,406,15,True)
items=[
 ('01','방문 목적','첫 혈액투석 상담인지, 기존 병원에서의 전원 상담인지 말씀해 주세요.'),
 ('02','시간과 접수 위치','가능한 상담 시간과 첫 접수 층을 확인하세요. 외래시간과 투석 일정은 다를 수 있습니다.'),
 ('03','준비할 기록','진료의뢰서·최근 검사 결과·복용약 목록 중 필요한 자료와 전달 방법을 물어보세요.'),
 ('04','기존 병원과 일정 조율','전원 시 기존 담당 의료진과 새 병원의 진료·투석 일정을 함께 확인하세요.')]
top=443
for number,label,body in items:
    text(number,36,top,10,True,MUTED);text(label,68,top,11,True)
    para(body,68,top+19,486,10)
    top+=57

rule(684)
text('면목동 · 상봉동 · 망우동 · 용마산에서 방문하신다면',36,699,10,True)
para('지도에 실제 출발지와 목적지 “면목로 398”을 입력하세요. 안내하는 병원은 한 곳입니다.',36,719,400,9)
link('공식 홈페이지',OFFICIAL,36,751,9)
link('인공신장실 안내',OFFICIAL+'18',139,751,9)
link('첫 방문·전원 질문표',BASE+'dialysis-consultation/',253,751,9)

qr=QrCodeWidget(BASE+'dialysis-consultation/')
b=qr.getBounds(); qsize=76
d=Drawing(qsize,qsize,transform=[qsize/(b[2]-b[0]),0,0,qsize/(b[3]-b[1]),0,0]);d.add(qr)
renderPDF.draw(d,c,483,H-774)
text('상담 준비 안내',491,775,7,color=MUTED)
para('공개 정보를 정리한 홍보·방문 안내입니다. 필요한 서류, 동행 조건과 현재 일정은 병원에 확인하세요.<br/>작성 2026.10.30 · 사진·병원 정보: 면목연세석내과 공식 홈페이지',36,796,523,7.5,leading=11)
c.showPage();c.save();print(OUT)
