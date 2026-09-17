-- ══════════════════════════════════════════════════════════════
--  정진한의원 — 회원과 치료 후기
--
--  Supabase > SQL Editor 에 통째로 붙여 넣고 실행하십시오.
--  여러 번 실행해도 괜찮게 적어 두었습니다.
--
--  ── 누가 무엇을 하나 ───────────────────────────────────────
--    원장  — 후기를 올리고 지웁니다. 회원 명부를 봅니다
--    회원  — 로그인하면 후기를 읽습니다. 쓰지는 못합니다
--    그 밖 — 아무것도 못 봅니다. 한 줄도 나가지 않습니다
--
--  마지막 줄이 이 파일의 이유입니다. 의료법 제56조 제2항 제2호는
--  환자의 치료경험담을 의료광고로 보아 금지하고, '불특정 다수에게
--  열려 있는가' 가 갈림길입니다. 정책을 지우지 마십시오.
--
--  ── 아이디 로그인에 대하여 ─────────────────────────────────
--  Supabase 는 이메일로만 로그인합니다. 아이디를 쓰기 위해
--  `아이디@u.jungjinhani.com` 이라는 가짜 주소를 만들어 인증에 씁니다.
--  진짜 이메일은 profiles.email 에 따로 담습니다.
--
--  그래서 **메일 확인(Confirm email)을 반드시 꺼야 합니다.**
--  켜 두면 가짜 주소로 확인 메일이 가고, 아무도 가입을 끝내지 못합니다.
--  Authentication > Sign In / Providers > Email > Confirm email = OFF
-- ══════════════════════════════════════════════════════════════

-- ── 1. 후기를 올릴 수 있는 사람 ────────────────────────────────
create table if not exists public.authors (
  user_id  uuid primary key references auth.users(id) on delete cascade,
  added_at timestamptz not null default now()
);

alter table public.authors enable row level security;
revoke all on public.authors from anon, authenticated;

create or replace function public.is_author()
returns boolean
language sql security definer stable
set search_path = public
as $$
  select exists (select 1 from public.authors where user_id = auth.uid());
$$;

grant execute on function public.is_author() to authenticated;
revoke execute on function public.is_author() from anon;

-- ── 2. 회원 명부 ──────────────────────────────────────────────
--    가입할 때 받은 것을 담습니다. 원장님이 환자명부와 대조하실 수
--    있도록 이름과 연락처를 받습니다. 이것이 '아무나'와 '우리 환자'를
--    가르는 자리라, 후기를 회원 전용으로 두는 근거가 됩니다.
create table if not exists public.profiles (
  user_id    uuid primary key references auth.users(id) on delete cascade,
  username   text not null unique
             check (username ~ '^[a-z0-9_]{4,20}$'),
  full_name  text not null check (char_length(full_name) between 2 and 20),
  phone      text not null unique
             check (phone ~ '^01[016789][0-9]{7,8}$'),   -- 하이픈 없이 숫자만
  birth      date not null,
  email      text not null,
  created_at timestamptz not null default now()
);

alter table public.profiles enable row level security;
revoke all on public.profiles from anon;
grant select, insert on public.profiles to authenticated;

-- 본인 것만 봅니다. 원장은 전부 봅니다(환자 대조용).
drop policy if exists "본인과 원장이 봅니다" on public.profiles;
create policy "본인과 원장이 봅니다"
  on public.profiles for select to authenticated
  using (user_id = (select auth.uid()) or public.is_author());

-- 가입할 때 본인 것 한 줄만 넣습니다.
drop policy if exists "본인 것만 넣습니다" on public.profiles;
create policy "본인 것만 넣습니다"
  on public.profiles for insert to authenticated
  with check (user_id = (select auth.uid()));

-- ── 3. 중복확인 ───────────────────────────────────────────────
--    가입 화면의 '중복확인' 단추가 부릅니다.
--    있다/없다만 답합니다 — 남의 아이디나 번호를 캐낼 수 없습니다.
--    로그인하지 않은 사람도 불러야 하므로 anon 에게도 엽니다.
create or replace function public.username_taken(p_username text)
returns boolean
language sql security definer stable
set search_path = public
as $$
  select exists (select 1 from public.profiles where username = lower(p_username));
$$;

create or replace function public.phone_taken(p_phone text)
returns boolean
language sql security definer stable
set search_path = public
as $$
  select exists (
    select 1 from public.profiles
     where phone = regexp_replace(p_phone, '[^0-9]', '', 'g'));
$$;

grant execute on function public.username_taken(text) to anon, authenticated;
grant execute on function public.phone_taken(text)    to anon, authenticated;

-- ── 4. 후기 ───────────────────────────────────────────────────
--    제목은 네 조각으로 나누어 담습니다 — 분류 · 나이 · 성별 · 성함.
--    화면에서 '척추관협착증, 66세, 여, 차OO님' 으로 합쳐 보여 줍니다.
--    자유 입력 한 칸으로 두지 않은 이유는, 실명이 들어가는 것을 막기 위해서입니다.
create table if not exists public.reviews (
  id          uuid primary key default gen_random_uuid(),
  body        text not null check (char_length(body) between 10 and 4000),
  created_at  timestamptz not null default now()
);

-- 옛 모양에서 넘어오기 — 이미 올리신 글이 있어도 지워지지 않습니다
alter table public.reviews add column if not exists category text;
alter table public.reviews add column if not exists age      integer;
alter table public.reviews add column if not exists sex      text;
alter table public.reviews add column if not exists who      text;
alter table public.reviews add column if not exists photo    text;   -- 사진 파일 이름

