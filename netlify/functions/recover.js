// ══════════════════════════════════════════════════════════════
//  아이디 찾기 · 비밀번호 재설정
//
//  2026-09-18. 그 전에는 "전화 주시면 원장이 바꿔 드립니다" 였습니다.
//
//  ── 왜 브라우저가 아니라 여기인가 ─────────────────────────────
//  명부(profiles)는 로그인한 본인과 원장만 볼 수 있습니다. 비밀번호를
//  잊은 사람은 로그인을 못 하므로 브라우저에서는 명부를 볼 수 없습니다.
//  그래서 대조는 여기 서버에서 service_role 열쇠로 합니다.
//
//  **이 열쇠는 Netlify 환경변수에만 둡니다.** 홈페이지 코드에 넣으면
//  후기가 전부 공개됩니다 — RLS 정책을 그냥 지나가는 마스터키입니다.
//    Netlify > Project configuration > Environment variables
//      SUPABASE_SERVICE_ROLE = Supabase > Settings > API Keys 의
//        Secret key (sb_secret_...) 또는 옛 service_role (eyJ...)
//
//  상태 보기 — /.netlify/functions/recover?check=1
//  열쇠가 창고를 여는지만 답합니다. 명부는 한 줄도 내보내지 않습니다.
//
//  ── 무엇으로 본인을 확인하나 ──────────────────────────────────
//  아이디 찾기      이름 · 휴대폰 · 생년월일        (셋)
//  비밀번호 재설정  + 아이디 · 이메일               (다섯)
//
//  가입할 때 적은 것과 **전부** 맞아야 합니다. 하나라도 다르면 무엇이
//  틀렸는지 알려 주지 않습니다 — 알려 주면 남의 정보를 맞춰 보는 데 쓰입니다.
//
//  메일로 링크를 보내는 방식이 더 안전합니다. 지금 구조에서는 못 합니다 —
//  아이디 로그인을 위해 인증 주소를 `아이디@u.jungjinhani.com` 이라는
//  가짜로 만들어 두어서, 메일이 갈 곳이 없습니다. 메일 보내는 곳을
//  붙이시면 그때 인증번호 단계를 이 위에 얹을 수 있습니다.
//
//  ── 원장 계정은 여기서 못 바꿉니다 ───────────────────────────
//  authors 표에 있는 계정은 거절합니다. 그 계정은 후기를 올리고 지울 수
//  있어, 이름·번호·생일을 아는 사람에게 넘어가면 피해가 다릅니다.
//  원장님 비밀번호는 Supabase 콘솔에서 바꾸십시오.
//
//  ── 같은 곳에서 계속 틀리면 ──────────────────────────────────
//  한 시간에 IP 10번 · 휴대폰 번호 5번까지입니다. 넘으면 막습니다.
//  시도는 recovery_log 에 남습니다 (휴대폰 뒤 4자리까지만).
// ══════════════════════════════════════════════════════════════

'use strict';

// 프로젝트 주소는 홈페이지 소스에도 들어 있는 공개 값입니다.
// partials.py 의 SUPABASE_URL 과 같아야 합니다. Supabase 를 옮기면 두 곳을 함께 고칩니다.
const URL_BASE = process.env.SUPABASE_URL || 'https://weutytwetagqfdqahvgd.supabase.co';
const KEY = process.env.SUPABASE_SERVICE_ROLE || '';

const 한시간 = 60 * 60 * 1000;
const IP_한도 = 10;      // 한 시간에 같은 IP 가 틀릴 수 있는 횟수
const 번호_한도 = 5;      // 한 시간에 같은 번호로 틀릴 수 있는 횟수

const ID_규칙 = /^[a-z0-9_]{4,20}$/;
const 폰_규칙 = /^01[016789][0-9]{7,8}$/;

// ── 잔손질 ────────────────────────────────────────────────────
const 숫자만 = (v) => String(v || '').replace(/[^0-9]/g, '');
const 다듬기 = (v) => String(v || '').trim().replace(/\s+/g, ' ');

/** 1988.10.25 · 19881025 · 1988-10-25 를 모두 1988-10-25 로. 못 읽으면 null. */
function 생년월일(v) {
  const d = 숫자만(v);
  if (d.length !== 8) return null;
  const y = +d.slice(0, 4), m = +d.slice(4, 6), day = +d.slice(6, 8);
  if (y < 1900 || y > new Date().getFullYear()) return null;
  if (m < 1 || m > 12 || day < 1 || day > 31) return null;
  const t = new Date(Date.UTC(y, m - 1, day));
  if (t.getUTCMonth() !== m - 1 || t.getUTCDate() !== day) return null;
  return d.slice(0, 4) + '-' + d.slice(4, 6) + '-' + d.slice(6, 8);
}

/** yangjj → yan***. 앞 세 글자만 보여 줍니다. */
function 가리기(id) {
  const s = String(id || '');
  if (s.length <= 3) return s.charAt(0) + '*'.repeat(Math.max(1, s.length - 1));
  return s.slice(0, 3) + '*'.repeat(s.length - 3);
}

