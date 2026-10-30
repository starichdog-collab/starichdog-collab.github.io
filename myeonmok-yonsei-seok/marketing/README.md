# 지역 검색 안내·미디어 작업 기록

최신 현황: 2026-10-30. 특정 검색어의 순위·색인 완료를 의미하지 않습니다.

## 현재 공개 자료

- HTML 안내 7개: 병원 안내, 내과, 만성질환, 신장투석, 첫 방문·전원 상담, 진료시간·위치, 영상.
- [공유 자료 모음](../assets/README.md): PDF 1종, 텍스트 질문표 2종, 실제 병원 사진으로 만든 소개 영상.
- [한 장 방문 안내 PDF](https://starichdog-collab.github.io/myeonmok-yonsei-seok/assets/myeonmok-visit-guide.pdf): 한국어 검색 가능 텍스트, 실제 시설 사진, 연락처, 클릭 링크와 QR코드.
- 사이트맵: HTML 7개와 PDF 1개. RSS: HTML 본문 7개.
- [공식 홈페이지 적용안](official-site-seo-package.md): HTTPS 대표주소, 중복 제목·설명, 시설 사진 대체 텍스트의 남은 템플릿 문구를 재점검했습니다. 공식 사이트에 적용 완료한 결과는 아닙니다.

아래는 2026-10-27 초기 작업 기록입니다. 당시 페이지 수는 현재 현황과 다릅니다.

## 공개 페이지

- [병원 안내](https://starichdog-collab.github.io/myeonmok-yonsei-seok/): 중랑구 신장투석 중심 제목·설명·H1 및 지역 안내 연결
- [방문 준비 안내](https://starichdog-collab.github.io/myeonmok-yonsei-seok/jungnang-dialysis/): 면목동의 실제 병원 위치, 상봉동·망우동에서 방문할 때 확인할 내용, 상담 준비 안내
- [영상 전용 페이지](https://starichdog-collab.github.io/myeonmok-yonsei-seok/video/): 30초 가로 영상, 한국어 자막, 텍스트 설명, 세로 영상 및 이미지 다운로드
- [병원 공식 홈페이지](https://www.xn--vb0bn4ecstcd77y.com/): 위 안내 페이지에서 연결하는 공식 정보 출처

## 검색 설정

각 페이지는 고유 title/description/canonical, 한국어 lang, 공유 이미지(OG), 색인 허용 메타데이터, WebPage/MedicalClinic/BreadcrumbList 구조화 데이터를 제공합니다. 영상 페이지에 실제 MP4의 VideoObject를 추가했습니다.

루트 robots.txt에서 병원 전용 sitemap.xml을 안내합니다. 전용 사이트맵은 실제 공개 페이지 3개와 이미지·영상 URL을 포함합니다. 기존 태양광 페이지와 링크는 수정하지 않았습니다.

## 링크 반영 범위

지역 안내 및 영상 페이지에서 병원 공식 홈페이지로 정상적인 HTML 링크를 연결했습니다. 같은 GitHub Pages 내 페이지 간 연결은 내부 링크이며, 서로 다른 외부 사이트의 추천 링크로 계산하지 않습니다. 제3자 블로그·카페 게시나 유튜브 업로드를 실행한 것은 아닙니다. 관련 운영 채널에 게시할 수 있는 문안은 publishing-copy.txt에 있습니다.

순위 조작용 링크 구매·자동 댓글·무관한 사이트에 대량 링크 게시·동네 이름만 바꾼 중복 페이지는 사용하지 않았습니다.

## 구글 확인에 필요한 주소

- 사이트맵: https://starichdog-collab.github.io/myeonmok-yonsei-seok/sitemap.xml
- URL 검사 대상: 현재 공개 HTML 안내 7개와 PDF 1개
- Search Console 소유자·전체 사용자 권한으로 사이트맵 제출 및 색인 상태 확인이 필요합니다. robots.txt를 통한 사이트맵 공개와 Search Console 제출은 별개입니다.

## 미디어

- 가로 1280×720, 세로 720×1280 / 각각 30초 / H.264 + AAC MP4
- 실제 병원 사진과 한국어 화면 자막, 자체 합성 배경음악을 편집한 슬라이드 형식입니다. 별도 내레이션이나 촬영 영상은 없습니다.
- build_video.py는 로컬 FFmpeg로 영상을 제작하며 유료 서비스/API를 호출하지 않습니다.
- 홍보용 일러스트 2장은 이미지 생성 도구로 제작했습니다. 실제 병원 시설 사진과 구분해 표시합니다.
- 사진·진료 정보 출처는 상위 README.md를 참고하세요.

## 참고한 구글 공식 문서

- https://developers.google.com/search/docs/essentials/spam-policies
- https://developers.google.com/search/docs/crawling-indexing/links-crawlable
- https://developers.google.com/search/docs/appearance/video
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl

## 2026-10-27 일반 내과 검색 안내 보강

- 신규 안내: https://starichdog-collab.github.io/myeonmok-yonsei-seok/myeonmok-internal-medicine/
- 홈페이지 제목·설명·첫 화면과 내과 안내를 보강하고, 기존 신장투석·영상 페이지를 유지했습니다.
- 진료 분야·의료진·외래시간·위치·방문 준비를 하나의 원본 안내 페이지에 모았습니다.
- 공식 병원 내과·신장·초음파·인공신장실·의료진 페이지에 문맥형 링크를 추가했습니다. 같은 GitHub 도메인에서 제공하는 링크이며 제3자 블로그·카페에 게시한 것은 아닙니다.
- 새 가로/세로 홍보 일러스트를 WebP로 게시하고, 이미지 대체 텍스트·OG·ImageObject·사이트맵에 반영했습니다.
- 도메인 변경은 별도 승인 대기 중입니다. Google Search Console 등록은 사용자가 직접 진행합니다.
