# 만성질환 홍보 이미지 제작 기록

- 제작일: 2026-10-28
- 제작 모드: 내장 이미지 생성 도구 (`image_gen`), 신규 이미지 생성, 불투명 배경.
- 용도: 만성질환 방문 안내 페이지 및 공유용 홍보물.
- 실제 병원·장비 사진이 아닌 상징적 생성 이미지입니다.
- 최종 웹 파일: `assets/myeonmok-chronic-care-guide.webp` (1536×864), `assets/myeonmok-chronic-care-poster.webp` (1024×1536).
- 원본 PNG에서 FFmpeg libwebp 품질 86으로 변환했습니다.

## 이미지 1 최종 프롬프트

```text
Use case: ads-marketing. Create a polished Korean clinic website landscape illustration, 1536x864, for 면목연세석내과. This is a NEW marketing image, not a real clinic photo. Warm ivory background, deep teal typography, muted sage green and soft peach, gentle paper texture, calm premium editorial design consistent with a neighborhood internal medicine clinic. Left side: spacious Korean typography with generous margins; right side: tasteful symbolic still life of a glucose meter with an unnumbered blank screen, a blood pressure cuff, a stethoscope, a closed medical folder, and a small leaf. No people, no real facility, no brand marks on devices, no numbers on readings, no anatomy diagrams, no clinical outcome claims. Exact Korean text only, crisp and correctly spelled:
"중랑구 · 면목동"
"당뇨 · 고지혈증 · 고혈압"
"진료 전 확인하세요"
"면목연세석내과"
"서울 중랑구 면목로 398 스마트빌딩 2층"
"진료 문의 02-437-0808"
Make the three conditions the dominant heading, line breaks may be tasteful. All copy fully inside frame. Do not add additional copy, guarantees, awards, rankings, or logos.
```

## 이미지 2 최종 프롬프트

```text
Use case: ads-marketing. Create a refined Korean portrait clinic information poster, 1024x1536, for 면목연세석내과, matching warm ivory, deep teal and muted sage palette with soft peach accent. NEW symbolic editorial illustration, not a hospital photograph. Elegant readable Korean typography and three balanced illustrated sections with a small medical folder, a glucose meter with NO readings/numbers, and a calendar plus telephone. Spacious margins and calm reassuring visual rhythm. Exact text:
"중랑구 · 면목동 내과"
"당뇨 · 고지혈증 · 고혈압"
"내과 방문 준비"
"면목연세석내과"
"검사 결과 확인"
"복용 중인 약 정리"
"진료 일정 문의"
"면목로 398 스마트빌딩 2층 외래"
"02-437-0808"
No other text. No people, no real facility, no medical instructions, no treatment efficacy promises, no rankings or invented badges. This is a symbolic clinic promotion poster with beautifully precise Hangul and clear hierarchy.
```

