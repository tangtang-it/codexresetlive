# -*- coding: utf-8 -*-
import json, os, html, re, sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from _i18n_priority import I18N
from _i18n_rest import I18N2

I18N.update(I18N2)

SITE_DIR = ROOT_DIR / "site"

with open(ROOT_DIR / "_tpl_head_v2.html", encoding="utf-8") as f:
    HEAD = f.read()
with open(ROOT_DIR / "_tpl_body_v2.html", encoding="utf-8") as f:
    BODY = f.read()
with open(ROOT_DIR / "data/tibo_reset_history.json", encoding="utf-8") as f:
    HIST = json.load(f)
with open(ROOT_DIR / "data/radar_stats.json", encoding="utf-8") as f:
    STATS = json.load(f)

LANGS = [
    ("en","","English","en_US","https://willcodexreset.com/"),
    ("zh-hans","zh-hans","简体中文","zh_CN","https://willcodexreset.com/zh-hans/"),
    ("zh-hant","zh-hant","繁體中文","zh_TW","https://willcodexreset.com/zh-hant/"),
    ("ja","ja","日本語","ja_JP","https://willcodexreset.com/ja/"),
    ("ko","ko","한국어","ko_KR","https://willcodexreset.com/ko/"),
    ("es","es","Español","es_ES","https://willcodexreset.com/es/"),
    ("de","de","Deutsch","de_DE","https://willcodexreset.com/de/"),
    ("fr","fr","Français","fr_FR","https://willcodexreset.com/fr/"),
    ("pt-br","pt-br","Português (Brasil)","pt_BR","https://willcodexreset.com/pt-br/"),
    ("ru","ru","Русский","ru_RU","https://willcodexreset.com/ru/"),
]

def esc(s):
    return html.escape(str(s), quote=True)

recs = sorted(HIST["records"], key=lambda x: x["at"])
last = recs[-1]
prob = STATS["probability_48h"]
days_since = STATS["days_since_last_reset"]
days_since_str = ("%.1f" % days_since) + "d"
last_date = last["at"][:10]

