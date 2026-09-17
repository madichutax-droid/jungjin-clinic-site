# -*- coding: utf-8 -*-
"""
치료 후기 · 회원 로그인 두 페이지.

── 왜 로그인 뒤에 두는가 ──────────────────────────────────────
의료법 제56조 제2항 제2호는 환자의 치료경험담을 의료광고로 보고 금지합니다.
'불특정 다수에게 공개되는가' 가 광고인지 아닌지를 가르는 자리라,
열람을 회원 뒤로 두고 검색엔진에서도 내립니다.

막는 자리가 넷입니다. 하나라도 빠지면 벽이 뚫립니다.

  ① 데이터베이스  Supabase RLS 가 비로그인 요청에 한 줄도 주지 않습니다
  ② 화면         로그인 전에는 후기가 DOM 에 들어오지 않습니다 (숨기는 게 아닙니다)
  ③ 검색엔진      noindex + robots.txt Disallow + sitemap 제외

후기는 **원장이 올립니다.** 회원은 로그인해서 읽기만 합니다.
글 쓰는 칸은 원장 계정으로 로그인했을 때만 열립니다 — 화면에서 숨기는 것이
아니라, 다른 계정이 올리려고 하면 데이터베이스가 거부합니다.

②만 해 두고 ①을 빼면 브라우저 개발자도구로 그대로 읽힙니다.
정책 파일은 `schema.sql`, 넣는 법은 `회원시스템-설치.md` 에 있습니다.

원고는 이 페이지를 위해 새로 지은 것이라 원장님 확인이 필요합니다.
"""

import partials as P
import content_subjects as C

M = C.M

# ── 원고 ──────────────────────────────────────────────────────
# 후기 페이지에 쓰는 문장. 확정 전까지는 여기만 고치면 됩니다.
R_TITLE = "치료 후기"
# 로그인 전후 양쪽에서 다 읽히는 문장이어야 합니다 — 히어로는 한 벌뿐입니다
R_LEAD  = f"진료를 받으신 분들이 남긴 글입니다.{M}회원만 보실 수 있습니다."

# 로그인 벽 앞에 서는 분께 — 왜 막혀 있는지 밝힙니다.
GATE_TITLE = "회원만 볼 수 있습니다"
GATE_BODY = [
    "치료 후기는 로그인하신 회원에게만 보입니다.",
    "의료법은 환자의 치료경험담을 광고로 보고, 누구에게나 열린 곳에 두는 것을 "
    "금하고 있습니다. 그래서 회원으로 들어오신 분에게만 엽니다.",
]

# 원장 화면에만 나오는 안내. 옮겨 적으실 때 걸리는 것들입니다.
WRITE_TITLE = "후기 올리기"
WRITE_NOTE = [
    "환자분께 <strong>동의를 받은 글만</strong> 올리십시오. 건강에 관한 내용이라 "
    "종이로 받아 두시는 편이 안전합니다.",
    "실명 대신 <strong>‘60대 · 여성’</strong> 이나 <strong>‘ㄱ님’</strong> 처럼 적으십시오. "
    "연락처·주민등록번호는 적지 마십시오.",
    "치료 효과를 단정하는 말이 들어 있으면 등록할 때 어느 말인지 알려 드립니다. "
    "그 말만 빼고 올리십시오.",
]

L_TITLE = "회원 로그인"
L_LEAD  = f"치료 후기를 보시려면{M}로그인이 필요합니다."


def _write_note():
    """원장 화면에만 붙는 안내."""
    lis = "\n".join(f"          <li>{x}</li>" for x in WRITE_NOTE)
    return f"""        <div class="notice-box">
          <h3 class="notice-box__title">올리시기 전에</h3>
          <ul>
{lis}
          </ul>
          <p class="notice-box__law">의료법 제56조(의료광고의 금지 등) · 개인정보 보호법 제23조</p>
        </div>"""


