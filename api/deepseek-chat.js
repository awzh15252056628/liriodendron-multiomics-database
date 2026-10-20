const DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions';
const DEFAULT_MODEL = 'deepseek-v4-flash';
const DEFAULT_MAX_TOKENS = 2048;
const DEFAULT_RATE_LIMIT = 30;

const buckets = new Map();

function getClientIp(req) {
  const forwarded = req.headers['x-forwarded-for'];
  if (typeof forwarded === 'string' && forwarded.trim()) {
    return forwarded.split(',')[0].trim();
  }
  return req.socket?.remoteAddress || 'unknown';
}

function checkRateLimit(ip) {
  const limit = Number(process.env.RATE_LIMIT_PER_MINUTE || DEFAULT_RATE_LIMIT);
  const now = Date.now();
  const bucket = buckets.get(ip) || { start: now, count: 0 };
  if (now - bucket.start > 60_000) {
    bucket.start = now;
    bucket.count = 0;
  }
  bucket.count += 1;
  buckets.set(ip, bucket);
  return bucket.count <= limit;
}

function setCors(req, res) {
  const origin = req.headers.origin || '';
  const allowedOrigins = (process.env.ALLOWED_ORIGIN || '')
    .split(',')
    .map(item => item.trim())
    .filter(Boolean);

  if (origin && allowedOrigins.length && allowedOrigins.includes(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
    res.setHeader('Vary', 'Origin');
  }
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
}

function normalizeBody(req) {
  if (!req.body) return {};
  if (typeof req.body === 'string') {
    try {
      return JSON.parse(req.body);
    } catch {
      return {};
    }
  }
  return req.body;
}

module.exports = async function handler(req, res) {
  setCors(req, res);

  if (req.method === 'OPTIONS') {
    res.status(204).end();
    return;
  }

  if (req.method === 'GET') {
    const ready = Boolean(process.env.DEEPSEEK_API_KEY);
    res.status(ready ? 200 : 503).json({
      status: ready ? 'ok' : 'missing_key',
      model: process.env.DEEPSEEK_MODEL || DEFAULT_MODEL
    });
    return;
  }

  if (req.method !== 'POST') {
    res.status(405).json({ error: { message: 'Method not allowed' } });
    return;
  }

  const apiKey = process.env.DEEPSEEK_API_KEY;
  if (!apiKey) {
    res.status(500).json({ error: { message: 'Server missing DEEPSEEK_API_KEY' } });
    return;
  }

  const ip = getClientIp(req);
  if (!checkRateLimit(ip)) {
    res.status(429).json({ error: { message: 'Too many requests, please try again later' } });
    return;
  }

  const body = normalizeBody(req);
  if (!Array.isArray(body.messages) || body.messages.length === 0) {
    res.status(400).json({ error: { message: 'messages is required' } });
    return;
  }

  const maxTokens = Math.min(
    Number(body.max_tokens || DEFAULT_MAX_TOKENS),
    Number(process.env.MAX_TOKENS || DEFAULT_MAX_TOKENS)
  );

  const payload = {
    model: process.env.DEEPSEEK_MODEL || body.model || DEFAULT_MODEL,
    messages: body.messages.slice(-12),
    max_tokens: maxTokens,
    temperature: Number.isFinite(Number(body.temperature)) ? Number(body.temperature) : 0.7,
    stream: false
  };

  try {
    const upstream = await fetch(DEEPSEEK_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      },
      body: JSON.stringify(payload)
    });

    const text = await upstream.text();
    res.status(upstream.status);
    res.setHeader('Content-Type', upstream.headers.get('content-type') || 'application/json');
    res.send(text);
  } catch (error) {
    res.status(502).json({ error: { message: error.message || 'DeepSeek request failed' } });
  }
};
