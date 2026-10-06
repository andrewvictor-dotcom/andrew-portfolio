# Andrew Victor · Portfolio

The live site: a single static page (`index.html`) on Vercel, with content and editing powered by Supabase and Zizo powered by Google Gemini.

## How it works

| Part | Where |
|---|---|
| Page, design, animations | `index.html` (one file, no build step) |
| Images that ship with the site | `media/` |
| New images uploaded from the editor | Supabase Storage, bucket `media` |
| Site content (text, projects, settings) | Supabase table `site`, row `live`. The page also carries a copy, so it still works if Supabase is unreachable. |
| Last 30 published versions | Supabase table `site_history` |
| Zizo (AI assistant) | `api/zizo.js` → Gemini. 5 questions per visitor per day, 300 per day in total. Falls back to built-in answers if Gemini is unavailable. |
| Database setup | `supabase/schema.sql` |

## Editing the site

1. Open the site with `?admin` at the end, e.g. `https://andrew-portfolio-lemon.vercel.app/?admin`
2. Enter your email and open the sign-in link it sends you, on the same device.
3. Click **Edit site**, make changes, then **Publish changes**. Visitors see them on their next visit.

Only emails in the Supabase `owners` table can publish.

## Settings (Vercel → Project → Settings → Environment Variables)

| Name | Required | What |
|---|---|---|
| `GEMINI_API_KEY` | yes | From Google AI Studio. Without it, Zizo uses quick-guide answers. |
| `GEMINI_MODEL` | no | Override the model, e.g. `gemini-2.5-flash` |
| `ZIZO_DAILY_TOTAL` | no | Max Zizo answers per day for everyone together (default 300) |
| `ZIZO_SALT` | no | Any random text, used to anonymise visitor IPs |

## Supabase settings

Authentication → URL Configuration → **Site URL** must be the live address (e.g. `https://andrew-portfolio-lemon.vercel.app`) so sign-in links open the site.
