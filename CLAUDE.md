# 정진한의원 홈페이지

https://jungjinmedi.netlify.app · 정적 사이트 20페이지 · 의료광고 규제 대상

---

## 절대 규칙 하나

**HTML 을 직접 고치지 않는다.** `_build/` 의 파이썬이 20개 HTML 과 sitemap.xml 을 찍어냅니다.
HTML 을 손으로 고치면 다음 빌드에서 전부 되돌아갑니다.

```bash
cd _build && python3 build.py     # 20페이지 + sitemap 재생성
```

내용을 고칠 곳:

| 고칠 것 | 파일 |
|---|---|
| 메뉴 · 상단바 · 푸터 · 오시는 길 · 진료시간 · 연락처 | `_build/partials.py` |
| 메인 페이지 구성 | `_build/build.py` |
| 허브 2개 (관절통증 · 자율신경질환) | `_build/build_hubs.py` |
| 질환 7페이지 원고 | `_build/content_specialty.py` · `content_pain.py` |
| 메인 원고 (히어로 · 다섯 가지 · 원장 이야기) | `_build/content_home.py` |
| 치료방법 · 약관 · 비급여 등 | `_build/build_pages.py` |
| 색 · 글꼴 · 여백 · 레이아웃 | `styles.css` (여기는 직접 고칩니다) |

**`styles.css` 를 고쳤으면 `partials.py` 의 `CSS_V` 를 반드시 올립니다.**
안 올리면 방문자 브라우저가 옛 CSS 를 계속 씁니다. 이미지·영상을 바꿨으면 `IMG_V`.

---

## 작업 순서

```
_build/ 고침 → python3 build.py → 브라우저로 확인 → git push → Netlify 자동 배포
```

