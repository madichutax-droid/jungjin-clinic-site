# -*- coding: utf-8 -*-
"""
모든 페이지가 공유하는 조각(머리말·상단바·헤더·푸터·퀵메뉴·CTA).

여기만 고치면 20개 페이지에 한 번에 반영됩니다.
예전에는 이 부분이 페이지마다 복사돼 있어서, 진료시간 한 줄 바꾸는 데
20개 파일을 손대야 했습니다.
"""

CSS_V = "106"
JS_V  = "4"
IMG_V = "3"

CLINIC   = "정진한의원"
ADDRESS  = "경기도 구리시 경춘로 223 명동빌딩 5층"
TEL      = "031-522-5923"
FAX      = "070-7507-5923"
BIZNO    = "880-46-01214"
# 진료 안내문은 각 페이지 본문 끝에 한 번만 둡니다(푸터 중복 제거, 2026-09-01).
NOTICE_LINE = "상태와 원인에 따라 접근이 달라질 수 있으며, 정확한 진단이 우선입니다."
YEAR = "2026"
LEGAL_DATE = "2026년 9월 1일"   # 약관·처리방침 시행일. 실제 공개일로 맞추십시오.
PRICE_DATE = "2026. 09. 01."   # 비급여 고지 시행일. 금액이 바뀌면 함께 갱신하십시오.
PRIVACY_OFFICER = "양정진"      # 개인정보 보호책임자

# 버스 — 경춘로 중앙차로 '구리역·롯데백화점' 정류장 기준입니다.
# 노선 번호는 경기버스정보·나무위키 두 곳에서 같은 목록을 확인해 적었습니다(2026-09-05).
# 노선은 개편될 수 있으니, 바뀌면 여기만 고치면 메인과 한의원 소개가 함께 바뀝니다.
# 처음 오시는 분은 도로명 주소보다 이 줄로 찾습니다.
# 마지막 100m 를 책임지는 문장이라 주소 바로 아래에 둡니다.
LANDMARK      = "돌다리사거리 · 구리전통시장 입구 맞은편"
LANDMARK_BLDG = "투썸플레이스 건물 5층"

BUS_STOP    = "구리역·롯데백화점 정류장 하차"
BUS_EXPRESS = "1115-6 · 1330-2 · 1330-3 · 1330-4 · 1330-44 · 8005 · 8409"
BUS_LOCAL   = "10-5 · 30 · 65 · 65-1 · 165 · 166-1 · 167-1 · 2000-1"


def bus_nos(s):
    """노선 번호마다 줄바꿈을 막습니다. 안 묶으면 좁은 화면에서 '166-1' 이
    하이픈에서 잘려 '166-' 와 '1' 로 갈라집니다."""
    return " · ".join(f'<span class="bus__no">{x}</span>' for x in s.split(" · "))

# 외부 채널 — 하단 퀵메뉴에 붙습니다. 주소가 없으면 그 아이콘은 나오지 않습니다.
BLOG     = "https://blog.naver.com/yjj2923"
PLACE    = ""   # TODO: 네이버 플레이스 주소
INSTA    = ""   # TODO: 인스타그램 주소
DOMAIN   = "https://jungjinmedi.netlify.app"
HOURS_BAR  = "진료시간 평일 09:00–20:00 (점심 13:00–14:00) · 토·공휴일 09:00–15:00 · 일요일 휴진"
HOURS_ROWS = ("평일 09:00–20:00<br />"
              "<span class=\"hours__sub\">점심시간 13:00–14:00</span><br />"
              "토요일·공휴일 09:00–15:00<br />"
              "<span class=\"hours__sub\">점심시간 없이 진료합니다</span><br />"
              "일요일 휴진<br />"
              "<span class=\"hours__sub\">설·추석 연휴는 휴진합니다</span>")
INK = "#262220"

REGION = "구리"          # 검색 유입용 지역명 (제목·설명에 붙습니다)
STATION = "구리역"

# ── 상단 메뉴 ─────────────────────────────────────────────────
#
# 2026-08-26 정리 — 다섯 칸으로 갑니다.
#   관절 / 어지럼증 / 공황장애 / 만성기침 / 위장
#
# 관절통증과 자율신경질환이 하위 과목을 드롭다운으로 답니다.
# 하위 이름은 진단명 그대로 씁니다 — 자기 병 이름을 알고 찾아오시는 분이
# 한눈에 집을 수 있게. 드롭다운은 2단까지만이라 자율신경질환 아래는
# 어지럼·불안·위장 계열의 진단명 다섯을 나란히 폅니다.
# 여성 질환은 메뉴·페이지·원고까지 모두 삭제했습니다.
#
# 2026-09-05 — 만성기침을 자율신경질환 아래로 넣었습니다.
# 오래된 기침은 위에서 올라오는 경우를 함께 보기 때문에 역류성식도염 옆이
# 제자리입니다. 모바일 메뉴는 하위 항목까지 한 번에 펼쳐지므로
# 상단 한 칸을 잃어도 기침으로 찾아오시는 분의 동선은 그대로입니다.
AXES = [
    ("pain",      "관절통증"),
    ("autonomic-disorders", "자율신경질환"),
]

