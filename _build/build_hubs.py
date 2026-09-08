# -*- coding: utf-8 -*-
"""
허브 두 갈래 + 교통사고 안내.

  pain.html                 관절통증     — 협착증 · 디스크 · 퇴행성 관절염
  autonomic-disorders.html  자율신경질환 — 이석증 · 어지럼증 · 공황장애 ·
                                           역류성식도염 · 기능성 소화불량 ·
                                           만성기침

카드가 셋이면 한 줄, 넷이면 두 줄로 폅니다. 셋에 하나가 남아 도는 모양은
피합니다.
"""

import partials as P
import content_pain as PN
import content_specialty as S

SHARED = "아픈 자리와 원인 자리는 다를 수 있습니다."

HUBS = {
    "pain": dict(
        slug="pain", label="관절통증",
        seo_kw="통증 치료",
        keywords="척추관협착증, 허리디스크, 목디스크, 퇴행성 관절염",
        title=f"아픈 자리와{PN.M}원인 자리는 다를 수 있습니다",
        desc=f"통증이 드러난 자리에서 시작해,{PN.M}그 통증을 만든 자리까지 확인합니다.",
        meta="통증 진료 — 척추관협착증·디스크·퇴행성 관절통을 봅니다",
        lead=f"{SHARED}{PN.M}통증에서는 근육이 서로 이어진 사슬을 따라 확인합니다.",
        source=PN.PAIN, order=PN.ORDER, children=P.PAIN_SUBJECTS,
    ),
    "autonomic-disorders": dict(
        slug="autonomic-disorders", label="자율신경질환",
        seo_kw="자율신경질환",
        keywords="자율신경, 어지럼증, 이석증, 공황장애, 역류성식도염, 기능성 소화불량, 만성기침",
        title=f"검사에는 이상이 없다는데{PN.M}계속 힘드신가요?",
        desc=f"긴장과 이완을 조절하는 균형이 무너지면{PN.M}검사로 잘 드러나지 않는 증상이{PN.M}여럿 함께 나타납니다.",
        meta="자율신경질환 — 어지럼·불안·위장·기침 증상을 한 갈래로 놓고 봅니다",
        lead=f"{SHARED}{PN.M}어지럼과 두근거림, 속의 불편과 기침이 따로 온 것처럼 보여도{PN.M}한 자리에서 이어져 있는 경우가 있습니다.",
        source=S.SPECIALTY, order=None, children=P.ANS_SUBJECTS,
        blocks=[
            ("몸은 이상이 없다는데, 계속 힘든 이유",
             ["긴장과 이완을 조절하는 자율신경의 균형이 무너지면, "
              "검사로는 잘 드러나지 않는 여러 증상이 함께 나타납니다. "
              "어지럼과 두근거림, 속의 불편이 한 사람에게 겹쳐 오는 것도 그래서입니다."]),
            ("이런 분께 권합니다",
             ["<ul class=\"blk-list\">"
              "<li>여러 검사에서 큰 이상이 없다는데 증상이 반복되는 분</li>"
              "<li>스트레스·과로로 컨디션이 무너진 분</li>"
              "<li>갱년기 전후의 변화로 힘든 분</li></ul>"]),
            ("이렇게 진행됩니다",
             [# 네 단계라 한 줄씩 끊어 둡니다. 붙여 쓰면 순서가 눈에 안 들어옵니다.
              "① 문진과 진맥으로 자율신경의 균형 상태와 몸의 원인을 확인합니다.<br />"
              "② 몸이 반응하는 방향을 보며 치료를 구성합니다.<br />"
              "③ 수면·식이·생활 관리를 함께 안내합니다.<br />"
              "④ 경과를 보며 계획을 조정합니다.",
              "※ 증상이 지속되거나 다른 원인이 의심되면 필요한 검사·협진을 안내합니다. "
              ]),
        ],
    ),
}


def _grid_mod(h):
    """카드 셋은 한 줄(3up), 넷은 두 줄(기본 2열)로 놓습니다."""
    return " svc__grid--3up" if len(h["children"]) == 3 else ""