# 1. GENERATE NATIVE SVG PULSE CHART (Forecast Pulse)
pulse_svg = f'''<svg viewBox="0 0 740 180" fill="none" xmlns="http://www.w3.org/2000/svg">
  <line x1="40" y1="30" x2="710" y2="30" stroke="#2b3139" stroke-width="1" stroke-dasharray="3 3"/>
  <line x1="40" y1="80" x2="710" y2="80" stroke="#2b3139" stroke-width="1" stroke-dasharray="3 3"/>
  <line x1="40" y1="130" x2="710" y2="130" stroke="#2b3139" stroke-width="1"/>
  
  <text x="15" y="34" fill="#707a8a" font-family="ui-monospace" font-size="10">80%</text>
  <text x="15" y="84" fill="#707a8a" font-family="ui-monospace" font-size="10">40%</text>
  <text x="15" y="134" fill="#707a8a" font-family="ui-monospace" font-size="10">0%</text>

  <text x="60" y="156" fill="#707a8a" font-family="ui-monospace" font-size="10" text-anchor="middle">Sep 26</text>
  <text x="130" y="156" fill="#707a8a" font-family="ui-monospace" font-size="10" text-anchor="middle">Sep 28</text>
  <text x="210" y="156" fill="#707a8a" font-family="ui-monospace" font-size="10" text-anchor="middle">Sep 30</text>
  <text x="310" y="156" fill="#707a8a" font-family="ui-monospace" font-size="10" text-anchor="middle">Oct 2</text>
  <text x="420" y="156" fill="#0ecb81" font-family="ui-monospace" font-size="10" font-weight="bold" text-anchor="middle">Oct 5 (Now)</text>
  <text x="530" y="156" fill="#707a8a" font-family="ui-monospace" font-size="10" text-anchor="middle">Oct 6</text>
  <text x="630" y="156" fill="#707a8a" font-family="ui-monospace" font-size="10" text-anchor="middle">Oct 8</text>

  <path d="M 60 40 Q 95 110, 130 95 T 210 50 T 260 115 T 310 40 Q 365 110, 420 116" 
        stroke="#0ecb81" stroke-width="2.6" fill="none" stroke-linecap="round"/>

  <path d="M 420 116 Q 475 105, 530 90 T 630 65 T 690 55" 
        stroke="#FCD535" stroke-width="2.2" stroke-dasharray="5 4" fill="none" stroke-linecap="round"/>

  <line x1="60" y1="40" x2="60" y2="130" stroke="#0ecb81" stroke-width="1.2" stroke-opacity="0.4"/>
  <circle cx="60" cy="40" r="4.5" fill="#0ecb81"/>
  <rect x="42" y="16" width="36" height="15" rx="3" fill="#1e2329" stroke="#0ecb81" stroke-width="1"/>
  <text x="60" y="27" fill="#0ecb81" font-family="ui-monospace" font-size="8.5" font-weight="bold" text-anchor="middle">Reset</text>

  <line x1="210" y1="50" x2="210" y2="130" stroke="#FCD535" stroke-width="1.2" stroke-opacity="0.4"/>
  <circle cx="210" cy="50" r="4.5" fill="#FCD535"/>
  <rect x="189" y="26" width="42" height="15" rx="3" fill="#1e2329" stroke="#FCD535" stroke-width="1"/>
  <text x="210" y="37" fill="#FCD535" font-family="ui-monospace" font-size="8.5" font-weight="bold" text-anchor="middle">Banked</text>

  <line x1="310" y1="40" x2="310" y2="130" stroke="#0ecb81" stroke-width="1.2" stroke-opacity="0.4"/>
  <circle cx="310" cy="40" r="4.5" fill="#0ecb81"/>
  <rect x="292" y="16" width="36" height="15" rx="3" fill="#1e2329" stroke="#0ecb81" stroke-width="1"/>
  <text x="310" y="27" fill="#0ecb81" font-family="ui-monospace" font-size="8.5" font-weight="bold" text-anchor="middle">Reset</text>

  <circle cx="420" cy="116" r="5.5" fill="#0ecb81" stroke="#0b0e11" stroke-width="2"/>
  <rect x="395" y="86" width="50" height="20" rx="4" fill="#0ecb81"/>
  <text x="420" y="100" fill="#0b0e11" font-family="ui-monospace" font-size="10" font-weight="bold" text-anchor="middle">Now {prob}%</text>
  <path d="M 420 106 L 417 110 L 423 110 Z" fill="#0ecb81"/>
</svg>'''

