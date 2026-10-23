# CodexReset.live SEO Action Plan (Post-Audit)

## 一、本次已执行并闭环的整改项
1. [x] 生成 1200x630 规范社交卡片：site/og-image.png 就绪。
2. [x] 补齐 Twitter / Open Graph 完整标签链：修复分享卡片元数据。
3. [x] 清除未经证实的 AggregateRating 评分架构：杜绝虚构数据风险。
4. [x] 为所有图片补全尺寸与 lazy 属性：消除潜在 CLS 抖动。
5. [x] 全站 44 个 HTML 重新编译：确保多语言、合规页面与 sitemap.xml 完全同步。

## 二、正式部署上线前的最终检查清单
1. Cloudflare 域名与 DNS 绑定：验证 https://codexresetlive.com/ 的 HTTPS 证书与 HSTS 开启状态。
2. Google Search Console 提交：提交 https://codexresetlive.com/sitemap.xml 并做 URL 检查。
3. Google 富媒体结果验证：使用 Rich Results Test 确认 JSON-LD 语法零警告。
