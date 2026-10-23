# CodexReset.live AdSense 审核前只读审计

审计日期：2026-10-23（Asia/Shanghai）
范围：源码、模板、数据、生成站点、Worker/Pages Function、验证脚本。
本阶段未修改业务代码、未部署、未访问线上数据库。

## 1. 结论摘要

原修改方案方向正确，但执行顺序需要调整：先解决不可信输出，再做内容扩张和 SEO。

| 优先级 | 已确认问题 | 证据 | 风险 |
|---|---|---|---|
| P0 | API 失败会伪装成成功结果 | functions/api/radar.js、src/worker.js 在失败时返回 HTTP 200、probability48h=51、currentUsers=46500000 | 产生无来源实时数据 |
| P0 | reset 关键词分类仍可能误判 | scripts/classifier.py 先以 reset + 宽泛肯定词判定 confirmed_reset | 最近重置、日历、概率可能错误 |
| P0 | 没有共享事件模型 | tibo_reset_history.json 主要只有 at/type/status/text/url | 无法区分帖子、声称、生效和适用范围 |
| P0 | 邮件订阅没有真实后端 | 模板只校验邮箱并显示 Subscribed successfully，未发现 POST、存储、退订 | 虚假承诺，隐私披露不一致 |
| P1 | About/Privacy/Terms 是首页弹窗，Contact 未发现 | _tpl_body_v2.html 的 #about/#privacy/#terms；site 无对应独立目录 | 爬虫、用户和 AdSense 审核不友好 |
| P1 | 缺失/过期预测不会显示 unavailable | compute_stats.py 总会生成概率；API fallback 固定 51；前端有数值回退 | 异常时仍像真实预测 |
| P1 | 静态信号、FAQ、动态数据混用 | build_studio.py 的 MOVES_DATA、FAQ 和 radar_stats/API 并行 | 模块互相矛盾、来源不可追踪 |
| P1 | 结构化数据真实性需复核 | site/index.html 含 FAQPage/WebApplication/Organization，FAQ 与动态数据不一致 | 可能产生不准确搜索结果 |
| P2 | SEO 静态基础存在但只做仓库级验证 | sitemap 40 URL，canonical/hreflang 存在；verify_site.py 通过 | 未证明线上响应、移动端和正文可读性 |

## 2. 当前数据流

- 构建入口：scripts/build_studio.py
- 模板：_tpl_head_v2.html、_tpl_body_v2.html
- 数据：data/tibo_reset_history.json、data/radar_stats.json
- 分类：scripts/classifier.py；缓存 data/classification_cache.json；覆盖 data/verified_resets.json
- 输出：10 种语言，每种首页、reset-today、history、methodology，共 40 页
- 统计：scripts/compute_stats.py
- API：functions/api/radar.js 与 src/worker.js 都实现 /api/radar
- 上游：https://willcodexreset.com/api/reset-radar，约 30 秒缓存
- 运行时：前端 fetch /api/radar；主题使用 localStorage('codex_theme')；二维码来自 api.qrserver.com

## 3. 关键模块审计

### Next 48h Reset Chance

构建值来自 radar_stats.json，运行时来自上游 API。compute_stats.py 实际是 days-since 为主的 sigmoid/hazard 启发式加 pending override，并非经过回测校准的真实概率。methodology 页面却描述 8 维权重和 [5%,98%] 边界；两者不一致。当前生成页面概率为 69，而 FAQ 文案仍写约 30%。

建议：统一 PredictionSnapshot，包含 value、status、asOf、modelVersion、inputs、isCalibrated=false。上游超时、空值、过期统一显示 unavailable，不返回 51/50 等伪默认值。

### Latest Reset / Days Since Reset

build_studio.py 通过分类器选择最后一个 confirmed_reset/banked_reset，再用帖子时间计算 days since。帖子发布时间不等于额度实际生效时间，且没有 scope/effectiveAt。应拆成“last public reset claim”和“last verified effective reset”，缺少生效证据时不得写 fully propagated/global reset。

### Live Signals / Verdict

MOVES_DATA 中存在静态强断言，例如 all subscribers worldwide、40M active users；动态帖子又被 API 全部标记 status=confirmed，且 type 只根据是否含 reset。应使用统一 SignalRecord：sourceUrl、publishedAt、claimStatus、verificationStatus、scope、evidenceNote。

### Monthly Calendar

月度统计依赖分类器；缺少范围、重复事件和生效状态模型。应只把 effective_confirmed 计入确认重置统计，pending/claim-only 单独展示或不计入。

### FAQ / Knowledge Base

