-- Andrew Victor portfolio · Supabase setup
-- Paste all of this into Supabase → SQL Editor → New query → Run. Safe to run twice.

-- 1. Who can edit the site
create table if not exists public.owners (email text primary key);
alter table public.owners enable row level security;
insert into public.owners(email) values ('andrw.victor2@gmail.com') on conflict do nothing;

create or replace function public.is_owner() returns boolean
language sql stable security definer set search_path = public as $$
  select exists(select 1 from public.owners o where lower(o.email) = lower(coalesce(auth.jwt()->>'email','')));
$$;
revoke all on function public.is_owner() from public;
grant execute on function public.is_owner() to anon, authenticated;

-- 2. Site content ('live' is what visitors see)
create table if not exists public.site (
  id text primary key,
  data jsonb not null,
  updated_at timestamptz not null default now()
);
alter table public.site enable row level security;
drop policy if exists "site readable by everyone" on public.site;
drop policy if exists "owner inserts site" on public.site;
drop policy if exists "owner updates site" on public.site;
create policy "site readable by everyone" on public.site for select to anon, authenticated using (true);
create policy "owner inserts site" on public.site for insert to authenticated with check (public.is_owner());
create policy "owner updates site" on public.site for update to authenticated using (public.is_owner()) with check (public.is_owner());

-- 3. The last 30 published versions, so a mistake can be undone
create table if not exists public.site_history (
  id bigint generated always as identity primary key,
  data jsonb not null,
  saved_at timestamptz not null default now()
);
alter table public.site_history enable row level security;
drop policy if exists "owner reads history" on public.site_history;
create policy "owner reads history" on public.site_history for select to authenticated using (public.is_owner());
create or replace function public.site_keep_history() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  insert into public.site_history(data) values (old.data);
  delete from public.site_history where id in (select id from public.site_history order by id desc offset 30);
  return new;
end $$;
drop trigger if exists site_history_trg on public.site;
create trigger site_history_trg before update on public.site for each row execute function public.site_keep_history();

-- 4. Zizo: 5 questions per visitor per day (Cairo time), 300 per day in total
create table if not exists public.zizo_usage (
  day date not null,
  visitor text not null,
  n int not null default 0,
  primary key(day, visitor)
);
alter table public.zizo_usage enable row level security;

create or replace function public.zizo_take(p_visitor text, p_limit int default 5, p_global int default 300)
returns json language plpgsql security definer set search_path = public as $$
declare d date := (now() at time zone 'Africa/Cairo')::date; mine int; total int;
begin
  if p_visitor is null or length(p_visitor) < 8 or length(p_visitor) > 128 then
    return json_build_object('allowed', false, 'used', 0, 'reason', 'bad');
  end if;
  select n into total from public.zizo_usage where day = d and visitor = '*';
  select n into mine from public.zizo_usage where day = d and visitor = p_visitor;
  if coalesce(mine,0) >= least(p_limit, 5) then
    return json_build_object('allowed', false, 'used', coalesce(mine,0), 'reason', 'visitor');
  end if;
  if coalesce(total,0) >= least(p_global, 1000) then
    return json_build_object('allowed', false, 'used', coalesce(mine,0), 'reason', 'global');
  end if;
  insert into public.zizo_usage(day, visitor, n) values (d, p_visitor, 1)
    on conflict (day, visitor) do update set n = public.zizo_usage.n + 1;
  insert into public.zizo_usage(day, visitor, n) values (d, '*', 1)
    on conflict (day, visitor) do update set n = public.zizo_usage.n + 1;
  delete from public.zizo_usage where day < d - 7;
  return json_build_object('allowed', true, 'used', coalesce(mine,0) + 1, 'reason', 'ok');
end $$;
revoke all on function public.zizo_take(text,int,int) from public;
grant execute on function public.zizo_take(text,int,int) to anon;

-- 5. Image storage for new uploads from the editor
insert into storage.buckets (id, name, public) values ('media','media', true) on conflict (id) do nothing;
drop policy if exists "owner uploads media" on storage.objects;
drop policy if exists "owner updates media" on storage.objects;
drop policy if exists "owner deletes media" on storage.objects;
create policy "owner uploads media" on storage.objects for insert to authenticated with check (bucket_id = 'media' and public.is_owner());
create policy "owner updates media" on storage.objects for update to authenticated using (bucket_id = 'media' and public.is_owner());
create policy "owner deletes media" on storage.objects for delete to authenticated using (bucket_id = 'media' and public.is_owner());