const 답 = (code, obj) => ({
  statusCode: code,
  headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' },
  body: JSON.stringify(obj),
});

// ── Supabase 부르기 ───────────────────────────────────────────
function 열쇠() {
  return { apikey: KEY, Authorization: 'Bearer ' + KEY, 'Content-Type': 'application/json' };
}

async function 표(path, opts) {
  const r = await fetch(URL_BASE + path, Object.assign({ headers: 열쇠() }, opts || {}));
  const t = await r.text();
  let j = null;
  try { j = t ? JSON.parse(t) : null; } catch (e) { j = null; }
  return { ok: r.ok, status: r.status, data: j, raw: t };
}

/** 시도를 남깁니다. 실패해도 본래 흐름을 막지 않습니다 —
 *  기록 때문에 비밀번호를 못 바꾸면 곤란하니까요.
 *  다만 조용히 넘기지는 않습니다. 안 쌓이면 한도 세기가 같이 죽습니다. */
async function 기록(kind, ok, ip, phone) {
  try {
    const r = await 표('/rest/v1/recovery_log', {
      method: 'POST',
      headers: Object.assign(열쇠(), { Prefer: 'return=minimal' }),
      body: JSON.stringify({ kind, ok, ip: ip || null, hint: phone ? phone.slice(-4) : null }),
    });
    if (!r.ok) console.error('recovery_log 기록 실패', r.status, r.raw);
  } catch (e) {
    console.error('recovery_log 기록 실패(예외)', e && e.message);
  }
}

/** 한 시간 안에 틀린 횟수가 한도를 넘었는지. */
async function 너무많이틀렸나(ip, phone) {
  const 부터 = new Date(Date.now() - 한시간).toISOString();
  const 세기 = async (q) => {
    const r = await 표('/rest/v1/recovery_log?select=id&ok=is.false&at=gte.' +
                       encodeURIComponent(부터) + q + '&limit=50');
    return r.ok && Array.isArray(r.data) ? r.data.length : 0;
  };
  if (ip && (await 세기('&ip=eq.' + encodeURIComponent(ip))) >= IP_한도) return true;
  if (phone && (await 세기('&hint=eq.' + encodeURIComponent(phone.slice(-4)))) >= 번호_한도) return true;
  return false;
}

/** 휴대폰 번호로 명부 한 줄. 번호는 unique 라 0 또는 1 줄입니다.
 *
 *  **'없다' 와 '못 봤다' 를 반드시 구분합니다.** 열쇠가 거절당한 것을
 *  '맞는 회원이 없다' 로 답하면, 바르게 적은 회원이 자기가 틀린 줄 압니다.
 *  밖에서 보면 두 경우가 똑같아 고장을 알아챌 수도 없습니다(2026-09-19에 겪었습니다).
 *
 *  돌려주는 것 — { 볼수있음: true, 줄: 명부한줄|null } */
async function 명부(phone) {
  const r = await 표('/rest/v1/profiles?select=user_id,username,full_name,phone,birth,email' +
                     '&phone=eq.' + encodeURIComponent(phone) + '&limit=1');
  if (!r.ok || !Array.isArray(r.data)) {
    console.error('명부를 읽지 못했습니다', r.status, r.raw);
    return { 볼수있음: false, 줄: null };
  }
  return { 볼수있음: true, 줄: r.data.length ? r.data[0] : null };
}

async function 원장인가(user_id) {
  const r = await 표('/rest/v1/authors?select=user_id&user_id=eq.' +
                     encodeURIComponent(user_id) + '&limit=1');
  return r.ok && Array.isArray(r.data) && r.data.length > 0;
}

