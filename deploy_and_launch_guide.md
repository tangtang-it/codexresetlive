# Codex 工具站极速上线与部署操作指南 (Cloudflare Pages + Vercel)

> **目标**：以零服务器成本（$0 运维）实现全站全球边缘加速、全量子目录与 HTTPS 部署，并在 24 小时内完成 GSC 收录冷启动。

---

## 一、 快速部署步骤 (两选一)

### 选项 A：使用 Cloudflare Pages (强烈推荐，全球高并发无限制)
1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)；
2. 导航至 **Workers & Pages** -> **Create application** -> **Pages** -> **Upload assets**；
3. 将本地目录 `outputs/site/` 中的全部文件（包含 `index.html`, `sitemap.xml`, `robots.txt`, `llms.txt` 及 `ja/`, `ko/`, `de/`, `es/` 子目录）直接拖拽上传；
4. 点击 **Deploy site**，秒级生成类似 `https://codex-reset.pages.dev` 的访问地址；
5. 在 **Custom domains** 中绑定你注册的独立域名（自动配齐免费 SSL 证书与全量 HTTP/3 支持）。

### 选项 B：使用 Vercel CLI (一键命令行上线)
在当前终端直接运行：
```bash
cd outputs/site
npx vercel --prod
```
按照命令行提示选择默认配置即可完成一键发布。

---

## 二、 收录冷启动 SOP (上线第 1 天必做清单)

1. **Google Search Console 验资与提交**：
   - 访问 [GSC 控制台](https://search.google.com/search-console) 添加域名资源；
   - 提交站点地图：`https://yourdomain.com/sitemap.xml`；
   - 针对首页 `/` 点击 **“网址检查” -> “请求编入索引”**。
2. **Bing Webmaster Tools 同步**：
   - 登录 [Bing 站长平台](https://www.bing.com/webmasters)，直接一键从 Google Search Console 导入配置。
3. **外部引蜘蛛 (外部高权重池冷启动)**：
   - 在 **V2EX**（程序员 / 分享发现节点）发布极简介绍帖，附带工具网址；
   - 在 **Reddit**（r/OpenAI, r/ChatGPTCoding, r/ClaudeAI）发帖：“*Built a tiny zero-login tool to calculate when your Codex 5-hour rolling quota resets in your local timezone.*”；
   - 蜘蛛会在 2~6 小时内顺着外链抓取并完成收录。
