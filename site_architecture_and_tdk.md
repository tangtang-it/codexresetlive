# Codex 工具站站内架构、AITDK 规范与 8 维体验设计

> **方法论依据**：严格对照《哥飞出海流量与 SEO 策略大脑》中 AITDK 黄金指标、Ahrefs 级技术审查门禁与精品工具站 8 维体验评分体系。

---

## 一、 核心页面 AITDK 黄金规范 (字符像素与 SERP 转化率控制)

### 1. 首页 (主打词: `codex quota reset`)
- **URL**: `/`
- **Target Title (54 字符 / 严格 <= 60)**:
  `Codex Quota Reset Time - Live Rate Limit & Status Tracker`
  - *分析*：核心词 `Codex Quota Reset` 强力前置在前 20 字符内，后缀补齐商业价值特征词。
- **Meta Description (142 字符 / 严格 120-155)**:
  `Check when your OpenAI Codex rate limit and quota resets in your local timezone. Free instant countdown tracker with zero-latency calculation.`
  - *分析*：包含 Free, Instant, Countdown 行动动词，解决时区困惑痛点。
- **H1 (全局唯一首位 H1)**:
  `OpenAI Codex Quota & Rate Limit Reset Tracker`
- **核心组件设计**:
  - 本地时区自动探测（UTC+8 / EST / PST 动态切换）；
  - 大字号动态倒计时时钟（小时 : 分钟 : 秒）；
  - 5 小时滚动窗口进度条展示（0% ~ 100% 消耗指示）；
  - “开启桌面 WebPush 刷新提醒” 授权按钮。

---

### 2. 独立二级内页 1: 5 小时重置机制计算器
- **URL**: `/5-hour-limit/`
- **Target Title (53 字符)**:
  `Codex 5-Hour Limit Reset Calculator - Rolling Window Tool`
- **Meta Description (138 字符)**:
  `Calculate exactly when your 5-hour rolling Codex limit unlocks. Input your last prompt timestamp to see your next prompt quota window.`
- **H1**:
  `Codex 5-Hour Rolling Limit Reset Calculator`
- **核心组件**:
  - 用户输入“触发限流时间”或者“最后一次提问时间”；
  - 自动输出精确到分钟的解锁时间点。

---

### 3. 独立二级内页 2: Codex vs Claude Code 限额横评 (Affiliate 变现主力)
- **URL**: `/vs-claude-code/`
- **Target Title (55 字符)**:
  `Codex vs Claude Code Rate Limits Compared: Which Is Better?`
- **Meta Description (146 字符)**:
  `In-depth comparison of OpenAI Codex and Claude Code usage limits, token quotas, and pricing tiers. Find the best AI coding assistant for heavy daily use.`
- **H1**:
  `OpenAI Codex vs Claude Code: Rate Limits & Quota Comparison`
- **核心组件**:
  - 交互式参数横向比对表格；
  - “额度不够用时的推荐替代工具” 高单价佣金卡片（Cursor / Windsurf / Claude 官方订阅引导）。

---

## 二、 精品工具站 8 维体验评分表自测 (目标: 85+ 分 / 通过 Google 7 天优待期)

对照哥飞知识库 KP-0026 及仿真推演引擎体验模型：

| 评估维度 | 满分 | 预估得分 | 落地实现要点 |
| :--- | :---: | :---: | :--- |
| **1. 工具直接集成** | 25 | **25** | 首屏直接展示倒计时与计算器，**严禁二次跳转新页面**。 |
| **2. 免登录直接可用** | 20 | **20** | 打开网页直接计算，无弹窗强制登录拦路，跳出率降至最低。 |
| **3. 免登录免费额度** | 10 | **10** | 纯前端逻辑运行，无 API 消耗成本，永久 100% 免费使用。 |
| **4. 结果与样例展示** | 15 | **12** | 默认载入“当前时区常用账号（Plus / Team）”推荐样例。 |
| **5. 移动端深度适配** | 10 | **10** | Tailwind 响应式布局，手机端大按钮与自适应时钟。 |
| **6. 秒级快速加载** | 10 | **10** | 纯静态单页架构（无重依赖），首屏渲染时间 (FCP) < 0.6s。 |
| **7. 登录送积分/增值功能** | 5 | **0** | (MVP 阶段暂不做复杂登录，保持纯粹)。 |
| **8. 每日签到/持续留存** | 5 | **3** | 提供“重置提醒（Web Push）”与“加入浏览器书签”引导。 |
| **总计预估评分** | **100** | **90 分 (优秀)** | 顺利激活 Google 上线后试探性优待期 (Grace Period)，大幅降低对外链数量的依赖。 |

---

## 三、 多语言全球捕捞子目录矩阵 (Hreflang 双向闭环)

按照哥飞全球捕捞法则，绝不使用二级子域名，全部采用**单域名独立子目录**：

- `/`：英语 (x-default / en)
- `/ja/`：日语（日本开发者集中，搜索量高，KD < 10）
- `/ko/`：韩语（韩国开发者，社区热度大）
- `/de/`：德语（欧洲高单价 CPC 区域）
- `/es/`：西班牙语（南美与欧洲庞大长尾群体）

### 严格的 Hreflang 声明示例 (注入每个页面的 `<head>`)：
```html
<link rel="alternate" hreflang="x-default" href="https://yourdomain.com/" />
<link rel="alternate" hreflang="en" href="https://yourdomain.com/" />
<link rel="alternate" hreflang="ja" href="https://yourdomain.com/ja/" />
<link rel="alternate" hreflang="ko" href="https://yourdomain.com/ko/" />
<link rel="alternate" hreflang="de" href="https://yourdomain.com/de/" />
<link rel="alternate" hreflang="es" href="https://yourdomain.com/es/" />
```

---

## 四、 结构化数据 (JSON-LD) 抢占 SERP 富摘要

在页面底部注入标准 Schema.org 代码，直接截留 Google SERP 的“FAQ”和“SoftwareApplication”位置：

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "SoftwareApplication",
      "name": "Codex Quota Reset Tracker",
      "operatingSystem": "All",
      "applicationCategory": "DeveloperApplication",
      "offers": {
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "USD"
      }
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "When does Codex rate limit reset?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "OpenAI Codex limits typically operate on a 5-hour rolling window based on when your first prompt was executed, rather than resetting at fixed midnight UTC."
          }
        },
        {
          "@type": "Question",
          "name": "How to check my remaining Codex quota?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "You can check your current Codex limit through the Codex app status panel or run diagnostic commands in your local terminal."
          }
        }
      ]
    }
  ]
}
```