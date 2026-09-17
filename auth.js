// ══════════════════════════════════════════════════════════════
// 회원 로그인 · 치료 후기
//
// 치료 후기·로그인 두 페이지에서만 실려 있습니다 (partials.auth_scripts).
// 나머지 20페이지는 지금도 script.js 하나만 받습니다.
//
// 후기는 **원장이 올립니다.** 회원은 로그인해서 읽기만 합니다.
//
// 이 파일은 **화면을 바꿀 뿐 아무것도 지키지 못합니다.** 후기를 실제로 막는
// 것은 Supabase 의 RLS 정책(_build/schema.sql)입니다. 여기서 hidden 을 붙이는
// 것은 보기 좋으라고 하는 일이고, 비로그인에게 한 줄도 안 나가게 하는 것도
// 원장 아닌 사람이 못 올리게 하는 것도 데이터베이스가 합니다.
// 둘을 헷갈리면 개발자도구로 그대로 읽힙니다.
// ══════════════════════════════════════════════════════════════

(function () {
  'use strict';

  const CFG = window.JJ_SUPABASE || {};
  if (!CFG.url || !CFG.key || !window.supabase) return;

  const sb = window.supabase.createClient(CFG.url, CFG.key);

  // ── 아이디 로그인 ───────────────────────────────────────────
  // Supabase 는 이메일로만 로그인합니다. 아이디를 쓰려고
  // `아이디@u.jungjinhani.com` 이라는 가짜 주소를 만들어 인증에 씁니다.
  // 진짜 이메일은 profiles.email 에 따로 담습니다.
  //
  // 그래서 Supabase 의 '메일 확인' 은 반드시 꺼져 있어야 합니다.
  // 켜 두면 가짜 주소로 확인 메일이 가고 아무도 가입을 끝내지 못합니다.
  const ID_DOMAIN = '@u.jungjinhani.com';
  const 가짜메일 = function (id) { return String(id).trim().toLowerCase() + ID_DOMAIN; };

  const ID_규칙 = /^[a-z0-9_]{4,20}$/;
  const 숫자만 = function (v) { return String(v || '').replace(/[^0-9]/g, ''); };
  const 폰_규칙 = /^01[016789][0-9]{7,8}$/;

  /** 1988.10.25 · 1988-10-25 · 19881025 을 모두 1988-10-25 로. 못 읽으면 null. */
  function 생년월일(v) {
    const d = 숫자만(v);
    if (d.length !== 8) return null;
    const y = +d.slice(0, 4), m = +d.slice(4, 6), day = +d.slice(6, 8);
    const 올해 = new Date().getFullYear();
    if (y < 1900 || y > 올해) return null;
    if (m < 1 || m > 12 || day < 1 || day > 31) return null;
    const t = new Date(y, m - 1, day);
    if (t.getFullYear() !== y || t.getMonth() !== m - 1 || t.getDate() !== day) return null;
    return d.slice(0, 4) + '-' + d.slice(4, 6) + '-' + d.slice(6, 8);
  }

  // ── 잔손질 ──────────────────────────────────────────────────
  const $ = function (id) { return document.getElementById(id); };

  /** 메시지 한 줄. kind 는 'ok' 또는 'bad'. */
  function say(el, text, kind) {
    if (!el) return;
    el.textContent = text;
    el.className = 'form__msg form__msg--' + (kind || 'bad');
    el.hidden = false;
  }
  function clear(el) { if (el) { el.hidden = true; el.textContent = ''; } }

  /** 버튼을 눌린 채로 잠급니다 — 두 번 눌러 두 번 등록되는 것을 막습니다. */
  function busy(btn, on, label) {
    if (!btn) return;
    if (on) {
      btn.dataset.label = btn.textContent;
      btn.textContent = label || '잠시만 기다려 주십시오';
      btn.disabled = true;
    } else {
      btn.textContent = btn.dataset.label || btn.textContent;
      btn.disabled = false;
    }
  }

  // Supabase 는 영어로 답합니다. 자주 나오는 것만 우리말로 바꿉니다.
  // 못 알아본 것은 원문을 그대로 보여 줍니다 — 삼켜 버리면 원인을 찾을 수 없습니다.
  const 안내 = [
    ['Invalid login credentials', '이메일 또는 비밀번호가 맞지 않습니다.'],
    ['Email not confirmed', '가입 확인 메일의 링크를 먼저 눌러 주십시오.'],
    ['User already registered', '이미 가입된 이메일입니다. 로그인해 주십시오.'],
    ['already been registered', '이미 가입된 이메일입니다. 로그인해 주십시오.'],
    ['Password should be at least', '비밀번호는 8자 이상이어야 합니다.'],
    ['Unable to validate email', '이메일 주소를 다시 확인해 주십시오.'],
    ['For security purposes', '잠시 뒤에 다시 시도해 주십시오.'],
    ['rate limit', '요청이 잦습니다. 잠시 뒤에 다시 시도해 주십시오.'],
    ['Failed to fetch', '연결이 되지 않았습니다. 잠시 뒤에 다시 시도해 주십시오.'],
  ];
  function 말로(err) {
    const m = (err && (err.message || err.error_description)) || '';
    for (let i = 0; i < 안내.length; i++) {
      if (m.indexOf(안내[i][0]) >= 0) return 안내[i][1];
    }
    return m || '처리하지 못했습니다. 잠시 뒤에 다시 시도해 주십시오.';
  }

  /** 상단바 인사에 쓸 이름. 가짜 메일의 앞부분이 곧 아이디입니다. */
  function 이름(user) {
    return (user && user.email) ? user.email.split('@')[0] : '회원';
  }

  function 날짜(iso) {
    const d = new Date(iso);
    if (isNaN(d)) return '';
    return d.getFullYear() + '. ' + (d.getMonth() + 1) + '. ' + d.getDate() + '.';
  }

  // ── 의료광고 금지 표현 ───────────────────────────────────────
  //
  // 홈페이지/CLAUDE.md 의 금지 목록과 같은 줄입니다. 한쪽에서 걸리는 표현은
  // 다른 쪽에서도 걸립니다. 환자분 말씀을 그대로 옮기다 보면 '완치' 같은 말이
  // 딸려 들어옵니다. 올리기 전에 한 번 붙잡아 드리는 자리입니다.
  const 금지 = ['완치', '100%', '반드시 낫', '보장', '무조건', '부작용 없', '부작용이 없',
                '재발 없', '재발이 없', '최고', '최상', '1위', '유일', '국내 최초',
                '명의', '권위자'];

  function 걸리는말(text) {
    const t = text.replace(/\s+/g, '');
    for (let i = 0; i < 금지.length; i++) {
      if (t.indexOf(금지[i].replace(/\s+/g, '')) >= 0) return 금지[i];
    }
    return null;
  }

  // ── 상단바 ──────────────────────────────────────────────────
  function 상단바(session) {
    const box = $('topbarAuth');
    if (!box) return;
    box.textContent = '';
    if (session) {
      const who = document.createElement('span');
      who.className = 'topbar__who';
      who.textContent = 이름(session.user) + '님';      // textContent — 이름에 태그가 들어와도 글자로만
      const out = document.createElement('button');
      out.type = 'button';
      out.className = 'linklike';
      out.textContent = '로그아웃';
      out.addEventListener('click', async function () {
        await sb.auth.signOut();
        location.href = 'index.html';
      });
      box.appendChild(who);
      box.appendChild(out);
    } else {
      const a = document.createElement('a');
      a.href = 'login.html';
      a.textContent = '로그인';
      box.appendChild(a);
    }
  }

  // ══════════════════════════════════════════════════════════
  //  치료 후기
  // ══════════════════════════════════════════════════════════
  const gate = $('reviewGate');
  const area = $('reviewArea');

  /** 후기 한 줄. 글은 전부 textContent 로만 넣습니다 —
   *  innerHTML 로 넣으면 후기 칸이 그대로 스크립트 주입 통로가 됩니다. */
  function 후기줄(row, 원장인가) {
    const li = document.createElement('li');
    li.className = 'review';

    const head = document.createElement('div');
    head.className = 'review__head';

    const who = document.createElement('span');
    who.className = 'review__who';
    who.textContent = row.author_name || '회원';
    head.appendChild(who);

    const when = document.createElement('time');
    when.className = 'review__when';
    when.dateTime = row.created_at;
    when.textContent = 날짜(row.created_at);
    head.appendChild(when);

    li.appendChild(head);

    const body = document.createElement('p');
    body.className = 'review__body';
    body.textContent = row.body;
    li.appendChild(body);

    // 지우기는 원장에게만 보입니다. 다른 사람이 눌러도 데이터베이스가 거부합니다.
    if (원장인가) {
      const del = document.createElement('button');
      del.type = 'button';
      del.className = 'linklike review__del';
      del.textContent = '지우기';
      del.addEventListener('click', async function () {
        if (!window.confirm('이 글을 지웁니다. 되돌릴 수 없습니다.')) return;
        const r = await sb.from('reviews').delete().eq('id', row.id);
        if (r.error) { window.alert(말로(r.error)); return; }
        목록(원장인가);
      });
      li.appendChild(del);
    }
    return li;
  }

  async function 목록(원장인가) {
    const list = $('reviewList');
    const state = $('reviewState');
    if (!list) return;

    // 걸러 내는 것은 아래 select 가 아니라 RLS 정책입니다.
    // 로그인하지 않은 브라우저는 여기서 빈 목록을 받습니다.
    const r = await sb.from('reviews')
      .select('id, author_name, body, created_at')
      .order('created_at', { ascending: false })
      .limit(200);

    list.textContent = '';
    if (r.error) {
      if (state) { state.textContent = 말로(r.error); state.hidden = false; }
      return;
    }
    const rows = r.data || [];
    if (!rows.length) {
      if (state) { state.textContent = '아직 올라온 글이 없습니다.'; state.hidden = false; }
      return;
    }
    if (state) state.hidden = true;
    for (let i = 0; i < rows.length; i++) list.appendChild(후기줄(rows[i], 원장인가));
  }

  /** 원장 화면에만 열리는 글쓰기 칸. */
  function 후기폼() {
    const form = $('reviewForm');
    if (!form) return;
    const who = $('reviewWho');
    const body = $('reviewBody');
    const msg = $('reviewMsg');
    const btn = $('reviewSubmit');
    const count = $('reviewCount');

    if (body && count) {
      body.addEventListener('input', function () {
        count.textContent = String(body.value.length);
      });
    }

    form.addEventListener('submit', async function (e) {
      e.preventDefault();
      clear(msg);
      const 이름 = (who.value || '').trim();
      const text = (body.value || '').trim();
      if (!이름) { say(msg, '‘쓰신 분’ 을 적어 주십시오. 예: 60대 · 여성'); return; }
      if (text.length < 10) { say(msg, '열 자 이상 적어 주십시오.'); return; }

      const 걸림 = 걸리는말(text);
      if (걸림) {
        say(msg, '‘' + 걸림 + '’ 이(가) 들어 있습니다. 의료법이 치료 효과를 단정하는 ' +
                 '말을 금하고 있으니, 그 말만 빼고 올리십시오.');
        return;
      }

      busy(btn, true, '올리는 중입니다');
      const r = await sb.from('reviews').insert({ author_name: 이름, body: text });
      busy(btn, false);

      if (r.error) { say(msg, 말로(r.error)); return; }
      who.value = '';
      body.value = '';
      if (count) count.textContent = '0';
      say(msg, '올렸습니다. 로그인한 회원에게 보입니다.', 'ok');
      목록(true);
    });
  }

  async function 후기페이지() {
    if (!gate || !area) return;
    const s = await sb.auth.getSession();
    const session = s.data.session;

    if (!session) { gate.hidden = false; area.hidden = true; return; }

    gate.hidden = true;
    area.hidden = false;

    // 원장인지 데이터베이스에 물어봅니다. 브라우저가 스스로 정하지 않습니다.
    // 여기서 거짓말을 해도 등록 단계에서 정책이 다시 막습니다.
    let 원장인가 = false;
    const a = await sb.rpc('is_author');
    if (!a.error) 원장인가 = a.data === true;

    if (원장인가) {
      const w = $('reviewWrite');
      if (w) w.hidden = false;
      후기폼();
    }
    목록(원장인가);
  }

  // ══════════════════════════════════════════════════════════
  //  로그인 · 회원가입 · 비밀번호
  // ══════════════════════════════════════════════════════════
  function 탭() {
    const tL = $('tabLogin'), tJ = $('tabJoin');
    const pL = $('paneLogin'), pJ = $('paneJoin');
    if (!tL || !tJ || !pL || !pJ) return;

    function 가자(join) {
      tL.classList.toggle('is-active', !join);
      tJ.classList.toggle('is-active', join);
      tL.setAttribute('aria-selected', String(!join));
      tJ.setAttribute('aria-selected', String(join));
      pL.hidden = join;
      pJ.hidden = !join;
    }
    tL.addEventListener('click', function () { 가자(false); });
    tJ.addEventListener('click', function () { 가자(true); });

    // 후기 페이지의 '회원가입' 단추가 #join 으로 옵니다
    if (location.hash === '#join') 가자(true);
  }

  function 로그인() {
    const form = $('loginForm');
    if (!form) return;
    const msg = $('loginMsg'), btn = $('loginSubmit');

    form.addEventListener('submit', async function (e) {
      e.preventDefault();
      clear(msg);
      const id = ($('loginId').value || '').trim().toLowerCase();
      const pw = $('loginPw').value || '';
      if (!id || !pw) { say(msg, '아이디와 비밀번호를 모두 적어 주십시오.'); return; }

      busy(btn, true, '들어가는 중입니다');
      const r = await sb.auth.signInWithPassword({ email: 가짜메일(id), password: pw });
      busy(btn, false);

      if (r.error) {
        // 아이디가 없는 것인지 비밀번호가 틀린 것인지 알려 주지 않습니다 —
        // 알려 주면 남의 아이디가 있는지 확인하는 데 쓰입니다.
        say(msg, '아이디 또는 비밀번호가 맞지 않습니다.');
        return;
      }
      location.href = 'reviews.html';
    });
  }

  // ── 중복확인 ────────────────────────────────────────────────
  // 답은 데이터베이스가 합니다(username_taken · phone_taken).
  // 있다/없다만 오므로 남의 아이디나 번호를 캐낼 수 없습니다.
  const 확인됨 = { id: '', phone: '' };   // 확인을 마친 값. 고치면 다시 받아야 합니다.

  function 쪽지(el, text, ok) {
    if (!el) return;
    el.textContent = text;
    el.className = 'field__note field__note--' + (ok ? 'ok' : 'bad');
    el.hidden = false;
  }

  function 중복확인() {
    const idInput = $('joinId'), phoneInput = $('joinPhone');

    const bId = $('checkId');
    if (bId && idInput) {
      idInput.addEventListener('input', function () {
        확인됨.id = ''; const n = $('idNote'); if (n) n.hidden = true;
      });
      bId.addEventListener('click', async function () {
        const note = $('idNote');
        const v = (idInput.value || '').trim().toLowerCase();
        idInput.value = v;
        if (!ID_규칙.test(v)) {
          쪽지(note, '영문 소문자·숫자·밑줄(_) 4~20자로 적어 주십시오.', false); return;
        }
        busy(bId, true, '확인 중');
        const r = await sb.rpc('username_taken', { p_username: v });
        busy(bId, false);
        if (r.error) { 쪽지(note, 말로(r.error), false); return; }
        if (r.data) { 쪽지(note, '이미 쓰고 있는 아이디입니다.', false); 확인됨.id = ''; return; }
        쪽지(note, '쓰실 수 있는 아이디입니다.', true);
        확인됨.id = v;
      });
    }

    const bP = $('checkPhone');
    if (bP && phoneInput) {
      // 010-1234-5678 로 저절로 벌려 줍니다
      phoneInput.addEventListener('input', function () {
        const d = 숫자만(phoneInput.value).slice(0, 11);
        phoneInput.value = d.length > 7 ? d.slice(0, 3) + '-' + d.slice(3, 7) + '-' + d.slice(7)
                         : d.length > 3 ? d.slice(0, 3) + '-' + d.slice(3)
                         : d;
        확인됨.phone = ''; const n = $('phoneNote'); if (n) n.hidden = true;
      });
      bP.addEventListener('click', async function () {
        const note = $('phoneNote');
        const d = 숫자만(phoneInput.value);
        if (!폰_규칙.test(d)) { 쪽지(note, '휴대폰 번호를 다시 확인해 주십시오.', false); return; }
        busy(bP, true, '확인 중');
        const r = await sb.rpc('phone_taken', { p_phone: d });
        busy(bP, false);
        if (r.error) { 쪽지(note, 말로(r.error), false); return; }
        if (r.data) { 쪽지(note, '이미 가입된 번호입니다. 로그인해 주십시오.', false); 확인됨.phone = ''; return; }
        쪽지(note, '쓰실 수 있는 번호입니다.', true);
        확인됨.phone = d;
      });
    }
  }

  /** 이메일 뒷자리 고르기 — 고르면 칸을 채우고 잠그고, '직접 입력' 이면 풉니다. */
  function 이메일고르기() {
    const pick = $('joinEmailPick'), tail = $('joinEmailTail');
    if (!pick || !tail) return;
    pick.addEventListener('change', function () {
      if (pick.value) { tail.value = pick.value; tail.readOnly = true; }
      else { tail.value = ''; tail.readOnly = false; tail.focus(); }
    });
  }

  function 가입() {
    const form = $('joinForm');
    if (!form) return;
    const msg = $('joinMsg'), btn = $('joinSubmit');

    form.addEventListener('submit', async function (e) {
      e.preventDefault();
      clear(msg);

      const id    = ($('joinId').value || '').trim().toLowerCase();
      const pw    = $('joinPw').value || '';
      const pw2   = $('joinPw2').value || '';
      const name  = ($('joinName').value || '').trim();
      const phone = 숫자만($('joinPhone').value);
      const birth = 생년월일($('joinBirth').value);
      const head  = ($('joinEmailHead').value || '').trim();
      const tail  = ($('joinEmailTail').value || '').trim();
      const email = head + '@' + tail;

      if (!ID_규칙.test(id)) { say(msg, '아이디는 영문 소문자·숫자·밑줄(_) 4~20자입니다.'); return; }
      if (확인됨.id !== id)  { say(msg, '아이디 중복확인을 해 주십시오.'); return; }
      if (pw.length < 8)     { say(msg, '비밀번호는 8자 이상이어야 합니다.'); return; }
      if (pw !== pw2)        { say(msg, '비밀번호가 서로 다릅니다.'); return; }
      if (name.length < 2)   { say(msg, '이름을 적어 주십시오.'); return; }
      if (!폰_규칙.test(phone))    { say(msg, '휴대폰 번호를 다시 확인해 주십시오.'); return; }
      if (확인됨.phone !== phone)  { say(msg, '휴대폰 번호 중복확인을 해 주십시오.'); return; }
      if (!birth)            { say(msg, '생년월일을 1988.10.25 처럼 적어 주십시오.'); return; }
      if (!head || !tail || tail.indexOf('.') < 0) { say(msg, '이메일 주소를 다시 확인해 주십시오.'); return; }
      const ag = $('agPrivacy');
      if (ag && !ag.checked) { say(msg, '개인정보 수집 및 이용에 동의하셔야 가입됩니다.'); return; }

      busy(btn, true, '가입하는 중입니다');

      // ① 인증 계정 — 가짜 메일로 만듭니다
      const up = await sb.auth.signUp({ email: 가짜메일(id), password: pw });
      if (up.error) { busy(btn, false); say(msg, 말로(up.error)); return; }
      if (!up.data.session) {
        busy(btn, false);
        say(msg, '가입은 됐지만 로그인되지 않았습니다. Supabase 의 메일 확인이 켜져 있는지 봐 주십시오.');
        return;
      }

      // ② 명부 — 여기서 걸리면 계정만 남으므로 되돌립니다
      const pr = await sb.from('profiles').insert({
        user_id: up.data.session.user.id,
        username: id, full_name: name, phone: phone, birth: birth, email: email,
      });
      busy(btn, false);

      if (pr.error) {
        await sb.auth.signOut();
        say(msg, '가입하지 못했습니다. ' + 말로(pr.error) + ' 계속 안 되시면 전화 주십시오.');
        return;
      }

      say(msg, '가입됐습니다. 치료 후기로 갑니다.', 'ok');
      setTimeout(function () { location.href = 'reviews.html'; }, 900);
    });
  }

  // 비밀번호 재설정 메일은 쓰지 않습니다 — 인증 주소가 가짜라 받을 수 없습니다.
  // 잊으신 분은 전화를 주시고, 원장님이 Supabase 에서 바꿔 드립니다.
  // 회원이 많아지면 그때 제대로 만들어야 합니다.

  // ── 시작 ────────────────────────────────────────────────────
  sb.auth.getSession().then(function (s) { 상단바(s.data.session); });
  sb.auth.onAuthStateChange(function (_e, session) { 상단바(session); });

  후기페이지();
  탭();
  로그인();
  가입();
  중복확인();
  이메일고르기();
})();
