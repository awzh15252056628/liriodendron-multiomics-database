// For same-origin deployments such as Vercel, keep the default value.
// For GitHub Pages plus a separately deployed proxy, replace it with:
// window.LMDB_AI_PROXY_URL = 'https://your-proxy.example.com/api/deepseek-chat';
window.LMDB_AI_PROXY_URL = window.LMDB_AI_PROXY_URL || '/api/deepseek-chat';
