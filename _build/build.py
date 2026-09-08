# -*- coding: utf-8 -*-
"""
정진한의원 홈페이지 생성기.

    cd _build && python3 build.py

상위 폴더에 22개 HTML 과 sitemap.xml 을 씁니다. 공통 부분(상단바·메뉴·푸터·퀵메뉴·CTA)은
partials.py 한 곳에만 있어서, 진료시간이나 메뉴를 바꿀 때 파일 하나만 고치면 됩니다.
"""

import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import partials as P
import content_subjects as C
import build_hubs

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = C.M

# ※ 아래 AUDIENCE 는 지금 화면에 나오지 않습니다.
#    원장님 지시로 메인의 '어디가 불편하신가요' 섹션을 지웠기 때문입니다(2026-08-26).
#    그 섹션을 되살리면 그대로 다시 쓰입니다.
import content_home as H

JSONLD = {
    "@context": "https://schema.org",
    "@type": "MedicalClinic",
    "name": P.CLINIC,
    "description": "원인 자리를 찾아 치료반응을 일으키는 한의원. 오래된 통증, 여러 곳을 거쳐 오신 분들을 주로 봅니다. 구리역 도보.",
    "url": P.DOMAIN + "/",
    "telephone": P.TEL,
    "faxNumber": P.FAX,
    "medicalSpecialty": "TraditionalChineseMedicine",
    "address": {"@type": "PostalAddress", "streetAddress": "경춘로 223 명동빌딩 5층",
                "addressLocality": "구리시", "addressRegion": "경기도", "addressCountry": "KR"},
    "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification",
         "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
         "opens": "09:00", "closes": "13:00"},
        {"@type": "OpeningHoursSpecification",
         "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
         "opens": "14:00", "closes": "20:00"},
        {"@type": "OpeningHoursSpecification",
         "dayOfWeek": ["Saturday", "PublicHolidays"],
         "opens": "09:00", "closes": "15:00"},
    ],
    "employee": {"@type": "Person", "name": "양정진", "jobTitle": "한의사"},
}


def _sec(inner, cls="section", sid=""):
    i = f' id="{sid}"' if sid else ""
    return f'\n  <section class="{cls}"{i}>\n    <div class="container container--read">\n{inner}\n    </div>\n  </section>\n'


