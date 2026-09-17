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
# 분류 — partials 의 진료 갈래를 그대로 씁니다.
# 여기서 새로 짓지 않습니다. 메뉴에 없는 이름이 후기에만 있으면 어긋납니다.
def 분류들():
    return [label for _, label, _ in P.SUBJECTS] + ["기타"]


R_TITLE = "치료 후기"
# 로그인 전후 양쪽에서 다 읽히는 문장이어야 합니다 — 히어로는 한 벌뿐입니다
R_LEAD  = f"진료를 받으신 분들이 남긴 글입니다.{M}회원만 보실 수 있습니다."

# 로그인하지 않은 분께 목록 위에 뜨는 줄.
# 목록은 보여 드리고 내용만 막습니다(원장님 지시, 2026-09-17).
GATE_TITLE = "내용은 회원만 볼 수 있습니다"
GATE_BODY = [
    "제목과 분류는 누구나 보실 수 있고, <strong>글 내용은 로그인하셔야</strong> 보입니다.",
    "의료법은 환자의 치료경험담을 광고로 보고, 누구에게나 열린 곳에 두는 것을 "
    "금하고 있습니다. 그래서 내용은 회원으로 들어오신 분에게만 엽니다.",
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
    cat_options = "\n".join(f'                  <option value="{c}">{c}</option>' for c in 분류들())
    cat_tabs = "\n".join(
        f'          <button type="button" class="rv-tab" data-cat="{c}" role="tab" '
        f'aria-selected="false" hidden>{c}</button>' for c in 분류들())

    return (
        P.head("reviews", f"{R_TITLE} | {P.CLINIC}",
               "회원 전용 페이지입니다.", noindex=True)
        + P.topbar() + P.header("reviews")
        + P.page_hero(R_TITLE, R_LEAD)
        + P.crumb(R_TITLE)
        + f"""
  <section class="section">
    <div class="container container--read">

      <!-- 원장 계정일 때만 열립니다.
           다른 계정이 열어 보려 해도 등록 단계에서 데이터베이스가 거부합니다. -->
      <div class="review-write" id="reviewWrite" hidden>
        <h2 class="review-write__title">{WRITE_TITLE}</h2>
        <form id="reviewForm" novalidate>

          <div class="field">
            <span class="field__label">제목</span>
            <span class="field__row field__row--title">
              <select id="reviewCat" class="field__input field__select" required>
                <option value="">분류</option>
{cat_options}
              </select>
              <input type="number" id="reviewAge" class="field__input field__input--age"
                     min="1" max="120" placeholder="66" aria-label="나이" required />
              <span class="field__at">세</span>
              <select id="reviewSex" class="field__input field__select field__input--sex"
                      aria-label="성별" required>
                <option value="여">여</option>
                <option value="남">남</option>
              </select>
              <input type="text" id="reviewWho" class="field__input" maxlength="20"
                     placeholder="차OO님" aria-label="성함 표기" required />
            </span>
            <span class="field__hint">이렇게 나옵니다 — <strong id="titlePreview">척추관협착증, 66세, 여, 차OO님</strong></span>
          </div>

          <div class="field">
            <span class="field__label">사진</span>
            <input type="file" id="reviewPhoto" class="field__file"
                   accept="image/jpeg,image/png,image/webp" />
            <span class="field__hint">
              <strong>서면 동의를 받은 사진만</strong> 올리십시오. 이 사진은
              로그인하지 않은 분께도 보입니다. 한 번 공개되면 거두기 어렵습니다.
            </span>

            <!-- 얼굴 가리기 — 사진을 고르면 열립니다 -->
            <div class="shot" id="shotBox" hidden>
              <canvas id="shotCanvas" class="shot__canvas"></canvas>
              <p class="shot__help">
                얼굴 위를 <strong>손가락이나 마우스로 문지르면</strong> 그 자리가 가려집니다.
                여러 번 칠하셔도 됩니다.
              </p>
              <div class="shot__act">
                <button type="button" class="btn btn--outline btn--check" id="shotUndo">되돌리기</button>
                <button type="button" class="btn btn--outline btn--check" id="shotClear">사진 빼기</button>
              </div>
            </div>
          </div>

          <label class="field">
            <span class="field__label">내용</span>
            <textarea id="reviewBody" class="field__input field__input--area"
                      rows="9" maxlength="4000" required></textarea>
          </label>
          <p class="field__count"><span id="reviewCount">0</span> / 4000자</p>
          <p class="form__msg" id="reviewMsg" role="status" aria-live="polite" hidden></p>
          <div class="form__actions">
            <button type="submit" class="btn btn--accent" id="reviewSubmit">올리기</button>
          </div>
        </form>
{_write_note()}
      </div>

      <h2 class="review-list__title">{R_TITLE}</h2>
      <p class="review-list__note">아래는 <strong>작성자 개인의 경험</strong>입니다.
        같은 치료를 받으신 다른 분에게 같은 결과가 나타난다는 뜻이 아니며,
        치료 효과에 대한 약속으로 읽지 말아 주십시오.</p>

      <!-- 로그인하지 않은 분께만 — auth.js 가 세션을 보고 폅니다.
           기본을 hidden 으로 두는 이유는, 로그인하고 오신 분께 잠깐이라도
           '로그인하십시오' 가 번쩍이지 않게 하려는 것입니다. -->
      <div class="rv-notice" id="rvNotice" hidden>
        <div class="rv-notice__body">
          <h3 class="rv-notice__title">{GATE_TITLE}</h3>
{gate_p}
        </div>
        <div class="rv-notice__act">
          <a href="login.html" class="btn btn--accent">로그인</a>
          <a href="login.html#join" class="btn btn--outline">회원가입</a>
        </div>
      </div>

      <div class="rv-tabs" id="reviewTabs" role="tablist" aria-label="분류">
        <button type="button" class="rv-tab is-active" data-cat="" role="tab" aria-selected="true">전체</button>
{cat_tabs}
      </div>

      <div class="rv-search">
        <label class="sr-only" for="reviewSearch">후기 검색</label>
        <input type="search" id="reviewSearch" class="field__input"
               placeholder="제목으로 찾기" autocomplete="off" />
      </div>

      <p class="review-list__state" id="reviewState">불러오는 중입니다.</p>
      <ol class="rv-list" id="reviewList"></ol>
      <nav class="rv-pager" id="reviewPager" aria-label="페이지" hidden></nav>

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
            <span class="field__label">아이디</span>
            <input type="text" id="loginId" class="field__input"
                   autocomplete="username" autocapitalize="off" spellcheck="false" required />
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
          아이디나 비밀번호가 기억나지 않으시면 <a href="tel:{P.TEL}">{P.TEL}</a> 로
          전화 주십시오. 확인해 드립니다.
        </p>
      </div>

      <!-- 회원가입 -->
      <div class="auth-pane" id="paneJoin" role="tabpanel" aria-labelledby="tabJoin" hidden>
        <form id="joinForm" novalidate>

          <label class="field">
            <span class="field__label">아이디 <em class="req">*</em></span>
            <span class="field__row">
              <input type="text" id="joinId" class="field__input" maxlength="20"
                     autocomplete="username" autocapitalize="off" spellcheck="false" required />
              <button type="button" class="btn btn--outline btn--check" id="checkId">중복확인</button>
            </span>
            <span class="field__hint">영문 소문자·숫자·밑줄(_) 4~20자. 로그인할 때 쓰십니다.</span>
            <span class="field__note" id="idNote" hidden></span>
          </label>

          <label class="field">
            <span class="field__label">비밀번호 <em class="req">*</em></span>
            <input type="password" id="joinPw" class="field__input"
                   autocomplete="new-password" minlength="8" required />
            <span class="field__hint">8자 이상. 영문과 숫자를 섞어 주십시오.</span>
          </label>

          <label class="field">
            <span class="field__label">비밀번호 확인 <em class="req">*</em></span>
            <input type="password" id="joinPw2" class="field__input"
                   autocomplete="new-password" required />
          </label>

          <label class="field">
            <span class="field__label">이름 <em class="req">*</em></span>
            <input type="text" id="joinName" class="field__input" maxlength="20"
                   autocomplete="name" placeholder="홍길동" required />
            <span class="field__hint">진료받으신 이름과 같아야 확인이 됩니다.</span>
          </label>

          <label class="field">
            <span class="field__label">휴대폰 번호 <em class="req">*</em></span>
            <span class="field__row">
              <input type="tel" id="joinPhone" class="field__input" maxlength="13"
                     autocomplete="tel" inputmode="numeric" placeholder="010-1234-5678" required />
              <button type="button" class="btn btn--outline btn--check" id="checkPhone">중복확인</button>
            </span>
            <span class="field__note" id="phoneNote" hidden></span>
          </label>

          <label class="field">
            <span class="field__label">생년월일 <em class="req">*</em></span>
            <input type="text" id="joinBirth" class="field__input" maxlength="10"
                   inputmode="numeric" placeholder="1988.10.25" required />
            <span class="field__hint">같은 이름이 계실 때 구분하는 데 씁니다.</span>
          </label>

          <div class="field">
            <span class="field__label">이메일 <em class="req">*</em></span>
            <span class="field__row field__row--email">
              <input type="text" id="joinEmailHead" class="field__input" maxlength="64"
                     autocapitalize="off" spellcheck="false" required />
              <span class="field__at">@</span>
              <input type="text" id="joinEmailTail" class="field__input" maxlength="64"
                     autocapitalize="off" spellcheck="false" required />
            </span>
            <select id="joinEmailPick" class="field__input field__select" aria-label="이메일 주소 고르기">
              <option value="">직접 입력</option>
              <option value="naver.com">naver.com</option>
              <option value="gmail.com">gmail.com</option>
              <option value="hanmail.net">hanmail.net</option>
              <option value="daum.net">daum.net</option>
              <option value="nate.com">nate.com</option>
              <option value="kakao.com">kakao.com</option>
            </select>
            <span class="field__hint">연락이 필요할 때 씁니다. 광고는 보내지 않습니다.</span>
          </div>

          <fieldset class="agree">
            <legend class="agree__legend">동의</legend>
            <label class="agree__row">
              <input type="checkbox" id="agPrivacy" required />
              <span><em>(필수)</em> <a href="privacy.html" target="_blank" rel="noopener">개인정보 수집 및 이용</a>에 동의합니다.</span>
              <span class="agree__note">이름·휴대폰·생년월일·이메일을 받습니다.
                후기 열람에 필요한 회원 확인에만 쓰고, 회원 정보는 일본 도쿄에 있는 서버에 보관됩니다.</span>
            </label>
          </fieldset>

          <p class="form__msg" id="joinMsg" role="status" aria-live="polite" hidden></p>
          <div class="form__actions">
            <button type="submit" class="btn btn--accent btn--full" id="joinSubmit">가입하기</button>
          </div>
        </form>
      </div>

      <p class="auth-foot">
        회원 정보는 치료 후기를 읽는 데에만 씁니다. 진료 예약은 회원과 관계없이
        <a href="tel:{P.TEL}">{P.TEL}</a> 로 받습니다.
      </p>

    </div>
  </section>
""" + P.tail(with_cta=False, extra_scripts=P.auth_scripts()))


# ── 환자 사진·후기 게시 동의서 ────────────────────────────────
#
# 종이로 받아 보관하시는 서식입니다. 메뉴에 없고 검색에도 안 걸립니다.
# 주소를 직접 쳐서 열고 인쇄하십시오 — jungjinhani.com/consent.html
#
# 이 서식이 지켜 주는 것과 못 지켜 주는 것이 다릅니다.
#   지켜 줍니다 — 초상권, 개인정보보호법(민감정보 처리)
#   못 지켜 줍니다 — 의료법 제56조. 환자가 동의해도 의료기관이 게시하면
#                   광고 규제를 받습니다. 동의서로 면제되지 않습니다.
CONSENT_TITLE = "치료 후기·사진 게시 동의서"

CONSENT = [
 ("1. 무엇에 동의하시는 것입니까",
  ["아래에 적으신 분은 {CLINIC}이 진료 경험에 관한 글과 사진을 "
   "홈페이지에 싣는 것에 동의하십니다.",
   "<strong>사진과 제목은 회원이 아닌 분께도 보입니다.</strong> 글 내용은 "
   "회원으로 가입해 로그인하신 분만 보실 수 있습니다."], []),

 ("2. 어떤 것이 실립니까", [],
  ["분류(질환명)·나이·성별과 <strong>성(姓)만 적은 표기</strong> — 예: 차OO님",
   "진료 경험에 관한 글",
   "사진 (동의하신 경우에만)"]),

 ("3. 사진에 대하여",
  ["사진은 <strong>한 번 공개되면 거두기 어렵습니다.</strong> 다른 사람이 "
   "내려받거나 옮겨 담은 것까지는 본원이 막을 수 없습니다.",
   "원하시면 <strong>얼굴을 가려서</strong> 실어 드립니다. 아래에 표시해 주십시오."],
  ["□ 얼굴이 보이는 그대로 실어도 좋습니다",
   "□ 얼굴을 가려 주십시오",
   "□ 사진은 싣지 말아 주십시오"]),

 ("4. 언제든 그만두실 수 있습니다",
  ["동의는 <strong>언제든 철회하실 수 있습니다.</strong> 전화 한 통이면 됩니다 — "
   "{TEL}",
   "말씀하시면 글과 사진을 지체 없이 내립니다. 다만 이미 다른 곳으로 "
   "퍼진 것은 되돌릴 수 없습니다.",
   "동의하지 않으셔도 <strong>진료에는 아무런 불이익이 없습니다.</strong>"], []),

 ("5. 보관",
  ["이 동의서는 본원이 종이로 보관합니다. 글과 사진을 내린 뒤에는 "
   "동의서도 함께 파기합니다."], []),
]


def build_consent():
    arts = []
    for h, paras, lis in CONSENT:
        arts.append(f"        <h2>{h}</h2>")
        for t in paras:
            arts.append(f'        <p>{t.replace("{CLINIC}", P.CLINIC).replace("{TEL}", P.TEL)}</p>')
        if lis:
            arts.append("        <ul>")
            arts += [f"          <li>{x}</li>" for x in lis]
            arts.append("        </ul>")

    return (P.head("consent", f"{CONSENT_TITLE} | {P.CLINIC}",
                   "환자분께 서면으로 받는 동의서입니다.", noindex=True)
            + P.topbar() + P.header("consent")
            + P.page_hero(CONSENT_TITLE,
                          f"진료 경험에 관한 글과 사진을{M}홈페이지에 싣는 것에 대한 동의서입니다.")
            + P.crumb(CONSENT_TITLE)
            + f"""
  <section class="section">
    <div class="container container--read">
      <div class="consent-print">
        <button type="button" class="btn btn--outline" onclick="window.print()">인쇄하기</button>
      </div>
      <article class="legal">
{chr(10).join(arts)}
        <h2>서명</h2>
        <dl class="consent-sign">
          <div><dt>성명</dt><dd></dd></div>
          <div><dt>생년월일</dt><dd></dd></div>
          <div><dt>연락처</dt><dd></dd></div>
          <div><dt>날짜</dt><dd>&nbsp; 년 &nbsp; 월 &nbsp; 일</dd></div>
          <div><dt>서명</dt><dd>(서명 또는 인)</dd></div>
        </dl>
        <p class="consent-foot">{P.CLINIC} · {P.ADDRESS} · {P.TEL}</p>
      </article>
    </div>
  </section>
""" + P.tail(with_cta=False))


def all_reviews():
    return {"reviews": build_reviews(), "login": build_login(),
            "consent": build_consent()}