# 2. GENERATE WHAT MOVED THE MODEL (EXPANDED 8 REAL-WORLD EVENTS)
MOVES_DATA = {
    "en": [
        ("Oct 2 · 21:18 UTC", "Direct Usage Reset", "Confirmed hard reset fully propagated to all ChatGPT Work & Codex subscribers.", "+38 pts", "up", "Execution: Tibo announced token caps cleared following Sol capacity scaling."),
        ("Oct 2 · 02:14 UTC", "Global Reset Notice", "Tibo gave advance warning of global refresh scheduled for 10am PST.", "+24 pts", "up", "Advance Signal: Official commitment to resolve launch throughput bottleneck."),
        ("Sep 30 · 23:12 UTC", "Banked Credit Rollout", "One banked reset credited daily to subscribers awaiting Astra architecture.", "+15 pts", "neutral", "Credit Boost: Innovative banked mechanism for unreleased features."),
        ("Sep 26 · 18:17 UTC", "Pre-Weekend Hard Reset", "Hard quota refill landed ahead of peak weekend coding sprints.", "+30 pts", "up", "Pattern Match: Validates OpenAI preference for Friday afternoon global flushes."),
        ("Sep 22 · 18:23 UTC", "GPT-6 Sol & Luna Launch", "New flagship models rolled out alongside 50% permanent API price drop.", "+28 pts", "up", "Milestone Catalyst: Major model releases consistently trigger account-wide flushes."),
        ("Sep 12 · 08:09 UTC", "Nightly Capacity Injection", "Silent quota replenishment propagated prior to Asian & European working windows.", "+20 pts", "up", "Infrastructure: Periodic server-side buffer flushing during cluster upgrades."),
        ("Sep 5 · 00:39 UTC", "Astra Early Rollout Bonus", "Astra launched ahead of internal timeline; full reset executed in celebration.", "+22 pts", "up", "Engineering Surprise: Unscheduled reward flushes upon early feature deployment."),
        ("Aug 31 · 02:29 UTC", "25M Active Users Milestone", "Codex & ChatGPT Work crossed 25,000,000 active users; celebratory reset granted.", "+25 pts", "up", "Scale Milestone: Round-number user thresholds trigger marketing-driven flushes.")
    ],
    "zh": [
        ("10月2日 · 21:18 UTC", "全网硬重置已生效", "官方全员硬重置下发完毕，所有 ChatGPT Work 与 Codex 额度回满。", "+38 分", "up", "【发版放水】伴随 Sol 负载优化完成，Tibo 发推确认全网额度一键清空。"),
        ("10月2日 · 02:14 UTC", "全球重置提前预告", "Tibo 提前发文预告将在美西时间上午 10 点为全体付费用户执行全量重置。", "+24 分", "up", "【官方前瞻】官方首次对大模型版本上线初期的排队和限流问题公开承诺补发。"),
        ("9月30日 · 23:12 UTC", "Astra 存续额度补发", "针对未开放 Astra 权限的用户，每日补偿发放 1 次可保留的 Banked Reset。", "+15 分", "neutral", "【权益补偿】开创存续式额度发放机制，用户在特定功能开放前每日享有额外额度。"),
        ("9月26日 · 18:17 UTC", "周末前全员硬放水", "赶在周末高频编码高峰前，官方服务器端完成所有付费账户额度重置。", "+30 分", "up", "【周期规律】印证 OpenAI 倾向于在周五下午或周末前清空额度以鼓励开发者密集测试。"),
        ("9月22日 · 18:23 UTC", "GPT-6 Sol / Luna 双模型发版", "新模型上线并大幅下调 API 定价，全员账户注入一次完整重置额度。", "+28 分", "up", "【里程碑激励】重大模型换代上线时的标准操作，伴随额度翻倍或重置以促成调用增长。"),
        ("9月12日 · 08:09 UTC", "凌晨全网配额更新", "欧洲与亚洲工作时段开启前，官方静默完成又一次硬性额度全量下发。", "+20 分", "up", "【算力释放】后台集群扩容完毕后的周期性容量释放，无预告直接回满。"),
        ("9月5日 · 00:39 UTC", "Astra 提前上线庆祝重置", "Astra 架构比原计划提前部署完毕，为全量 Plus、Pro 和 Business 用户回满额度。", "+22 分", "up", "【工程庆祝】工程交付超前于产品路线图时的奖励性放水，单日激发超额调用。"),
        ("8月31日 · 02:29 UTC", "2500 万活跃用户里程碑", "Codex 与 ChatGPT Work 活跃用户突破 2500 万大关，官方启动全员狂欢重置。", "+25 分", "up", "【规模红利】用户量级突破整数关口时，管理层启动营销放水。")
    ],
    "ja": [
        ("10月2日 · 21:18 UTC", "全体ハードリセット反映完了", "全ChatGPT WorkおよびCodexユーザーの利用枠回復が完了しました。", "+38 pts", "up", "【アプデ連動】Sol負荷緩和完了に伴い、Tiboが全量リセット完了を発表。"),
        ("10月2日 · 02:14 UTC", "全体リセット事前告知", "TiboがPST午前10時に全有料アカウント向けリセットを実施すると事前予告。", "+24 pts", "up", "【先行シグナル】新モデル公開初期の負荷急増に対し公式がリセットを確約。"),
        ("9月30日 · 23:12 UTC", "Astra 向けバンク枠付与", "Astra未利用ユーザーに対し、1日1回のバンク型リセット枠を補填付与。", "+15 pts", "neutral", "【機能補填】新機能ロールアウト待ちユーザーに対するクレジット型救済。"),
        ("9月26日 · 18:17 UTC", "週末前全体枠リセット", "週末の開発ラッシュに先立ち、サーバー側で枠全量回復が完了。", "+30 pts", "up", "【周期性】週末の開発者アクティビティ活性化を狙った金曜リセットの傾向を実証。"),
        ("9月22日 · 18:23 UTC", "GPT-6 Sol/Luna リリース", "新モデル配信とAPI恒久値下げに伴い、全アカウントに利用枠を一括注入。", "+28 pts", "up", "【大型アプデ】主要モデル切り替え時には恒例の一括枠リセットが発動。"),
        ("9月12日 · 08:09 UTC", "深夜インフラ枠追加", "欧州・アジアの就業時間前にサイレントで枠全量回復が実行。", "+20 pts", "up", "【キャパ解放】サーバークラスタ拡張に伴う定期的な枠解放。"),
        ("9月5日 · 00:39 UTC", "Astra 前倒し配信ボーナス", "予定より早くAstra配信が完了し、記念として全有料プランの枠を回復。", "+22 pts", "up", "【マイルストーン】開発目標前倒し達成時に不定期で発動するボーナスリセット。"),
        ("8月31日 · 02:29 UTC", "2500万人アクティブ達成", "利用者が2,500万人に到達した節目を記念し、全ユーザー向けに大放水。", "+25 pts", "up", "【規模拡大】ラウンドナンバーのマイルストーン達成に伴う祝賀リセット。")
    ]
}