def _not_ready(page, label, lead):
    """Supabase 설정이 비어 있을 때 나가는 쪽.

    링크가 404 로 떨어지는 것보다, 준비 중이라고 적힌 쪽이 낫습니다.
    메뉴에는 이때 후기 칸이 아예 나오지 않으므로 주소를 직접 친 분만 봅니다."""
    return (P.head(page, f"{label} | {P.CLINIC}", f"{label} | {P.CLINIC}", noindex=True)
            + P.topbar() + P.header(page)
            + P.page_hero(label, lead) + P.crumb(label)
            + f"""
  <section class="section">
    <div class="container container--read">
      <p class="section__lead">준비 중입니다.</p>
      <p>진료 문의는 <a href="tel:{P.TEL}">{P.TEL}</a> 로 받습니다.</p>
      <div class="location__actions">
        <a href="index.html#hero" class="btn btn--accent">홈으로</a>
        <a href="faq.html" class="btn btn--outline">자주 묻는 질문</a>
      </div>
    </div>
  </section>
""" + P.tail(with_cta=False))


def build_reviews():
    if not P.reviews_ready():
        return _not_ready("reviews", R_TITLE, R_LEAD)

    gate_p = "\n".join(f'          <p>{P.lines(x)}</p>' for x in GATE_BODY)

    return (
        P.head("reviews", f"{R_TITLE} | {P.CLINIC}",
               "회원 전용 페이지입니다.", noindex=True)
        + P.topbar() + P.header("reviews")
        + P.page_hero(R_TITLE, R_LEAD)
        + P.crumb(R_TITLE)
        + f"""
  <section class="section">
    <div class="container container--read">

      <!-- 로그인 전 — 서버가 찍어내는 기본 상태입니다.
           auth.js 가 세션을 확인하면 이 칸을 닫고 아래 회원 칸을 엽니다.
           자바스크립트가 꺼져 있으면 여기서 멈춥니다. 그래도 괜찮습니다. -->
      <div class="review-gate" id="reviewGate">
        <div class="review-gate__inner">
          <h2 class="review-gate__title">{GATE_TITLE}</h2>
{gate_p}
          <div class="location__actions">
            <a href="login.html" class="btn btn--accent">로그인</a>
            <a href="login.html#join" class="btn btn--outline">회원가입</a>
          </div>
        </div>
      </div>

      <!-- 로그인 후 — hidden 으로 나갑니다. 내용은 비어 있고,
           후기 본문은 로그인한 브라우저만 Supabase 에서 받아 옵니다. -->
      <div class="review-area" id="reviewArea" hidden>

        <!-- 글 쓰는 칸 — 원장 계정일 때만 열립니다.
             다른 계정이 열어 보려 해도 등록 단계에서 데이터베이스가 거부합니다. -->
        <div class="review-write" id="reviewWrite" hidden>
          <h2 class="review-write__title">{WRITE_TITLE}</h2>
          <form id="reviewForm" novalidate>
            <label class="field">
              <span class="field__label">쓰신 분</span>
              <input type="text" id="reviewWho" class="field__input" maxlength="20"
                     required placeholder="60대 · 여성" />
              <span class="field__hint">화면에 이대로 나옵니다. 실명은 적지 마십시오.</span>
            </label>
            <label class="field">
              <span class="field__label">내용</span>
              <textarea id="reviewBody" class="field__input field__input--area"
                        rows="8" maxlength="2000" required></textarea>
            </label>
            <p class="field__count"><span id="reviewCount">0</span> / 2000자</p>
            <p class="form__msg" id="reviewMsg" role="status" aria-live="polite" hidden></p>
            <div class="form__actions">
              <button type="submit" class="btn btn--accent" id="reviewSubmit">올리기</button>
            </div>
          </form>
{_write_note()}
        </div>

        <h2 class="review-list__title">치료 후기</h2>
        <p class="review-list__state" id="reviewState">불러오는 중입니다.</p>
        <ol class="review-list" id="reviewList"></ol>

      </div>

      <p class="programs__note">{P.NOTICE_LINE}</p>
    </div>
  </section>
""" + P.tail(with_cta=False, extra_scripts=P.auth_scripts()))


