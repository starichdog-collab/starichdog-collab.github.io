# 네이버 검색 수집 및 플레이스 관리

정보 확인일: 2026-10-27

## 사이트에 적용한 사항

- 페이지별 고유 제목·설명·대표 주소, 한국어 HTML 본문, 이미지 설명과 사이트맵을 유지합니다.
- 길었던 신장투석 안내 제목을 간결하게 정리하고 면목동·상봉동·망우동 방문 정보는 본문에 유지했습니다.
- 병원명·주소·전화번호가 일치하는 네이버 플레이스(ID 1648448794)를 확인하고 지도 링크와 병원 구조화 데이터에 연결했습니다.
- 공유 정보에 사이트명·이미지 형식·크기를 추가했습니다.
- 본문 전체와 절대 주소를 포함하는 `feed.xml`을 생성하고 모든 안내 페이지에서 연결했습니다.
- 네이버 IndexNow에 병원 경로의 갱신만 알릴 수 있는 공개 확인 파일과 전송 스크립트를 준비했습니다. 이 공개 키는 로그인 비밀번호가 아닙니다.

## 제출 주소

- 만성질환 안내: https://starichdog-collab.github.io/myeonmok-yonsei-seok/chronic-care/

- 병원 안내: https://starichdog-collab.github.io/myeonmok-yonsei-seok/
- 사이트맵: https://starichdog-collab.github.io/myeonmok-yonsei-seok/sitemap.xml
- RSS: https://starichdog-collab.github.io/myeonmok-yonsei-seok/feed.xml
- 일반 내과: https://starichdog-collab.github.io/myeonmok-yonsei-seok/myeonmok-internal-medicine/
- 신장투석: https://starichdog-collab.github.io/myeonmok-yonsei-seok/jungnang-dialysis/
- 소개 영상: https://starichdog-collab.github.io/myeonmok-yonsei-seok/video/

## 서치어드바이저 등록의 현재 제약

네이버 웹마스터도구는 경로별 등록이 아닌 호스트 단위 등록을 지원합니다. 현재 호스트의 루트 `https://starichdog-collab.github.io/`는 다른 사업 사이트로 JavaScript 및 meta refresh 이동을 수행하고 있습니다. 네이버는 이런 루트 이동 방식에서 소유 확인이 지원되지 않는다고 안내합니다. 병원 경로의 검색 수집 자체가 불가능하다는 뜻은 아닙니다.

병원 전용 도메인으로 이전하면 그 도메인을 등록하는 것이 명확합니다. 이전은 별도 확인 대기 상태이며 이번 작업에서 기존 계정이나 루트 페이지를 변경하지 않았습니다. 서치어드바이저 계정의 등록 현황은 로그인 전이라 확인하지 못했습니다. 사이트맵·RSS의 관리 화면 제출도 아직 완료한 것으로 표시하지 않습니다.

IndexNow는 병원 하위 경로에 둔 공개 키의 `keyLocation`을 명시하여 해당 경로의 페이지만 알릴 수 있습니다. 다른 사업의 URL은 전송 대상에서 제외합니다. API의 200은 전송 성공, 202는 URL 수신 후 키 확인 중을 의미하며 색인 완료나 순위 상승을 뜻하지 않습니다.

## 업데이트할 때

병원 HTML 수정 후 다음 명령으로 본문 전체 RSS를 갱신합니다.

```sh
python marketing/build-search-feeds.py
```

GitHub Pages 배포와 공개 키의 정상 응답을 확인한 뒤, 아래 명령으로 네이버에 한 번 알립니다. 스크립트는 공개 키를 읽을 수 있는지 확인하고 사이트맵에 있는 안내 URL만 전송합니다. `--submit` 없이 실행하면 미리보기만 출력합니다.

```sh
python marketing/notify-indexnow.py --submit
```

신규 도메인으로 이전할 때는 해당 도메인용 키를 새로 만들고 사이트맵·대표 주소·RSS를 함께 갱신해야 합니다. 현재 도메인의 키를 다른 도메인에 재사용하지 않습니다.

## 플레이스에 남은 작업

병원 플레이스는 이미 공개되어 있습니다. 새 업체를 중복 등록하지 말고 병원 관리 권한이 있는 계정의 기존 업체에서 수정합니다. `naver-place-copy.txt`에 공개 정보와 일치하는 소개문·대표 키워드 후보를 준비했습니다. 업체명은 실제 명칭을 유지하며 공식 홈페이지, 진료시간, 전화번호를 정확히 관리합니다. 대표 사진은 실제 병원 사진을 사용합니다.

이 문안의 플레이스 저장·제출은 아직 진행하지 않았습니다. 웹사이트 변경과 플레이스 검색 결과 관리는 별개입니다.

## 공식 참고 자료

- [네이버 검색 최적화 기초](https://searchadvisor.naver.com/guide/seo-basic-intro)
- [사이트맵·RSS 안내](https://searchadvisor.naver.com/guide/request-feed)
- [IndexNow 공개 키](https://searchadvisor.naver.com/guide/indexnow-api-key)
- [IndexNow 갱신 알림과 응답 코드](https://searchadvisor.naver.com/guide/indexnow-request)
- [플레이스 검색 운영 안내](https://new.smartplace.naver.com/help/policy?menu=abuse&tab=smartplace)