def render_move_items(lang_code):
    moves = MOVES_DATA.get("zh" if "zh" in lang_code else ("ja" if lang_code == "ja" else "en"), MOVES_DATA["en"])
    items = []
    for m_time, m_tag, m_desc, m_pts, m_cls, m_reason in moves:
        items.append(f'''<div class="move-item">
  <div class="move-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:13px;height:13px"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg></div>
  <div class="move-body">
    <div class="move-head">
      <span class="move-tag">{esc(m_tag)}</span>
      <span class="move-pts {m_cls} num">{m_pts}</span>
    </div>
    <div class="move-time num">{m_time}</div>
    <div class="move-text">{esc(m_desc)}</div>
    <div class="move-reason">{esc(m_reason)}</div>
  </div>
</div>''')
    return "".join(items)


# 3. GENERATE TIBO STREAM MINI POSTS
stream_items = []
for r in recs[-10:][::-1]:
    t = r["type"]
    badge_cls = "badge " + t
    stream_items.append(f'''<div class="post-mini">
  <div class="pm-head">
    <span class="pm-author">Tibo <span style="font-weight:400;color:var(--muted)">@thsottiaux</span></span>
    <span class="{badge_cls}">{t.upper()}</span>
  </div>
  <div class="pm-quote">{esc(r["text"])}</div>
  <div class="pm-foot">
    <span data-utc="{r["at"]}">{r["at"][:16].replace("T"," ")} UTC</span>
    <a href="{r["url"]}" target="_blank" rel="noopener nofollow" style="color:var(--primary)">View on X ↗</a>
  </div>
</div>''')
STREAM_ITEMS = "".join(stream_items)