def build_login():
    if not P.reviews_ready():
        return _not_ready("login", L_TITLE, L_LEAD)

    return (
        P.head("login", f"{L_TITLE} | {P.CLINIC}",
               "회원 로그인 페이지입니다.", noindex=True)
        + P.topbar() + P.header("login")
        + P.page_hero(L_TITLE, L_LEAD)
        + P.crumb(L_TITLE)
        + f"""
  <section class="section">
    <div class="container container--narrow">

      <!-- id="join" — 후기 페이지의 '회원가입' 단추가 #join 으로 옵니다.
           auth.js 도 같은 조각을 보고 가입 칸을 폅니다. 둘 중 하나만 있으면
           자바스크립트가 꺼진 브라우저에서 아무 데도 가지 않습니다. -->
      <div class="auth-tabs" id="join" role="tablist">
        <button type="button" class="auth-tab is-active" id="tabLogin"
                role="tab" aria-selected="true" aria-controls="paneLogin">로그인</button>
        <button type="button" class="auth-tab" id="tabJoin"
                role="tab" aria-selected="false" aria-controls="paneJoin">회원가입</button>
      </div>

      <!-- 로그인 -->
      <div class="auth-pane" id="paneLogin" role="tabpanel" aria-labelledby="tabLogin">
        <form id="loginForm" novalidate>
          <label class="field">
            <span class="field__label">이메일</span>
            <input type="email" id="loginEmail" class="field__input"
                   autocomplete="email" required />
          </label>
          <label class="field">
            <span class="field__label">비밀번호</span>
            <input type="password" id="loginPw" class="field__input"
                   autocomplete="current-password" required />
          </label>
          <p class="form__msg" id="loginMsg" role="status" aria-live="polite" hidden></p>
          <div class="form__actions">
            <button type="submit" class="btn btn--accent btn--full" id="loginSubmit">로그인</button>
          </div>
        </form>
        <p class="auth-help">
          <button type="button" class="linklike" id="resetLink">비밀번호를 잊으셨습니까?</button>
        </p>
      </div>

      <!-- 회원가입 -->
      <div class="auth-pane" id="paneJoin" role="tabpanel" aria-labelledby="tabJoin" hidden>
        <form id="joinForm" novalidate>
          <label class="field">
            <span class="field__label">이메일</span>
            <input type="email" id="joinEmail" class="field__input"
                   autocomplete="email" required />
            <span class="field__hint">가입 확인 메일이 갑니다. 받으신 메일의 링크를 누르셔야 로그인됩니다.</span>
          </label>
          <label class="field">
            <span class="field__label">비밀번호</span>
            <input type="password" id="joinPw" class="field__input"
                   autocomplete="new-password" minlength="8" required />
            <span class="field__hint">8자 이상. 영문과 숫자를 섞어 주십시오.</span>
          </label>

          <!-- 체크칸 대신 한 줄로 갈음합니다.
               개인정보보호법 제15조 제1항 제4호(계약의 이행)와 제28조의8 제3호
               (계약 이행에 필요한 국외 보관 + 처리방침 공개)에 기대고 있습니다.
               그래서 처리방침 5-1 의 여섯 항목이 빠지면 안 됩니다. 그것이 근거입니다. -->
          <p class="agree-line">
            <strong>가입하기</strong>를 누르시면
            <a href="terms.html" target="_blank" rel="noopener">이용약관</a>과
            <a href="privacy.html" target="_blank" rel="noopener">개인정보처리방침</a>에
            동의하시는 것으로 봅니다. 회원 정보는 일본 도쿄에 있는 서버에 보관되며,
            자세한 것은 <a href="privacy.html#abroad" target="_blank" rel="noopener">국외 이전 조항</a>에 있습니다.
          </p>

          <p class="form__msg" id="joinMsg" role="status" aria-live="polite" hidden></p>
          <div class="form__actions">
            <button type="submit" class="btn btn--accent btn--full" id="joinSubmit">가입하기</button>
          </div>
        </form>
      </div>

      <p class="auth-foot">
        회원 정보는 치료 후기를 쓰고 읽는 데에만 씁니다. 진료 예약은 회원과 관계없이
        <a href="tel:{P.TEL}">{P.TEL}</a> 로 받습니다.
      </p>

    </div>
  </section>
""" + P.tail(with_cta=False, extra_scripts=P.auth_scripts()))


def all_reviews():
    return {"reviews": build_reviews(), "login": build_login()}