# (슬러그, 메뉴에 쓰는 진단명, 페이지에서 쓰는 증상어)
PAIN_SUBJECTS = [
    ("stenosis", "척추관협착증",  "걸으면 다리가 저려 쉬어야 한다"),
    ("disc",     "디스크", "허리·목에서 팔다리로 내려가는 저림"),
    ("joint",    "어깨·무릎 관절", "팔이 안 올라가고, 계단을 내려가기 어렵다"),
]
# 자율신경질환 — 어지럼 계열 · 불안 계열 · 위장 계열 · 기침을 한 갈래로 묶었습니다.
# 기침은 역류성식도염 바로 뒤에 둡니다. 위에서 올라와 생기는 기침이라
# 앞 칸에서 읽던 이야기가 그대로 이어집니다.
ANS_SUBJECTS = [
    ("dizziness", "어지럼증",     "천장이 도는 어지럼 · 일어설 때 아찔함"),
    ("panic",     "공황장애",     "가슴 두근거림·불안"),
    ("stomach",   "역류성식도염", "속쓰림·트림·체함"),
    ("cough",     "만성기침",     "감기약을 먹어도 낫지 않는 기침"),
]
INTERNAL_SUBJECTS = list(ANS_SUBJECTS)

INTRO_CHILDREN = [
    ("story-philosophy#story",      "원장 이야기"),
    ("story-philosophy#philosophy", "진료와 치료철학"),
    ("story-philosophy#cv",         "약력 · 자격"),
    ("story-philosophy#facility",   "내부 시설"),
    ("story-philosophy#location",   "오시는 길"),
]

AXIS_CHILDREN = {
    "pain":                PAIN_SUBJECTS,
    "autonomic-disorders": ANS_SUBJECTS,
}

SUBJECTS = PAIN_SUBJECTS + INTERNAL_SUBJECTS

PAGE_LABELS = {"pain": "관절통증", "autonomic-disorders": "자율신경질환"}
PAGE_LABELS.update({slug: label for slug, label, _ in SUBJECTS})


import json as _json
import re as _re

# 한글 종결어미 뒤의 공백만 줄바꿈으로 바꿉니다.
# 문장이 <strong>…</strong> 안에서 끝나는 경우가 있어 닫는 태그는 건너뜁니다.
_SENT = _re.compile(
    r'([다요죠까네][.!?][\u201d\u2019"\']?)((?:</(?:strong|em|b|i|a)>)*)\s+')

BR_M = '<br class="only-mobile" />'

# 휴대폰(390px)에서 한 줄에 들어가는 글자 수. 한글 19~20자, 공백까지 24자쯤입니다.
# 이 길이를 넘는 문장은 어차피 두 줄이 되므로, 아무 데서나 넘어가지 않도록
# 절이 끝나는 자리에서 우리가 먼저 끊습니다.
MOBILE_CAP = 24

_TAG = _re.compile(r'<[^>]+>')

# 끊어도 안전한 자리 — 쉼표와, 명사로 오해할 일이 없는 연결어미만 씁니다.
_CLAUSE = _re.compile(
    r'(,|(?<=[가-힣])(?:는데|은데|지만|면서|라서|아서|어서|해서|으며|하며'
    r'|으면|하면|되면|어도|아도|니까|거나))'
    r'((?:</(?:strong|em|b|i|a)>)*)\s+')


def _vis_len(t):
    """태그를 뺀 실제 글자 수."""
    return len(_TAG.sub("", t))