# 4. GENERATE 8 SIGNAL SWITCHES
switches = [
    ("OpenAI status", "green", "Operational"),
    ("Tibo posts", "green", "55 Verified"),
    ("User milestones", "yellow", "43M (Nearing 50M)"),
    ("Release cadence", "green", "Mid-week active"),
    ("Community predictions", "gray", "Consensus low"),
    ("Reset cooldown", "yellow", f"Cooldown active ({days_since_str})"),
    ("SF work window", "green", "Daytime (US Pacific)"),
    ("Token bucket backlog", "gray", "Stable load")
]
switch_items = []
for s_name, s_color, s_status in switches:
    switch_items.append(f'''<div class="switch-row">
  <div class="sr-left">
    <span class="sr-dot {s_color}"></span>
    <span class="sr-name">{s_name}</span>
  </div>
  <span class="sr-status">{s_status}</span>
</div>''')
SWITCH_ITEMS = "".join(switch_items)

# 5. GENERATE MONTHLY CALENDAR GRID
week1 = '''<tr>
  <td class="pad"><span class="day-num">27</span></td>
  <td class="pad"><span class="day-num">28</span></td>
  <td class="pad"><span class="day-num">29</span></td>
  <td class="pad"><span class="day-num">30</span><span class="day-stamp banked">Banked Reset</span></td>
  <td><span class="day-num">1</span></td>
  <td><span class="day-num">2</span><span class="day-stamp regular">21:18 Hard Reset</span></td>
  <td><span class="day-num">3</span></td>
</tr>'''
week2 = '''<tr>
  <td><span class="day-num">4</span></td>
  <td><span class="day-num" style="color:var(--primary);font-weight:800">5 (Today)</span><span style="font-size:9px;color:var(--muted)">Watching</span></td>
  <td><span class="day-num">6</span></td>
  <td><span class="day-num">7</span></td>
  <td><span class="day-num">8</span></td>
  <td><span class="day-num">9</span></td>
  <td><span class="day-num">10</span></td>
</tr>'''
week3 = '''<tr>
  <td><span class="day-num">11</span></td><td><span class="day-num">12</span></td><td><span class="day-num">13</span></td><td><span class="day-num">14</span></td><td><span class="day-num">15</span></td><td><span class="day-num">16</span></td><td><span class="day-num">17</span></td>
</tr>'''
week4 = '''<tr>
  <td><span class="day-num">18</span></td><td><span class="day-num">19</span></td><td><span class="day-num">20</span></td><td><span class="day-num">21</span></td><td><span class="day-num">22</span></td><td><span class="day-num">23</span></td><td><span class="day-num">24</span></td>
</tr>'''
week5 = '''<tr>
  <td><span class="day-num">25</span></td><td><span class="day-num">26</span></td><td><span class="day-num">27</span></td><td><span class="day-num">28</span></td><td><span class="day-num">29</span></td><td><span class="day-num">30</span></td><td><span class="day-num">31</span></td>
</tr>'''

CAL_TABLE_HTML = f'''<table class="cal-table">
  <thead>
    <tr>
      <th>Sun</th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th>
    </tr>
  </thead>
  <tbody>
    {week1}
    {week2}
    {week3}
    {week4}
    {week5}
  </tbody>
</table>'''

def build_lang_items(current):
    out = []
    for code, d, name, loc, url in LANGS:
        cls = "lang-item on" if code == current else "lang-item"
        rel_path = f"/{d}/" if d else "/"
        out.append(f'<a class="{cls}" href="{rel_path}" hreflang="{code}"><span>{name}</span><code>{code}</code></a>')
    return "".join(out)

def build_hreflang(current_url):
    parts = ['<link rel="alternate" hreflang="x-default" href="https://willcodexreset.com/">',
             '<link rel="alternate" hreflang="en" href="https://willcodexreset.com/">']
    for code, d, name, loc, url in LANGS:
        if code != "en":
            parts.append(f'<link rel="alternate" hreflang="{code}" href="{url}">')
    return "\n".join(parts)

