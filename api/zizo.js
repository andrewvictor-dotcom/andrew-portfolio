// Zizo, Andrew's AI sidekick. Runs on Vercel, answers with Google Gemini,
// limits every visitor to 5 questions a day (counted in Supabase).
// If Gemini is unavailable or out of free quota, the page falls back to
// its built-in quick-guide answers, so Zizo never breaks.
import crypto from 'node:crypto';

const SB_URL = process.env.SUPABASE_URL || 'https://cegbdtgmhgsngfrstigc.supabase.co';
const SB_KEY = process.env.SUPABASE_ANON_KEY || 'sb_publishable_Eccdsxg6cOV1P690TKmdEg_7fmbbkck';
const PER_VISITOR = 5;
const PER_DAY_TOTAL = Number(process.env.ZIZO_DAILY_TOTAL || 300);

const LIMIT_TEXT = "That's your 5 questions with me for today (Andrew's rules, not mine). Want to keep the conversation going with the real Andrew?\n\n[[book]]\n\n[[contact]]";
const BUSY_TEXT = "I've answered a lot of questions today, so I'm resting my circuits until tomorrow. You can still reach Andrew directly:\n\n[[book]]\n\n[[contact]]";

async function gate(visitor) {
  try {
    const r = await fetch(SB_URL + '/rest/v1/rpc/zizo_take', {
      method: 'POST',
      headers: { apikey: SB_KEY, Authorization: 'Bearer ' + SB_KEY, 'Content-Type': 'application/json' },
      body: JSON.stringify({ p_visitor: visitor, p_limit: PER_VISITOR, p_global: PER_DAY_TOTAL }),
    });
    if (r.ok) return await r.json();
  } catch (e) { /* if the counter is unreachable, still answer */ }
  return { allowed: true, used: 0 };
}

async function askGemini(key, model, system, contents, fit, thinking) {
  const generationConfig = { temperature: 0.6, maxOutputTokens: fit ? 1400 : 700 };
  if (!thinking) generationConfig.thinkingConfig = { thinkingBudget: 0 };
  const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'x-goog-api-key': key },
    body: JSON.stringify({ systemInstruction: { parts: [{ text: system }] }, contents, generationConfig }),
  });
  if (!r.ok) return { status: r.status };
  const j = await r.json();
  const c = j.candidates && j.candidates[0];
  const text = ((c && c.content && c.content.parts) || []).map((p) => p.text || '').join('').trim();
  return { status: 200, text, truncated: c && c.finishReason === 'MAX_TOKENS' };
}

export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' });

  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch { body = {}; } }
  const msgs = Array.isArray(body && body.messages) ? body.messages : [];
  if (msgs.length < 2 || msgs.length > 14) return res.status(400).json({ fallback: true });

  const system = String(msgs[0].content || '').slice(0, 90000);
  const contents = msgs.slice(1).map((m) => ({
    role: m.role === 'assistant' ? 'model' : 'user',
    parts: [{ text: String(m.content || '').slice(0, 12000) }],
  }));
  if (contents[contents.length - 1].role !== 'user') return res.status(400).json({ fallback: true });

  const key = process.env.GEMINI_API_KEY;
  if (!key) return res.json({ fallback: true, reason: 'no-key' });

  const ip = String(req.headers['x-forwarded-for'] || '').split(',')[0].trim() || (req.socket && req.socket.remoteAddress) || 'unknown';
  const visitor = crypto.createHash('sha256').update(ip + '|' + (process.env.ZIZO_SALT || 'andrew-portfolio')).digest('hex').slice(0, 32);
  const g = await gate(visitor);
  if (!g.allowed) return res.json({ text: g.reason === 'global' ? BUSY_TEXT : LIMIT_TEXT, limited: true });

  const models = [...new Set([process.env.GEMINI_MODEL, 'gemini-flash-latest', 'gemini-flash-lite-latest', 'gemini-2.5-flash'].filter(Boolean))];
  for (const model of models) {
    for (const thinking of [false, true]) {
      try {
        const a = await askGemini(key, model, system, contents, !!body.fit, thinking);
        if (a.status === 200 && a.text) {
          return res.json({ text: a.text, truncated: !!a.truncated, left: Math.max(0, PER_VISITOR - (g.used || 0)) });
        }
        if (a.status !== 400) break; // 400 may mean the thinking setting isn't supported: retry once with it on
      } catch (e) { break; }
    }
  }
  return res.json({ fallback: true });
}