def _rows(n):
    """글자 수 n 이 휴대폰에서 몇 줄로 그려지는지."""
    return max(1, -(-n // MOBILE_CAP))


def _cost(parts):
    """조각 묶음의 점수. 작을수록 좋습니다.

    1) 꼬리줄 — 마지막 줄이 한 줄의 40% 도 안 되게 남는 조각 수
    2) 줄 수  — 화면에서 차지하는 줄
    3) 조각 수 — 같은 값이면 덜 끊는 쪽

    이 순서로 봅니다. 꼬리를 없애는 것이 먼저이고,
    그 다음이 짧은 토막을 만들지 않는 것입니다.
    """
    stub = rows = 0
    for p in parts:
        n = _vis_len(p)
        r = _rows(n)
        rows += r
        if r > 1 and (n - (r - 1) * MOBILE_CAP) / MOBILE_CAP < 0.40:
            stub += 1
    return (stub, rows, len(parts))


def _plan(seg, depth=0):
    """끊을 자리를 골라 조각 목록을 만듭니다.

    가운데(25~75%)에 있는 후보를 모두 넣어 보고 점수가 가장 좋은 것을 씁니다.
    가운데에서 가장 가까운 자리가 늘 좋은 것은 아닙니다 —
    한쪽을 또 끊게 만들어 짧은 토막이 생기는 경우가 있습니다.
    """
    best = [seg]
    if depth >= 2 or _vis_len(seg) <= MOBILE_CAP:
        return best
    total = _vis_len(seg)
    for m in _CLAUSE.finditer(seg):
        ratio = _vis_len(seg[:m.end()]) / total
        if not (0.25 <= ratio <= 0.75):
            continue
        cand = (_plan(seg[:m.start()] + m.group(1) + m.group(2), depth + 1)
                + _plan(seg[m.end():], depth + 1))
        if _cost(cand) < _cost(best):
            best = cand
    return best


def _split_clause(seg):
    return (BR_M + " ").join(_plan(seg))


def lines(t):
    """줄바꿈은 휴대폰에서만 넣습니다. PC 는 글이 자연스럽게 흐르게 둡니다.

    1) 문장이 끝나면 줄을 바꿉니다.
    2) 그러고도 한 줄(24자)을 넘는 문장은 절이 끝나는 자리에서 한 번 더 끊습니다.

    PC(한 줄 35자)에서는 문장마다 강제로 끊으면 오른쪽이 들쭉날쭉해지므로,
    모든 줄바꿈에 only-mobile 을 달아 화면이 넓어지면 사라지게 합니다.
    "1. " 같은 번호나 링크 주소(.html)의 점은 건드리지 않습니다.
    """
    if not t:
        return t
    t = _SENT.sub(r'\1\2' + BR_M + ' ', t)
    return (BR_M + " ").join(
        _split_clause(seg) for seg in t.split(BR_M + " "))


# ── 검색 설명문 ───────────────────────────────────────────────
# 페이지마다 따로 씁니다. 짧으면 검색 결과에서 자리를 못 채우고,
# 길면 잘립니다. 한글 기준 75~110자를 맞췄습니다.
SEO_DESC = {
 "acupuncture": "굳은 자리와 눌렀을 때 통증이 재현되는 자리를 손으로 짚어 판단하고, 침을 놓은 뒤 치료반응으로 확인합니다. 강도가 모자랄 때는 약침을 함께 씁니다. 구리역 정진한의원.",
 "chuna": "관절과 근육이 어디서 막혀 있는지 손으로 확인하고 움직임이 살아나도록 조정하는 추나요법입니다. 건강보험이 적용되며 상태에 따라 침 치료와 함께 씁니다. 구리역 정진한의원.",
 "herb": "대변·소변·소화·땀을 먼저 살핀 뒤 부족한 것을 채웁니다. 같은 병명이라도 몸이 반응하는 방향이 다르면 처방이 달라집니다. 구리 구리역 정진한의원 1:1 맞춤 한약.",
 "care": "처음 오시면 어떤 순서로 진행되는지, 침을 놓은 뒤 몸에서 무엇이 느껴지는지 미리 정리했습니다. 회복의 기준과 자주 받는 질문도 함께 담았습니다. 구리역 정진한의원.",
 "faq": "예약·대기 시간·건강보험·자동차보험·주차·한약 처방 일수까지, 오시기 전에 궁금하신 것을 모았습니다. 구리 구리역 정진한의원 진료 안내.",
 "pain": "척추관협착증·디스크·어깨무릎 관절통. 아픈 자리에서 멈추지 않고, 그 자리에 부담을 넘긴 곳까지 손으로 짚어 찾습니다. 구리역 도보 정진한의원.",
 "autonomic-disorders": "검사에는 이상이 없다는데 어지럼·두근거림·속의 불편·기침이 반복된다면. 따로 온 것처럼 보이는 증상을 한 갈래로 놓고 봅니다. 구리역 도보 정진한의원.",
 "stenosis": "걸으면 다리가 저려 쉬어야 하는 척추관협착증. 걸을 수 있는 거리를 기준으로 경과를 판단하고, 허리만이 아니라 부담을 넘긴 자리까지 봅니다. 구리역 정진한의원.",
 "disc": "허리·목에서 팔다리로 내려가는 저림. 영상에 보이는 크기와 실제 통증이 늘 비례하지는 않아, 눌렀을 때 통증이 재현되는 자리를 손으로 찾습니다. 구리역 정진한의원.",
 "joint": "팔이 안 올라가고 계단을 내려가기 어려운 어깨·무릎 관절통. 관절에 실리는 부하를 위아래까지 짚어 봅니다. 구리 구리역 도보 정진한의원.",
 "dizziness": "천장이 도는 어지럼과 일어설 때 아찔한 어지럼은 다릅니다. 어떤 어지럼인지 먼저 가린 뒤 원인 자리를 찾습니다. 구리 구리역 정진한의원 어지럼증·이석증.",
 "panic": "가슴이 두근거리고 숨이 막히는데 검사는 괜찮다고 들으셨다면. 몸을 편하게 만드는 일과 피해온 자리로 돌아가는 일을 함께 봅니다. 구리역 정진한의원.",
 "stomach": "속쓰림·트림·체함이 반복될 때, 증상이 시작된 순서를 되짚어 어디서 비롯됐는지 가립니다. 구리 구리역 정진한의원 역류성식도염·기능성 소화불량.",
 "cough": "감기약을 먹어도 낫지 않는 기침. 목에서 온 기침과 위에서 올라오는 기침을 여섯 가지로 구별해 볼 방향을 정합니다. 구리역 도보 정진한의원 만성기침.",
 "story-philosophy": "교통사고로 두 달을 누워 있던 한의사가, 왜 손으로 짚고 왜 치료반응을 확인하는지 씁니다. 양정진 원장 이야기와 진료철학. 구리 구리역 정진한의원.",
 "pricing": "상담료·한약·약침 등 건강보험이 적용되지 않는 항목의 진료비용을 안내합니다. 의료법 제45조에 따른 고지입니다. 구리 구리역 정진한의원.",
 "terms": "정진한의원 홈페이지 이용약관입니다. 서비스 이용 조건과 책임 범위, 최종 개정일을 안내합니다. 구리 구리역 정진한의원.",
 "privacy": "정진한의원 개인정보처리방침입니다. 수집 항목과 보유 기간, 진료기록 10년 보관 근거를 안내합니다. 구리 구리역 정진한의원.",
 "404": "요청하신 페이지를 찾을 수 없습니다. 진료과목과 오시는 길로 이동하실 수 있습니다. 구리 구리역 정진한의원.",
}


def faq_ld(pairs):
    """문답 목록을 FAQPage JSON-LD 로. head() 의 extra 에 그대로 넣습니다.

    화면에 보이는 답과 같은 글이어야 합니다 — 검색엔진은 페이지에 없는 내용을
    스키마에만 넣는 것을 규정 위반으로 봅니다. 그래서 lines() 로 줄을 나누기
    전의 원문을 쓰고, 태그만 걷어냅니다.
    문답이 없으면 빈 문자열이라 부르는 쪽에서 따로 나눌 필요가 없습니다."""
    if not pairs:
        return ""

    def plain(t):
        t = t.replace("{TEL}", TEL)
        t = _re.sub(r"<br\s*/?>", " ", t)      # 줄바꿈은 공백으로. 지우면 낱말이 붙습니다
        return _re.sub(r"\s+", " ", _TAG.sub("", t)).strip()

    body = _json.dumps(
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": plain(q),
                         "acceptedAnswer": {"@type": "Answer", "text": plain(a)}}
                        for q, a in pairs]},
        ensure_ascii=False, indent=2)
    # 본문에 </script> 가 들어가면 태그가 거기서 끊깁니다
    body = body.replace("</", "<\\/")
    return '  <script type="application/ld+json">\n  ' + body.replace("\n", "\n  ") + "\n  </script>\n"