FAQPage JSON-LD 与动态概率、日期不一致。30–90 分钟传播、banked reset 过期、购买额外额度等句子应逐条有官方来源，否则改为谨慎说明。当前 guides 主要是首页锚点，不是四篇独立可维护原创指南。

### 邮件通知

未发现真实邮件服务、数据库、验证码、双重确认、退订 token 或退订页面。当前提示 Subscribed successfully 是 P0 问题。未实现前应取消邮箱收集和成功提示；若实现，则必须补充双重确认、退订、保留/删除政策并同步 Privacy。

### 统计数字

currentUsers 在 API 缺失时固定为 46,500,000；历史帖子中有 7M、8M、9M、20M、25M、40M 里程碑。应区分 OpenAI 公布的 active users、CodexReset.live subscribers、site visitors。没有当前可追踪来源的实时数字应删除或标记 not independently verified。

### 合规页面

当前只有首页 #about/#privacy/#terms 弹窗，未发现 /about/、/privacy/、/terms/、/contact/。Privacy 声明“Zero Personal Data Tracking”与邮箱输入、第三方二维码、Cloudflare 日志和可能的 Analytics 不匹配。应创建独立可访问页面，并按真实部署服务撰写。

### SEO

site/sitemap.xml 有 40 个 URL；robots、canonical、hreflang 静态存在，verify_site.py 通过。仍需线上只读验证状态码、Content-Type、404、正文可读性、hreflang reciprocal 和 og-image.png 是否真实存在。不要迁移已有 URL。

## 4. 推荐整改顺序

### P0

1. 删除 API fallback 的固定概率、用户数和 HTTP 200 假成功。
2. 邮件未实现前取消 Subscribed successfully。
3. 引入事件状态机，区分 signal_only、reset_claimed、banked_credit_claimed、effective_partially_confirmed、effective_confirmed、not_a_reset、unknown/unavailable。
4. FAQ、雷达、时间线、日历、最近重置全部消费同一事件模型。
5. 为动态值增加来源、asOf、过期阈值和 unavailable 状态。

### P1

1. 新增 data/events.json 或等价共享模型，不删除旧记录，只增加审核字段。
2. 创建独立 /about/、/privacy/、/terms/、/contact/。
3. 新增四篇原创指南：How to Check Your Codex Usage Limits、Codex Rate Limit Reset: How It Works、Codex Rate Limit Reached: What to Do、Codex Reset History and Timeline。
4. 重写 methodology，使文字与实际模型一致，明确未校准。
5. 复核 FAQPage、WebApplication、Organization 结构化数据。

### P2

1. 扩展 sitemap 和导航到真实新增页面。
2. 增加状态码、Content-Type、链接、API 失败、时区、移动端和浏览器测试。
3. 仅在允许时做线上只读验证；不部署。

## 5. 当前验证

已执行 python scripts/verify_site.py：

- 40 个 HTML 文件通过现有完整性、schema、链接和 section 审计。
- 不能证明 API fallback、邮件订阅、生产状态码、移动端交互、FAQ 一致性或隐私声明真实性。

## 6. 修改前需人工确认

1. 实际部署是 Pages Functions、Workers Static Assets，还是两者之一。
2. 是否真的要收集邮箱；若是，选择邮件服务、数据库、双重确认和退订方案。
3. Analytics 提供商、Cookie、日志和第三方服务。
4. 46.5M 的第一方来源、发布时间和范围。
5. 历史记录是否仅保留帖子声明，不把额度生效写成确认。
6. 联系邮箱、运营主体、适用法律地区。
7. 是否维持 10 种语言，还是先保证英文合规页面质量。

## 7. AdSense 提交前清单

- [ ] 实时数据有来源、时间戳、口径和过期状态
- [ ] API 异常不再伪造概率、用户数或 confirmed
- [ ] 邮件成功提示与真实后端一致
- [ ] About / Privacy / Terms / Contact 为独立可访问页面
- [ ] Privacy 与 Analytics、Cookie、localStorage、Cloudflare、第三方资源一致
- [ ] FAQ 与可见内容一致，结构化数据不含虚构事实
- [ ] 四篇原创指南完成来源核验和内部链接
- [ ] sitemap、robots、canonical、hreflang、404、Content-Type 完成线上检查
- [ ] 移动端交互和主要正文可访问
- [ ] 不声称与 OpenAI 关联，独立项目免责声明清晰
- [ ] 人工补充联系信息、运营主体和地区同意管理方案

阶段结论：该项目可以进入第二阶段，但应先完成 P0，不建议直接大规模新增内容或语言页面。历史记录不得删除或静默重分类，应保留原文并增加审核字段。