- 이 폴더에서 세션을 시작하면 **미리보기 서버가 자동으로 뜹니다** (http://localhost:8765)
- `quickmenu()` 가 `</body></html>` 까지 함께 내보냅니다. `tail()` 에 무엇을 더할 때는
  **반드시 그 앞에** 넣으십시오 — 뒤에 두면 body 밖으로 나가서, 화면에는 보이는데
  `getElementById` 로는 안 잡히는 상태가 됩니다
- `git push` 하면 Netlify 가 알아서 배포합니다. **zip 을 만들어 끌어다 놓지 마십시오** — 다음 push 때 덮어써집니다
- 배포 전에는 아래 "완료 전 점검" 을 돌립니다

---

## 완료 전 점검 — 눈으로 보지 말고 재십시오

python-pptx 처럼 조용히 깨지는 것이 많습니다. **브라우저에서 값을 재서 확인합니다.**

반드시 확인할 것:

1. **가로 넘침** — 320 · 375 · 768 · 1280 · 1440px 에서 `scrollWidth > clientWidth` 인 페이지가 하나도 없어야 합니다
2. **컨테이너 좌측 정렬** — 1280px 에서 모든 `.container` 의 `left` 가 같은 값(53px)이어야 합니다
3. **깨진 링크 · 앵커** — 파일 존재와 `#id` 대상 존재
4. **제목 규격** — 크기당 행간·자간이 하나여야 합니다 (아래 표)
5. **글꼴** — Pretendard 와 나눔명조 둘 말고 다른 것이 나오면 안 됩니다
6. **의료광고 표현** — 아래 목록이 하나도 없어야 합니다

숨은 iframe 에 각 페이지를 폭별로 띄워 재는 방식이 빠릅니다. `.js-reveal` 은
`opacity:1; transform:none` 로 눌러 두고 재야 위치가 정확합니다.

### 재는 방법 — 이 맥의 Chrome 을 직접 띄웁니다

그림으로 뽑아 눈으로 볼 수도 있고, 값을 재서 숫자로 받을 수도 있습니다.

```bash
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# 화면을 그림으로
perl -e 'alarm 30; exec @ARGV' "$CH" --headless --disable-gpu --hide-scrollbars \
  --virtual-time-budget=4000 --user-data-dir=/tmp/cprof/a --window-size=1440,900 \
  --screenshot=/tmp/shot.png http://localhost:8765/index.html

# 값을 재서 — 잰 값을 document.title 에 넣고 DOM 을 덤프해 받습니다
perl -e 'alarm 30; exec @ARGV' "$CH" --headless --disable-gpu \
  --virtual-time-budget=4000 --user-data-dir=/tmp/cprof/b \
  --dump-dom http://localhost:8765/_probe.html | grep -o '<title>[^<]*</title>'
```

걸리는 곳이 셋 있습니다. 모르면 시간을 크게 버립니다.

- **Chrome 은 창을 500px 아래로 줄이지 못합니다.** `--window-size=390,780` 을 줘도
  `innerWidth` 는 500 입니다. 스크린샷만 390 으로 잘려 나오기 때문에 **멀쩡한 화면이
  오른쪽 잘린 것처럼 보입니다.** 320 · 390px 은 폭을 지정한 iframe 안에 띄워서
  재십시오 — 그래야 진짜 그 폭으로 조판됩니다
- **한 번 띄우는 데 20~30초 걸립니다** (지도 embed). `perl -e 'alarm 30; exec @ARGV'`
  로 감싸지 않으면 명령이 안 끝납니다
- `--user-data-dir` 은 매번 다른 경로로 주십시오. 고친 CSS 가 캐시에서 나오는지
  의심하느라 시간을 쓰지 않게 됩니다

**node 는 안 깔려 있습니다.** 자바스크립트 문법만 보려면 JavaScriptCore 를 씁니다.

```bash
JSC=/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc
echo "try { new Function(read('script.js')); print('ok') } catch(e) { print(e) }" > /tmp/c.js
"$JSC" /tmp/c.js
```

`_probe*.html` 같은 검사용 파일은 재고 나면 **지웁니다.** 저장소에 남기지 마십시오.

---

## 의료광고 — 어길 수 없다

의료법 제56조 대상입니다. 후기 페이지는 이미 없앴고 `_redirects` 가 FAQ 로 보냅니다.

**금지 표현**
완치 · 100% · 반드시 낫 · 보장 · 무조건 · 부작용 없 · 재발 없 ·
최고 · 최상 · 1위 · 유일 · 국내 최초 · 명의 · 권위자 ·
후기 · 체험담 · 전후 사진 · 이벤트 · 할인 · 무료 진료 · 선착순

**그 밖에**

- 치료 결과를 성과로 제시하지 않습니다 (횟수 · 기간 · 성공률 · 보행거리 향상)
- 다른 의료기관·치료법을 낮추지 않습니다
- 수술을 받지 말라거나 미루라고 하지 않습니다
- 환자 얼굴 · 치료 전후 비교 사진을 쓰지 않습니다
- **안전 문구를 각 페이지 본문 끝에 한 번 둡니다** —
  `상태와 원인에 따라 접근이 달라질 수 있으며, 정확한 진단이 우선입니다.`
  (`partials.NOTICE_LINE`)
- 비급여 진료비용 고지(의료법 제45조)는 `pricing.html` 이 담당합니다. 금액이 바뀌면
  `partials.PRICE_DATE` 도 함께 갱신합니다

지역명(구리 · 구리역)과 원장 이름(양정진)은 **씁니다.** 검색 유입과 법정 표기에 필요합니다.

---

## 말투

원장이 확실히 지적한 부분입니다. **"이렇게 해 드립니다" 가 아니라 무엇인지를 씁니다.**

| ✗ 진행 서술 | ✓ 내용 진술 |
|---|---|
| 통증이 어떻게 생기는지 설명드립니다 | 디스크가 신경을 자극해 생기는 통증입니다 |
| 순서와 방법을 알려 드립니다 | 원인이 되는 자리를 손으로 짚어 확인합니다 |

예외 — 환자에게 하는 **약속**은 그대로 둡니다.
("필요한 것만 권해 드립니다", "매번 설명해 드립니다")

**원고를 새로 짓지 않습니다.** 새 문구가 필요하면 원장에게 확인받거나,
이미 사이트에 있는 문장을 가져다 씁니다.

---

## 디자인 시스템

`styles.css` 맨 위 `:root` 가 유일한 출처입니다. 값을 새로 정하지 말고 토큰을 씁니다.

**색 — 넷뿐입니다**

```
--brown  #3a2a20   어두운 면 (상단바 · 히어로 · 마무리 배너 · 푸터)
--brand  #4e1412   로고 원색 (로고 · 파비콘에만)
--accent-deep #6b2019   강조 글자 · 링크
--text   #262220 / --muted #655c54 / --line #e6e1d7
```

**글꼴 — 두 벌뿐입니다**

- **Pretendard Variable** — 읽는 글 전부 (jsdelivr)
- **나눔명조 700** — 큰 제목만 (Google Fonts). 굵기는 700 하나만 받습니다

폼 요소는 글꼴을 물려받지 않으므로 `button, input, select, textarea { font: inherit }` 가
있습니다. 지우면 버튼이 Arial 로 떨어집니다.

**제목 규격 — 크기당 한 줄. 새 값을 만들지 마십시오**

| 크기 | 행간 | 자간 | 어디 |
|---|---|---|---|
| 48px | 1.25 | −0.035em | 히어로 제목 |
| 40px | 1.25 | −0.030em | 페이지 상단 제목 |
| 38px | 1.28 | −0.030em | 섹션 제목 |
| 32px | 1.35 | −0.028em | 기사 제목 · 마무리 배너 |
| 24 · 21px | 1.45 | −0.015em | 중제목 · 소제목 |

읽는 글은 18px · 행간 1.85 · 자간 0. **한글 본문에 음수 자간을 주지 마십시오** —
받침이 붙어 오히려 읽기 나빠집니다. 15px 이하 라벨만 `+0.04em` 으로 벌립니다.

**레이아웃**

- `.container` 최대 1160px · 좌우 여백 24px
- 섹션 세로 여백은 역할별로 고정 — 본문 섹션 92~104px, 페이지 상단 84/76, 마무리 배너 72
- 그림자는 쓰지 않습니다 (`--shadow: none`). 구조는 얇은 선으로 드러냅니다
- 카드 그리드는 `.svc__grid` 계열을 씁니다. 새 열 수가 필요하면 변형을 추가합니다

---

## 페이지 구성

```
index                    메인
story-philosophy         한의원 소개 (원장 이야기 · 철학 · 약력 · 시설 · 오시는 길)
pain                     관절통증 허브 → stenosis · disc · joint
autonomic-disorders      자율신경질환 허브 → dizziness · panic · stomach · cough
faq                      자주 묻는 질문
care · acupuncture · chuna · herb    치료 방법 — 메뉴에 없고 본문 링크로만 들어갑니다
pricing · privacy · terms · 404      푸터 링크
```

상단 메뉴는 네 칸입니다: 한의원 소개 ▾ / 관절통증 ▾ / 자율신경질환 ▾ / 자주 묻는 질문.
드롭다운 하위는 진단명 그대로 씁니다 — 자기 병 이름을 알고 오시는 분이 한눈에 집도록.

메인에는 `#subjects` 구획이 있습니다. 진단명 일곱을 **이름만** 폅니다 —
상단 메뉴를 못 찾은 분에게 이것이 진료 페이지로 가는 유일한 길입니다.
증상어와 설명은 각 페이지에 있으니 여기서 되풀이하지 마십시오.
목록은 `partials.AXES` · `AXIS_CHILDREN` 을 그대로 읽으므로 따로 손댈 곳이 없습니다.

---

## 아직 열려 있는 것

- **사진** — 사이트 전체 이미지가 로고 빼면 두 장뿐입니다. 진료 장면 · 대기실 · 진료실 ·
  치료실 · 탕전실 · 건물 외관 여섯 장이 필요합니다. `assets/facility/` 는 아직 없습니다
- **버스 노선번호** — `partials.BUS_EXPRESS` · `BUS_LOCAL`. 공개 자료 두 곳이 일치한 값이지만
  현장 확인은 안 됐습니다
- **얇은 페이지** — `pain.html` 414자, `herb.html` 436자
- 모바일 히어로 안내줄이 11.6px (한 줄 유지를 위한 의도적 축소)