def head(page, title, desc, extra="", keywords=""):
    """<head> 전체. canonical·og 를 페이지마다 자동으로 맞춥니다."""
    url = DOMAIN + "/" + ("" if page == "index" else page + ".html")
    desc = SEO_DESC.get(page, desc)      # 페이지별 설명문이 있으면 그것을 씁니다
    kw_tag = f'<meta name="keywords" content="{keywords}" />\n  ' if keywords else ""
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <script>
    /* PC 버전 선택을 기억했다가, 화면이 그려지기 전에 적용합니다 (깜빡임 방지) */
    (function () {{
      try {{
        if (localStorage.getItem('viewMode') === 'pc') {{
          document.querySelector('meta[name="viewport"]').setAttribute('content', 'width=1280');
        }}
      }} catch (e) {{}}
    }})();
  </script>
  <meta name="theme-color" content="{INK}" />
  <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png?v={IMG_V}" />
  <link rel="apple-touch-icon" sizes="180x180" href="assets/apple-touch-icon.png?v={IMG_V}" />
  <link rel="manifest" href="site.webmanifest" />
  <meta name="description" content="{desc}" />
  {kw_tag}<title>{title}</title>
  <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin />
  <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Nanum+Myeongjo:wght@700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="styles.css?v={CSS_V}" />
  <link rel="canonical" href="{url}" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="{CLINIC}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{DOMAIN}/assets/logo.png?v={IMG_V}" />
  <meta property="og:locale" content="ko_KR" />
{extra}</head>
<body>
  <a class="skip-link" href="#main">본문 바로가기</a>
