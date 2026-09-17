-- ══════════════════════════════════════════════════════════════
--  정진한의원 — 치료 후기
--
--  Supabase > SQL Editor 에 통째로 붙여 넣고 한 번 실행하십시오.
--  두 번 실행해도 괜찮게 적어 두었습니다.
--
--  ── 누가 무엇을 하나 ───────────────────────────────────────
--    원장  — 후기를 올리고 지웁니다
--    회원  — 로그인하면 읽습니다. 쓰지는 못합니다
--    그 밖 — 아무것도 못 봅니다. 한 줄도 나가지 않습니다
--
--  마지막 줄이 이 파일의 이유입니다. 의료법 제56조 제2항 제2호는
--  환자의 치료경험담을 의료광고로 보아 금지하고, '불특정 다수에게
--  열려 있는가' 가 갈림길입니다. 화면에서 숨기는 것으로는 안 되고,
--  데이터베이스가 안 주어야 합니다. 아래 정책을 지우지 마십시오.
-- ══════════════════════════════════════════════════════════════

-- ── 1. 후기를 올릴 수 있는 사람 ────────────────────────────────
--    원장님 계정 하나만 들어갑니다. 등록하는 법은 아래 4번에 있습니다.
create table if not exists public.authors (
  user_id uuid primary key references auth.users(id) on delete cascade,
  added_at timestamptz not null default now()
);

alter table public.authors enable row level security;
revoke all on public.authors from anon, authenticated;

-- 지금 로그인한 사람이 원장인지 답하는 함수.
-- security definer — 회원은 authors 표를 직접 볼 수 없지만,
-- 이 함수에게 "나 원장이야?" 하고 물어볼 수는 있습니다.
create or replace function public.is_author()
returns boolean
language sql
security definer
stable
set search_path = public
as $$
  select exists (select 1 from public.authors where user_id = auth.uid());
$$;

grant execute on function public.is_author() to authenticated;
revoke execute on function public.is_author() from anon;

-- ── 2. 후기 ───────────────────────────────────────────────────
create table if not exists public.reviews (
  id          uuid primary key default gen_random_uuid(),

  -- 화면에 나오는 이름. 원장님이 직접 적으십니다.
  -- 실명 대신 '60대 · 여성' 이나 'ㄱ님' 처럼 적으십시오.
  author_name text not null check (char_length(author_name) between 1 and 20),

  body        text not null check (char_length(body) between 10 and 2000),
  created_at  timestamptz not null default now()
);

create index if not exists reviews_created_idx
  on public.reviews (created_at desc);

-- ── 3. 잠급니다 ────────────────────────────────────────────────
alter table public.reviews enable row level security;

-- 로그인하지 않은 쪽(anon)에게는 권한 자체를 거둡니다.
revoke all on public.reviews from anon;
grant select, insert, delete on public.reviews to authenticated;

-- 읽기 — 로그인한 회원이면 누구나
drop policy if exists "회원은 읽습니다" on public.reviews;
create policy "회원은 읽습니다"
  on public.reviews for select
  to authenticated
  using (true);

-- 쓰기 — 원장만
drop policy if exists "원장만 올립니다" on public.reviews;
create policy "원장만 올립니다"
  on public.reviews for insert
  to authenticated
  with check (public.is_author());

-- 지우기 — 원장만
drop policy if exists "원장만 지웁니다" on public.reviews;
create policy "원장만 지웁니다"
  on public.reviews for delete
  to authenticated
  using (public.is_author());

-- 고치기 정책은 일부러 없습니다. 고치실 일이 있으면 지우고 다시 올리십시오.

-- ── 4. 원장 계정 등록 ─────────────────────────────────────────
--
-- 홈페이지에서 원장님 이메일로 **먼저 회원가입**하신 뒤,
-- 아래 한 줄을 SQL Editor 에서 실행하십시오. 이메일만 바꾸시면 됩니다.
--
--   insert into public.authors (user_id)
--   select id from auth.users where email = '원장님이메일@example.com'
--   on conflict do nothing;
--
-- 등록됐는지 보려면:
--
--   select u.email from public.authors a join auth.users u on u.id = a.user_id;
--
-- 이걸 안 하시면 원장님 화면에도 글 쓰는 칸이 안 나옵니다.

-- ── 5. 확인 ────────────────────────────────────────────────────
-- 정책 셋이 나와야 합니다.
--
--   select policyname, cmd from pg_policies where tablename = 'reviews';