def build_index():
    extra = ('  <script type="application/ld+json">\n  '
             + json.dumps(JSONLD, ensure_ascii=False, indent=2).replace("\n", "\n  ")
             + "\n  </script>\n")

    head_html = P.head(
        "index",
        f"{P.REGION} 협착증·디스크·관절통 한의원 – {P.CLINIC}({P.STATION})",
        "원인 자리를 찾아 치료반응을 일으키는 한의원입니다. 눌렀을 때 통증이 재현되는 자리를 손으로 찾습니다. "
        "구리역 도보, 협착증·디스크·관절통·만성기침·속쓰림·어지럼 진료. 평일 09–20시.",
        extra=extra,
        keywords=f"{P.REGION} 한의원, {P.STATION} 한의원, 척추관협착증, 허리디스크, "
                 f"어깨 통증, 퇴행성 관절염, 어지럼증, 공황장애, 만성 기침, 역류성식도염")
    head_html = head_html.replace('href="#main"', 'href="#hero"')
    head_html = head_html.replace(
        f'<meta property="og:title" content="{P.REGION} 협착증·디스크·관절통 한의원 – {P.CLINIC}({P.STATION})" />',
        f'<meta property="og:title" content="자리가 맞아야, 몸이 반응합니다 — {P.CLINIC}({P.STATION})" />')

    # 01 히어로
    hero = f"""
  <section class="hero" id="hero">
    <video class="hero__video" muted loop playsinline preload="none"
           poster="{H.VIDEO['poster']}?v={P.IMG_V}"
           data-src="{H.VIDEO['src']}?v={P.IMG_V}"
           aria-hidden="true" tabindex="-1"></video>
    <div class="hero__overlay"></div>
    <div class="container hero__inner">
      <h1 class="hero__title">{H.HERO_TITLE}</h1>
      <p class="hero__desc">{"<br />".join(H.HERO_DESC)}</p>
      <div class="hero__actions">
        <a href="tel:{P.TEL}" class="btn btn--primary btn--lg">진료 예약하기</a>
      </div>
      <p class="hero__note">{H.HERO_NOTE}</p>
    </div>
    <a href="#method" class="hero__scroll" aria-label="아래로 스크롤">⌄</a>
  </section>
"""

    # 치료가 되는 자리 — 세 원의 교집합
    # 세 번째 항목(충분한 치료 강도)에만 --key 를 붙여 도해·본문에서 함께 강조합니다.
    KEY = ' class="is-key"'
    legend = "\n".join(
        f'        <li{KEY if i == 2 else ""}><b>{t}</b><br />{P.lines(d)}</li>'
        for i, (t, d) in enumerate(H.METHOD_CIRCLES))
    method = _sec(
        f'      <div class="section__head section__head--center">\n'
        f'        <h2 class="section__title">{H.METHOD_TITLE}</h2>\n'
        f'        <p class="section__lead">{H.METHOD_LEAD}</p>\n'
        f'      </div>\n'
        + P.venn(H.METHOD_CIRCLES)
        + f'      <ol class="venn__legend">\n{legend}\n      </ol>\n'
          f'      <p class="venn__key">{H.METHOD_KEY}</p>\n'
          f'      <p class="venn__note">{P.lines(H.METHOD_NOTE)}</p>\n'
          f'      <p class="programs__note">{P.NOTICE_LINE}</p>',
        cls="section section--cream", sid="method")

    # 07-B 원장 이야기 (짧은 버전)
    story = _sec(
        f'      <div class="section__head section__head--center">\n'
        f'        <h2 class="section__title">{H.STORY_SHORT_TITLE}</h2>\n'
        f'      </div>\n'
        + "\n".join(f'      <p class="why-text">{P.lines(x)}</p>' for x in H.STORY_SHORT)
        + f'\n      <div class="section__more"><a href="story-philosophy.html#story" class="read-more">'
          f'원장 이야기 전문 읽기 →</a></div>',
        cls="section section--cream", sid="story")

    # 04 진료실 5가지 약속
    pri = "\n".join(
        f'        <li class="principle">\n'
        f'          <span class="principle__num">{n}</span>\n'
        f'          <div class="principle__body">\n'
        f'            <h3 class="principle__title">{t}</h3>\n'
        f'            <p class="principle__desc">{P.lines(d)}</p>\n'
        f'          </div>\n'
        f'        </li>' for n, t, d in H.PROMISES)
    promise = _sec(
        f'      <div class="section__head section__head--center">\n'
        f'        <h2 class="section__title">{H.PROMISE_TITLE}</h2>\n'
        f'      </div>\n'
        f'      <ol class="principles">\n{pri}\n      </ol>',
        sid="promise")

    # ── 진료 내용 ─────────────────────────────────────────
    # 메인 본문에 진료 페이지로 가는 길이 하나도 없었습니다. 상단 메뉴를
    # 못 찾은 분은 무엇을 보는 곳인지 알 방법이 없었습니다. (2026-09-08)
    # 이름만 폅니다 — 증상어와 설명은 각 페이지에 있습니다.
    # 안전 문구는 메인에 이미 한 번 있어 여기서는 넣지 않습니다.
    groups = "\n".join(
        '      <div class="subjects__group">\n'
        f'        <a class="subjects__axis" href="{axis}.html">{label}</a>\n'
        '        <ul class="subjects__names">\n'
        + "\n".join(f'          <li><a href="{slug}.html">{name}</a></li>'
                     for slug, name, _ in P.AXIS_CHILDREN[axis])
        + '\n        </ul>\n      </div>'
        for axis, label in P.AXES)
    subjects = _sec(
        '      <div class="section__head section__head--center">\n'
        '        <h2 class="section__title">진료 내용</h2>\n'
        '      </div>\n'
        f'      <div class="subjects">\n{groups}\n      </div>',
        cls="section section--alt", sid="subjects")

    return (head_html + P.topbar() + P.header("index")
            + hero + method + subjects + promise + story
            + P.location_section() + P.tail(cta_title=H.CTA_TITLE, cta_desc=H.CTA_DESC))


if __name__ == "__main__":
    import build_pages, build_specialty
    pages = {"index": build_index()}
    pages.update(build_hubs.all_hubs())
    pages.update(build_specialty.all_subjects())
    pages.update(build_pages.all_pages())

    for name, html in pages.items():
        with open(os.path.join(OUT, name + ".html"), "w", encoding="utf-8") as f:
            f.write(html)

    # sitemap.xml — 페이지 목록에서 자동으로 만듭니다. 손으로 고치지 마십시오.
    # 404 와 아직 준비 중인 페이지는 검색에 올리지 않습니다.
    SKIP = {"404", "accident"}
    urls = []
    for name in sorted(pages):
        if name in SKIP:
            continue
        loc = P.DOMAIN + "/" + ("" if name == "index" else name + ".html")
        urls.append("  <url>\n    <loc>%s</loc>\n"
                    "    <changefreq>monthly</changefreq>\n  </url>" % loc)
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + "\n".join(urls) + "\n</urlset>\n")
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)

    print("생성 완료: %d개 페이지 + sitemap.xml(%d개 주소)" % (len(pages), len(urls)))