"""


def topbar():
    return f"""  <div class="topbar">
    <div class="container topbar__inner">
      <span class="topbar__hours">{HOURS_BAR}</span>
      <a class="topbar__tel" href="tel:{TEL}">{TEL}</a>
    </div>
  </div>
"""


def _logo(home_prefix):
    return f"""      <a href="{home_prefix}#hero" class="logo">
        <img src="assets/logo.png?v={IMG_V}" alt="{CLINIC}" class="logo__img" width="800" height="223" />
      </a>"""


def header(page):
    """page 는 파일 이름(확장자 제외). 현재 위치를 메뉴에 표시합니다."""
    home = "index.html" if page != "index" else ""

    def li(slug, label, href, children=()):
        """상단 메뉴 한 칸. children 이 있으면 드롭다운이 붙습니다."""
        here = page == slug or page in [c[0].split('#')[0] for c in children]
        cls = (["has-sub"] if children else []) + (["is-active"] if here else [])
        attr = f' class="{" ".join(cls)}"' if cls else ""
        caret = ' <span class="caret" aria-hidden="true">▾</span>' if children else ""
        cur = ' aria-current="page"' if page == slug else ""
        out = [f'          <li{attr} data-nav="{slug}">',
               f'            <a{cur} href="{href}">{label}{caret}</a>']
        if children:
            out.append('            <ul class="subnav">')
            for child in children:
                s2, l2 = child[0], child[1]
                base, _, frag = s2.partition("#")
                href2 = base + ".html" + ("#" + frag if frag else "")
                on  = ' class="is-active"' if base == page and not frag else ""
                cur2 = ' aria-current="page"' if base == page and not frag else ""
                out.append(f'              <li data-nav="{base}"{on}>'
                           f'<a{cur2} href="{href2}">{l2}</a></li>')
            out.append('            </ul>')
        out.append('          </li>')
        return "\n".join(out)

    # AXES 가 비어 있으면 메뉴 항목이 하나도 나오지 않습니다.
    items = "\n".join(li(slug, label, slug + ".html", AXIS_CHILDREN.get(slug, []))
                      for slug, label in AXES)

    return f"""  <header class="header" id="header">
    <div class="container header__inner">
{_logo(home)}
      <nav class="nav" id="nav">
        <ul class="nav__list">
{li('story-philosophy', '한의원 소개', 'story-philosophy.html', INTRO_CHILDREN)}
{items}
{li('faq', '자주 묻는 질문', 'faq.html')}
        </ul>
      </nav>
      <button class="nav-toggle" id="navToggle" aria-label="메뉴 열기">
        <span></span><span></span><span></span>
      </button>
    </div>
  </header>
"""


def page_hero(title, desc):
    return f"""
  <section id="main" class="page-hero">
    <div class="container">
      <h1 class="page-hero__title">{title}</h1>
      <p class="page-hero__desc">{desc}</p>
    </div>
  </section>
"""


def crumb(label, parent=None):
    """parent 를 주면 '홈 › 관절치료 › 허리·골반 통증' 처럼 한 단계가 더 붙습니다."""
    mid = ""
    if parent:
        slug = parent
        mid = f'<a href="{slug}.html">{PAGE_LABELS.get(slug, slug)}</a> &nbsp;›&nbsp; '
    return f"""
  <div class="crumb">
    <div class="container"><a href="index.html#hero">홈</a> &nbsp;›&nbsp; {mid}{label}</div>
  </div>
"""


def cta(title='지금,<br class="only-mobile" /> 원인부터 확인해 보세요',
        desc="무엇이 원인인지 판단해 설명드립니다."):
    """모든 콘텐츠 페이지의 마무리. 읽고 나서 갈 곳을 만들어 줍니다."""
    return f"""
  <section class="cta-banner">
    <div class="container">
      <div class="cta-banner__inner">
        <h2 class="cta-banner__title">{title}</h2>
        <p class="cta-banner__desc">{desc}</p>
        <a href="tel:{TEL}" class="btn btn--primary btn--lg">진료 예약하기</a>
      </div>
    </div>
  </section>
