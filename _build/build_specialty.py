# -*- coding: utf-8 -*-
"""
특화 4과목 페이지 생성 — 내용은 content_specialty.py.

제안서가 정한 공통 뼈대 여섯 블록을 그대로 씁니다.
  #symptoms  이런 증상이라면
  #why       왜 낫지 않았을까
  #points    어디를 함께 보는가
  #process   어떻게 진행되는가
  #method    어떤 방법을 쓰는가
  #faq       자주 묻는 질문
"""

import partials as P
import content_specialty as S
import content_pain as PN
import content_subjects as C


def _aside(text, cls="notice-box"):
    return (f'      <div class="{cls}">\n'
            f'        <p>{P.lines(text)}</p>\n'
            f'      </div>\n')


def _sym_rows(items):
    return "\n".join(
        f'        <div class="audience__item">\n'
        f'          <span class="audience__mark">✓</span>\n'
        f'          <p>{t}</p>\n'
        f'        </div>' for t in items)


def block_symptoms(d):
    note = (f'        <p class="section__lead">{d["symptoms_note"]}</p>\n'
            if d.get("symptoms_note") else "")
    if d.get("symptom_groups"):
        body = "".join(
            f'      <h3 class="sym-group">{g}</h3>\n'
            f'      <div class="audience__grid" style="margin-bottom:28px;">\n'
            f'{_sym_rows(items)}\n      </div>\n'
            for g, items in d["symptom_groups"])
    else:
        body = f'      <div class="audience__grid">\n{_sym_rows(d["symptoms"])}\n      </div>\n'
    aside = _aside(d["symptoms_aside"]) if d.get("symptoms_aside") else ""
    return f"""
  <section class="section" id="symptoms">
    <div class="container">
      <div class="section__head section__head--center">
        <h2 class="section__title">이런 증상이라면</h2>
{note}      </div>
{body}{aside}    </div>
  </section>
"""


def block_why(d):
    lead = (f'        <p class="section__lead">{d["why_lead"]}</p>\n'
            if d.get("why_lead") else "")

    steps = ""
    if d.get("why_steps"):
        cards = "\n".join(
            f'        <article class="program-card">\n'
            f'          <span class="program-card__step">{i:02d}</span>\n'
            f'          <h3 class="program-card__title">{t}</h3>\n'
            + (f'          <p class="program-card__desc">— {sub}</p>\n' if sub else "")
            + f'        </article>'
            for i, (t, sub) in enumerate(d["why_steps"], 1))
        steps = f'      <div class="programs__grid">\n{cards}\n      </div>\n'

    paras = "\n".join(f'      <p class="why-text">{P.lines(p)}</p>' for p in d["why"])

    sub = ""
    if d.get("why_sub"):
        w = d["why_sub"]
        sub_paras = "\n".join(f'      <p class="why-text">{P.lines(p)}</p>' for p in w["paras"])
        sub = (f'      <div class="section__head section__head--center" style="margin-top:48px;">\n'
               f'        <h2 class="section__title">{w["title"]}</h2>\n'
               f'      </div>\n{sub_paras}\n')

    aside = _aside(d["why_aside"]) if d.get("why_aside") else ""

    return f"""
  <section class="section section--cream" id="why">
    <div class="container container--read">
      <div class="section__head section__head--center">
        <h2 class="section__title">왜 낫지 않았을까</h2>
{lead}      </div>
{steps}{paras}
{sub}{aside}    </div>
  </section>
"""


def _table(rows, head=None):
    thead = (f'          <thead><tr><th scope="col">{head[0]}</th>'
             f'<th scope="col">{head[1]}</th></tr></thead>\n' if head else "")
    body = "\n".join(f'            <tr><th scope="row">{a}</th><td>{P.lines(b)}</td></tr>'
                     for a, b in rows)
    return (f'      <div class="table-scroll">\n'
            f'        <table class="legal-table">\n{thead}'
            f'          <tbody>\n{body}\n          </tbody>\n'
            f'        </table>\n      </div>\n')


