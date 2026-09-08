// 애니메이션 최소화를 원하는 사용자 여부
const reduceMotion =
  window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// 히어로 배경 영상.
// 주소를 HTML 이 아니라 여기서 넣습니다 — HTML 에 박아 두면 화면에서 숨겨도
// 브라우저가 미리 받아 버리기 때문입니다.
// 처음에는 원본이 5.8MB 라 좁은 화면에서 아예 막았지만, 안전 구간만 잘라
// 1MB 아래로 내려가면서 그럴 이유가 없어졌습니다(2026-09-02). 이제 휴대폰에서도 돕니다.
// '동작 줄이기' 를 켜신 분에게는 포스터 사진만 보여 줍니다.
(function () {
  const v = document.querySelector('.hero__video');
  if (!v || !v.dataset.src) return;
  if (reduceMotion) return;
  v.src = v.dataset.src;
  v.load();
  const go = function () { const p = v.play(); if (p) p.catch(function () {}); };
  if (v.readyState >= 2) go();
  else v.addEventListener('loadeddata', go, { once: true });
})();

// 모바일 메뉴 열고 닫기
const navToggle = document.getElementById('navToggle');
const nav = document.getElementById('nav');

if (navToggle && nav) {
  navToggle.setAttribute('aria-expanded', 'false');

  // 메뉴가 실제로 쓸 수 있는 높이를 계산합니다.
  // (헤더의 backdrop-filter 로 fixed 기준점이 헤더가 되므로 고정값을 쓸 수 없습니다)
  const fitNav = () => {
    const top = nav.getBoundingClientRect().top;
    nav.style.setProperty('--nav-max', Math.max(200, window.innerHeight - top) + 'px');
  };
  fitNav();
  window.addEventListener('resize', fitNav);

  navToggle.addEventListener('click', () => {
    fitNav();
    const open = nav.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', String(open));
    navToggle.setAttribute('aria-label', open ? '메뉴 닫기' : '메뉴 열기');
    // 메뉴가 열려 있는 동안 뒤쪽 페이지가 같이 밀리지 않게 잠급니다.
    document.body.style.overflow = open ? 'hidden' : '';
  });

  // 메뉴 안의 링크를 누르면 닫기 (모바일)
  nav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      nav.classList.remove('open');
      navToggle.setAttribute('aria-expanded', 'false');
      navToggle.setAttribute('aria-label', '메뉴 열기');
      document.body.style.overflow = '';
    });
  });
}

// 스크롤하면 헤더에 옅은 그림자
const header = document.getElementById('header');
if (header) {
  const onScroll = () => {
    header.style.boxShadow = window.scrollY > 10 ? '0 6px 20px rgba(38,34,32,.10)' : 'none';
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

/* ===== 스크롤에 따라 나타나기 =====
   원칙 세 가지
   1. 작게  — 14px 만 올라옵니다. 크게 밀려 들어오면 싸 보입니다.
   2. 한 번 — 나타난 뒤에는 다시 숨기지 않습니다(unobserve).
   3. 첫 화면은 건드리지 않습니다 — 히어로가 늦게 뜨면 느려 보입니다.
   숨기는 일은 자바스크립트가 합니다. 스크립트가 없으면 그냥 다 보입니다. */
if (!reduceMotion) {
  const REVEAL = [
    '.section__head', '.section__media', '.section__body',
    '.audience__bridge', '.audience__grid',
    '.svc-card', '.principle', '.reaction-card', '.program-card',
    '.doctor-brief', '.doctor-card',
    '.faq-item', '.notice-box', '.methods-band', '.voices',
    '.location__map', '.location__info', '.prep-box'
  ].join(', ');

  const fold = window.innerHeight * 0.9;
  const revealEls = [...document.querySelectorAll(REVEAL)]
    // 이미 첫 화면에 들어와 있는 것은 애니메이션 없이 바로 보여 줍니다
    .filter((el) => el.getBoundingClientRect().top > fold);

  revealEls.forEach((el) => el.classList.add('js-reveal'));

  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        // 나란히 놓인 형제끼리만 순차로 — 최대 3단계까지만 늦춥니다
        const sibs = el.parentElement
          ? [...el.parentElement.children].filter((c) => c.classList.contains('js-reveal'))
          : [];
        const step = Math.min(Math.max(sibs.indexOf(el), 0), 3);
        el.style.setProperty('--reveal-delay', step * 70 + 'ms');
        el.classList.add('js-reveal-in');
        io.unobserve(el);
      });
    },
    { threshold: 0.1, rootMargin: '0px 0px -6% 0px' }
  );
  revealEls.forEach((el) => io.observe(el));

  // 안전장치: 관찰이 어떤 이유로든 안 걸려도 3초 뒤에는 반드시 보이게 합니다
  setTimeout(() => {
    revealEls.forEach((el) => el.classList.add('js-reveal-in'));
  }, 3000);
}

/* ===== PC 버전 / 모바일 버전 전환 =====
   뷰포트 폭을 고정값으로 바꿔 모바일에서도 데스크톱 배치로 봅니다.
   선택은 localStorage 에 남아 다음 방문에도 유지됩니다. */
(function () {
  const btn = document.getElementById('viewToggle');
  if (!btn) return;

  // 실제 기기 화면이 넓으면(=진짜 PC) 버튼 자체가 필요 없습니다.
  // screen.width 는 viewport 를 바꿔도 변하지 않아 판별 기준으로 씁니다.
  if (window.screen && window.screen.width > 1024) {
    btn.hidden = true;
    return;
  }

  const meta = document.querySelector('meta[name="viewport"]');
  const read = () => { try { return localStorage.getItem('viewMode') === 'pc'; } catch (e) { return false; } };
  const paint = () => {
    const pc = read();
    btn.textContent = pc ? '모바일 버전으로 보기' : 'PC 버전으로 보기';
    btn.setAttribute('aria-pressed', String(pc));
  };
  paint();

  btn.addEventListener('click', () => {
    const next = read() ? 'mobile' : 'pc';
    try { localStorage.setItem('viewMode', next); } catch (e) {}
    meta.setAttribute('content', next === 'pc' ? 'width=1280' : 'width=device-width, initial-scale=1.0');
    paint();
    window.scrollTo(0, 0);
  });
})();