"""


def _channel_links():
    """네이버 채널 — 주소가 있는 것만 내보냅니다."""
    # 블로그는 아래 퀵메뉴에 있어서 푸터에서는 뺐습니다(원장님 지시, 2026-09-01).
    out = []
    if PLACE: out.append(f'        <a href="{PLACE}" target="_blank" rel="noopener">네이버 플레이스</a>')
    return "\n".join(out)


def _bizno():
    """사업자등록번호는 확정된 뒤에만 내보냅니다 — 가짜 번호를 띄우지 않기 위해서입니다."""
    return f" &nbsp;|&nbsp; 사업자등록번호 {BIZNO}" if BIZNO else ""


def footer():
    return f"""
  <footer class="footer">
    <div class="container footer__inner">
      <div class="footer__brand">
        <img src="assets/logo-white.png?v={IMG_V}" alt="{CLINIC}" class="footer__logo" width="800" height="223" />
        <p class="footer__slogan">치료반응이 다음 자리를 정합니다.</p>
      </div>
      <div class="footer__info">
        <p>대표 · 양정진{_bizno()}</p>
        <p>{ADDRESS}</p>
        <p>대표전화 <a href="tel:{TEL}">{TEL}</a> &nbsp;|&nbsp; 팩스 {FAX}</p>
      </div>
      <div class="footer__links">
{_channel_links()}
        <a href="terms.html">이용약관</a>
        <a href="privacy.html">개인정보처리방침</a>
        <a href="pricing.html">비급여 진료비용</a>
      </div>
    </div>
    <div class="footer__copy">
      <div class="container footer__copy-inner">
        <span>© {YEAR} {CLINIC}</span>
        <button type="button" class="view-toggle" id="viewToggle">PC 버전으로 보기</button>
      </div>
    </div>
  </footer>
"""


def quickmenu():
    ico = {
        "blog": "<path d='M12 20h9'/><path d='M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4 12.5-12.5z'/>",
        "place": "<path d='M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z'/><circle cx='12' cy='10' r='3'/>",
        "insta": ("<rect x='2' y='2' width='20' height='20' rx='5.5'/><circle cx='12' cy='12' r='4.2'/>"
                  "<circle cx='17.4' cy='6.6' r='1.15' fill='currentColor' stroke='none'/>"),
        "book": "<rect x='3' y='4' width='18' height='18' rx='2.5'/><path d='M16 2v4M8 2v4M3 10h18'/>",
        "tel": ("<path d='M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6 "
                "19.8 19.8 0 0 1-3.1-8.7A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.3 1.8.6 2.7a2 2 0 0 1-.5 2.1"
                "L8 9.7a16 16 0 0 0 6 6l1.2-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.5 2.7.6a2 2 0 0 1 1.7 2z'/>"),
    }

    def item(href, key, label, cls="", target=True):
        t = ' target="_blank" rel="noopener"' if target else ''
        return (f'    <a class="qm{cls}" href="{href}"{t} style="--qm:{INK}" aria-label="{label}">\n'
                f'      <span class="qm__ico"><svg viewBox="0 0 24 24">{ico[key]}</svg></span>\n'
                f'      <span class="qm__label">{label}</span>\n    </a>')

    return f"""
  <div class="quickmenu" aria-label="바로가기">
{item(BLOG, 'blog', '블로그') if BLOG else ''}
{item(PLACE, 'place', '플레이스') if PLACE else ''}
{item(INSTA, 'insta', '인스타그램') if INSTA else ''}
{item('tel:' + TEL, 'tel', '전화', target=False)}
{item('tel:' + TEL, 'book', '예약', cls=' qm--book', target=False)}
  </div>
  <script src="script.js?v={JS_V}"></script>