// ── 본체 ──────────────────────────────────────────────────────
exports.handler = async function (event) {
  // 상태 보기 — /.netlify/functions/recover?check=1
  // 열쇠가 창고를 여는지만 답합니다. 명부는 한 줄도 내보내지 않습니다
  // (limit=0 으로 물어 문이 열리는지만 봅니다).
  const q = event.queryStringParameters || {};
  if (event.httpMethod === 'GET' && q.check === '1') {
    if (!KEY) return 답(200, { ok: false, 상태: '열쇠가 없습니다 (SUPABASE_SERVICE_ROLE)' });
    // 열쇠의 '종류' 만 봅니다. 값 자체는 어떤 경우에도 내보내지 않습니다.
    const 종류 = KEY.indexOf('sb_secret_') === 0 ? 'sb_secret (맞습니다)'
               : KEY.indexOf('sb_publishable_') === 0 ? 'sb_publishable (공개 열쇠입니다 — 이게 아닙니다)'
               : KEY.indexOf('eyJ') === 0 ? '옛 JWT (service_role 또는 anon)'
               : '알 수 없는 모양';
    const 앞뒤공백 = KEY !== KEY.trim() ? '있습니다 — 붙여넣을 때 섞였습니다' : '없습니다';
    const r = await 표('/rest/v1/profiles?select=user_id&limit=1');
    const w = await 표('/rest/v1/recovery_log?select=id&limit=1');
    return 답(200, {
      ok: r.ok && w.ok,
      열쇠종류: 종류,
      앞뒤공백: 앞뒤공백,
      명부: r.ok ? '열립니다' : '거절됨 ' + r.status + ' ' + String(r.raw || '').slice(0, 200),
      기록표: w.ok ? '열립니다' : '거절됨 ' + w.status + ' ' + String(w.raw || '').slice(0, 200),
    });
  }

  if (event.httpMethod !== 'POST') return 답(405, { ok: false, message: '잘못된 요청입니다.' });
  if (!KEY) {
    console.error('SUPABASE_SERVICE_ROLE 이 없습니다 — Netlify 환경변수를 확인하십시오.');
    return 답(500, { ok: false, message: '아직 준비되지 않았습니다. 전화로 문의해 주십시오.' });
  }

  let 몸 = null;
  try { 몸 = JSON.parse(event.body || '{}'); } catch (e) { 몸 = null; }
  if (!몸 || typeof 몸 !== 'object') return 답(400, { ok: false, message: '잘못된 요청입니다.' });

  const h = event.headers || {};
  const ip = (h['x-nf-client-connection-ip'] ||
              String(h['x-forwarded-for'] || '').split(',')[0] || '').trim() || null;

  const kind = 몸.action === 'password' ? 'password' : 'id';
  const phone = 숫자만(몸.phone);
  const name = 다듬기(몸.name);
  const birth = 생년월일(몸.birth);

  // 모양부터 봅니다. 여기서 걸리는 것은 기록하지 않습니다 — 오타까지 남길 일은 아닙니다.
  if (!폰_규칙.test(phone) || name.length < 2 || !birth) {
    return 답(400, { ok: false, message: '적어 주신 내용을 다시 확인해 주십시오.' });
  }

  if (await 너무많이틀렸나(ip, phone)) {
    return 답(429, {
      ok: false,
      message: '확인 시도가 많았습니다. 한 시간 뒤에 다시 해 주시거나 전화로 문의해 주십시오.',
    });
  }

  const 조회 = await 명부(phone);
  if (!조회.볼수있음) {
    // 열쇠가 거절당했거나 창고가 답하지 않는 경우입니다. 회원 탓으로 돌리지 않습니다.
    return 답(503, { ok: false, message: '지금은 확인할 수 없습니다. 잠시 뒤 다시 해 주시거나 전화로 문의해 주십시오.' });
  }
  const 줄 = 조회.줄;
  const 맞나 = !!줄 && 다듬기(줄.full_name) === name && String(줄.birth) === birth;

  // ── 아이디 찾기 ─────────────────────────────────────────────
  if (kind === 'id') {
    await 기록('id', 맞나, ip, phone);
    if (!맞나) {
      return 답(200, { ok: false, message: '적어 주신 내용과 맞는 회원이 없습니다.' });
    }
    return 답(200, { ok: true, username: 가리기(줄.username) });
  }

  // ── 비밀번호 재설정 ─────────────────────────────────────────
  const username = String(몸.username || '').trim().toLowerCase();
  const email = String(몸.email || '').trim().toLowerCase();
  const pw = String(몸.password || '');

  if (!ID_규칙.test(username) || email.indexOf('@') < 1 || pw.length < 8) {
    return 답(400, { ok: false, message: '적어 주신 내용을 다시 확인해 주십시오.' });
  }
  if (pw === username) {
    return 답(400, { ok: false, message: '비밀번호를 아이디와 다르게 정해 주십시오.' });
  }

  const 다맞나 = 맞나 &&
    String(줄.username).toLowerCase() === username &&
    String(줄.email).trim().toLowerCase() === email;

  if (!다맞나) {
    await 기록('password', false, ip, phone);
    return 답(200, { ok: false, message: '적어 주신 내용과 맞는 회원이 없습니다.' });
  }

  if (await 원장인가(줄.user_id)) {
    await 기록('password', false, ip, phone);
    return 답(200, {
      ok: false,
      message: '이 계정은 여기에서 바꿀 수 없습니다. 원장님께 직접 문의해 주십시오.',
    });
  }

  const up = await 표('/auth/v1/admin/users/' + encodeURIComponent(줄.user_id), {
    method: 'PUT',
    body: JSON.stringify({ password: pw }),
  });

  if (!up.ok) {
    console.error('비밀번호 바꾸기 실패', up.status, up.raw);
    await 기록('password', false, ip, phone);
    return 답(500, { ok: false, message: '바꾸지 못했습니다. 잠시 뒤 다시 해 주십시오.' });
  }

  await 기록('password', true, ip, phone);
  return 답(200, { ok: true });
};
