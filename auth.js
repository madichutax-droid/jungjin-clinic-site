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

  // ── 후기 목록 ───────────────────────────────────────────────
  // 받아 온 글을 여기 담아 두고, 분류·검색·페이지는 이 배열 위에서 거릅니다.
  // 회원은 어차피 전부 읽을 수 있으므로 매번 다시 물어볼 이유가 없습니다.
  const 창고 = { 전부: [], 분류: '', 검색: '', 쪽: 1, 원장: false, 회원: false };
  const 한쪽 = 10;

  /** 사진 주소. 공개 창고라 로그인 없이도 열립니다. */
  function 사진주소(이름) {
    if (!이름) return '';
    return CFG.url + '/storage/v1/object/public/reviews/' + 이름;
  }

  function 제목(r) {
    return r.category + ', ' + r.age + '세, ' + r.sex + ', ' + r.who;
  }

  /** 카드 하나. 글은 전부 textContent 로만 넣습니다 —
   *  innerHTML 로 넣으면 후기 칸이 그대로 스크립트 주입 통로가 됩니다.
   *
   *  로그인하지 않은 분께는 제목만 보이고, 누르면 로그인 화면으로 갑니다.
   *  본문은 화면에서 숨기는 것이 아니라 **아예 받아 오지 않습니다** —
   *  reviews_public 통로에 body 칸이 없습니다. */
  function 카드(row) {
    const li = document.createElement('li');
    li.className = 'rv';

    const head = document.createElement(창고.회원 ? 'button' : 'a');
    head.className = 'rv__head';
    if (창고.회원) {
      head.type = 'button';
      head.setAttribute('aria-expanded', 'false');
    } else {
      head.href = 'login.html';
      li.classList.add('rv--locked');
    }

    if (row.photo) {
      const shot = document.createElement('img');
      shot.className = 'rv__shot';
      shot.src = 사진주소(row.photo);
      shot.alt = '';                       // 제목이 바로 옆에 있어 읽어 줄 필요가 없습니다
      shot.loading = 'lazy';
      shot.decoding = 'async';
      head.appendChild(shot);
      li.classList.add('rv--shot');
    }

    const cat = document.createElement('span');
    cat.className = 'rv__cat';
    cat.textContent = row.category;
    head.appendChild(cat);

    const t = document.createElement('span');
    t.className = 'rv__title';
    t.textContent = 제목(row);
    head.appendChild(t);

    const when = document.createElement('time');
    when.className = 'rv__when';
    when.dateTime = row.created_at;
    when.textContent = 날짜(row.created_at);
    head.appendChild(when);

    li.appendChild(head);

    if (!창고.회원) return li;      // 본문도 지우기도 없습니다

    const body = document.createElement('div');
    body.className = 'rv__body';
    body.hidden = true;
    const p = document.createElement('p');
    p.textContent = row.body;
    body.appendChild(p);

    if (창고.원장) {
      const fix = document.createElement('button');
      fix.type = 'button';
      fix.className = 'linklike rv__fix';
      fix.textContent = '고치기';
      fix.addEventListener('click', function () { 고치기시작(row); });
      body.appendChild(fix);

      const del = document.createElement('button');
      del.type = 'button';
      del.className = 'linklike rv__del';
      del.textContent = '지우기';
      del.addEventListener('click', async function () {
        if (!window.confirm('이 글을 지웁니다. 되돌릴 수 없습니다.')) return;
        const r = await sb.from('reviews').delete().eq('id', row.id);
        if (r.error) { window.alert(말로(r.error)); return; }
        // 글을 지우면 사진도 함께 지웁니다. 남겨 두면 주소를 아는 사람에게
        // 계속 보입니다 — 환자분이 내려 달라고 하셨을 때 이것이 남으면 안 됩니다.
        if (row.photo) await sb.storage.from('reviews').remove([row.photo]);
        목록();
      });
      body.appendChild(del);
    }
    li.appendChild(body);

    head.addEventListener('click', function () {
      const 열림 = !body.hidden;
      body.hidden = 열림;
      head.setAttribute('aria-expanded', String(!열림));
      li.classList.toggle('is-open', !열림);
    });
    return li;
  }

  /** 지금 조건에 맞는 글만. */
  function 거른것() {
    const q = 창고.검색.trim().toLowerCase();
    return 창고.전부.filter(function (r) {
      if (창고.분류 && r.category !== 창고.분류) return false;
      if (!q) return true;
      const 밭 = 제목(r) + (창고.회원 && r.body ? ' ' + r.body : '');
      return 밭.toLowerCase().indexOf(q) >= 0;
    });
  }

  function 쪽번호(총쪽) {
    const nav = $('reviewPager');
    if (!nav) return;
    nav.textContent = '';
    if (총쪽 <= 1) { nav.hidden = true; return; }
    nav.hidden = false;

    function 단추(라벨, 쪽, 지금) {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'rv-page' + (지금 ? ' is-active' : '');
      b.textContent = 라벨;
      if (지금) b.setAttribute('aria-current', 'page');
      b.addEventListener('click', function () {
        창고.쪽 = 쪽;
        그리기();
        const t = $('reviewList');
        if (t) t.scrollIntoView({ block: 'start', behavior: 'smooth' });
      });
      return b;
    }
    if (창고.쪽 > 1) nav.appendChild(단추('‹', 창고.쪽 - 1, false));
    for (let i = 1; i <= 총쪽; i++) nav.appendChild(단추(String(i), i, i === 창고.쪽));
    if (창고.쪽 < 총쪽) nav.appendChild(단추('›', 창고.쪽 + 1, false));
  }

  function 그리기() {
    const list = $('reviewList'), state = $('reviewState');
    if (!list) return;

    const 것들 = 거른것();
    const 총쪽 = Math.max(1, Math.ceil(것들.length / 한쪽));
    if (창고.쪽 > 총쪽) 창고.쪽 = 총쪽;

    list.textContent = '';
    if (!것들.length) {
      if (state) {
        state.textContent = 창고.검색 ? '찾으시는 글이 없습니다.' : '아직 올라온 글이 없습니다.';
        state.hidden = false;
      }
      쪽번호(1);
      return;
    }
    if (state) state.hidden = true;

    const 처음 = (창고.쪽 - 1) * 한쪽;
    것들.slice(처음, 처음 + 한쪽).forEach(function (r) { list.appendChild(카드(r)); });
    쪽번호(총쪽);
  }

  /** 글이 하나도 없는 분류는 탭에서 감춥니다 — 눌러도 빈 화면만 나오니까요. */
  function 탭정리() {
    const box = $('reviewTabs');
    if (!box) return;
    const 있는분류 = {};
    창고.전부.forEach(function (r) { 있는분류[r.category] = 1; });
    const tabs = box.querySelectorAll('.rv-tab');
    for (let i = 0; i < tabs.length; i++) {
      const c = tabs[i].dataset.cat;
      tabs[i].hidden = c ? !있는분류[c] : false;
    }
  }

  async function 목록() {
    const state = $('reviewState');
    // 회원은 본문까지, 그 밖은 목록만. 통로 자체가 다릅니다 —
    // reviews_public 에는 body 칸이 없어서 새어 나갈 수가 없습니다.
    const r = 창고.회원
      ? await sb.from('reviews')
          .select('id, category, age, sex, who, photo, body, created_at')
          .order('created_at', { ascending: false }).limit(500)
      : await sb.from('reviews_public')
          .select('id, category, age, sex, who, photo, created_at')
          .order('created_at', { ascending: false }).limit(500);

    if (r.error) {
      if (state) { state.textContent = 말로(r.error); state.hidden = false; }
      return;
    }
    창고.전부 = r.data || [];
    탭정리();
    그리기();
  }

  /** 분류 탭과 검색칸. */
  function 거르기단추() {
    const box = $('reviewTabs');
    if (box) {
      box.addEventListener('click', function (e) {
        const b = e.target.closest('.rv-tab');
        if (!b) return;
        const tabs = box.querySelectorAll('.rv-tab');
        for (let i = 0; i < tabs.length; i++) {
          tabs[i].classList.toggle('is-active', tabs[i] === b);
          tabs[i].setAttribute('aria-selected', String(tabs[i] === b));
        }
        창고.분류 = b.dataset.cat || '';
        창고.쪽 = 1;
        그리기();
      });
    }
    const q = $('reviewSearch');
    if (q) {
      let 시계 = null;
      q.addEventListener('input', function () {
        // 한 글자마다 다시 그리면 목록이 깜빡입니다. 잠깐 기다렸다 그립니다.
        clearTimeout(시계);
        시계 = setTimeout(function () {
          창고.검색 = q.value || '';
          창고.쪽 = 1;
          그리기();
        }, 200);
      });
    }
  }

  // ── 사진 고르기와 얼굴 가리기 ────────────────────────────────
  //
  // 환자 얼굴이 담기는 사진이고, 로그인하지 않은 분께도 보입니다.
  // 올리기 전에 얼굴을 가릴 수 있게 해 두었습니다. 가린 자국은 그림 자체에
  // 찍혀 나갑니다 — 화면에서 덮는 것이 아니라 원본을 바꿔서 올립니다.
  // 그래서 나중에 벗겨낼 수 없습니다. 그게 맞습니다.
  const 사진 = { canvas: null, ctx: null, 되돌리기: [], 있음: false, 뺌: false };
  // 고치는 중이면 { id, photo }. 아니면 null.
  let 편집 = null;
  const 최대폭 = 1400;
  const 붓 = 34;          // 문지르는 붓의 굵기
  const 알갱이 = 14;      // 모자이크 알갱이 크기

  function 모자이크(x, y, r) {
    const c = 사진.canvas, ctx = 사진.ctx;
    const x0 = Math.max(0, Math.round(x - r)), y0 = Math.max(0, Math.round(y - r));
    const w = Math.min(c.width - x0, Math.round(r * 2));
    const h = Math.min(c.height - y0, Math.round(r * 2));
    if (w <= 0 || h <= 0) return;

    const 작게 = document.createElement('canvas');
    작게.width = Math.max(1, Math.round(w / 알갱이));
    작게.height = Math.max(1, Math.round(h / 알갱이));
    작게.getContext('2d').drawImage(c, x0, y0, w, h, 0, 0, 작게.width, 작게.height);

    ctx.save();
    ctx.imageSmoothingEnabled = false;      // 뭉개져야 알갱이가 보입니다
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.clip();
    ctx.drawImage(작게, 0, 0, 작게.width, 작게.height, x0, y0, w, h);
    ctx.restore();
  }

  function 사진붙이기() {
    const 고르기 = $('reviewPhoto'), box = $('shotBox'), c = $('shotCanvas');
    if (!고르기 || !box || !c) return;

    사진.canvas = c;
    사진.ctx = c.getContext('2d', { willReadFrequently: true });

    고르기.addEventListener('change', function () {
      const f = 고르기.files && 고르기.files[0];
      if (!f) { box.hidden = true; 사진.있음 = false; return; }

      const url = URL.createObjectURL(f);
      const img = new Image();
      img.onload = function () {
        // 큰 사진을 그대로 올리면 휴대폰에서 느립니다. 긴 변을 1400px 으로 줄입니다.
        const 배 = Math.min(1, 최대폭 / Math.max(img.width, img.height));
        c.width = Math.round(img.width * 배);
        c.height = Math.round(img.height * 배);
        사진.ctx.drawImage(img, 0, 0, c.width, c.height);
        사진.되돌리기 = [사진.ctx.getImageData(0, 0, c.width, c.height)];
        사진.있음 = true;
        box.hidden = false;
        URL.revokeObjectURL(url);
      };
      img.onerror = function () {
        URL.revokeObjectURL(url);
        window.alert('사진을 읽지 못했습니다. 다른 파일로 해 보십시오.');
      };
      img.src = url;
    });

    // 문지르면 가려집니다
    let 칠하는중 = false;
    function 자리(e) {
      const r = c.getBoundingClientRect();
      const t = e.touches ? e.touches[0] : e;
      return { x: (t.clientX - r.left) * (c.width / r.width),
               y: (t.clientY - r.top) * (c.height / r.height) };
    }
    function 시작(e) {
      if (!사진.있음) return;
      e.preventDefault();
      // 한 번 칠하기 시작할 때만 담아 둡니다 — 획마다 되돌아갑니다
      사진.되돌리기.push(사진.ctx.getImageData(0, 0, c.width, c.height));
      if (사진.되돌리기.length > 12) 사진.되돌리기.shift();
      칠하는중 = true;
      const p = 자리(e); 모자이크(p.x, p.y, 붓);
    }
    function 이동(e) {
      if (!칠하는중) return;
      e.preventDefault();
      const p = 자리(e); 모자이크(p.x, p.y, 붓);
    }
    function 끝() { 칠하는중 = false; }

    c.addEventListener('mousedown', 시작);
    c.addEventListener('mousemove', 이동);
    window.addEventListener('mouseup', 끝);
    c.addEventListener('touchstart', 시작, { passive: false });
    c.addEventListener('touchmove', 이동, { passive: false });
    c.addEventListener('touchend', 끝);

    const undo = $('shotUndo');
    if (undo) undo.addEventListener('click', function () {
      if (사진.되돌리기.length < 2) return;
      const 앞 = 사진.되돌리기.pop();
      사진.ctx.putImageData(앞, 0, 0);
    });

    const clear = $('shotClear');
    if (clear) clear.addEventListener('click', function () {
      고르기.value = '';
      box.hidden = true;
      사진.있음 = false;
      사진.되돌리기 = [];
    });

    // 고치는 중에 '이미 붙어 있는 사진' 을 떼는 단추
    const drop = $('shotDrop');
    if (drop) drop.addEventListener('click', function () {
      사진.뺌 = true;
      const cur = $('shotCurrent');
      if (cur) cur.hidden = true;
    });
  }

  /** 글쓰기 칸을 비우고 '올리기' 상태로 되돌립니다. */
  function 폼비우기() {
    편집 = null;
    사진.뺌 = false;
    사진.있음 = false;
    사진.되돌리기 = [];

    const cat = $('reviewCat'), age = $('reviewAge'), sex = $('reviewSex');
    const who = $('reviewWho'), body = $('reviewBody');
    if (cat) cat.value = '';
    if (age) age.value = '';
    if (sex) sex.value = '여';
    if (who) who.value = '';
    if (body) body.value = '';
    const count = $('reviewCount'); if (count) count.textContent = '0';

    const 고르기 = $('reviewPhoto'); if (고르기) 고르기.value = '';
    const box = $('shotBox'); if (box) box.hidden = true;
    const cur = $('shotCurrent'); if (cur) cur.hidden = true;

    const title = $('writeTitle'); if (title) title.textContent = '후기 올리기';
    const btn = $('reviewSubmit'); if (btn) btn.textContent = '올리기';
    const cancel = $('reviewCancel'); if (cancel) cancel.hidden = true;
    clear($('reviewMsg'));

    const prev = $('titlePreview');
    if (prev) prev.textContent = '척추관협착증, 66세, 여, 차OO님';
  }

  /** 카드의 '고치기' 를 누르면 글쓰기 칸으로 끌어올립니다. */
  function 고치기시작(row) {
    const write = $('reviewWrite');
    if (!write || write.hidden) return;

    편집 = { id: row.id, photo: row.photo || null };
    사진.뺌 = false;
    사진.있음 = false;
    사진.되돌리기 = [];

    $('reviewCat').value = row.category;
    $('reviewAge').value = row.age;
    $('reviewSex').value = row.sex;
    $('reviewWho').value = row.who;
    $('reviewBody').value = row.body;
    const count = $('reviewCount');
    if (count) count.textContent = String((row.body || '').length);

    // 붙어 있던 사진은 그림판에 올리지 않고 그대로 보여 주기만 합니다.
    // 남의 서버에서 온 그림을 그림판에 올리면 내보내기가 막힙니다.
    // 얼굴을 더 가리셔야 하면 새 파일로 다시 올리시는 편이 확실합니다.
    const 고르기 = $('reviewPhoto'); if (고르기) 고르기.value = '';
    const box = $('shotBox'); if (box) box.hidden = true;
    const cur = $('shotCurrent'), curImg = $('shotCurrentImg');
    if (cur && curImg) {
      if (row.photo) { curImg.src = 사진주소(row.photo); cur.hidden = false; }
      else cur.hidden = true;
    }

    $('writeTitle').textContent = '후기 고치기';
    $('reviewSubmit').textContent = '고쳐서 올리기';
    const cancel = $('reviewCancel'); if (cancel) cancel.hidden = false;
    clear($('reviewMsg'));

    const prev = $('titlePreview');
    if (prev) prev.textContent = 제목(row);

    write.scrollIntoView({ block: 'start', behavior: 'smooth' });
  }

  /** 칠한 자국이 찍힌 그림을 파일로. 사진이 없으면 null. */
  function 사진파일() {
    return new Promise(function (res) {
      if (!사진.있음 || !사진.canvas) { res(null); return; }
      사진.canvas.toBlob(function (b) { res(b); }, 'image/jpeg', 0.82);
    });
  }

  /** 원장 화면에만 열리는 글쓰기 칸. */
  function 후기폼() {
    const form = $('reviewForm');
    if (!form) return;
    const cat = $('reviewCat'), age = $('reviewAge'), sex = $('reviewSex'), who = $('reviewWho');
    const body = $('reviewBody'), msg = $('reviewMsg'), btn = $('reviewSubmit');
    const count = $('reviewCount'), prev = $('titlePreview');

    function 미리보기() {
      if (!prev) return;
      prev.textContent = (cat.value || '분류') + ', ' + (age.value || '00') + '세, '
                       + sex.value + ', ' + (who.value || '차OO님');
    }
    [cat, age, sex, who].forEach(function (el) {
      if (el) el.addEventListener('input', 미리보기);
      if (el) el.addEventListener('change', 미리보기);
    });

    if (body && count) {
      body.addEventListener('input', function () {
        count.textContent = String(body.value.length);
      });
    }

    const cancel = $('reviewCancel');
    if (cancel) cancel.addEventListener('click', function () {
      폼비우기();
      const list = $('reviewList');
      if (list) list.scrollIntoView({ block: 'start', behavior: 'smooth' });
    });

    form.addEventListener('submit', async function (e) {
      e.preventDefault();
      clear(msg);

      const c = cat.value;
      const a = parseInt(age.value, 10);
      const x = sex.value;
      const w = (who.value || '').trim();
      const t = (body.value || '').trim();

      if (!c) { say(msg, '분류를 고르십시오.'); return; }
      if (!a || a < 1 || a > 120) { say(msg, '나이를 적어 주십시오.'); return; }
      if (!w) { say(msg, '성함 표기를 적어 주십시오. 예: 차OO님'); return; }
      if (t.length < 10) { say(msg, '내용을 열 자 이상 적어 주십시오.'); return; }

      const 걸림 = 걸리는말(t + ' ' + w);
      if (걸림) {
        say(msg, '‘' + 걸림 + '’ 이(가) 들어 있습니다. 의료법이 치료 효과를 단정하는 ' +
                 '말을 금하고 있으니, 그 말만 빼고 올리십시오.');
        return;
      }

      const 고치는중 = !!편집;
      busy(btn, true, 고치는중 ? '고치는 중입니다' : '올리는 중입니다');

      // 사진부터 정리합니다. 새 파일을 고르셨으면 그것을 올리고,
      // '사진 빼기' 를 누르셨으면 떼고, 아무것도 안 하셨으면 그대로 둡니다.
      let 파일이름 = 고치는중 ? 편집.photo : null;
      const 옛사진 = 고치는중 ? 편집.photo : null;

      const blob = await 사진파일();
      if (blob) {
        파일이름 = (Date.now().toString(36) + Math.random().toString(36).slice(2, 8)) + '.jpg';
        const up = await sb.storage.from('reviews')
          .upload(파일이름, blob, { contentType: 'image/jpeg', cacheControl: '31536000' });
        if (up.error) {
          busy(btn, false);
          say(msg, '사진을 올리지 못했습니다. ' + 말로(up.error));
          return;
        }
      } else if (사진.뺌) {
        파일이름 = null;
      }

      const 값 = { category: c, age: a, sex: x, who: w, body: t, photo: 파일이름 };
      const r = 고치는중
        ? await sb.from('reviews').update(값).eq('id', 편집.id)
        : await sb.from('reviews').insert(값);
      busy(btn, false);

      if (r.error) {
        // 저장이 안 됐으면 방금 올린 사진은 거둡니다
        if (blob && 파일이름) await sb.storage.from('reviews').remove([파일이름]);
        say(msg, 말로(r.error));
        return;
      }

      // 저장이 끝났으니 더 이상 쓰지 않는 옛 사진을 지웁니다.
      // 남겨 두면 주소를 아는 사람에게 계속 보입니다.
      if (옛사진 && 옛사진 !== 파일이름) {
        await sb.storage.from('reviews').remove([옛사진]);
      }

      폼비우기();
      say(msg, 고치는중 ? '고쳤습니다.' : '올렸습니다. 로그인한 회원에게 보입니다.', 'ok');
      목록();
    });
  }

  async function 후기페이지() {
    if (!$('reviewList')) return;      // 후기 페이지가 아니면 아무것도 하지 않습니다

    const s = await sb.auth.getSession();
    const session = s.data.session;
    창고.회원 = !!session;

    if (창고.회원) {
      // 원장인지 데이터베이스에 물어봅니다. 브라우저가 스스로 정하지 않습니다.
      // 여기서 거짓말을 해도 등록 단계에서 정책이 다시 막습니다.
      const a = await sb.rpc('is_author');
      창고.원장 = (!a.error && a.data === true);
      if (창고.원장) {
        const w = $('reviewWrite');
        if (w) w.hidden = false;
        후기폼();
        사진붙이기();
      }
    }
    거르기단추();
    목록();
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