</body>
</html>
"""


# ── 지도 ──────────────────────────────────────────────────────
#
# 네이버 지도는 iframe 으로 붙일 수 없습니다.
# map.naver.com 이 x-frame-options: DENY 로 삽입을 막아 두었습니다. (2026-08-28 확인)
#
# 네이버로 바꾸려면 '네이버 클라우드 플랫폼 > Maps' 에서
#   ① 애플리케이션 등록 ② 서비스 URL 에 실제 도메인 등록 ③ Client ID 발급
# 을 거쳐야 합니다. 도메인이 확정되어야 등록이 되므로 지금은 받을 수 없습니다.
#
# 준비가 되면 아래 두 값을 채우십시오. 채워지면 네이버로, 비어 있으면 구글로 나갑니다.
NAVER_MAP_KEY = ""      # TODO: 네이버 클라우드 플랫폼 Client ID
NAVER_LATLNG = ""       # TODO: "37.5943,127.1296" 형식의 위도,경도

NAVER_PLACE = ("https://map.naver.com/p/search/"
               "경기도%20구리시%20경춘로%20223%20명동빌딩")


def map_embed():
    if NAVER_MAP_KEY and NAVER_LATLNG:
        lat, lng = NAVER_LATLNG.split(",")
        return (f'<div id="naverMap" style="width:100%;aspect-ratio:3/2;"></div>\n'
                f'          <script src="https://oapi.map.naver.com/openapi/v3/maps.js'
                f'?ncpKeyId={NAVER_MAP_KEY}"></script>\n'
                f'          <script>\n'
                f'            (function () {{\n'
                f'              var at = new naver.maps.LatLng({lat}, {lng});\n'
                f'              var map = new naver.maps.Map("naverMap", '
                f'{{ center: at, zoom: 17 }});\n'
                f'              new naver.maps.Marker({{ position: at, map: map, '
                f'title: "{CLINIC}" }});\n'
                f'            }})();\n'
                f'          </script>')
    g = ("https://www.google.com/maps?q=%EA%B2%BD%EA%B8%B0%EB%8F%84+%EA%B5%AC%EB%A6%AC%EC%8B%9C"
         "+%EA%B2%BD%EC%B6%98%EB%A1%9C+223&amp;hl=ko&amp;z=17&amp;output=embed")
    return (f'<iframe src="{g}"\n'
            f'            title="{CLINIC} 위치 — {ADDRESS}"\n'
            f'            loading="lazy" referrerpolicy="no-referrer-when-downgrade" '
            f'allowfullscreen></iframe>')


def location_section(lead=f"{LANDMARK} {LANDMARK_BLDG}입니다."):
    """오시는 길 — 메인과 한의원 소개가 같은 조각을 씁니다."""
    return f"""
  <!-- 오시는 길 -->
  <section class="section location" id="location">
    <div class="container">
      <div class="section__head section__head--center">
        <h2 class="section__title">오시는 길</h2>
        <p class="section__lead">{lead}</p>
      </div>
      <div class="location__grid">
        <div class="location__map">
          {map_embed()}
        </div>
        <div class="location__info">
          <dl class="location__list">
            <div class="location__row"><dt>주소</dt><dd>{ADDRESS.replace("경기도 구리시 경춘로 223 ", "경기도 구리시 경춘로 223<br />")}</dd></div>
            <div class="location__row"><dt>지하철</dt><dd>{STATION}(경의중앙·경춘선)에서 도보 이용</dd></div>
            <div class="location__row"><dt>버스</dt><dd>{BUS_STOP}<br /><span class="hours__sub">광역·좌석 {bus_nos(BUS_EXPRESS)}</span><br /><span class="hours__sub">일반 {bus_nos(BUS_LOCAL)}</span></dd></div>
            <div class="location__row"><dt>전화</dt><dd><a href="tel:{TEL}">{TEL}</a></dd></div>
            <div class="location__row"><dt>팩스</dt><dd>{FAX}</dd></div>
            <div class="location__row"><dt>진료시간</dt><dd>{HOURS_ROWS}</dd></div>
            <div class="location__row"><dt>주차</dt><dd>건물 주차장 이용</dd></div>
          </dl>
          <div class="location__actions">
            <a href="{NAVER_PLACE}" target="_blank" rel="noopener" class="btn btn--accent">네이버 지도에서 보기</a>
          </div>
          <p class="location__note">※ 지도를 눌러 확대·이동하실 수 있습니다. 길찾기는 위 버튼으로 네이버 지도에서 이용해 주세요.</p>
        </div>
      </div>
    </div>
  </section>
"""


# ── 내부 시설 ─────────────────────────────────────────────────
#
# 사진과 이름은 원장님 확인이 필요합니다.
# 아래 목록을 실제 공간에 맞게 고치고, 사진이 준비되면
# assets/facility/ 에 넣은 뒤 img_name 을 채우면 사진으로 바뀝니다.
FACILITIES = [
    ("대기실",       "처음 오신 분이 앉아 기다리시는 곳입니다.", ""),
    ("진료실",       "문진하고, 손으로 짚어 판단하고, 설명드리는 곳입니다.", ""),
    ("치료실",       "침 치료와 추나가 이루어지는 곳입니다.", ""),
    ("탕전실",       "한약을 달이는 곳입니다.", ""),
]


def facilities_section():
    """내부 시설.

    사진이 하나도 없으면 빈 액자 네 개가 늘어서 '만들다 만 쪽'으로 보입니다.
    그래서 사진이 들어오기 전까지는 방 이름과 설명만 글로 보여주고,
    FACILITIES 에 파일 이름이 채워지는 순간 사진 격자로 돌아갑니다.
    """
    if not any(img for _, _, img in FACILITIES):
        rows = "\n".join(
            f'        <div class="location__row"><dt>{name}</dt>'
            f'<dd>{lines(line)}</dd></div>' for name, line, _ in FACILITIES)
        body = f'      <dl class="location__list">\n{rows}\n      </dl>\n'
        lead = "진료 공간은 네 곳으로 나뉘어 있습니다."
    else:
        cards = []
        for name, line, img in FACILITIES:
            media = (f'<img class="facility__img" src="assets/facility/{img}?v={IMG_V}" '
                     f'alt="{CLINIC} {name}" loading="lazy" />' if img
                     else '<div class="media-placeholder"><span>사진 준비 중</span></div>')
            cards.append(f"""        <figure class="facility">
          {media}
          <figcaption>
            <h3>{name}</h3>
            <p>{lines(line)}</p>
          </figcaption>
        </figure>""")
        body = f'      <div class="facility__grid">\n{chr(10).join(cards)}\n      </div>\n'
        lead = "오시기 전에 어떤 곳인지 미리 보실 수 있습니다."
    return f"""
  <!-- 내부 시설 -->
  <section class="section section--alt" id="facility">
    <div class="container">
      <div class="section__head section__head--center">
        <h2 class="section__title">내부 시설</h2>
        <p class="section__lead">{lead}</p>
      </div>
{body}    </div>
  </section>
