# -*- coding: utf-8 -*-
"""
치료 방법 5페이지 + 의료진·이야기·후기·비급여·약관·404.

2026-08-26, 본문을 전부 걷어냈습니다. 블록 개수와 배치만 남아 있습니다.
비급여·개인정보처리방침·이용약관은 원래부터 '틀' 상태라 그대로 두었습니다.
"""

import partials as P
import content_subjects as C
import content_home as H

M = C.M


# 원장 프로필 — 약력 목록 위에 얼굴과 이름을 먼저 둡니다.
# 사진은 3:4 로 잘라 두었고, 260px 칸에 맞춰 들어갑니다.
# 문구는 원장 이야기 4·5번 마디에서 그대로 가져왔습니다. 여기서 새로 짓지 않습니다.
DOCTOR = dict(
    name="양정진",
    role="대표원장 · 한의사",
    desc="아픈 자리와 그 자리를 만든 곳은 다를 수 있습니다. "
         "자리를 찾았다면 반응이 날 만큼 충분히 치료합니다.",
    src="assets/doctor-profile.jpg", w=900, h=1200,
    alt="정진한의원 대표원장 양정진 한의사",
)


def _doctor_brief():
    d = DOCTOR
    return (
        '      <div class="doctor-brief">\n'
        f'        <img class="doctor-brief__photo" src="{d["src"]}?v={P.IMG_V}" alt="{d["alt"]}"\n'
        f'             width="{d["w"]}" height="{d["h"]}" loading="lazy" decoding="async" />\n'
        '        <div class="doctor-brief__body">\n'
        f'          <h3>{d["name"]}</h3>\n'
        f'          <p class="doctor-brief__role">{d["role"]}</p>\n'
        f'          <p class="doctor-brief__desc">{P.lines(d["desc"])}</p>\n'
        '        </div>\n'
        '      </div>')


def _detail(slug, label, title, desc, meta, blocks, extra="", with_subjects=False,
            notice=None, head_extra=""):
    """치료 방법 페이지 공통 뼈대."""
    body = "\n".join(blocks)
    sub = ""
    if with_subjects:
        cards = "\n".join(
            f'        <a class="svc-card svc-card--plain" href="{slug}.html">\n'
            f'          <p class="svc-card__line">{sym}</p>\n'
            f'          <h3>{dx}</h3>\n'
            f'          <span class="svc-card__more">진료 보기 →</span>\n'
            f'        </a>' for slug, dx, sym in P.PAIN_SUBJECTS)
        sub = f"""
  <section class="section section--alt">
    <div class="container">
      <div class="section__head section__head--center">
        <h2 class="section__title">어떤 통증에 쓰나요</h2>
        <p class="section__lead">세 과목 모두 상태에 따라 함께 씁니다.</p>
      </div>
      <div class="svc__grid svc__grid--3">
{cards}
      </div>
    </div>
  </section>
"""
    nb = ""
    if notice:
        items = "\n".join(f"          <li>{P.lines(x)}</li>" for x in notice[1])
        nb = f"""      <div class="notice-box">
        <h2 class="notice-box__title">{notice[0]}</h2>
        <ul>
{items}
        </ul>
      </div>
"""
    return (P.head(slug, f"{label} | {P.CLINIC}", f"{meta} | {P.CLINIC}", extra=head_extra)
            + P.topbar() + P.header(slug)
            + P.page_hero(title, desc) + P.crumb(label)
            + f"""
  <section class="section">
    <div class="container container--read">
{body}
{nb}    </div>
  </section>
{extra}{sub}
  <section class="section">
    <div class="container container--read">
      <p class="programs__note">{C.PROGRAMS_NOTE}</p>
    </div>
  </section>
""" + P.tail())


def _blk(h, *ps, items=None):
    """블록 하나. items 를 주면 문장 대신 목록으로 나갑니다 —
    '이런 분께 권합니다' 처럼 나열되는 내용은 목록이 훨씬 잘 읽힙니다."""
    body = "\n".join(f"        <p>{P.lines(p)}</p>" for p in ps)
    if items:
        body += ('\n        <ul class="blk-list">'
                 + "".join(f"<li>{P.lines(x)}</li>" for x in items)
                 + "</ul>")
    return f"""      <div class="svc-detail__block">
        <h2>{h}</h2>
{body}
      </div>"""


