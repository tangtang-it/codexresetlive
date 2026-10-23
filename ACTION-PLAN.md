# CodexReset.live SEO Action Plan

## P0：提交 AdSense 前完成

1. 删除 WebApplication JSON-LD 的 aggregateRating、ratingValue、ratingCount、reviewCount。
2. 删除首页 FAQPage JSON-LD，保留可见 FAQ。
3. 创建真实 A 风格 og-image.png，补齐 OG image 尺寸和 alt。
4. 增加 twitter:title、twitter:description、twitter:image。
5. 更新 verify_site.py，使首页不再强制要求 FAQPage。

## P1：高价值改进

1. 将首页 H1 改为 Did Codex Reset Today?，品牌词保留在 title 和 description。
2. 明确合规页 hreflang 方案：人工生成完整语言页，或保持英文单版本并避免错误互链。
3. 为 QR 图片添加 width=140、height=140、loading=lazy，并在打开分享弹窗时再加载。
4. 延迟非首屏第三方脚本和外部资源。
5. 在 About/Methodology 增加维护主体、审核规则、模型版本、Last reviewed 和修订记录。

## P2：内容与 GEO

1. 建立四篇独立指南：
   - /guides/check-codex-usage-limits/
   - /guides/codex-rate-limit-reset-explained/
   - /guides/codex-rate-limit-reached/
   - /guides/codex-reset-history/
2. 每篇使用官方来源、编辑日期、内部链接和明确限制。
3. 首页只保留当前状态、最近来源、下一次信号和个人计时器，详细内容通过内部链接承接。

## P3：生产环境验收

部署到真实域名后运行：

- robots checker
- sitemap checker
- broken links
- redirect checker
- security headers
- PageSpeed mobile/desktop
- Rich Results Test
- Search Console URL Inspection
- 移动端截图与正文可读性检查

## 推荐顺序

1. Schema 真实性修复。
2. OG/Twitter 元数据和分享图片。
3. 首页 H1/摘要。
4. hreflang 方案。
5. QR/第三方脚本和真实 CWV。
6. 原创指南和 GEO 内容扩展。