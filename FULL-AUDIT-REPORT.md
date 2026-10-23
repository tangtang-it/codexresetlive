# CodexReset.live SEO Full Audit Report

审计日期：2026-10-23  
范围：本地首页 http://localhost:8080/、生成模板、site/ 静态产物、sitemap、robots 和 44 个 sitemap URL。  
类型：single-page full audit，补充仓库级静态检查。

## A. Audit Summary

整体评分：68/100，评分置信度：Medium。页面基础 SEO 结构完整，但结构化数据真实性、社交分享资源、合规页 hreflang 和性能测量存在明显缺口。

| 区域 | 分数 | 结论 |
|---|---:|---|
| On-page SEO | 78 | title 58 字符、description 155 字符、单一 H1；H1 语义仍不够自然 |
| Content Quality | 68 | 内容丰富，但首页同时承担雷达、教程、工具、FAQ 和广告，主题较散 |
| Technical SEO | 76 | canonical、viewport、robots、sitemap、hreflang 基础存在 |
| Structured Data | 48 | 存在未经证实的 AggregateRating，并使用商业站点不适合的 FAQPage |
| Images | 72 | 头像 alt/尺寸/lazy 较好；OG 图片缺失，二维码缺少尺寸 |
| Performance | 58 | 首页约 206KB，内联资源和第三方脚本偏重，真实 CWV 未测 |
| GEO / AI readiness | 72 | 有 llms.txt、来源链接和 methodology，但作者和证据状态仍需加强 |

Top 3 issues：

1. WebApplication JSON-LD 包含未发现证据支持的 4.9 分、342 ratings、128 reviews。
2. 商业站点首页使用 FAQPage JSON-LD，当前富结果资格受限。
3. og:image 指向 /og-image.png，但该文件不在 site/ 根目录。

Top 3 opportunities：

1. 收敛首页 H1 和摘要到 public Codex reset tracker / personal recovery timer。
2. 补全或收敛 About、Privacy、Terms、Contact 的 hreflang 策略。
3. 延迟第三方 QR/广告/分析资源，减少移动端 LCP、CLS 和主线程压力。

## B. Confirmed Findings

### 1. 虚构或不可追踪的评分数据

Severity: Warning  
Confidence: Confirmed

Evidence：site/index.html 和 scripts/build_studio.py 存在 WebApplication aggregateRating：

- ratingValue: 4.9
- ratingCount: 342
- reviewCount: 128

Impact：结构化数据必须反映真实可见内容。未经来源支持的评分会带来信任和结构化数据质量风险。

Fix：删除 aggregateRating 及相关评分数据，除非未来有真实可核验的评分来源和页面展示。

### 2. FAQPage 结构化数据受限

Severity: Warning  
Confidence: Confirmed

Evidence：首页 JSON-LD 含 @type FAQPage。

Impact：商业站点不应把 FAQPage 作为富结果策略，且会增加动态 FAQ 与 JSON-LD 同步负担。

Fix：删除 FAQPage JSON-LD，保留可见 FAQ 内容；保留 WebApplication、WebSite、Organization 和 BreadcrumbList。

### 3. OG 图片目标不存在

Severity: Warning  
Confidence: Confirmed

Evidence：

meta property=og:image 指向 https://codexresetlive.com/og-image.png；静态检查未找到 site/og-image.png。

Impact：社交分享可能无法生成预览。

Fix：创建真实的 A 风格 OG 图片或改为已存在图片，并添加 og:image:width、og:image:height、og:image:alt。

### 4. Twitter Card 字段不完整

Severity: Warning  
Confidence: Confirmed

Evidence：当前只有 twitter:creator 和 twitter:card，没有 twitter:title、twitter:description、twitter:image。

Impact：部分社交客户端无法稳定读取分享标题和摘要。

Fix：补齐 Twitter Card 字段，并与 OG 字段保持一致。

### 5. 合规页 hreflang 不完整

Severity: Warning  
Confidence: Confirmed

Evidence：About、Privacy、Terms、Contact 每页只有 x-default 和 en；首页和主要功能页有 10 个语言版本。

Impact：语言选择信号不一致。

Fix：要么人工创建完整语言版本，要么明确合规页只提供英文，不制造错误的语言互链。

### 6. 首页 H1 语义不自然