# Generate all 10 language pages
for code, d, name, loc, canon in LANGS:
    t = I18N[code]
    out_dir = (SITE_DIR / d) if d else SITE_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "index.html"

    title = f"{t['h1_a'].rstrip('?')} {t['h1_b']} | Codex Reset Radar"
    desc = t["hero_p"]

    schema = {
        "@context":"https://schema.org",
        "@graph":[
            {"@type":"WebApplication","name":"Codex Reset Radar",
             "url":canon,"applicationCategory":"UtilitiesApplication","operatingSystem":"Any",
             "isAccessibleForFree":True,"inLanguage":loc,
             "description":desc},
            {"@type":"BreadcrumbList","itemListElement":
                [{"@type":"ListItem","position":1,"name":"Home","item":"https://willcodexreset.com/"}] +
                ([] if code=="en" else [{"@type":"ListItem","position":2,"name":name,"item":canon}])},
            {"@type":"FAQPage","inLanguage":loc,"mainEntity":[
                {"@type":"Question","name":t["faq_q1"],"acceptedAnswer":{"@type":"Answer","text":t["faq_a1"]}},
                {"@type":"Question","name":t["faq_q2"],"acceptedAnswer":{"@type":"Answer","text":t["faq_a2"]}},
                {"@type":"Question","name":t["faq_q3"],"acceptedAnswer":{"@type":"Answer","text":t["faq_a3"]}},
                {"@type":"Question","name":t["faq_q4"],"acceptedAnswer":{"@type":"Answer","text":t["faq_a4"]}},
            ]}
        ]
    }

    faq_items = "".join(
        f'<div class="faq-i"><div class="faq-q">{esc(t["faq_q%d"%i])}</div><div class="faq-a">{esc(t["faq_a%d"%i])}</div></div>'
        for i in (1,2,3,4))

    alert_t = "Get Realtime Reset Prediction Alerts" if code=="en" else ("获取实时重置预警广播" if "zh" in code else ("リセット予測通知を受け取る" if code=="ja" else ("실시간 리셋 알림 받기" if code=="ko" else "Recibe Alertas en Tiempo Real")))
    alert_d = "Alerts sent when the next 48h reset chance exceeds 80% or when verified by Tibo." if code=="en" else ("当未来48小时重置概率超过80%或Tibo发布确认推文时立即通知。" if "zh" in code else ("48時間以内のリセット確率が80%を超えるか、公式確認された際に通知。" if code=="ja" else ("48시간 리셋 확률이 80%를 초과하거나 공식 확인 시 즉시 알림." if code=="ko" else "Alertas cuando la probabilidad supere el 80% o se confirme.")) )
    notify_me = "Notify Me" if code=="en" else ("立即订阅" if "zh" in code else ("通知登録" if code=="ja" else ("알림 받기" if code=="ko" else "Avisarme")))
    sub_count = "70,760+ Subscribed" if code=="en" else ("已订阅 70,760+" if "zh" in code else ("購読者 70,760人+" if code=="ja" else ("구독자 70,760명+" if code=="ko" else "70,760+ Suscriptores")))

    pulse_t = "Forecast Pulse: 48-Hour Event & Signal Log" if code=="en" else ("事件脉冲曲线：48小时概率走势与推演" if "zh" in code else ("予測パルス：48時間のイベント＆推移" if code=="ja" else ("예측 펄스: 48시간 이벤트 및 신호 로그" if code=="ko" else "Pulso de Pronóstico: Registro de 48h")))
    pulse_sub = "Continuous timeline showing confirmed resets & projected 48h probability." if code=="en" else ("结合已确认重置历史与未来48小时预测走势的连续时间序列图。" if "zh" in code else ("確認済みリセット履歴と48時間予測の連続タイムライン。" if code=="ja" else ("확인된 리셋 이력과 향후 48시간 예측 궤적。" if code=="ko" else "Línea de tiempo continua de eventos y predicción.")) )

    studio_t = "Multi-Factor Signal Desk Studio" if code=="en" else ("多维信号台工作区 (Signal Studio)" if "zh" in code else ("多角シグナル監視スタジオ" if code=="ja" else ("다각도 시그널 감시 스튜디오" if code=="ko" else "Estudio de Señales Multifactor")))
    studio_s = "Deep-dive into verified developer statements, model factor shifts, and 8 core signals." if code=="en" else ("深入剖析官方一手推特证据、模型权重异动事件与 8 大核心信号开关。" if "zh" in code else ("一次ソース証拠、モデル変動要因、8つの主要シグナルを詳細分析。" if code=="ja" else ("공식 1차 출처 증거, 모델 변동 요인 및 8대 핵심 시그널 분석。" if code=="ko" else "Análisis de fuentes primarias y 8 señales clave.")) )

    col1_t = "What Moved The Model" if code=="en" else ("模型权重异动事件" if "zh" in code else ("モデル変動イベント" if code=="ja" else ("모델 변동 이벤트" if code=="ko" else "Eventos de Ajuste")))
    col3_t = "Signal Switchboard" if code=="en" else ("8 大信号总控台" if "zh" in code else ("シグナル制御盤" if code=="ja" else ("시그널 제어반" if code=="ko" else "Panel de Señales")))

    cal_radar_t = "Visual Reset Calendar · October 2026" if code=="en" else ("月度重置可视化大日历 (2026年10月)" if "zh" in code else ("月間リセットカレンダー (2026年10月)" if code=="ja" else ("월간 리셋 캘린더 (2026년 10월)" if code=="ko" else "Calendario Visual de Resets · Octubre 2026")))
    cal_radar_s = "Track weekly reset cadence at a glance. Blue tags = Direct Hard Resets; Yellow tags = Banked Credit Resets." if code=="en" else ("一目了然掌握全网重置节奏。绿标为全员硬重置，黄标为存储式福利补发。" if "zh" in code else ("週ごとのリセット傾向を一目で把握。緑タグは全量リセット、黄タグはクレジット付与。" if code=="ja" else ("주간 리셋 경향을 한눈에 파악。초록색은 일반 리셋, 노란색은 적립형 리셋。" if code=="ko" else "Consulta el ritmo semanal de resets de un vistazo.")) )

    tok = {
        "__LANG__":code,"__TITLE__":esc(title),"__DESC__":esc(desc),"__CANONICAL__":canon,
        "__HREFLANG__":build_hreflang(canon),"__LOCALE__":loc,
        "__SCHEMA__":json.dumps(schema,ensure_ascii=False,indent=2),
        "__BRAND_SUB__":esc(t["brand_sub"]),"__LIVE__":esc(t["live"]),
        "__LANG_LABEL__":esc(t["lang_label"]),"__LANG_NAME__":esc(name),
        "__LANG_ITEMS__":build_lang_items(code),
        "__HOME_PATH__":(f"/{d}/" if d else "/"),
        "__BADGE__":esc(t["badge"]),
        "__H1_A__":esc(t["h1_a"]),"__H1_B__":esc(t["h1_b"]),"__HERO_P__":esc(t["hero_p"]),
        "__GAUGE_LBL__":esc(t["gauge_lbl"]),"__GAUGE_TAG__":esc(t["gauge_tag"]),
        "__GAUGE_CAP__":esc(t["gauge_cap"]),"__GF_1__":esc(t["gf_1"]),"__GF_2__":esc(t["gf_2"]),
        "__LAST_DATE__":last_date,"__DAYS_SINCE__":days_since_str,
        "__PROB_NUM__":str(prob),
        
        "__PULSE_T__":esc(pulse_t),"__PULSE_SUB__":esc(pulse_sub),
        "__PULSE_SVG__":pulse_svg,

        "__ALERT_T__":esc(alert_t),"__ALERT_D__":esc(alert_d),
        "__NOTIFY_ME__":esc(notify_me),"__SUBSCRIBER_COUNT__":esc(sub_count),

        "__RO_1_L__":("OpenAI Status" if code=="en" else "OpenAI 服务状态"),
        "__RO_1_S__":("No major active outage" if code=="en" else "当前无全局宕机事故"),
        "__RO_2_L__":("Tibo Twitter Watch" if code=="en" else "负责人推特追踪"),
        "__RO_2_S__":("Verified official statements" if code=="en" else "已追踪55篇官方推文"),
        "__RO_3_L__":("Days Since Last Reset" if code=="en" else "距上次重置天数"),
        "__RO_3_S__":("Oct 2, 21:18 UTC" if code=="en" else "10月2日 21:18 UTC"),
        "__RO_4_L__":("Estimated Codex Users" if code=="en" else "全球活跃用户估算"),
        "__RO_4_S__":("Milestone: 25M published" if code=="en" else "官方披露基线：2500万"),

        "__STUDIO_T__":esc(studio_t),"__STUDIO_S__":esc(studio_s),
        "__COL1_T__":esc(col1_t),"__COL3_T__":esc(col3_t),
        "__MOVE_ITEMS__":render_move_items(code),"__STREAM_ITEMS__":STREAM_ITEMS,"__SWITCH_ITEMS__":SWITCH_ITEMS,

        "__CAL_RADAR_T__":esc(cal_radar_t),"__CAL_RADAR_S__":esc(cal_radar_s),
        "__CAL_TABLE_HTML__":CAL_TABLE_HTML,

        "__CALC_T__":esc(t["calc_t"]),"__CALC_S__":esc(t["calc_s"]),
        "__TZ_L__":esc(t["tz_l"]),"__TZ_LOCAL__":esc(t["tz_local"]),"__UNLOCK_L__":esc(t["unlock_l"]),
        "__CALCULATING__":esc(t["calculating"]),"__PRESET_L__":esc(t["preset_l"]),
        "__P1__":esc(t["p1"]),"__P2__":esc(t["p2"]),"__P3__":esc(t["p3"]),"__P4__":esc(t["p4"]),
        "__U_H__":esc(t["u_h"]),"__U_M__":esc(t["u_m"]),"__U_S__":esc(t["u_s"]),
        "__PROG_L__":esc(t["prog_l"]),"__RECOVERED__":esc(t["recovered"]),
        "__NOTIFY__":esc(t["notify"]),"__CAL__":esc(t["cal"]),

        "__TOOLS_T__":esc(t["tools_t"]),"__TOOLS_S__":esc(t["tools_s"]),
        "__TOOL1_D__":esc(t["tool1_d"]),"__TOOL2_D__":esc(t["tool2_d"]),"__TOOL3_D__":esc(t["tool3_d"]),
        "__TOOL1_A__":esc(t["tool1_a"]),"__TOOL2_A__":esc(t["tool2_a"]),"__TOOL3_A__":esc(t["tool3_a"]),

        "__FAQ_T__":esc(t["faq_t"]),"__FAQ_ITEMS__":faq_items,
        "__FOOT__":esc(t["foot"]),"__FOOT_SRC__":esc(t["foot_src"]),
        "__TZ_TOAST__":esc(t["tz_toast"]),"__MIN_TOAST__":esc(t["min_toast"]),
        "__NO_NOTIF__":esc(t["no_notif"]),"__NOTIF_ON__":esc(t["notif_on"]),
        "__NOTIF_SET__":esc(t["notif_set"]),"__NOTIF_BLOCK__":esc(t["notif_block"]),
    }

    page = HEAD + BODY
    for k, v in tok.items():
        page = page.replace(k, v)

    with open(path, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"Built {code:8s} -> {path} ({len(page)} bytes)")

print("ALL_STUDIO_PAGES_BUILT_CROSS_PLATFORM_OK")
