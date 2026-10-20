# 让别人也能用 AI 助手

不要把 DeepSeek API Key 直接写进 HTML。HTML 上传到 GitHub 后，任何人都可以打开源码看到 key。

推荐用 Vercel：

1. 把这个文件夹上传到 GitHub。
2. 在 Vercel 新建项目，导入这个 GitHub 仓库。
3. 在 Vercel 的 Project Settings -> Environment Variables 里添加：
   - `DEEPSEEK_API_KEY`：你的 DeepSeek API Key
   - `DEEPSEEK_MODEL`：`deepseek-v4-flash`
   - `RATE_LIMIT_PER_MINUTE`：`30`
   - `MAX_TOKENS`：`2048`
4. 重新部署。

部署后，网页会优先访问 `/api/deepseek-chat`。访客不需要输入 key，真实 key 只存在 Vercel 后端环境变量里。

如果只用 GitHub Pages：

GitHub Pages 不能运行 `/api/deepseek-chat`，所以公共 AI 代理不会生效。页面会退回到本机浏览器保存 key 的方式，也就是每个使用者需要输入自己的 DeepSeek API Key。