"""


def venn(labels):
    """세 원이 겹치는 도해. 글자가 작아지지 않도록 viewBox 안에서 크게 씁니다."""
    (a, _), (b, _), (c, _) = labels
    return f"""      <svg class="venn" viewBox="0 0 640 560" role="img"
           aria-label="아픈 자리·원인 자리·충분한 치료 강도가 겹치는 곳에서 치료반응이 일어납니다">
        <g class="venn__ring">
          <circle cx="320" cy="196" r="152" />
          <circle cx="232" cy="356" r="152" />
          <circle class="venn__ring--key" cx="408" cy="356" r="152" />
        </g>
        <text class="venn__label" x="320" y="104" text-anchor="middle">{a}</text>
        <text class="venn__label" x="168" y="436" text-anchor="middle">{b}</text>
        <text class="venn__label venn__label--key" x="470" y="414" text-anchor="middle">{c.split()[0]}
          <tspan x="470" dy="31">{" ".join(c.split()[1:])}</tspan></text>
        <text class="venn__core" x="320" y="326" text-anchor="middle">치료반응</text>
      </svg>
"""


# ── 개원 안내 창 ─────────────────────────────────────────────
# 개원하면 OPENING_ON = False 하나만 바꾸십시오. 20개 페이지에서 한 번에 사라집니다.
OPENING_ON   = True
OPENING_WHEN = "10월 초"
OPENING_BODY = [
    f"{CLINIC}은 {OPENING_WHEN} 진료를 시작합니다.",
    "표기된 진료시간은 개원 후 기준입니다.",
    "정확한 날짜는 정해지는 대로 알려 드리겠습니다.",
]


def opening_popup():
    """개원 전까지 모든 페이지에 뜨는 안내 창.

    hidden 으로 내보내고 script.js 가 벗깁니다 — 자바스크립트가 꺼져 있으면
    닫을 방법이 없는 창이 화면을 덮게 되므로, 그럴 때는 아예 열지 않습니다."""
    if not OPENING_ON:
        return ""
    body = "\n".join(f"          <p>{t}</p>" for t in OPENING_BODY)
    return f"""  <div class="popup" id="openingPopup" hidden>
    <div class="popup__dim" data-popup-close></div>
    <div class="popup__card" role="dialog" aria-modal="true"
         aria-labelledby="openingTitle" tabindex="-1">
      <div class="popup__body">
        <p class="popup__eyebrow">개원 안내</p>
        <h2 class="popup__title" id="openingTitle">{OPENING_WHEN},<br />문을 엽니다</h2>
        <div class="popup__text">
{body}
        </div>
        <p class="popup__where">{LANDMARK}<br />{LANDMARK_BLDG}</p>
        <a class="btn btn--accent popup__tel" href="tel:{TEL}">전화로 문의하기 <span class="popup__no">{TEL}</span></a>
      </div>
      <div class="popup__foot">
        <button type="button" class="popup__today" data-popup-today>오늘 하루 보지 않기</button>
        <button type="button" class="popup__close" data-popup-close>닫기</button>
      </div>
    </div>
  </div>
"""


def tail(with_cta=True, cta_title=None, cta_desc=None):
    """페이지 마무리 한 벌 — CTA + 푸터 + 퀵메뉴."""
    parts = []
    if with_cta:
        kw = {}
        if cta_title:
            kw["title"] = cta_title
        if cta_desc:
            kw["desc"] = cta_desc
        parts.append(cta(**kw))
    parts.append(footer())
    # quickmenu() 가 </body></html> 까지 함께 내보냅니다.
    # 팝업은 반드시 그 앞에 와야 합니다 — 뒤에 두면 body 밖으로 나갑니다.
    parts.append(opening_popup())
    parts.append(quickmenu())
    return "".join(parts)