def all_pages():
    pages = {}

    # ── 원인 자리 침·약침 치료 ────────────────────────────
    pages["acupuncture"] = _detail(
        "acupuncture", "원인 자리 침·약침 치료",
        f"손으로 찾고,{M}침으로 확인합니다",
        f"아픈 자리가 아니라{M}통증이 시작된 자리를 찾아,<br />침과 약침으로 치료반응을 확인하며 진행합니다.",
        "원인 자리 침·약침 치료 — 손으로 찾고 치료반응을 확인하며 진행합니다",
        [_blk("손으로 찾고, 침으로 확인합니다",
              "통증이 시작된 자리는 사진이나 검사지에 늘 나오지는 않습니다. 그래서 손으로 눌러가며 굳어 있는 자리, 눌렀을 때 통증이 재현되는 자리를 먼저 찾습니다.",
              "찾은 자리에 침을 놓은 뒤에는 치료반응을 확인합니다. 그 반응으로 자리를 정합니다. 짚는 데서 그치지 않는다는 뜻입니다."),
         _blk("개수가 아니라 자리입니다",
              "침을 많이 놓는다고 효과가 비례하지는 않습니다. 꼭 필요한 자리를 먼저 찾고, 찾은 뒤에는 충분히 합니다. 자리가 맞으면 개수는 줄어들고 몸의 부담도 줄어듭니다."),
         _blk("자리를 찾고도 강도가 모자랄 때 — 약침",
              "침으로 자리를 찾았는데 반응이 약하거나, 오래 굳어 한 번의 자극으로는 "
              "움직이지 않는 자리가 있습니다. 그럴 때 그 자리에 약침을 함께 씁니다.",
              "한약재에서 뽑아 정제한 약액을 찾은 자리에 직접 넣는 치료입니다. "
              "침이 자리를 자극하고 끝난다면, 약침은 그 자리에 남아 작용합니다. "
              "찾은 자리가 같아도 도달하는 강도가 달라집니다.",
              "상태에 따라 재생약침과 특수약침을 나누어 씁니다. 건강보험이 적용되지 않아 "
              "부위 수와 횟수에 따라 금액이 달라지며, 진료 전에 미리 안내합니다.",
              '<a href="pricing.html" class="btn btn--outline" style="margin-top:6px;">비급여 진료비용 보기</a>'),
         _blk("치료 중 몸에서 일어나는 일",
              "침이 굳어 있던 자리에 닿으면 근육이 순간적으로 움찔할 수 있습니다. 놀라실 수 있지만 그 자리를 제대로 찾았다는 신호입니다.",
              "아픈 곳이 아니라 전혀 다른 곳에서 느낌이 오기도 합니다. 이상한 것이 아니라, 그 자리들이 서로 연결돼 있다는 뜻입니다.")],
        with_subjects=True)

    # ── 추나요법 ─────────────────────────────────────────
    pages["chuna"] = _detail(
        "chuna", "추나요법",
        f"굳어서 안 움직이는 자리를{M}손으로 풉니다",
        f"관절과 근육이 어디서 막혀 있는지{M}손으로 확인하고,<br />움직임이 살아나도록 조정합니다.",
        "추나요법 — 굳어서 잘 움직이지 않는 자리를 손으로 확인하고 조정합니다",
        [_blk("추나요법이 무엇인가요",
              "한의사가 손이나 신체 일부를 이용해 관절과 근육, 인대의 위치와 움직임을 조정하는 치료입니다. 뻣뻣해서 잘 움직이지 않는 자리를 직접 만져 확인하고, 움직임의 범위가 넓어지도록 단계적으로 진행합니다.",
              "기계가 아니라 손으로 하기 때문에, 그날의 몸 상태에 맞춰 힘과 방향을 조절할 수 있습니다."),
         _blk("침 치료와 함께 봅니다",
              "침이 굳어 있는 자리의 긴장을 다룬다면, 추나는 그 자리가 다시 움직이도록 돕습니다. 두 가지가 서로 다른 일을 하기 때문에 상태에 따라 한 가지만 쓰기도 하고, 함께 쓰기도 합니다.",
              '<a href="acupuncture.html" class="btn btn--outline" style="margin-top:6px;">원인 자리 침·약침 치료 보기</a>'),
         _blk("건강보험이 적용됩니다",
              "추나요법은 건강보험이 적용되는 치료입니다. 다만 연간 받을 수 있는 횟수에 한도가 있고, 상태와 적용 방식에 따라 본인부담이 달라져 진료 시 미리 안내합니다.")],
        notice=("먼저 확인이 필요한 경우",
                ["골다공증이 심하거나 골절·급성 염증이 의심되는 경우에는 추나가 적절하지 않을 수 있습니다. "
                 "그런 경우에는 그렇게 말씀드리고, 필요하면 검사나 병원 연계를 안내합니다."]),
        with_subjects=True)

    # ── 1:1 맞춤 한약 ────────────────────────────────────
    pages["herb"] = _detail(
        "herb", "1:1 맞춤 한약",
        "1:1 맞춤 한약",
        f"증상만 억누르는 것이 아니라,<br />몸속 \u2018환경\u2019을 바꾸어{M}몸의 균형을 되찾는 1:1 맞춤 한약입니다.",
        "1:1 맞춤 한약 — 몸이 반응하는 방향을 살펴 처방을 정합니다",
        [_blk(f"같은 병명이라도,{M}몸의 \u2018환경\u2019은 저마다 다릅니다",
              "병을 만들어낸 몸의 상태는 사람마다 다릅니다. 진맥과 문진으로 회복을 방해하는 것이 무엇인지 확인한 뒤, 그에 맞춰 한약을 구성합니다."),
         _blk("처방 전, 이렇게 살핍니다",
              "몸이 에너지를 받아들이고 노폐물을 내보내는 통로가 열려 있어야 좋은 약도 제대로 흡수됩니다. 그 바탕을 먼저 살핍니다.",
              items=["대변과 소변", "소화 상태", "땀", "잠과 기력"]),
         _blk("이런 분께 권합니다",
              "\u203b 몸의 상태에 따라 처방과 기간은 달라집니다. 자세한 내용은 진료 시 말씀드립니다.",
              items=["남들이 좋다는 약·영양제를 먹어도 반응이 없던 분",
                     "통증 치료와 함께 몸 전체의 회복력을 끌어올리고 싶은 분",
                     "피로·소화·순환 문제로 늘 개운하지 않은 분"])])

    # ── 처음 오시는 분께 ───────────────────────────────────
    #
    # 메인에 있던 '진료 받는 순서 · 회복의 기준 · 자주 받는 질문' 을
    # 이리로 옮겼습니다. 메인이 너무 길어졌기 때문입니다. (2026-09-01)
    steps = "\n".join(
        f'        <article class="program-card">\n'
        f'          <span class="program-card__step">{n}</span>\n'
        f'          <h3 class="program-card__title">{t}</h3>\n'
        f'          <p class="program-card__desc">{P.lines(d)}</p>\n'
        f'        </article>' for n, t, d in H.STEPS)
    rec = "\n".join(f'          <li>{x}</li>' for x in H.RECOVERY)
    faq = "\n".join(
        f'        <details class="faq-item">\n'
        f'          <summary>{q}</summary>\n'
        f'          <div class="faq-item__a"><p>{P.lines(a)}</p></div>\n'
        f'        </details>' for q, a in H.FAQ)

    pages["care"] = _detail(
        "care", "치료 전 알아두실 점",
        "치료 전 알아두실 점",
        f"진료가 어떤 순서로 이루어지는지,{M}치료 중 몸에서 무엇이 느껴지는지 정리했습니다.",
        "치료 전 알아두실 점 — 진료 순서와 치료 중 몸에서 일어나는 일",
        [_blk("근육이 \u201c툭\u201d 하고 움직일 때가 있습니다",
              "침이 굳어 있던 자리에 정확히 닿으면 근육이 순간적으로 움찔합니다. 놀라실 수 있지만, 그 자리를 제대로 찾았다는 신호입니다."),
         _blk("치료반응이 다른 곳에서 느껴질 수 있습니다",
              "아픈 곳이 아니라 전혀 다른 곳에서 느낌이 올 때가 있습니다. 이상한 것이 아니라, 그 자리들이 서로 이어져 있다는 뜻입니다."),
         _blk("치료 당일이나 다음 날 뻐근할 수 있습니다",
              "오래 굳어 있던 자리가 움직이기 시작하면서 생기는 치료반응입니다. 대개 하루이틀 안에 가라앉습니다. 오래가거나 심해지면 알려주세요."),
         _blk("개수는 줄이고, 자리에는 충분히 합니다",
              "침의 개수로 효과가 정해지지는 않습니다. 다만 자리를 찾은 뒤 약하게 지나가면 그날로 끝납니다. "
              "꼭 필요한 자리에, 감당하실 수 있는 선 안에서 충분히 하는 것을 기준으로 삼습니다.")],
        extra=f"""
  <section class="section section--cream" id="flow">
    <div class="container container--read">
      <div class="section__head section__head--center">
        <h2 class="section__title">{H.STEPS_TITLE}</h2>
      </div>
      <div class="programs__grid">
{steps}
      </div>
      <p class="programs__note">{P.lines(H.STEPS_NOTE)}</p>
    </div>
  </section>

  <section class="section" id="recovery">
    <div class="container container--read">
      <div class="section__head section__head--center">
        <h2 class="section__title">{H.RECOVERY_TITLE}</h2>
        <p class="section__lead">{H.RECOVERY_LEAD}</p>
      </div>
      <ul class="blk-list blk-list--two">
{rec}
      </ul>
    </div>
  </section>

  <section class="section section--cream" id="faq">
    <div class="container container--read">
      <div class="section__head section__head--center">
        <h2 class="section__title">{H.FAQ_TITLE}</h2>
      </div>
      <div class="faq__list">
{faq}
      </div>
    </div>
  </section>
""",
        head_extra=P.faq_ld(H.FAQ))
    pages["care"] = pages["care"].replace(
        '지금 가장 불편한 것부터<br />말씀해 주세요',
        '궁금한 점이 있으면,<br class="only-mobile" /> 편히 물어보세요')

    # ── 한의원 소개 — 원장 이야기 + 진료철학 + 약력 ─────────
    #
    # 환자였던 시간과 그래서 이렇게 진료한다는 이야기는 한 흐름이라
    # 두 페이지를 하나로 합쳤습니다. (2026-08-31)
    cv = [
        ("주요 경력", ["현) 정진한의원 대표원장", "전) 마디추한의원 대표원장",
                    "전) 본스필한의원 대구점 진료원장", "전) 바를정한방병원 신림점 진료원장",
                    "전) 군산시 나포보건지소 한방과장", "전) 군산시 보건소 이동진료팀 한방과장"]),
        ("소속 학회", ["대한한방비만학회 회원", "대한한의영상학회 회원",
                    "한의레이저의학회 회원", "대한한방부인과학회 회원"]),
        ("수료 · 자격", ["턱관절균형의학회 전문가과정 수료", "면역약침 임상실습과정 수료"]),
    ]
    rows = "\n".join(
        '          <div class="cv__row">\n'
        f'            <dt>{t}</dt>\n            <dd>\n              <ul>\n'
        + "\n".join(f"                <li>{x}</li>" for x in items)
        + '\n              </ul>\n            </dd>\n          </div>' for t, items in cv)

    # 사고 사진은 눌러야 보입니다. <details> 라 자바스크립트 없이도 열리고,
    # 닫혀 있는 동안에는 브라우저가 사진을 내려받지도 않습니다.
    ph = H.STORY_PHOTO
    photo = (
        '\n        <figure class="story-photo">\n'
        '          <details class="story-photo__box">\n'
        '            <summary class="story-photo__toggle">\n'
        f'              <span class="is-closed">{ph["open_label"]}</span>\n'
        f'              <span class="is-open">{ph["close_label"]}</span>\n'
        '            </summary>\n'
        f'            <img src="{ph["src"]}?v={P.IMG_V}" alt="{ph["alt"]}"\n'
        f'                 width="{ph["w"]}" height="{ph["h"]}" loading="lazy" decoding="async" />\n'
        '          </details>\n'
        f'          <figcaption>{P.lines(ph["cap"])}</figcaption>\n'
        '        </figure>')
    story = "\n\n".join(
        '      <div class="article__section">\n'
        '        <h3>%d. %s</h3>\n%s%s\n      </div>' % (
            i, h, "\n".join("        <p>%s</p>" % P.lines(x) for x in ps),
            photo if i == ph["after"] else "")
        for i, (h, ps) in enumerate(H.STORY_LONG, 1))
    vows = "".join(f"<li>{P.lines(v)}</li>" for v in H.STORY_VOWS)

    # 메인의 세 원 도해를 치료철학 첫머리에도 둡니다.
    # 네 가지 원칙을 읽기 전에 방법 전체가 한눈에 보이도록 하기 위해서입니다.
    KEY = ' class="is-key"'
    venn_legend = "\n".join(
        f'          <li{KEY if i == 2 else ""}><b>{t}</b><br />{P.lines(d)}</li>'
        for i, (t, d) in enumerate(H.METHOD_CIRCLES))
    venn_block = (
        '      <div class="article__section venn-block">\n'
        f'        <h3>{H.METHOD_TITLE}</h3>\n'
        f'        <p>{H.METHOD_LEAD}</p>\n'
        + P.venn(H.METHOD_CIRCLES).replace("\n", "\n  ")
        + f'        <ol class="venn__legend">\n{venn_legend}\n        </ol>\n'
          f'        <p class="venn__key">{H.METHOD_KEY}</p>\n'
          f'        <p class="venn__note">{P.lines(H.METHOD_NOTE)}</p>\n'
        '      </div>')

    philo = "\n\n".join(
        '      <div class="article__section">\n'
        '        <h3>%s</h3>\n%s\n      </div>' % (
            h, "\n".join("        <p>%s</p>" % P.lines(x) for x in ps))
        for h, ps in H.PHILO)

    pages["story-philosophy"] = (
        P.head("story-philosophy", f"한의원 소개 | {P.CLINIC}",
               f"환자였던 시간을 지나 온 한의사. {P.CLINIC} 양정진 원장 소개와 진료철학.")
        + P.topbar() + P.header("story-philosophy")
        + P.page_hero("한의원 소개", "환자였던 시간을 지나 온 한의사가,{M}무엇을 보고 어떻게 판단하는지 씁니다.".replace("{M}", M))
        + P.crumb("한의원 소개")
        + f"""
  <main class="section" id="story">
    <div class="container article__container">
      <h2 class="article__title">{H.STORY_TITLE}</h2>

{story}
      <ul class="blk-list">{vows}</ul>

      <p class="article__pull">{P.lines(H.STORY_CLOSE)}</p>
    </div>
  </main>

  <section class="section section--cream" id="philosophy">
    <div class="container article__container">
      <h2 class="article__title">{H.PHILO_TITLE}</h2>

      <p class="article__pull">{H.PHILO_PULL.replace("{M}", M)}</p>

{venn_block}

{philo}

      <p class="programs__note">{H.NOTICE}</p>
    </div>
  </section>

  <section class="section" id="cv">
    <div class="container container--read">
      <div class="section__head section__head--center">
        <h2 class="section__title">약력 · 자격</h2>
      </div>
{_doctor_brief()}
      <dl class="cv">
{rows}
      </dl>
    </div>
  </section>
""" + P.facilities_section() + P.location_section() + P.tail())

    # ── 진료 전 자주 묻는 질문 ────────────────────────────
    #    옛 reviews.html 을 대신합니다. 치료 경험담 게시는 의료법 제56조
    #    제한 대상이라, 방문 전 실무 질문으로 성격을 바꿨습니다.
    #    reviews.html → faq.html 이동은 _redirects 가 처리합니다.
    faq_items = "\n".join(
        f'        <details class="faq-item">\n'
        f'          <summary>{q}</summary>\n'
        f'          <div class="faq-item__a"><p>{P.lines(a_.replace("{TEL}", P.TEL))}</p></div>\n'
        f'        </details>' for q, a_ in H.FAQ_PAGE)
    pages["faq"] = (
        P.head("faq", f"{H.FAQ_PAGE_TITLE} | {P.CLINIC} ({P.STATION})",
               "예약·대기·건강보험·자동차보험·주차처럼 오시기 전에 궁금하신 것들을 "
               f"모았습니다. {P.REGION} {P.STATION} {P.CLINIC}.",
               extra=P.faq_ld(H.FAQ_PAGE))
        + P.topbar() + P.header("faq")
        + P.page_hero(H.FAQ_PAGE_TITLE, H.FAQ_PAGE_LEAD.replace(" ", "{M}", 1).replace("{M}", M))
        + P.crumb(H.FAQ_PAGE_TITLE)
        + f"""
  <section class="section" id="faq">
    <div class="container container--read">
      <div class="faq-list">
{faq_items}
      </div>
      <p class="programs__note">{P.NOTICE_LINE}</p>
    </div>
  </section>
""" + P.tail())

    # ── 비급여 진료비용 ───────────────────────────────────
    # 실제 고지 금액. 바뀌면 여기만 고치면 됩니다.
    price_rows = [
        ("상담", [("기본 상담료", "1회", "20,000")]),
        ("한약", [("일반 한약", "20일분", "500,000"),
                 ("일반 한약", "30일분", "600,000"),
                 ("녹용 한약", "20일분", "750,000"),
                 ("녹용 한약", "30일분", "900,000")]),
        ("약침", [("재생약침", "2부위 1회", "20,000"),
                 ("특수약침", "2부위 1회", "50,000")]),
    ]
    body = []
    for cat, items in price_rows:
        for i, (nm, unit, cost) in enumerate(items):
            th = f'<th rowspan="{len(items)}">{cat}</th>' if i == 0 else ""
            body.append(f'          <tr>{th}<td>{nm}</td><td>{unit}</td>'
                        f'<td class="price-table__won">{cost}</td></tr>')
    pages["pricing"] = (
        P.head("pricing", f"비급여 진료비용 고지 | {P.CLINIC}",
               f"비급여 진료비용 고지 | {P.CLINIC}")
        + P.topbar() + P.header("pricing")
        + P.page_hero("비급여 진료비용 고지",
                      f"건강보험이 적용되지 않는 항목의{M}진료비용을 안내합니다.")
        + P.crumb("비급여 진료비용 고지")
        + f"""
  <section class="section">
    <div class="container container--read">
      <div class="table-scroll">
      <table class="price-table">
        <caption class="price-table__cap">{P.PRICE_DATE} 기준 · 단위: 원</caption>
        <thead>
          <tr><th>구분</th><th>항목</th><th>단위</th><th>비용</th></tr>
        </thead>
        <tbody>
{chr(10).join(body)}
        </tbody>
      </table>
      </div>
      <div class="notice-box">
        <h2 class="notice-box__title">안내 말씀</h2>
        <ul>
          <li><strong>기본 상담료는 한약을 처방받으시거나 치료를 받으시면 받지 않습니다.</strong> 상담만 하고 가시는 경우에만 발생합니다.</li>
          <li>한약은 처방 구성에 따라 금액이 달라지며, 진료 후 정확한 금액을 미리 안내합니다.</li>
          <li>약침은 부위 수와 횟수에 따라 금액이 달라집니다.</li>
          <li>침·뜸·부항과 추나요법은 건강보험이 적용되어 이 표에 포함되지 않습니다.</li>
        </ul>
        <p class="notice-box__law">의료법 제45조(비급여 진료비용 등의 고지)에 따른 고지입니다.</p>
      </div>
    </div>
  </section>
""" + P.tail(with_cta=False))

    # ── 개인정보처리방침 · 이용약관 ────────────────────────
    def legal(slug, label, intro, sections):
        arts = []
        for h, paras, lis in sections:
            arts.append(f"        <h2>{h}</h2>")
            for p in paras:
                arts.append(f"        <p>{p}</p>")
            if lis:
                arts.append("        <ul>")
                arts += [f"          <li>{x}</li>" for x in lis]
                arts.append("        </ul>")
        return (P.head(slug, f"{label} | {P.CLINIC}", f"{label} | {P.CLINIC}")
                + P.topbar() + P.header(slug)
                + P.page_hero(label, intro) + P.crumb(label)
                + f"""
  <section class="section">
    <div class="container container--read">
      <article class="legal">
{chr(10).join(arts)}
      </article>
    </div>
  </section>
""" + P.tail(with_cta=False))

    pages["privacy"] = legal(
        "privacy", "개인정보처리방침",
        f"{P.CLINIC}은 환자분의 개인정보를{M}소중히 보호합니다.",
        [("1. 수집하는 개인정보 항목",
          ["본원 홈페이지는 회원가입·문의 양식 등 개인정보를 입력받는 기능을 두고 있지 않습니다. "
           "따라서 홈페이지를 둘러보는 것만으로는 개인정보가 수집되지 않습니다.",
           "개인정보는 아래의 경우에만 수집됩니다."],
          ["전화로 진료를 예약하실 때 — 성명, 연락처",
           "내원하여 진료를 받으실 때 — 의료법에 따라 작성되는 진료기록"]),

         ("2. 개인정보의 이용 목적", ["수집한 정보는 다음 목적으로만 이용하며, 그 밖의 용도로 쓰지 않습니다."],
          ["진료 예약 확인 및 안내", "진료 및 상담 제공", "법령에 따른 진료기록 보존"]),

         ("3. 보유 및 이용 기간",
          ["관계 법령에서 정한 기간 동안 보관하며, 기간이 지나거나 목적이 달성되면 지체 없이 파기합니다.",
           "진료기록부는 의료법 시행규칙 제15조에 따라 10년간 보관합니다. "
           "예약을 위해 받은 연락처는 예약 목적이 끝나면 파기합니다."], []),

         ("4. 개인정보의 파기 절차와 방법",
          ["보유 기간이 지난 정보는 지체 없이 파기합니다."],
          ["전자 파일 — 복구할 수 없는 방법으로 영구 삭제합니다",
           "종이 문서 — 분쇄하거나 소각합니다"]),

         ("5. 개인정보의 제3자 제공 및 처리 위탁",
          ["본원은 환자분의 개인정보를 제3자에게 제공하지 않으며, 외부에 처리를 위탁하지 않습니다. "
           "다만 법령에 따른 요구가 있거나 정보주체의 생명·신체의 급박한 위험을 막기 위해 "
           "필요한 경우는 예외로 합니다."], []),

         ("6. 자동으로 수집되는 정보",
          ["본원 홈페이지는 접속자를 추적하거나 분석하는 도구를 쓰지 않으며, "
           "광고를 위한 쿠키도 사용하지 않습니다.",
           "다만 화면 보기 방식(휴대폰·PC) 선택을 기억하기 위해 이용자의 브라우저에 "
           "설정값 하나를 저장합니다. 이 값은 본원으로 전송되지 않으며, "
           "브라우저 설정에서 언제든 지우실 수 있습니다."], []),

         ("7. 개인정보의 안전성 확보 조치",
          ["본원은 개인정보를 안전하게 관리하기 위해 다음과 같이 조치하고 있습니다."],
          ["진료기록을 다루는 인원을 최소한으로 제한합니다",
           "개인정보가 담긴 문서와 저장 장치를 잠금장치가 있는 곳에 보관합니다",
           "관련 법령과 지침에 따라 접근 권한을 관리합니다"]),

         ("8. 정보주체의 권리와 행사 방법",
          ["환자분은 언제든지 본인의 개인정보에 대해 열람·정정·삭제·처리정지를 요구하실 수 있습니다. "
           "본원에 전화하시거나 내원하여 요청하시면 지체 없이 조치합니다.",
           "다만 의료법 등 다른 법령에서 보존을 의무로 정한 정보는 "
           "그 기간 동안 삭제가 제한될 수 있습니다."], []),

         ("9. 개인정보 보호책임자",
          [f'책임자: {P.PRIVACY_OFFICER} (대표원장) · 연락처: '
           f'<a href="tel:{P.TEL}">{P.TEL}</a>',
           "개인정보 처리에 관한 문의, 불만, 피해 구제는 위 연락처로 말씀해 주십시오."], []),

         ("10. 권익침해 구제 방법",
          ["개인정보 침해로 도움이 필요하시면 아래 기관에 문의하실 수 있습니다."],
          ["개인정보 분쟁조정위원회 — 1833-6972 (www.kopico.go.kr)",
           "개인정보침해 신고센터 — 118 (privacy.kisa.or.kr)",
           "대검찰청 사이버수사과 — 1301", "경찰청 사이버수사국 — 182"]),

         ("부칙", [f"본 방침은 {P.LEGAL_DATE}부터 시행합니다.",
                  "내용이 추가·삭제·수정될 때에는 시행 전에 홈페이지를 통해 공지합니다."], [])])

    pages["terms"] = legal(
        "terms", "이용약관", "홈페이지 이용에 관한 안내입니다.",
        [("제1조 (목적)",
          [f"본 약관은 {P.CLINIC}(이하 \u2018본원\u2019)이 운영하는 홈페이지의 이용 조건과 절차, "
           "이용자와 본원의 권리·의무 및 책임사항을 정함을 목적으로 합니다."], []),

         ("제2조 (약관의 효력 및 변경)", [],
          ["본 약관은 홈페이지에 게시함으로써 효력이 발생합니다.",
           "본원은 관련 법령을 위배하지 않는 범위에서 약관을 변경할 수 있으며, "
           "변경 시 시행일과 변경 내용을 사전에 공지합니다."]),

         ("제3조 (서비스의 내용)",
          ["본원이 홈페이지를 통해 제공하는 것은 다음과 같습니다. "
           "홈페이지에서 직접 예약이 이루어지지는 않으며, 예약은 전화로 받습니다."],
          ["진료 안내 및 병원 정보 제공", "진료 시간·위치 안내",
           "건강 정보 콘텐츠 제공"]),

         ("제4조 (서비스의 중단)",
          ["본원은 시스템 점검·교체, 통신 두절, 천재지변 등 부득이한 사유가 발생한 경우 "
           "서비스 제공을 일시적으로 중단할 수 있습니다. "
           "이 경우 사전에 공지하되, 미리 알릴 수 없는 사정이 있으면 사후에 공지합니다."], []),

         ("제5조 (이용자의 의무)", ["이용자는 다음 행위를 하여서는 안 됩니다."],
          ["타인의 정보를 도용하거나 허위 사실을 등록하는 행위",
           "본원 및 제3자의 저작권 등 권리를 침해하는 행위",
           "홈페이지 운영을 방해하거나 안정적 운영에 지장을 주는 행위"]),

         ("제6조 (저작권)",
          ["홈페이지에 게시된 모든 콘텐츠(문구, 이미지, 영상 등)의 저작권은 본원 또는 "
           "정당한 권리자에게 있으며, 무단 복제·배포·전송을 금합니다."], []),

         ("제7조 (의료 정보에 관한 면책)", [],
          ["홈페이지에 게시된 건강 정보는 <strong>일반적인 정보 제공을 목적</strong>으로 하며, "
           "개별 환자에 대한 진단이나 처방을 대신하지 않습니다.",
           "같은 병명이라도 상태와 원인에 따라 접근이 달라질 수 있으며, "
           "정확한 진단과 치료는 반드시 <strong>내원 후 의료진의 진료</strong>를 통해 "
           "이루어져야 합니다.",
           "본원은 이용자가 홈페이지의 정보만을 근거로 행한 판단에 대하여 책임을 지지 않습니다."]),

         ("제8조 (개인정보의 보호)",
          ["본원은 이용자의 개인정보를 관계 법령에 따라 보호합니다. "
           "자세한 내용은 <a href=\"privacy.html\">개인정보처리방침</a>에서 확인하실 수 있습니다."], []),

         ("제9조 (분쟁의 해결)",
          ["본 약관과 관련하여 분쟁이 발생한 경우 본원과 이용자는 성실히 협의하여 해결합니다. "
           "협의가 이루어지지 않으면 관계 법령과 상관례에 따릅니다."], []),

         ("부칙", [f"본 약관은 {P.LEGAL_DATE}부터 시행합니다."], [])])

    # ── 404 ─────────────────────────────────────────────
    pages["404"] = (
        P.head("404", f"페이지를 찾을 수 없습니다 | {P.CLINIC}",
               f"요청하신 페이지를 찾을 수 없습니다 | {P.CLINIC}")
        + P.topbar() + P.header("404")
        + P.page_hero(f"페이지를{M}찾을 수 없습니다",
                      f"주소가 바뀌었거나{M}삭제된 페이지일 수 있습니다.")
        + f"""
  <section class="section">
    <div class="container container--read">
      <p class="section__lead">아래에서 필요한 곳으로 이동하실 수 있습니다.</p>
      <div class="location__actions">
        <a href="index.html#hero" class="btn btn--accent">홈으로</a>
        <a href="pain.html" class="btn btn--outline">관절 진료 보기</a>
      </div>
    </div>
  </section>
""" + P.tail(with_cta=False))

    return pages