Severity: Warning  
Confidence: Confirmed

Evidence：首页 H1 是 Will CodexReset Today?。

Impact：用户搜索意图更接近 Codex rate limit reset，而不是 CodexReset 品牌词拼接。

Fix：建议使用 Did Codex Reset Today?，品牌名放在 title、logo 和 description。

### 7. 首页内容主题过宽

Severity: Warning  
Confidence: Likely

Evidence：首页同时包含实时状态、预测、历史、个人计时器、替代工具、FAQ、来源矩阵和赞助内容。

Impact：主题焦点分散，首屏 HTML 和维护成本较高。

Fix：首页聚焦当前状态、最近来源、下一次信号和个人计时器；详细方法论、历史、指南和替代工具通过内部链接承接。

### 8. 性能潜在风险

Severity: Warning  
Confidence: Likely

Evidence：

- 首页约 206KB，多个语言首页和 reset-today 页面超过 200KB。
- 首屏加载 Monetag、Google Analytics、Google Fonts。
- 分享二维码来自第三方 QR Server。
- 真实 LCP、INP、CLS 未测得。

Impact：可能影响移动端 LCP、CLS 和主线程响应。

Fix：延迟 QR 图片和非首屏脚本，给广告/图片预留尺寸，评估拆分重复内联 CSS/JS，并在生产域名测量真实 CWV。

### 9. QR 图片缺少尺寸

Severity: Warning  
Confidence: Confirmed

Evidence：share-wechat-qr 有 alt，但没有 width、height、loading。

Impact：弹窗加载时可能造成布局变化。

Fix：添加 width=140、height=140、loading=lazy，或只在打开分享弹窗后加载。

### 10. E-E-A-T 仍有提升空间

Severity: Warning  
Confidence: Likely

Evidence：已有 About、Privacy、Terms、Contact、Methodology 和公开来源，但 JSON-LD 组织名称仍是泛化的 CodexReset Radar Team；本站维护者与 Tibo 数据来源没有完全区分。

Impact：实时事件和预测工具需要清楚说明谁维护、如何审核、来源等级是什么。

Fix：About/Methodology 增加维护主体、审核规则、模型版本、Last reviewed 和修订记录。

### 11. Crawlability 基础通过

Severity: Pass  
Confidence: Confirmed

Evidence：

- canonical 存在且首页自引用。
- viewport 存在。
- 首页只有一个 H1。
- sitemap 有 44 个 URL。
- robots.txt 存在并声明 sitemap。
- 主要功能页存在 hreflang。
- scripts/verify_site.py 已通过 44 个 HTML 页面。

## C. Static Evidence

- title length：58。
- meta description length：155。
- homepage H1 count：1。
- sitemap loc count：44。
- homepage static parser word count：2139，包含 UI/FAQ/导航文本，不等同于纯正文。
- readability script：Flesch 20.9，grade 13.4；由于页面包含大量 UI 和技术术语，作为低置信度内容信号。
- 本地头像均有 alt、width、height 和 lazy。
- site/og-image.png 不存在。
- 页面 JSON-LD 类型：Organization、WebSite、WebApplication、BreadcrumbList、FAQPage。

## D. Environment Limitations

SEO 脚本的安全策略阻止直接抓取 localhost/127.0.0.1，所以 fetch_page、robots、broken-links、security-headers、redirect 和 internal-links 未能获得真实 HTTP 响应。PageSpeed API 不能测量 localhost，并返回 rate limit。生产状态码、Content-Type、Cloudflare headers、外链状态和真实 CWV 需要部署后复核，未将它们误判为线上 Confirmed 问题。

## E. Score Derivation

Positive signals：

- title/description 长度合适。
- 单一 H1、canonical、viewport 存在。
- 图片 alt 和尺寸基础较好。
- sitemap、robots、hreflang、llms.txt、methodology 和合规页存在。

Deficit signals：

- AggregateRating 无证据来源。
- FAQPage 对商业站点受限。
- OG 图片缺失。
- Twitter Card 不完整。
- 合规页 hreflang 不完整。
- 首页 HTML/第三方脚本偏重，真实 CWV 未确认。

评分：68/100。优势是基础结构完整，主要扣分来自结构化数据真实性、社交资源、国际 SEO 和性能未知项。