def _cards(h):
    out = []
    for slug, dx, sym in h["children"]:
        d = h["source"][slug]
        line = d["desc"].replace(PN.M, " ").replace("<br />", " ")
        # 한 페이지가 진단명 둘 이상을 담으면 카드에 함께 적어 줍니다.
        names = [x.strip() for x in d.get("diagnoses", "").split(",") if x.strip()]
        dx_line = ""
        if len(names) > 1:
            dx_line = ('          <p class="svc-card__dx">%s</p>\n'
                       % " · ".join(names))
        out.append(
            f'        <a class="svc-card svc-card--plain" href="{slug}.html">\n'
            f'          <p class="svc-card__line">{sym}</p>\n'
            f'          <h3>{dx}</h3>\n'
            f'{dx_line}'
            f'          <p class="svc-card__desc">{P.lines(line)}</p>\n'
            f'          <span class="svc-card__more">진료 보기 →</span>\n'
            f'        </a>')
    return "\n".join(out)


def _blocks(h):
    if not h.get("blocks"):
        return ""
    out = []
    for title, paras in h["blocks"]:
        body = "\n".join("        <p>%s</p>" % P.lines(x) for x in paras)
        out.append('      <div class="svc-detail__block">\n'
                   '        <h3>%s</h3>\n%s\n      </div>' % (title, body))
    return ('\n  <section class="section section--cream">\n'
            '    <div class="container container--read">\n'
            + "\n".join(out) + '\n    </div>\n  </section>\n')


def build_hub(slug):
    h = HUBS[slug]
    title = f"{P.REGION} {h['seo_kw']} 한의원 – {P.CLINIC}({P.STATION})"
    desc = f"{P.REGION}·{P.STATION} {P.CLINIC}. {h['meta']}."
    return (P.head(slug, title, desc, keywords=h["keywords"])
            + P.topbar() + P.header(slug)
            + P.page_hero(h["title"], h["desc"]) + P.crumb(h["label"])
            + f"""
  <section class="section">
    <div class="container">
      <div class="section__head section__head--center">
        <h2 class="section__title">어디가 불편하신가요</h2>
        <p class="section__lead">{h['lead']}</p>
      </div>
      <div class="svc__grid{_grid_mod(h)}">
{_cards(h)}
      </div>
      <p class="programs__note">{P.NOTICE_LINE}</p>
    </div>
  </section>
""" + _blocks(h) + P.tail())


def build_accident():
    """교통사고 후유증 — 진료과목이 아니라 보험 절차 안내입니다. 내용은 원장 확인 후."""
    fill = PN.f
    todo = [
        "자동차보험 접수 절차 — 접수번호를 어디서 받아 오시게 안내할지",
        "본인부담금이 있는지, 있다면 어떤 경우인지",
        "합의 전후로 치료가 어떻게 달라지는지",
        "진단서·통원확인서 발급 안내",
        "이 페이지를 메뉴에 올릴지, 푸터 링크로만 둘지",
    ]
    items = "\n".join(f"          <li>{t}</li>" for t in todo)
    return (P.head("accident", f"교통사고 후유증 안내 | {P.CLINIC}",
                   f"교통사고 후유증 안내 | {P.CLINIC}")
            + P.topbar() + P.header("accident")
            + P.page_hero("교통사고 후유증 안내", fill("한 줄 소개 — 원장 확인"))
            + P.crumb("교통사고 후유증 안내")
            + f"""
  <section class="section">
    <div class="container container--read">
      <div class="draft-banner">
        <strong>⚠️ 내용 준비 중입니다.</strong>
        교통사고는 진료과목이 아니라 <strong>보험 절차 안내</strong>로 분리했습니다.
        아래를 확정해야 공개할 수 있습니다.
        <ul style="margin-top:10px;">
{items}
        </ul>
      </div>
      <p class="why-text">{fill("교통사고 후유증 안내 본문 — 원장 확인")}</p>
    </div>
  </section>
""" + P.tail())


def all_hubs():
    # 교통사고 안내(build_accident)는 내용이 정해지지 않아 당분간 내보내지 않습니다.
    # 보험 절차 원고가 나오면 아래에 pages["accident"] = build_accident() 를 되살리면 됩니다.
    return {slug: build_hub(slug) for slug in HUBS}