do $$
begin
  if exists (select 1 from information_schema.columns
              where table_schema = 'public' and table_name = 'reviews'
                and column_name = 'author_name') then
    update public.reviews
       set who = coalesce(who, nullif(author_name, ''), '환자분')
     where who is null;
    alter table public.reviews drop column author_name;
  end if;
end $$;

update public.reviews
   set category = coalesce(category, '기타'),
       age      = coalesce(age, 60),
       sex      = coalesce(sex, '여'),
       who      = coalesce(who, '환자분')
 where category is null or age is null or sex is null or who is null;

alter table public.reviews alter column category set not null;
alter table public.reviews alter column age      set not null;
alter table public.reviews alter column sex      set not null;
alter table public.reviews alter column who      set not null;

do $$
begin
  if not exists (select 1 from pg_constraint where conname = 'reviews_sex_chk') then
    alter table public.reviews add constraint reviews_sex_chk check (sex in ('남', '여'));
  end if;
  if not exists (select 1 from pg_constraint where conname = 'reviews_age_chk') then
    alter table public.reviews add constraint reviews_age_chk check (age between 1 and 120);
  end if;
  if not exists (select 1 from pg_constraint where conname = 'reviews_who_chk') then
    alter table public.reviews add constraint reviews_who_chk
      check (char_length(who) between 1 and 20);
  end if;
  if not exists (select 1 from pg_constraint where conname = 'reviews_cat_chk') then
    alter table public.reviews add constraint reviews_cat_chk
      check (char_length(category) between 1 and 30);
  end if;
end $$;

create index if not exists reviews_created_idx  on public.reviews (created_at desc);
create index if not exists reviews_category_idx on public.reviews (category);

alter table public.reviews enable row level security;
revoke all on public.reviews from anon;
grant select, insert, delete on public.reviews to authenticated;

drop policy if exists "회원은 읽습니다" on public.reviews;
create policy "회원은 읽습니다"
  on public.reviews for select to authenticated using (true);

drop policy if exists "원장만 올립니다" on public.reviews;
create policy "원장만 올립니다"
  on public.reviews for insert to authenticated
  with check (public.is_author());

drop policy if exists "원장만 지웁니다" on public.reviews;
create policy "원장만 지웁니다"
  on public.reviews for delete to authenticated
  using (public.is_author());

-- 고치기 정책은 일부러 없습니다. 지우고 다시 올리십시오.

-- ── 4-2. 목록만 내보내는 통로 ─────────────────────────────────
--
--  로그인하지 않은 분께도 **목록은** 보여 드립니다(원장님 지시, 2026-09-17).
--  제목을 누르면 로그인 화면으로 갑니다.
--
--  ★ 이 통로에 body 를 넣지 마십시오. ★
--    photo 는 일부러 넣었습니다 — 사진은 공개하기로 했습니다.
--    금지된 것은 body 하나입니다.
--  아래 select 에 적힌 칸만 밖으로 나갑니다. body 가 여기 없기 때문에
--  후기 본문은 어떤 방법으로도 비로그인에게 가지 않습니다. 정책이 아니라
--  '아예 담지 않는' 방식이라, 실수로 열릴 여지가 없습니다.
--
--  뷰는 만든 사람(postgres) 권한으로 돌아 reviews 의 잠금을 지나갑니다.
--  그래서 칸 목록이 곧 벽입니다. 한 칸도 더하지 마십시오.
create or replace view public.reviews_public as
  select id, category, age, sex, who, photo, created_at
    from public.reviews;

grant select on public.reviews_public to anon, authenticated;


-- ── 4-3. 사진 창고 ────────────────────────────────────────────
--
--  후기에 붙는 사진을 담습니다. **공개 창고입니다** — 주소를 아는 사람은
--  로그인 없이 볼 수 있습니다(2026-09-17 원장님 지시).
--
--  올리고 지우는 것은 원장만 합니다.
--
--  ※ 환자 얼굴이 담기는 곳입니다. 서면 동의를 받은 사진만 올리십시오.
--    환자분이 내려 달라고 하시면 글과 사진을 함께 지우셔야 합니다.
--    한 번 공개된 사진은 이미 퍼진 것을 거둘 수 없습니다.
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('reviews', 'reviews', true, 5242880,
        array['image/jpeg', 'image/png', 'image/webp'])
on conflict (id) do update
  set public = true,
      file_size_limit = 5242880,
      allowed_mime_types = array['image/jpeg', 'image/png', 'image/webp'];

drop policy if exists "원장만 사진을 올립니다" on storage.objects;
create policy "원장만 사진을 올립니다"
  on storage.objects for insert to authenticated
  with check (bucket_id = 'reviews' and public.is_author());

drop policy if exists "원장만 사진을 지웁니다" on storage.objects;
create policy "원장만 사진을 지웁니다"
  on storage.objects for delete to authenticated
  using (bucket_id = 'reviews' and public.is_author());

-- ── 5. 원장 계정 등록 ─────────────────────────────────────────
--
-- 홈페이지에서 원장님 아이디로 **먼저 회원가입**하신 뒤, 아래를 실행하십시오.
-- 아이디만 바꾸시면 됩니다.
--
--   insert into public.authors (user_id)
--   select user_id from public.profiles where username = '원장아이디'
--   on conflict do nothing;
--
-- 확인:
--
--   select p.username, p.full_name, (a.user_id is not null) as 글올리기권한
--     from public.profiles p
--     left join public.authors a on a.user_id = p.user_id;

-- ── 6. 확인 ───────────────────────────────────────────────────
--   select tablename, policyname, cmd from pg_policies
--    where schemaname = 'public' order by tablename;