def block_red_flags(d):
    """응급·검사 우선 안내. 안전 문구라 눈에 띄게 따로 뺍니다."""
    if not d.get("red_flags"):
        return ""
    items = "\n".join(f'          <li>{t}</li>' for t in d["red_flags"])
    note = (f'        <p class="notice-box__law">{d["red_flags_note"]}</p>\n'
            if d.get("red_flags_note") else "")
    return f"""      <div class="notice-box notice-box--warn">
        <h3 class="notice-box__title">⚠️ {PN.RED_FLAG_TITLE}</h3>
        <ul>
{items}
        </ul>
{note}      </div>
"""


def block_types(d):
    """증상 유형을 가려 보는 표. 위험한 유형 바로 아래에 경고를 붙입니다.

    어지럼처럼 유형에 따라 대응이 갈리는 과목에서는, 환자가 자기 줄을
    먼저 찾을 수 있어야 합니다. 그래서 본문보다 앞에 놓습니다.
    """
    if not d.get("types"):
        return ""
    lead = ('        <p class="section__lead">%s</p>\n' % P.lines(d["types_lead"])
            if d.get("types_lead") else "")
    return ('\n  <section class="section section--cream" id="types">\n'
            '    <div class="container container--read">\n'
            '      <div class="section__head section__head--center">\n'
            '        <h2 class="section__title">%s</h2>\n%s'
            '      </div>\n%s%s    </div>\n  </section>\n'
            % (d["types_title"], lead,
               _table(d["types"], head=d.get("types_head")),
               block_red_flags(d)))


def block_points(d):
    title = d.get("points_title", "어디를 함께 보는가")
    lead = (f'        <p class="section__lead">{d["points_lead"]}</p>\n'
            if d.get("points_lead") else "")

    if d.get("points_table"):
        body = _table(d["points_table"], d.get("points_table_head"))
    else:
        items = "\n".join(f'          <li>{t}</li>' for t in d["points"])
        body = (f'      <div class="notice-box">\n'
                f'        <ul>\n{items}\n        </ul>\n      </div>\n')

    if d.get("points_table2"):
        lead2 = (f'      <p class="section__lead" style="margin:32px 0 14px;">'
                 f'{d["points_table2_lead"]}</p>\n' if d.get("points_table2_lead") else "")
        body += lead2 + _table(d["points_table2"], d.get("points_table2_head"))

    aside = _aside(d["points_aside"]) if d.get("points_aside") else ""
    aside += "" if d.get("types") else block_red_flags(d)

    return f"""
  <section class="section section--alt" id="points">
    <div class="container container--read">
      <div class="section__head section__head--center">
        <h2 class="section__title">{title}</h2>
{lead}      </div>
{body}{aside}    </div>
  </section>
"""


def block_process(d):
    aside = _aside(d["process_aside"]) if d.get("process_aside") else ""
    note = _aside(d["process_note"]) if d.get("process_note") else ""
    method = block_method(d)
    cards = "\n".join(
        f'        <article class="program-card">\n'
        f'          <span class="program-card__step">{i:02d}</span>\n'
        f'          <h3 class="program-card__title">{t}</h3>\n'
        f'          <p class="program-card__desc">{P.lines(p)}</p>\n'
        f'        </article>' for i, (t, p) in enumerate(d["process"], 1))
    return f"""
  <section class="section" id="process">
    <div class="container container--read">
      <div class="section__head section__head--center">
        <h2 class="section__title">어떻게 진행되는가</h2>
      </div>
{aside}      <div class="programs__grid">
{cards}
      </div>
{note}{method}    </div>
  </section>
"""


def block_method(d):
    """치료 방법 — 따로 떼지 않고 진행 블록 끝에 붙입니다.
    환자분은 '무엇을 받는지'보다 '가면 뭘 하는지'를 먼저 궁금해하십니다."""
    m = d["method"]
    paras = m if isinstance(m, (list, tuple)) else [m]
    body = "\n".join(f'      <p class="why-text">{P.lines(t)}</p>' for t in paras)
    band = C.METHODS_BAND_PAIN if d.get("parent") == "pain" else C.METHODS_BAND_ANS
    return f"""
      <h3 class="sub-head" id="method">어떤 방법을 쓰는가</h3>
{body}
      <p class="methods-band">{band}</p>
"""


def block_method_section(d):
    """치료 방법 — 전에는 '어떻게 진행되는가' 안에 붙어 있었습니다.
    그 구획을 빼면서 침·추나·한약 안내까지 사라져, 따로 떼어 둡니다."""
    return ('\n  <section class="section" id="method-section">\n'
            '    <div class="container container--read">\n'
            + block_method(d)
            + '    </div>\n  </section>\n')


def block_extras(d):
    out = []
    for x in d.get("extras", []):
        lead = (f'        <p class="section__lead">{x["lead"]}</p>\n' if x.get("lead") else "")
        if x.get("table"):
            head = x.get("table_head")
            thead = (f'          <thead><tr><th scope="col">{head[0]}</th>'
                     f'<th scope="col">{head[1]}</th></tr></thead>\n' if head else "")
            rows = "\n".join(
                f'            <tr><th scope="row">{a}</th><td>{P.lines(b)}</td></tr>'
                for a, b in x["table"])
            body = (f'      <div class="table-scroll">\n'
                    f'        <table class="legal-table">\n{thead}'
                    f'          <tbody>\n{rows}\n          </tbody>\n'
                    f'        </table>\n      </div>\n')
        else:
            items = "\n".join(f'          <li>{P.lines(t)}</li>' for t in x["items"])
            body = (f'      <div class="notice-box">\n'
                    f'        <ul>\n{items}\n        </ul>\n      </div>\n')
        out.append(f"""
  <section class="section">
    <div class="container container--read">
      <div class="section__head section__head--center">
        <h2 class="section__title">{x['title']}</h2>
{lead}      </div>
{body}    </div>
  </section>
""")
    return "".join(out)


def block_faq(d):  # noqa: D401
    items = "\n".join(
        f'        <details class="faq-item">\n'
        f'          <summary>{q}</summary>\n'
        f'          <div class="faq-item__a"><p>{P.lines(a)}</p></div>\n'
        f'        </details>' for q, a in d["faq"])
    return f"""
  <section class="section section--alt" id="faq">
    <div class="container">
      <div class="section__head section__head--center">
        <h2 class="section__title">자주 묻는 질문</h2>
      </div>
      <div class="faq__list">
{items}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container container--read">
      <p class="programs__note">{d.get("notice", S.NOTICE)}</p>
    </div>
  </section>
"""


def build(d):
    title = f"{P.REGION} {d['seo_kw']} 한의원 – {P.CLINIC}({P.STATION})"
    desc = f"{P.REGION}·{P.STATION} {P.CLINIC}. {d['meta']}."
    intro = ""
    if d.get("intro_aside"):
        intro = (f'\n  <section class="section">\n'
                 f'    <div class="container container--read">\n'
                 f'{_aside(d["intro_aside"])}'
                 f'    </div>\n  </section>\n')
    return (
        P.head(d["slug"], title, desc, keywords=d.get("keywords", ""))
        + P.topbar()
        + P.header(d["slug"])
        + P.page_hero(d["title"], d["desc"])
        + P.crumb(d["label"], d.get("parent"))
        + intro
        + block_symptoms(d)
        + block_types(d)
        + block_why(d)
        + block_points(d)
        # '어떻게 진행되는가' 구획은 원장님 지시로 내보내지 않습니다(2026-09-01).
        # 원고(process)는 content_* 에 그대로 두었으니, 되살리려면 아래 한 줄만 켜면 됩니다.
        # + block_process(d)
        + block_method_section(d)
        + block_extras(d)
        + block_faq(d)
        + P.tail(cta_title=d.get("cta_title"), cta_desc=d.get("cta_desc"))
    )


def all_subjects():
    """통증 3과목 + 내과 5과목."""
    pages = {}
    for slug in PN.ORDER:
        d = dict(PN.PAIN[slug], parent="pain", notice=PN.NOTICE)
        pages[slug] = build(d)
    for slug in S.ORDER:
        # 만성기침도 2026-09-05 부터 자율신경질환 아래입니다.
        d = dict(S.SPECIALTY[slug], notice=S.NOTICE, parent="autonomic-disorders")
        pages[slug] = build(d)
    return pages
