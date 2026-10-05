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
    ("en","","English","en_US","https://codexresetlive.com/"),
    ("zh-hans","zh-hans","简体中文","zh_CN","https://codexresetlive.com/zh-hans/"),
    ("zh-hant","zh-hant","繁體中文","zh_TW","https://codexresetlive.com/zh-hant/"),
    ("ja","ja","日本語","ja_JP","https://codexresetlive.com/ja/"),
    ("ko","ko","한국어","ko_KR","https://codexresetlive.com/ko/"),
    ("es","es","Español","es_ES","https://codexresetlive.com/es/"),
    ("de","de","Deutsch","de_DE","https://codexresetlive.com/de/"),
    ("fr","fr","Français","fr_FR","https://codexresetlive.com/fr/"),
    ("pt-br","pt-br","Português (Brasil)","pt_BR","https://codexresetlive.com/pt-br/"),
    ("ru","ru","Русский","ru_RU","https://codexresetlive.com/ru/"),
]

def esc(s):
    return html.escape(str(s), quote=True)

recs = sorted(HIST["records"], key=lambda x: x["at"])
last = recs[-1]
prob = STATS["probability_48h"]
days_since = STATS["days_since_last_reset"]
days_since_str = ("%.1f" % days_since) + "d"
last_date = last["at"][:10]

# --- Shared UI Components ---
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
  <path d="M 60 40 Q 95 110, 130 95 T 210 50 T 260 115 T 310 40 Q 365 110, 420 116" stroke="#0ecb81" stroke-width="2.6" fill="none" stroke-linecap="round"/>
  <path d="M 420 116 Q 475 105, 530 90 T 630 65 T 690 55" stroke="#FCD535" stroke-width="2.2" stroke-dasharray="5 4" fill="none" stroke-linecap="round"/>
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

MOVES_DATA = {
    "en": [
        ("Oct 2 · 21:18 UTC", "Direct Usage Reset", "Confirmed hard reset fully propagated to all ChatGPT Work & Codex subscribers.", "+38 pts", "up", "Execution: Tibo announced token caps cleared following Sol capacity scaling."),
        ("Oct 2 · 02:14 UTC", "Global Reset Notice", "Tibo gave advance warning of global refresh scheduled for 10am PST.", "+24 pts", "up", "Advance Signal: Official commitment to resolve launch throughput bottleneck."),
        ("Sep 30 · 23:12 UTC", "Banked Credit Rollout", "One banked reset credited daily to subscribers awaiting Astra architecture.", "+15 pts", "neutral", "Credit Boost: Innovative banked mechanism for unreleased features."),
        ("Sep 26 · 18:17 UTC", "Pre-Weekend Hard Reset", "Hard quota refill landed ahead of peak weekend coding sprints.", "+30 pts", "up", "Pattern Match: Validates OpenAI preference for Friday afternoon global flushes."),
        ("Sep 22 · 18:23 UTC", "GPT-6 Sol & Luna Launch", "New flagship models rolled out alongside 50% permanent API price drop.", "+28 pts", "up", "Milestone Catalyst: Major model releases consistently trigger account-wide flushes.")
    ],
    "zh": [
        ("10月2日 · 21:18 UTC", "全网硬重置已生效", "官方全员硬重置下发完毕，所有 ChatGPT Work 与 Codex 额度回满。", "+38 分", "up", "【发版放水】伴随 Sol 负载优化完成，Tibo 发推确认全网额度一键清空。"),
        ("10月2日 · 02:14 UTC", "全球重置提前预告", "Tibo 提前发文预告将在美西时间上午 10 点为全体付费用户执行全量重置。", "+24 分", "up", "【官方前瞻】官方首次对大模型版本上线初期的排队和限流问题公开承诺补发。"),
        ("9月30日 · 23:12 UTC", "Astra 存续额度补发", "针对未开放 Astra 权限的用户，每日补偿发放 1 次可保留的 Banked Reset。", "+15 分", "neutral", "【权益补偿】开创存续式额度发放机制，用户在特定功能开放前每日享有额外额度。"),
        ("9月26日 · 18:17 UTC", "周末前全员硬放水", "赶在周末高频编码高峰前，官方服务器端完成所有付费账户额度重置。", "+30 分", "up", "【周期规律】印证 OpenAI 倾向于在周五下午或周末前清空额度以鼓励开发者密集测试。"),
        ("9月22日 · 18:23 UTC", "GPT-6 Sol / Luna 双模型发版", "新模型上线并大幅下调 API 定价，全员账户注入一次完整重置额度。", "+28 分", "up", "【里程碑激励】重大模型换代上线时的标准操作，伴随额度翻倍或重置以促成调用增长。")
    ],
    "ja": [
        ("10月2日 · 21:18 UTC", "全体ハードリセット反映完了", "全ChatGPT WorkおよびCodexユーザーの利用枠回復が完了しました。", "+38 pts", "up", "【アプデ連動】Sol負荷緩和完了に伴い、Tiboが全量リセット完了を発表。"),
        ("10月2日 · 02:14 UTC", "全体リセット事前告知", "TiboがPST午前10時に全有料アカウント向けリセットを実施すると事前予告。", "+24 pts", "up", "【先行シグナル】新モデル公開初期の負荷急増に対し公式がリセットを確約。"),
        ("9月30日 · 23:12 UTC", "Astra 向けバンク枠付与", "Astra未利用ユーザーに対し、1日1回のバンク型リセット枠を補填付与。", "+15 pts", "neutral", "【機能補填】新機能ロールアウト待ちユーザーに対するクレジット型救済。"),
        ("9月26日 · 18:17 UTC", "週末前全体枠リセット", "週末の開発ラッシュに先立ち、サーバー側で枠全量回復が完了。", "+30 pts", "up", "【周期性】週末の開発者アクティビティ活性化を狙った金曜リセットの傾向を実証。"),
        ("9月22日 · 18:23 UTC", "GPT-6 Sol/Luna リリース", "新モデル配信とAPI恒久値下げに伴い、全アカウントに利用枠を一括注入。", "+28 pts", "up", "【大型アプデ】主要モデル切り替え時には恒例の一括枠リセットが発動。")
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


# Compact resets for client-side calendar navigation
compact_resets = []
for r in recs:
    d = r["at"][:10]
    t = r["type"]
    time_str = r["at"][11:16] if len(r["at"]) > 16 else ""
    lbl = f"{time_str} Hard Reset".strip() if t == "regular" else "Banked Reset"
    compact_resets.append({"d": d, "t": t, "l": lbl})
ALL_RESETS_JSON = json.dumps(compact_resets, ensure_ascii=False)

def get_cal_js(code):
    is_zh = "true" if "zh" in code else "false"
    is_ja = "true" if code == "ja" else "false"
    return f"""
<script>
(function(){{
  var resets = {ALL_RESETS_JSON};
  var resetMap = {{}};
  for(var i=0; i<resets.length; i++){{
    var r = resets[i];
    if(!resetMap[r.d]) resetMap[r.d] = [];
    resetMap[r.d].push(r);
  }}

  var minYear = 2025, minMonth = 8;
  var maxYear = 2026, maxMonth = 9;
  var curYear = 2026, curMonth = 9;

  var monthNamesEn = ["January","February","March","April","May","June","July","August","September","October","November","December"];
  var isZh = {is_zh};
  var isJa = {is_ja};

  var titleEl = document.getElementById('calMonthTitle');
  var badgeEl = document.getElementById('calMonthBadge');
  var wrapEl = document.getElementById('calTableWrap');
  var prevBtn = document.getElementById('calPrevBtn');
  var nextBtn = document.getElementById('calNextBtn');

  function renderCal(){{
    if(!wrapEl) return;
    if(isZh || isJa) {{
      if(titleEl) titleEl.textContent = curYear + "年 " + (curMonth + 1) + "月";
    }} else {{
      if(titleEl) titleEl.textContent = monthNamesEn[curMonth] + " " + curYear;
    }}

    var ymPrefix = curYear + "-" + (curMonth < 9 ? "0" + (curMonth + 1) : (curMonth + 1));
    var monthResets = 0;
    for(var k in resetMap){{
      if(k.indexOf(ymPrefix) === 0){{
        monthResets += resetMap[k].length;
      }}
    }}
    if(badgeEl){{
      if(isZh) badgeEl.textContent = monthResets + " 次重置";
      else if(isJa) badgeEl.textContent = monthResets + " 回リセット";
      else badgeEl.textContent = monthResets + (monthResets === 1 ? " Reset" : " Resets");
    }}

    if(prevBtn) prevBtn.disabled = (curYear === minYear && curMonth === minMonth);
    if(nextBtn) nextBtn.disabled = (curYear === maxYear && curMonth === maxMonth);

    var firstDay = new Date(curYear, curMonth, 1).getDay();
    var daysInCur = new Date(curYear, curMonth + 1, 0).getDate();
    var daysInPrev = new Date(curYear, curMonth, 0).getDate();

    var html = '<table class="cal-table"><thead><tr>';
    var dayHeaders = (isZh ? ["周日","周一","周二","周三","周四","周五","周六"] : (isJa ? ["日","月","火","水","木","金","土"] : ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]));
    for(var h=0; h<7; h++) html += '<th>' + dayHeaders[h] + '</th>';
    html += '</tr></thead><tbody><tr>';

    var cellCount = 0;
    for(var p = firstDay - 1; p >= 0; p--){{
      var dayNum = daysInPrev - p;
      var prevM = curMonth === 0 ? 12 : curMonth;
      var prevY = curMonth === 0 ? curYear - 1 : curYear;
      var pDate = prevY + "-" + (prevM < 10 ? "0" + prevM : prevM) + "-" + (dayNum < 10 ? "0" + dayNum : dayNum);
      html += '<td class="pad"><span class="day-num">' + dayNum + '</span>' + getStamps(pDate) + '</td>';
      cellCount++;
    }}

    for(var d = 1; d <= daysInCur; d++){{
      if(cellCount > 0 && cellCount % 7 === 0){{
        html += '</tr><tr>';
      }}
      var cDate = ymPrefix + "-" + (d < 10 ? "0" + d : d);
      var isToday = (curYear === 2026 && curMonth === 9 && d === 5);
      var todayStyle = isToday ? ' style="color:var(--primary);font-weight:800"' : '';
      var todayLabel = isToday ? (isZh ? '<span style="font-size:9px;color:var(--muted)">观察中</span>' : (isJa ? '<span style="font-size:9px;color:var(--muted)">観測中</span>' : '<span style="font-size:9px;color:var(--muted)">Watching</span>')) : '';
      var dayDisplay = isToday ? d + (isZh ? ' (今天)' : (isJa ? ' (今日)' : ' (Today)')) : d;

      html += '<td><span class="day-num"' + todayStyle + '>' + dayDisplay + '</span>' + todayLabel + getStamps(cDate) + '</td>';
      cellCount++;
    }}

    var remaining = (7 - (cellCount % 7)) % 7;
    for(var n = 1; n <= remaining; n++){{
      var nextM = curMonth === 11 ? 1 : curMonth + 2;
      var nextY = curMonth === 11 ? curYear + 1 : curYear;
      var nDate = nextY + "-" + (nextM < 10 ? "0" + nextM : nextM) + "-" + (n < 10 ? "0" + n : n);
      html += '<td class="pad"><span class="day-num">' + n + '</span>' + getStamps(nDate) + '</td>';
      cellCount++;
    }}
    html += '</tr></tbody></table>';
    wrapEl.innerHTML = html;
  }}

  function getStamps(dateStr){{
    var list = resetMap[dateStr];
    if(!list || list.length === 0) return '';
    var out = '';
    for(var i=0; i<list.length; i++){{
      var item = list[i];
      out += '<span class="day-stamp ' + item.t + '">' + item.l + '</span>';
    }}
    return out;
  }}

  if(prevBtn) prevBtn.addEventListener('click', function(){{
    if(curYear === minYear && curMonth === minMonth) return;
    if(curMonth === 0){{ curMonth = 11; curYear--; }}
    else {{ curMonth--; }}
    renderCal();
  }});

  if(nextBtn) nextBtn.addEventListener('click', function(){{
    if(curYear === maxYear && curMonth === maxMonth) return;
    if(curMonth === 11){{ curMonth = 0; curYear++; }}
    else {{ curMonth++; }}
    renderCal();
  }});

  renderCal();
}})();
</script>
"""


CAL_TABLE_HTML = '''<table class="cal-table">
  <thead>
    <tr>
      <th>Sun</th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="pad"><span class="day-num">27</span></td>
      <td class="pad"><span class="day-num">28</span></td>
      <td class="pad"><span class="day-num">29</span></td>
      <td class="pad"><span class="day-num">30</span><span class="day-stamp banked">Banked Reset</span></td>
      <td><span class="day-num">1</span></td>
      <td><span class="day-num">2</span><span class="day-stamp regular">21:18 Hard Reset</span></td>
      <td><span class="day-num">3</span></td>
    </tr>
    <tr>
      <td><span class="day-num">4</span></td>
      <td><span class="day-num" style="color:var(--primary);font-weight:800">5 (Today)</span><span style="font-size:9px;color:var(--muted)">Watching</span></td>
      <td><span class="day-num">6</span></td>
      <td><span class="day-num">7</span></td>
      <td><span class="day-num">8</span></td>
      <td><span class="day-num">9</span></td>
      <td><span class="day-num">10</span></td>
    </tr>
    <tr>
      <td><span class="day-num">11</span></td><td><span class="day-num">12</span></td><td><span class="day-num">13</span></td><td><span class="day-num">14</span></td><td><span class="day-num">15</span></td><td><span class="day-num">16</span></td><td><span class="day-num">17</span></td>
    </tr>
    <tr>
      <td><span class="day-num">18</span></td><td><span class="day-num">19</span></td><td><span class="day-num">20</span></td><td><span class="day-num">21</span></td><td><span class="day-num">22</span></td><td><span class="day-num">23</span></td><td><span class="day-num">24</span></td>
    </tr>
    <tr>
      <td><span class="day-num">25</span></td><td><span class="day-num">26</span></td><td><span class="day-num">27</span></td><td><span class="day-num">28</span></td><td><span class="day-num">29</span></td><td><span class="day-num">30</span></td><td><span class="day-num">31</span></td>
    </tr>
  </tbody>
</table>'''

def render_direct_ans(code):
    if "zh" in code:
        return f'''<div class="direct-ans-banner">
  <div class="dab-left">
    <span class="dab-badge"><span class="dot"></span> 实时状态判定：低放水概率 · 观察中</span>
    <div class="dab-h">Codex 今天会全网重置吗？ <strong>今日暂无放水迹象（{prob}% 概率）</strong></div>
    <div class="dab-p">今日尚未监测到官方全量重置记录。最近一次官方放水发生在 <strong>{days_since_str} 前</strong>（{last_date}）。建议保持正常开发节奏，下方可测算个人 5 小时解锁倒计时。</div>
  </div>
  <div class="dab-right">
    <a href="#calculator" class="dab-btn">测算个人解锁时间 ↓</a>
  </div>
</div>'''
    elif code == "ja":
        return f'''<div class="direct-ans-banner">
  <div class="dab-left">
    <span class="dab-badge"><span class="dot"></span> リアルタイム判定：低確率 · 観測中</span>
    <div class="dab-h">Codexは今日リセットされますか？ <strong>現時点でリセットなし（確率 {prob}%）</strong></div>
    <div class="dab-p">本日公式による一括リセットは記録されていません。直近のリセットは <strong>{days_since_str} 前</strong>（{last_date}）です。個人向け5時間制限の回復時間は以下より算出できます。</div>
  </div>
  <div class="dab-right">
    <a href="#calculator" class="dab-btn">個人の解除時間を計算 ↓</a>
  </div>
</div>'''
    else:
        return f'''<div class="direct-ans-banner">
  <div class="dab-left">
    <span class="dab-badge"><span class="dot"></span> LIVE VERDICT: LOW SIGNAL · WATCHING</span>
    <div class="dab-h">Will Codex reset today? <strong>Not yet ({prob}% probability)</strong></div>
    <div class="dab-p">No global reset recorded today. The last verified reset was <strong>{days_since_str} ago</strong> ({last_date}). Normal building conditions — calculate your personal 5-hour rolling window below.</div>
  </div>
  <div class="dab-right">
    <a href="#calculator" class="dab-btn">Check Personal Recovery ↓</a>
  </div>
</div>'''

def render_guides(code):
    if "zh" in code:
        g1 = ("底层架构", "当你触发 Codex 限流时，到底重置了什么？", "解析 5 小时滑动 Token 桶、上下文窗口容量、深度思考（Thinking Effort）与智能体共享配额的底层消耗机制。", "查看计算机制 →")
        g2 = ("重置机制", "Hard Reset（硬重置）与 Banked Reset（存续额度）的区别", "官方突发全网放水会立即清空全员限流；而存续额度（Banked Reset）则作为补偿抵扣券存放，可随时主动激活。", "查看历史验证记录 →")
        g3 = ("故障排查", "服务宕机（Outage）、配额耗尽还是本地被限流？", "3 步精准自查指南：教你快速判断究竟是 OpenAI 服务器遭遇故障，还是你个人的订阅周期达到了上限。", "查看应急替代方案 →")
    elif code == "ja":
        g1 = ("アーキテクチャ", "Codex制限に達した際、実際に何がリセットされるのか？", "5時間のローリングTokenバケット、コンテキストウィンドウ、Reasoning Effort、Agent共有枠の消費モデルを解説。", "計算ロジックを見る →")
        g2 = ("メカニズム", "ハードリセット（即時全量）とバンク枠（補填クレジット）の違い", "突発的な全体リセットは全アカウントの制限を一括解除し、バンク枠はユーザーが任意で適用可能な補填枠です。", "検証ログを見る →")
        g3 = ("トラブル診断", "サーバー障害（Outage）か、利用制限か、スロットルか？", "OpenAI全体のインフラ障害なのか、個人プランの上限到達なのかを3秒で切り分ける実践的診断フロー。", "代替ツールを見る →")
    else:
        g1 = ("ARCHITECTURE", "What actually resets when you hit a Codex limit?", "Understand rolling 5-hour token buckets, context window saturation, reasoning effort depth, and shared agentic pools.", "Explore calculations →")
        g2 = ("MECHANICS", "Hard Reset vs. Banked Reset: Key differences", "Spontaneous global flushes instantly clear quota for all subscribers, while banked resets store redeemable vouchers for later use.", "View verified history →")
        g3 = ("DIAGNOSIS", "Outage, quota limit, or server throttle?", "A practical 3-step diagnostic to identify whether OpenAI is suffering platform downtime or your account reached personal caps.", "See fallback tools →")

    return f'''<div class="guide-card">
  <div class="guide-tag">{esc(g1[0])}</div>
  <h3 class="guide-title">{esc(g1[1])}</h3>
  <p class="guide-desc">{esc(g1[2])}</p>
  <a href="#calculator" class="guide-link">{esc(g1[3])}</a>
</div>
<div class="guide-card">
  <div class="guide-tag">{esc(g2[0])}</div>
  <h3 class="guide-title">{esc(g2[1])}</h3>
  <p class="guide-desc">{esc(g2[2])}</p>
  <a href="#studio" class="guide-link">{esc(g2[3])}</a>
</div>
<div class="guide-card">
  <div class="guide-tag">{esc(g3[0])}</div>
  <h3 class="guide-title">{esc(g3[1])}</h3>
  <p class="guide-desc">{esc(g3[2])}</p>
  <a href="#tools" class="guide-link">{esc(g3[3])}</a>
</div>'''

def render_monitors(code):
    return """<div class="monitor-card">
  <div class="monitor-avatar">
    <img class="monitor-avatar-img" src="/assets/avatars/tibo.jpg" alt="Tibo Sottiaux" width="42" height="42" loading="lazy">
  </div>
  <div class="monitor-info">
    <div class="monitor-name">Tibo Sottiaux <span class="monitor-tag p1">PRIMARY</span></div>
    <div class="monitor-role">Head of Codex, OpenAI</div>
    <a class="monitor-handle" href="https://x.com/thsottiaux" target="_blank" rel="noopener nofollow">@thsottiaux &#x2197;</a>
  </div>
</div>
<div class="monitor-card">
  <div class="monitor-avatar">
    <img class="monitor-avatar-img" src="/assets/avatars/sama.jpg" alt="Sam Altman" width="42" height="42" loading="lazy">
  </div>
  <div class="monitor-info">
    <div class="monitor-name">Sam Altman <span class="monitor-tag p1">EXECUTIVE</span></div>
    <div class="monitor-role">CEO, OpenAI</div>
    <a class="monitor-handle" href="https://x.com/sama" target="_blank" rel="noopener nofollow">@sama &#x2197;</a>
  </div>
</div>
<div class="monitor-card">
  <div class="monitor-avatar">
    <img class="monitor-avatar-img" src="/assets/avatars/openai.jpg" alt="OpenAI Official" width="42" height="42" loading="lazy">
  </div>
  <div class="monitor-info">
    <div class="monitor-name">OpenAI Official <span class="monitor-tag p2">SYSTEM</span></div>
    <div class="monitor-role">Company Announcements</div>
    <a class="monitor-handle" href="https://x.com/OpenAI" target="_blank" rel="noopener nofollow">@OpenAI &#x2197;</a>
  </div>
</div>
<div class="monitor-card">
  <div class="monitor-avatar">
    <img class="monitor-avatar-img" src="/assets/avatars/agekhtman.jpg" alt="Alexander Gekhtman" width="42" height="42" loading="lazy">
  </div>
  <div class="monitor-info">
    <div class="monitor-name">Alexander Gekhtman <span class="monitor-tag p2">PRODUCT</span></div>
    <div class="monitor-role">Codex Product Lead</div>
    <a class="monitor-handle" href="https://x.com/agekhtman" target="_blank" rel="noopener nofollow">@agekhtman &#x2197;</a>
  </div>
</div>
<div class="monitor-card">
  <div class="monitor-avatar">
    <img class="monitor-avatar-img" src="/assets/avatars/openaidevs.jpg" alt="OpenAI Developers" width="42" height="42" loading="lazy">
  </div>
  <div class="monitor-info">
    <div class="monitor-name">OpenAI Developers <span class="monitor-tag p3">DEVREL</span></div>
    <div class="monitor-role">Platform & API Status</div>
    <a class="monitor-handle" href="https://x.com/OpenAIDevs" target="_blank" rel="noopener nofollow">@OpenAIDevs &#x2197;</a>
  </div>
</div>"""

def render_footer_dir(code, base_href):
    if "zh" in code:
        t1, t2, t3 = "AI 订阅与配额指南", "开发者效率工具箱", "机器可读与官方信源"
        l1 = [("ChatGPT Plus & Pro 配额上限解析", f"{base_href}#calculator"), ("Claude 3.7 Sonnet 独立额度规则", f"{base_href}#tools"), ("Cursor IDE Pro 全球定价与折扣", f"{base_href}#tools"), ("Windsurf 级联开发工具配额", f"{base_href}#tools"), ("OpenAI Codex 企业版团队席位", f"{base_href}#monitors")]
        l2 = [("5 小时限流滑动倒计时钟", f"{base_href}#calculator"), ("Tibo 官方放水信号监控台", f"{base_href}#studio"), ("2026 年 10 月放水历史日历", f"{base_href}#calendar-grid"), ("Codex 深度原理解析指南", f"{base_href}#guides"), ("Codex 限流常见问题知识库", f"{base_href}#faq")]
        l3 = [("AI 知识上下文 (llms.txt)", "/llms.txt"), ("全量问答知识库 (llms-full.txt)", "/llms-full.txt"), ("XML 网站地图 (sitemap.xml)", "/sitemap.xml"), ("OpenAI 实时状态监控 ↗", "https://status.openai.com"), ("Tibo 官方推特主页 ↗", "https://x.com/thsottiaux")]
    elif code == "ja":
        t1, t2, t3 = "AI サブスクリプション", "開発者向けツール", "機械可読データ & 公式ソース"
        l1 = [("ChatGPT Plus & Pro 利用枠ガイド", f"{base_href}#calculator"), ("Claude 3.7 Sonnet コーディング料金", f"{base_href}#tools"), ("Cursor IDE Pro グローバル価格", f"{base_href}#tools"), ("Windsurf Cascade 無料枠活用", f"{base_href}#tools"), ("OpenAI Codex Enterprise 枠仕様", f"{base_href}#monitors")]
        l2 = [("5時間制限ローリング回復時計", f"{base_href}#calculator"), ("Tibo リセット信号スイッチボード", f"{base_href}#studio"), ("2026年10月 リセット履歴カレンダー", f"{base_href}#calendar-grid"), ("Codex アーキテクチャ解説", f"{base_href}#guides"), ("Codex リセットFAQ知識ベース", f"{base_href}#faq")]
        l3 = [("AI向け要約 (llms.txt)", "/llms.txt"), ("完全知識ベース (llms-full.txt)", "/llms-full.txt"), ("サイトマップ (sitemap.xml)", "/sitemap.xml"), ("OpenAI 稼働状況 ↗", "https://status.openai.com"), ("Tibo 公式Xアカウント ↗", "https://x.com/thsottiaux")]
    else:
        t1, t2, t3 = "AI Subscriptions & Pricing", "Developer Utilities", "Machine Readable & Sources"
        l1 = [("ChatGPT Plus & Pro Quota Limits", f"{base_href}#calculator"), ("Claude 3.7 Sonnet Coding Pricing", f"{base_href}#tools"), ("Cursor IDE Pro Global Pricing", f"{base_href}#tools"), ("Windsurf AI Cascade Quota Pool", f"{base_href}#tools"), ("OpenAI Codex Enterprise Quotas", f"{base_href}#monitors")]
        l2 = [("5-Hour Rate Limit Recovery Clock", f"{base_href}#calculator"), ("Tibo Reset Signal Switchboard", f"{base_href}#studio"), ("Monthly Reset Calendar 2026-10", f"{base_href}#calendar-grid"), ("Understand Codex Limits Guide", f"{base_href}#guides"), ("Codex Rate Limit FAQ Knowledge Base", f"{base_href}#faq")]
        l3 = [("LLMs Context Summary (llms.txt)", "/llms.txt"), ("Full Knowledge Base (llms-full.txt)", "/llms-full.txt"), ("XML Sitemap Protocol", "/sitemap.xml"), ("OpenAI Live Status ↗", "https://status.openai.com"), ("Tibo on X ↗", "https://x.com/thsottiaux")]

    col1 = "".join(f'<li><a href="{href}">{esc(txt)}</a></li>' for txt, href in l1)
    col2 = "".join(f'<li><a href="{href}">{esc(txt)}</a></li>' for txt, href in l2)
    col3 = "".join(f'<li><a href="{href}"{" target=\"_blank\" rel=\"noopener nofollow\"" if href.startswith("http") else ""}>{esc(txt)}</a></li>' for txt, href in l3)

    return f'''<div class="footer-dir">
  <div class="dir-col">
    <div class="dir-title">{esc(t1)}</div>
    <ul class="dir-list">{col1}</ul>
  </div>
  <div class="dir-col">
    <div class="dir-title">{esc(t2)}</div>
    <ul class="dir-list">{col2}</ul>
  </div>
  <div class="dir-col">
    <div class="dir-title">{esc(t3)}</div>
    <ul class="dir-list">{col3}</ul>
  </div>
</div>'''

FAQS_DATA = {
    "en": [
        ("Will Codex reset today?", "There is currently a low probability (around 30%) of a spontaneous global reset today. No announcement has been posted by OpenAI or Tibo yet. The last verified reset was 2 days ago. We recommend relying on your personal 5-hour rolling recovery window."),
        ("Is there an official schedule for Codex resets?", "No. Global resets are irregular and non-guaranteed. They are manually triggered by OpenAI leadership (chiefly Tibo Sottiaux) to celebrate user milestones, deploy major model architecture upgrades, or compensate for prolonged cluster outages."),
        ("What is the difference between a regular reset and a banked reset?", "A regular (hard) reset immediately clears token usage limits for every paid user on the platform. A banked reset provides a stored daily credit voucher that you can manually activate whenever you hit a quota wall."),
        ("Do banked resets expire?", "Banked resets generally persist across multiple days during promotional rollout periods, but OpenAI reserves the right to expire unused promotional tokens upon general availability of the relevant feature."),
        ("Tibo posted a reset on X, but my usage limit hasn't changed. Why?", "Global resets roll out across distributed server clusters over a 30 to 90 minute propagation window. If your account does not reflect the refill immediately, wait for full edge CDN synchronization or log out and back in."),
        ("Can I purchase extra Codex quota or pay for an instant reset?", "Currently, OpenAI does not sell individual one-off quota refills for Codex. The only official ways to increase capacity are upgrading from Plus to Pro/Enterprise or waiting for your rolling 5-hour window to unlock."),
        ("How can I keep coding without waiting for quota to recover?", "You can instantly switch to alternative top-tier agentic IDEs such as Cursor IDE, Windsurf, or Claude Code. Each maintains an independent monthly usage pool and provides generous free tier credits.")
    ],
    "zh": [
        ("Codex 今天会全网重置吗？", "目前今日全网放水的概率偏低（约 30%）。OpenAI 官方或 Tibo 尚未发布放水通知。最近一次全量重置发生在 2 天前。建议优先关注个人 5 小时滑动恢复倒计时。"),
        ("官方是否有固定的 Codex 重置时间表？", "没有。全网公共重置没有固定排期，完全由 OpenAI 核心团队（主要是 Tibo Sottiaux）视工程与公关节点手动触发，例如重大模型上线、活跃用户突破里程碑或大规模集群故障后的补偿。"),
        ("常规硬重置（Hard Reset）与存续额度（Banked Reset）有什么区别？", "常规硬重置会瞬间清空全体付费用户的限流状态；而存续额度（Banked Reset）相当于一张存放在账户里的额度抵扣券，在你触发限流时可随时手动点击抵扣。"),
        ("存续额度（Banked Reset）会过期失效吗？", "在特定功能灰度期内，存续额度通常可以跨天累积；但在新架构全量开放后，官方通常会清空未使用的活动存续额度。"),
        ("Tibo 在推特宣布了重置，为什么我的额度没有恢复？", "全网重置需要在全球各区域数据中心逐步同步，通常需要 30 到 90 分钟的生效窗口。如果未立刻体现，请耐心等待边缘节点刷新，或尝试重新登录。"),
        ("我可以单独花钱购买 Codex 额外额度或购买即时重置吗？", "目前 OpenAI 官方不提供单次付费重置功能。要获得更多额度，只能将 Plus 升级为 Pro 或 Enterprise 企业版，或者等待 5 小时滑动窗口自动恢复。"),
        ("额度打满等不及恢复时，如何继续高效写代码？", "建议无缝切换至 Cursor IDE、Windsurf 或 Claude Code 等顶尖备用 AI 编程工具。这些工具拥有独立的免费调用池与专属额度，无需干等。")
    ],
    "ja": [
        ("Codexは今日リセットされますか？", "本日の全体リセット確率は約30%と低めです。公式やTiboからの告知はまだありません。直近のリセットは2日前です。個人向けの5時間ローリング枠回復を優先してご確認ください。"),
        ("Codexのリセットに決まったスケジュールはありますか？", "ありません。全体リセットは定例ではなく、OpenAIのCodex責任者Tiboの裁量により、新モデル公開やユーザー数達成、大規模障害のお詫びとして不定期に発動されます。"),
        ("通常リセットとバンク枠（Banked Reset）の違いは何ですか？", "通常リセットは全有料ユーザーの利用枠を即座に満タンに戻します。バンク枠はアカウントに付与される保存型チケットで、制限到達時に任意で使用可能です。"),
        ("バンク枠に有効期限はありますか？", "特定の機能テスト期間中は保持されますが、正式リリース時に未使用のボーナス枠が失効する場合があります。"),
        ("TiboがXでリセットを発表したのに枠が戻りません。なぜ？", "世界中のサーバークラスタへの配信には30〜90分程度かかります。反映されない場合は時間をおいて再ログインをお試しください。"),
        ("Codexの枠を追加購入したりリセットをお金で買えますか？", "現在、都度課金での単発リセット購入はできません。枠を増やすにはPro/Enterpriseへのアップグレードか、5時間の自然回復を待つ必要があります。"),
        ("制限解除を待たずに開発を続ける最善の方法は？", "Cursor IDE、Windsurf、Claude Codeなどの代替AIエディタへ一時的に切り替えることを推奨します。独立した無料枠ですぐに開発を再開できます。")
    ]
}

def render_faq_items(code):
    faqs = FAQS_DATA.get("zh" if "zh" in code else ("ja" if code == "ja" else "en"), FAQS_DATA["en"])
    return "".join(f'''<div class="faq-i">
  <div class="faq-q">{esc(q)}</div>
  <div class="faq-a">{esc(a)}</div>
</div>''' for q, a in faqs)

def get_faq_schema(code):
    faqs = FAQS_DATA.get("zh" if "zh" in code else ("ja" if code == "ja" else "en"), FAQS_DATA["en"])
    return [{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in faqs]

# --- Nav & Language Switcher with Subpage Routing Support ---
def render_nav(code, dir_prefix, active_slug):
    # active_slug: "radar" | "today" | "history" | "methodology"
    base = f"/{dir_prefix}/" if dir_prefix else "/"
    today_href = f"/{dir_prefix}/reset-today/" if dir_prefix else "/reset-today/"
    hist_href = f"/{dir_prefix}/history/" if dir_prefix else "/history/"
    meth_href = f"/{dir_prefix}/methodology/" if dir_prefix else "/methodology/"

    if "zh" in code:
        labels = ("雷达总览", "今日重置", "历史档案", "预测算法")
    elif code == "ja":
        labels = ("レーダー", "今日のリセット", "履歴アーカイブ", "予測モデル")
    elif code == "ko":
        labels = ("레이더", "오늘의 리셋", "리셋 기록", "예측 알고리즘")
    elif code == "es":
        labels = ("Radar", "Reset Hoy", "Historial", "Metodología")
    elif code == "de":
        labels = ("Radar", "Reset Heute", "Historie", "Methodik")
    elif code == "fr":
        labels = ("Radar", "Reset Aujourd'hui", "Historique", "Méthodologie")
    else:
        labels = ("Radar", "Reset Today", "History", "Methodology")

    c1 = "nav-item on" if active_slug == "radar" else "nav-item"
    c2 = "nav-item on" if active_slug == "today" else "nav-item"
    c3 = "nav-item on" if active_slug == "history" else "nav-item"
    c4 = "nav-item on" if active_slug == "methodology" else "nav-item"

    return f'''<a class="{c1}" href="{base}">{labels[0]}</a>
<a class="{c2}" href="{today_href}">{labels[1]}</a>
<a class="{c3}" href="{hist_href}">{labels[2]}</a>
<a class="{c4}" href="{meth_href}">{labels[3]}</a>'''

def build_lang_items(current_code, page_slug):
    # Preserves current subpage on language switch!
    sub = f"{page_slug}/" if page_slug else ""
    out = []
    for code, d, name, loc, url in LANGS:
        cls = "lang-item on" if code == current_code else "lang-item"
        rel_path = f"/{d}/{sub}" if d else f"/{sub}"
        out.append(f'<a class="{cls}" href="{rel_path}" hreflang="{code}"><span>{name}</span><code>{code}</code></a>')
    return "".join(out)

def build_hreflang(page_slug):
    sub = f"{page_slug}/" if page_slug else ""
    parts = [f'<link rel="alternate" hreflang="x-default" href="https://codexresetlive.com/{sub}">',
             f'<link rel="alternate" hreflang="en" href="https://codexresetlive.com/{sub}">']
    for code, d, name, loc, url in LANGS:
        if code != "en":
            target_url = f"https://codexresetlive.com/{d}/{sub}"
            parts.append(f'<link rel="alternate" hreflang="{code}" href="{target_url}">')
    return "\n".join(parts)

# --- SITEMAP TRACKER ---
SITEMAP_URLS = []

print("STARTING MULTIPAGE GENERATION ENGINE (40 PAGES TOTAL)...")

# --- PAGE BUILDERS ---

# 1. Full History Table Generator for History Page
def render_full_hist_table(code):
    rows = []
    for r in recs[::-1]:
        t = r["type"]
        badge_cls = "badge " + t
        utc_ts = r["at"][:16].replace("T", " ")
        rows.append(f'''<tr>
  <td class="num" style="white-space:nowrap;font-weight:600"><span data-utc="{r["at"]}">{utc_ts} UTC</span></td>
  <td><span class="{badge_cls}">{t.upper()}</span></td>
  <td style="line-height:1.5">{esc(r["text"])}</td>
  <td style="white-space:nowrap;text-align:right"><a href="{r["url"]}" target="_blank" rel="noopener nofollow" style="color:var(--primary);font-size:12px;font-weight:600">View on X ↗</a></td>
</tr>''')
    return "".join(rows)

for code, d, name, loc, base_url in LANGS:
    t = I18N[code]
    out_dir = (SITE_DIR / d) if d else SITE_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Common variables
    alert_t = "Get Realtime Reset Prediction Alerts" if code=="en" else ("获取实时重置预警广播" if "zh" in code else ("リセット予測通知を受け取る" if code=="ja" else "Recibe Alertas en Tiempo Real"))
    alert_d = "Alerts sent when the next 48h reset chance exceeds 80% or when verified by Tibo." if code=="en" else ("当未来48小时重置概率超过80%或Tibo发布确认推文时立即通知。" if "zh" in code else ("48時間以内のリセット確率が80%を超えるか、公式確認された際に通知。" if code=="ja" else "Alertas cuando la probabilidad supere el 80% o se confirme."))
    notify_me = "Notify Me" if code=="en" else ("立即订阅" if "zh" in code else ("通知登録" if code=="ja" else "Avisarme"))
    sub_count = "70,760+ Subscribed" if code=="en" else ("已订阅 70,760+" if "zh" in code else ("購読者 70,760人+" if code=="ja" else "70,760+ Suscriptores"))

    studio_t = "Live Signals & Verdict Breakdown" if code=="en" else ("实时信号源与模型判定明细" if "zh" in code else ("リアルタイムシグナルと判定詳細" if code=="ja" else "Señales en Vivo y Veredicto"))
    studio_s = "Transparent factor weighting updated continuously from public developer signals." if code=="en" else ("持续同步 OpenAI 核心团队与开发社区一手信号，算法权重完全透明。" if "zh" in code else ("公式開発者の投稿とコミュニティシグナルをリアルタイム集計。" if code=="ja" else "Ponderación transparente basada en señales oficiales."))
    col1_t = "Why the number moved" if code=="en" else ("模型积分异动明细" if "zh" in code else ("スコア変動要因" if code=="ja" else "Por qué varió el puntaje"))
    col3_t = "Signal Switchboard" if code=="en" else ("8维信号控制台" if "zh" in code else ("シグナル制御盤" if code=="ja" else "Panel de Señales"))

    cal_radar_t = "Monthly Reset Calendar & Radar" if code=="en" else ("月度重置日历与放水雷达" if "zh" in code else ("月間リセットカレンダー" if code=="ja" else "Calendario Mensual de Resets"))
    cal_radar_s = "Historical verified cadence across October 2026. Spot weekly patterns before coding sprints." if code=="en" else ("2026 年 10 月全量放水与存续额度真实分布，助你在高频编码前掌握规律。" if "zh" in code else ("2026年10月の確定リセット実績。開発ラッシュ前に周期を確認。" if code=="ja" else "Historial de resets verificados en octubre 2026."))

    guides_t = "Understand Codex Limits & Reset Mechanics" if code=="en" else ("深入理解 Codex 限制与重置机制" if "zh" in code else ("Codexの制限とリセット仕様を理解する" if code=="ja" else "Comprende los Límites de Codex"))
    guides_s = "Essential guides on token architecture, banked rollover credits, and server diagnosis." if code=="en" else ("深度解析 Token 滑动窗口、存续抵扣券与服务器故障诊断指南。" if "zh" in code else ("Tokenウィンドウ、バンク枠、障害診断の完全ガイド。" if code=="ja" else "Guías clave sobre arquitectura de tokens y diagnóstico."))

    monitors_t = "Who We Monitor for Reset Signals" if code=="en" else ("重置信号源监控权威矩阵" if "zh" in code else ("監視対象のアカウント一覧" if code=="ja" else "A Quiénes Monitoreamos"))
    monitors_s = "Primary signals are prioritized based on executive proximity, technical leadership, and historical accuracy." if code=="en" else ("根据决策权、工程领导力与历史命中率多维度加权的核心信源矩阵。" if "zh" in code else ("経営陣、技術リーダー、過去の的中実績に基づく監視網。" if code=="ja" else "Fuentes priorizadas según proximidad y autoridad técnica."))

    # =========================================================================
    # PAGE 1: RADAR (HOME)
    # =========================================================================
    p1_path = out_dir / "index.html"
    p1_canon = f"https://codexresetlive.com/{d}/" if d else "https://codexresetlive.com/"
    p1_title = f"{t['h1_a'].rstrip('?')} {t['h1_b']} | Codex Reset Radar"
    p1_desc = t["hero_p"]
    
    p1_schema = {
        "@context":"https://schema.org",
        "@graph":[
            {"@type":"WebApplication","name":"Codex Reset Radar",
             "url":p1_canon,"applicationCategory":"UtilitiesApplication","operatingSystem":"Any",
             "isAccessibleForFree":True,"inLanguage":loc,
             "description":p1_desc},
            {"@type":"BreadcrumbList","itemListElement":
                [{"@type":"ListItem","position":1,"name":"Home","item":"https://codexresetlive.com/"}] +
                ([] if code=="en" else [{"@type":"ListItem","position":2,"name":name,"item":p1_canon}])},
            {"@type":"FAQPage","inLanguage":loc,"mainEntity":get_faq_schema(code)}
        ]
    }

    # Header replacement
    p1_head = HEAD.replace("__LANG__", code).replace("__TITLE__", esc(p1_title)).replace("__DESC__", esc(p1_desc))
    p1_head = p1_head.replace("__CANONICAL__", p1_canon).replace("__LOCALE__", loc)
    p1_head = p1_head.replace("__HREFLANG__", build_hreflang(""))
    p1_head = p1_head.replace("__SCHEMA__", json.dumps(p1_schema, ensure_ascii=False, indent=2))

    p1_body = BODY.replace("__HOME_PATH__", f"/{d}/" if d else "/")
    p1_body = p1_body.replace("__NAV_ITEMS__", render_nav(code, d, "radar"))
    p1_body = p1_body.replace("__BRAND_SUB__", esc(t["brand_sub"])).replace("__LIVE__", esc(t["live"]))
    p1_body = p1_body.replace("__LANG_LABEL__", esc(t["lang_label"])).replace("__LANG_NAME__", esc(name))
    p1_body = p1_body.replace("__LANG_ITEMS__", build_lang_items(code, ""))

    p1_body = p1_body.replace("__DIRECT_ANS_BANNER__", render_direct_ans(code))
    p1_body = p1_body.replace("__BADGE__", esc(t["badge"])).replace("__H1_A__", esc(t["h1_a"])).replace("__H1_B__", esc(t["h1_b"])).replace("__HERO_P__", esc(t["hero_p"]))
    p1_body = p1_body.replace("__GAUGE_LBL__", esc(t["gauge_lbl"])).replace("__GAUGE_TAG__", esc(t["gauge_tag"])).replace("__GAUGE_CAP__", esc(t["gauge_cap"]))
    p1_body = p1_body.replace("__GF_1__", esc(t["gf_1"])).replace("__GF_2__", esc(t["gf_2"])).replace("__LAST_DATE__", esc(last_date)).replace("__DAYS_SINCE__", esc(days_since_str))
    p1_body = p1_body.replace("__PULSE_T__", "48-Hour Forecast Pulse" if code=="en" else ("未来48小时预测脉冲曲线" if "zh" in code else "48時間予測パルス曲線"))
    p1_body = p1_body.replace("__PULSE_SUB__", "Realtime probability trajectory & verified event markers" if code=="en" else ("实时概率推演轨迹与已确认事件标记" if "zh" in code else "リアルタイム確率軌跡と確認済みイベント"))
    p1_body = p1_body.replace("__PULSE_SVG__", pulse_svg)

    p1_body = p1_body.replace("__ALERT_T__", esc(alert_t)).replace("__ALERT_D__", esc(alert_d)).replace("__NOTIFY_ME__", esc(notify_me)).replace("__SUBSCRIBER_COUNT__", esc(sub_count))
    p1_body = p1_body.replace("__RO_1_L__", "OpenAI Status").replace("__RO_1_S__", "API & Platform healthy")
    p1_body = p1_body.replace("__RO_2_L__", "Tibo Watch").replace("__RO_2_S__", "55 Verified posts monitored")
    p1_body = p1_body.replace("__RO_3_L__", "Days Since Reset").replace("__RO_3_S__", f"Last: {last_date}")
    p1_body = p1_body.replace("__RO_4_L__", "Active Developers").replace("__RO_4_S__", "43M+ Estimated users")

    p1_body = p1_body.replace("__STUDIO_T__", esc(studio_t)).replace("__STUDIO_S__", esc(studio_s)).replace("__COL1_T__", esc(col1_t))
    p1_body = p1_body.replace("__MOVE_ITEMS__", render_move_items(code)).replace("__STREAM_ITEMS__", STREAM_ITEMS)
    p1_body = p1_body.replace("__COL3_T__", esc(col3_t)).replace("__SWITCH_ITEMS__", SWITCH_ITEMS)

    p1_body = p1_body.replace("__CAL_RADAR_T__", esc(cal_radar_t)).replace("__CAL_RADAR_S__", esc(cal_radar_s)).replace("__CAL_TABLE_HTML__", CAL_TABLE_HTML)

    p1_body = p1_body.replace("__CALC_T__", esc(t["calc_t"])).replace("__CALC_S__", esc(t["calc_s"]))
    p1_body = p1_body.replace("__TZ_L__", esc(t["tz_l"])).replace("__TZ_LOCAL__", esc(t["tz_local"])).replace("__UNLOCK_L__", esc(t["unlock_l"])).replace("__CALCULATING__", esc(t["calculating"]))
    p1_body = p1_body.replace("__PRESET_L__", esc(t["preset_l"])).replace("__P1__", esc(t["p1"])).replace("__P2__", esc(t["p2"])).replace("__P3__", esc(t["p3"])).replace("__P4__", esc(t["p4"]))
    p1_body = p1_body.replace("__U_H__", esc(t["u_h"])).replace("__U_M__", esc(t["u_m"])).replace("__U_S__", esc(t["u_s"]))
    p1_body = p1_body.replace("__PROG_L__", esc(t["prog_l"])).replace("__RECOVERED__", esc(t["recovered"])).replace("__NOTIFY__", esc(t["notify"])).replace("__CAL__", esc(t["cal"]))

    p1_body = p1_body.replace("__GUIDES_T__", esc(guides_t)).replace("__GUIDES_S__", esc(guides_s)).replace("__GUIDES_HTML__", render_guides(code))
    p1_body = p1_body.replace("__MONITORS_T__", esc(monitors_t)).replace("__MONITORS_S__", esc(monitors_s)).replace("__MONITOR_HTML__", render_monitors(code))

    p1_body = p1_body.replace("__TOOLS_T__", esc(t["tools_t"])).replace("__TOOLS_S__", esc(t["tools_s"]))
    p1_body = p1_body.replace("__TOOL1_D__", esc(t["tool1_d"])).replace("__TOOL1_A__", esc(t["tool1_a"]))
    p1_body = p1_body.replace("__TOOL2_D__", esc(t["tool2_d"])).replace("__TOOL2_A__", esc(t["tool2_a"]))
    p1_body = p1_body.replace("__TOOL3_D__", esc(t["tool3_d"])).replace("__TOOL3_A__", esc(t["tool3_a"]))

    p1_body = p1_body.replace("__FAQ_T__", esc(t["faq_t"])).replace("__FAQ_ITEMS__", render_faq_items(code))
    p1_body = p1_body.replace("__FOOTER_DIR_HTML__", render_footer_dir(code, f"/{d}/" if d else "/"))
    p1_body = p1_body.replace("__FOOT__", esc(t["foot"])).replace("__FOOT_SRC__", esc(t["foot_src"]))

    p1_body = p1_body.replace("__PROB_NUM__", str(prob))
    p1_body = p1_body.replace("__TZ_TOAST__", esc(t["tz_toast"])).replace("__MIN_TOAST__", esc(t["min_toast"]))
    p1_body = p1_body.replace("__NO_NOTIF__", esc(t["no_notif"])).replace("__NOTIF_ON__", esc(t["notif_on"]))
    p1_body = p1_body.replace("__NOTIF_SET__", esc(t["notif_set"])).replace("__NOTIF_BLOCK__", esc(t["notif_block"]))

    p1_path.write_text(p1_head + "\n" + p1_body.replace('</body>', get_cal_js(code) + '</body>'), encoding="utf-8")
    SITEMAP_URLS.append((p1_canon, "1.0"))

    # =========================================================================
    # PAGE 2: RESET TODAY (/reset-today/)
    # =========================================================================
    p2_dir = out_dir / "reset-today"
    p2_dir.mkdir(parents=True, exist_ok=True)
    p2_path = p2_dir / "index.html"
    p2_canon = f"https://codexresetlive.com/{d}/reset-today/" if d else "https://codexresetlive.com/reset-today/"

    p2_title = "Did Codex Reset Today? Live Quota Status & Verdict | Codex Reset Radar" if code=="en" else ("Codex 今天重置了吗？今日配额放水实时判定 | Codex Reset Radar" if "zh" in code else ("Codexは今日リセットされましたか？リアルタイム判定 | Codex Reset Radar" if code=="ja" else "Did Codex Reset Today? | Codex Reset Radar"))
    p2_desc = f"Did Codex quota reset today? Live verified verdict from Tibo Sottiaux and OpenAI. Probability currently at {prob}%. Track token limits, 48h forecasts, and personal 5-hour recovery." if code=="en" else (f"Codex 今天重置了吗？官方最新放水判定结果已更新。当前 48 小时放水概率为 {prob}%。提供一手推文证据与个人 5 小时解锁计算器。" if "zh" in code else f"Codexの利用枠は本日リセットされたのか？最新の公式確認シグナルを判定。現在のリセット確率は{prob}%。")

    p2_schema = {
        "@context":"https://schema.org",
        "@graph":[
            {"@type":"WebPage","name":p2_title,"url":p2_canon,"inLanguage":loc,"description":p2_desc},
            {"@type":"BreadcrumbList","itemListElement":[
                {"@type":"ListItem","position":1,"name":"Home","item":p1_canon},
                {"@type":"ListItem","position":2,"name":"Reset Today","item":p2_canon}
            ]},
            {"@type":"FAQPage","inLanguage":loc,"mainEntity":get_faq_schema(code)}
        ]
    }

    p2_head = HEAD.replace("__LANG__", code).replace("__TITLE__", esc(p2_title)).replace("__DESC__", esc(p2_desc))
    p2_head = p2_head.replace("__CANONICAL__", p2_canon).replace("__LOCALE__", loc)
    p2_head = p2_head.replace("__HREFLANG__", build_hreflang("reset-today"))
    p2_head = p2_head.replace("__SCHEMA__", json.dumps(p2_schema, ensure_ascii=False, indent=2))

    p2_body = p1_body # reuse body but change nav and hero title
    p2_body = p2_body.replace(render_nav(code, d, "radar"), render_nav(code, d, "today"))
    p2_body = p2_body.replace(build_lang_items(code, ""), build_lang_items(code, "reset-today"))
    p2_body = p2_body.replace(esc(t["h1_a"]), "Did Codex Reset" if code=="en" else ("Codex 今天" if "zh" in code else "Codexは今日"))
    p2_body = p2_body.replace(esc(t["h1_b"]), "Today?" if code=="en" else ("重置了吗？" if "zh" in code else "リセットされましたか？"))

    p2_path.write_text(p2_head + "\n" + p2_body.replace('</body>', get_cal_js(code) + '</body>'), encoding="utf-8")
    SITEMAP_URLS.append((p2_canon, "0.9"))

    # =========================================================================
    # PAGE 3: HISTORY (/history/ & /reset-history/)
    # =========================================================================
    p3_dir = out_dir / "history"
    p3_dir.mkdir(parents=True, exist_ok=True)
    p3_path = p3_dir / "index.html"
    p3_canon = f"https://codexresetlive.com/{d}/history/" if d else "https://codexresetlive.com/history/"

    p3_title = "Codex Reset History & Archive: All Verified Public Resets | Codex Reset Radar" if code=="en" else ("Codex 历史重置完整档案与日历记录 | Codex Reset Radar" if "zh" in code else ("Codex リセット全履歴・確定アーカイブ | Codex Reset Radar" if code=="ja" else "Codex Reset History | Codex Reset Radar"))
    p3_desc = f"Complete verified historical archive of all {len(recs)} public Codex quota resets announced by Tibo Sottiaux since September 2025. Track regular hard flushes, banked credits, and cadence trends." if code=="en" else (f"自 2025 年 9 月以来官方宣布的全部 {len(recs)} 次 Codex 公共额度重置完整历史档案与日历记录。一手推文证据与放水周期规律深度梳理。" if "zh" in code else f"2025年9月以降に発表された全{len(recs)}回のCodexリセット履歴の完全アーカイブ。")

    p3_schema = {
        "@context":"https://schema.org",
        "@graph":[
            {"@type":"DataCatalog","name":"Codex Quota Reset History Archive","url":p3_canon,"inLanguage":loc,"description":p3_desc},
            {"@type":"BreadcrumbList","itemListElement":[
                {"@type":"ListItem","position":1,"name":"Home","item":p1_canon},
                {"@type":"ListItem","position":2,"name":"History","item":p3_canon}
            ]}
        ]
    }

    p3_head = HEAD.replace("__LANG__", code).replace("__TITLE__", esc(p3_title)).replace("__DESC__", esc(p3_desc))
    p3_head = p3_head.replace("__CANONICAL__", p3_canon).replace("__LOCALE__", loc)
    p3_head = p3_head.replace("__HREFLANG__", build_hreflang("history"))
    p3_head = p3_head.replace("__SCHEMA__", json.dumps(p3_schema, ensure_ascii=False, indent=2))

    hist_table_html = render_full_hist_table(code)
    hist_h1 = "Codex Reset History" if code=="en" else ("Codex 历史重置记录" if "zh" in code else "Codex リセット全履歴")
    hist_sub = f"Every verified public quota reset announced by Tibo Sottiaux (@thsottiaux) since September 2025 ({len(recs)} total events)." if code=="en" else (f"收录自 2025 年 9 月至今由 Tibo Sottiaux 宣布的全部 {len(recs)} 次公共重置记录，按时间倒序排列。" if "zh" in code else f"2025年9月以降の全{len(recs)}件の確定リセット記録一覧。")

    # Construct dedicated history page body
    p3_body_custom = f'''<body>
<header class="hdr">
<div class="wrap hdr-in">
<a class="brand" href="{f"/{d}/" if d else "/"}">
<span class="brand-mark" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none"><path d="M12 2.75C6.89 2.75 2.75 6.89 2.75 12C2.75 14.54 3.78 16.84 5.45 18.5" stroke="#FCD535" stroke-width="2"/><path d="M21.25 12C21.25 17.11 17.11 21.25 12 21.25" stroke="#FCD535" stroke-width="2"/><circle cx="12" cy="12" r="5.2" stroke="#FCD535" stroke-width="1.6"/><circle cx="12" cy="12" r="2.2" fill="#FCD535"/></svg></span>
<span class="brand-txt"><span class="brand-name">CodexReset<span style="color:var(--primary)">.live</span></span><span class="brand-sub">{esc(t["brand_sub"])}</span></span>
</a>
<nav class="hdr-nav" aria-label="Main Navigation">{render_nav(code, d, "history")}</nav>
<div style="display:flex;align-items:center;gap:14px">
<div class="lang">
<button class="lang-btn" id="langBtn"><span>{esc(name)}</span><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg></button>
<div class="lang-panel" id="langPanel"><div class="lang-grid">{build_lang_items(code, "history")}</div></div>
</div>
</div>
</div>
</header>
<main>
<div class="wrap">
<div class="sub-hero">
<span class="sub-badge">● VERIFIED HISTORICAL ARCHIVE</span>
<h1 class="sub-h1">{hist_h1}</h1>
<p class="sub-p">{hist_sub}</p>
</div>

<!-- 4 Key Historical Metrics -->
<div class="readout" style="margin-bottom:28px">
<div class="readout-item"><div class="ro-l">Total Verified Resets</div><div class="ro-v num y">{len(recs)} Events</div><div class="ro-s">Since Sep 2025</div></div>
<div class="readout-item"><div class="ro-l">Regular Hard Resets</div><div class="ro-v num up">49%</div><div class="ro-s">Instant full refills</div></div>
<div class="readout-item"><div class="ro-l">Banked Credit Resets</div><div class="ro-v num y">51%</div><div class="ro-s">Rollover coupons</div></div>
<div class="readout-item"><div class="ro-l">Average Cadence</div><div class="ro-v num">3.2 Days</div><div class="ro-s">Between global resets</div></div>
</div>

<!-- Calendar Grid -->
<div class="cal-grid-card" style="margin-bottom:28px">
<div class="cal-top">
<div class="cal-title">
<svg class="ico" style="color:var(--primary);width:17px;height:17px" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>
<span id="calMonthTitle">October 2026</span>
<span class="cal-month-badge" id="calMonthBadge">2 Resets</span>
</div>
<div class="cal-right">
<div class="cal-legend">
<span class="leg-item"><span class="leg-dot leg-reg"></span> <span>Regular Hard Reset</span></span>
<span class="leg-item"><span class="leg-dot leg-bnk"></span> <span>Banked Reset</span></span>
</div>
<div class="cal-nav-btns">
<button class="cal-nav-btn" id="calPrevBtn" aria-label="Previous Month" title="Previous Month">
<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
</button>
<button class="cal-nav-btn" id="calNextBtn" aria-label="Next Month" title="Next Month">
<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
</button>
</div>
</div>
</div>
<div id="calTableWrap">
{CAL_TABLE_HTML}
</div>
</div>

<!-- Full Archive Table -->
<div class="sec-h"><span class="sec-kick">CHRONOLOGICAL LOG</span><h2 class="sec-t">Complete Verified History Table ({len(recs)} entries)</h2></div>
<div class="hist-table-card">
<table class="hist-full-table">
<thead>
<tr>
  <th style="width:170px">Timestamp</th>
  <th style="width:110px">Type</th>
  <th>Announcement & Quote</th>
  <th style="width:100px;text-align:right">Source</th>
</tr>
</thead>
<tbody>
{hist_table_html}
</tbody>
</table>
</div>

<!-- Alternatives -->
<section id="tools" style="margin-top:40px">
<div class="sec-h"><span class="sec-kick">ALTERNATIVES</span><h2 class="sec-t">{esc(t["tools_t"])}</h2><p class="sec-s">{esc(t["tools_s"])}</p></div>
<div class="tools">
<div class="tool feat"><span class="tool-flag">Top</span><div><div class="tool-h"><span class="tool-n">Cursor IDE</span></div><p class="tool-d">{esc(t["tool1_d"])}</p></div><a class="tool-a" href="https://cursor.com/?ref=codexreset" target="_blank" rel="noopener nofollow">{esc(t["tool1_a"])}</a></div>
<div class="tool"><div><div class="tool-h"><span class="tool-n">Windsurf</span></div><p class="tool-d">{esc(t["tool2_d"])}</p></div><a class="tool-a" href="https://codeium.com/windsurf?ref=codexreset" target="_blank" rel="noopener nofollow">{esc(t["tool2_a"])}</a></div>
<div class="tool"><div><div class="tool-h"><span class="tool-n">Claude Code</span></div><p class="tool-d">{esc(t["tool3_d"])}</p></div><a class="tool-a" href="https://claude.ai/code?ref=codexreset" target="_blank" rel="noopener nofollow">{esc(t["tool3_a"])}</a></div>
</div>
</section>

</div>
</main>
<footer>
<div class="wrap foot-in">
{render_footer_dir(code, f"/{d}/" if d else "/")}
<div class="foot-links"><a href="/llms.txt">llms.txt</a><a href="/llms-full.txt">llms-full.txt</a><a href="/sitemap.xml">sitemap.xml</a></div>
<p class="foot-c">© 2026 CodexReset.live — {esc(t["foot"])}</p>
</div>
</footer>
<script>
var lb=document.getElementById('langBtn'),lp=document.getElementById('langPanel');
lb.addEventListener('click',function(e){{e.stopPropagation();lp.classList.toggle('open');lb.classList.toggle('open');}});
document.addEventListener('click',function(e){{if(!lp.contains(e.target)&&!lb.contains(e.target)){{lp.classList.remove('open');lb.classList.remove('open');}}}});
</script>
</body>'''

    p3_path.write_text(p3_head + "\n" + p3_body_custom.replace('</body>', get_cal_js(code) + '</body>'), encoding="utf-8")
    SITEMAP_URLS.append((p3_canon, "0.8"))

    # Also write /reset-history/ alias for competitor link compatibility
    p3_alias_dir = out_dir / "reset-history"
    p3_alias_dir.mkdir(parents=True, exist_ok=True)
    (p3_alias_dir / "index.html").write_text(p3_head + "\n" + p3_body_custom.replace('</body>', get_cal_js(code) + '</body>'), encoding="utf-8")

    # =========================================================================
    # PAGE 4: METHODOLOGY (/methodology/)
    # =========================================================================
    p4_dir = out_dir / "methodology"
    p4_dir.mkdir(parents=True, exist_ok=True)
    p4_path = p4_dir / "index.html"
    p4_canon = f"https://codexresetlive.com/{d}/methodology/" if d else "https://codexresetlive.com/methodology/"

    p4_title = "Codex Reset Radar Methodology: Prediction Algorithm & Factors | Codex Reset Radar" if code=="en" else ("Codex 重置雷达算法白皮书与信源权重说明 | Codex Reset Radar" if "zh" in code else ("Codex リセット予測モデル・評価手法解説 | Codex Reset Radar" if code=="ja" else "Codex Reset Radar Methodology | Codex Reset Radar"))
    p4_desc = "Mathematical scoring formula, factor weightings, and real-time Twitter/API ingestion pipeline behind the Codex Reset Radar 48-hour probability forecast." if code=="en" else "详细解析 Codex 重置雷达的 48 小时概率预测数学模型、8 维信号开关权重分配、核心监控人物权力矩阵与实时数据抓取机制。" if "zh" in code else "Codexリセット予測モデルの計算式、8つの評価指標、重み付けアルゴリズムの技術解説。"

    p4_schema = {
        "@context":"https://schema.org",
        "@graph":[
            {"@type":"TechArticle","headline":p4_title,"url":p4_canon,"inLanguage":loc,"description":p4_desc},
            {"@type":"BreadcrumbList","itemListElement":[
                {"@type":"ListItem","position":1,"name":"Home","item":p1_canon},
                {"@type":"ListItem","position":2,"name":"Methodology","item":p4_canon}
            ]}
        ]
    }

    p4_head = HEAD.replace("__LANG__", code).replace("__TITLE__", esc(p4_title)).replace("__DESC__", esc(p4_desc))
    p4_head = p4_head.replace("__CANONICAL__", p4_canon).replace("__LOCALE__", loc)
    p4_head = p4_head.replace("__HREFLANG__", build_hreflang("methodology"))
    p4_head = p4_head.replace("__SCHEMA__", json.dumps(p4_schema, ensure_ascii=False, indent=2))

    meth_h1 = "Prediction Methodology & Architecture" if code=="en" else ("预测模型算法白皮书与架构" if "zh" in code else "予測アルゴリズム手法とアーキテクチャ")
    meth_sub = "Transparent, inspectable factor weighting. Decisions behind actual resets are not guesswork — here is how the model scores each signal." if code=="en" else ("算法完全可审计。背后的概率不是凭空猜测 —— 本文完整公开我们的 8 维打分公式、权重分配与数据抓取链路。" if "zh" in code else "ブラックボックスを排除した透明な予測アルゴリズムの全貌。")

    p4_body_custom = f'''<body>
<header class="hdr">
<div class="wrap hdr-in">
<a class="brand" href="{f"/{d}/" if d else "/"}">
<span class="brand-mark" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none"><path d="M12 2.75C6.89 2.75 2.75 6.89 2.75 12C2.75 14.54 3.78 16.84 5.45 18.5" stroke="#FCD535" stroke-width="2"/><path d="M21.25 12C21.25 17.11 17.11 21.25 12 21.25" stroke="#FCD535" stroke-width="2"/><circle cx="12" cy="12" r="5.2" stroke="#FCD535" stroke-width="1.6"/><circle cx="12" cy="12" r="2.2" fill="#FCD535"/></svg></span>
<span class="brand-txt"><span class="brand-name">CodexReset<span style="color:var(--primary)">.live</span></span><span class="brand-sub">{esc(t["brand_sub"])}</span></span>
</a>
<nav class="hdr-nav" aria-label="Main Navigation">{render_nav(code, d, "methodology")}</nav>
<div style="display:flex;align-items:center;gap:14px">
<div class="lang">
<button class="lang-btn" id="langBtn"><span>{esc(name)}</span><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg></button>
<div class="lang-panel" id="langPanel"><div class="lang-grid">{build_lang_items(code, "methodology")}</div></div>
</div>
</div>
</div>
</header>
<main>
<div class="wrap">
<div class="sub-hero">
<span class="sub-badge">● TRANSPARENT ALGORITHM WHITEPAPER</span>
<h1 class="sub-h1">{meth_h1}</h1>
<p class="sub-p">{meth_sub}</p>
</div>

<!-- Mathematical Formula Card -->
<div class="math-card">
<h2 class="sec-t" style="margin-bottom:8px">1. Mathematical Scoring Formula</h2>
<p class="sec-s">The 48-hour probability P(t) is computed as an inspectable weighted sum bounded between [5%, 98%]:</p>
<div class="math-formula">
P(t) = Baseline(t) + W_tibo · S_tibo + W_status · S_status + W_cadence · S_cadence + W_milestone · S_milestone - Cooldown(Δt)
</div>
<p style="font-size:12px;color:var(--muted-strong);line-height:1.6">Where <strong>Baseline(t)</strong> is the Poisson arrival baseline (typically 12%), <strong>S_tibo</strong> represents verified announcement semantic strength, and <strong>Cooldown(Δt)</strong> exponentially suppresses the likelihood immediately following a confirmed flush.</p>
</div>

<!-- 8 Switches Grid -->
<div class="sec-h" style="margin-top:36px"><span class="sec-kick">WEIGHT BREAKDOWN</span><h2 class="sec-t">2. The 8 Signal Switches & Weight Distribution</h2></div>
<div class="math-grid">
<div class="math-item"><div class="math-item-t"><span>Tibo Posts Semantic Hint</span><span class="num" style="color:var(--up)">Weight: 35%</span></div><div class="math-item-d">Natural language extraction via LLM from @thsottiaux tweets. Mentions of "ship", "refresh", "bonus", or "sol limits" heavily boost this factor.</div></div>
<div class="math-item"><div class="math-item-t"><span>Reset Cooldown Decay</span><span class="num" style="color:var(--down)">Weight: 20%</span></div><div class="math-item-d">Historical median gap between resets is 3.2 days. A reset in the last 48 hours strongly reduces near-term refill odds.</div></div>
<div class="math-item"><div class="math-item-t"><span>OpenAI Incident Status</span><span class="num" style="color:var(--primary)">Weight: 15%</span></div><div class="math-item-d">Monitored directly via status.openai.com. Extended degraded performance on Codex models frequently triggers compensatory flushes.</div></div>
<div class="math-item"><div class="math-item-t"><span>Major Model Launch Cadence</span><span class="num" style="color:var(--info)">Weight: 10%</span></div><div class="math-item-d">Historical releases (e.g. GPT-6 Sol, Astra) correlate with account-wide resets to encourage developer testing.</div></div>
<div class="math-item"><div class="math-item-t"><span>User Milestone Achievements</span><span class="num" style="color:var(--primary)">Weight: 8%</span></div><div class="math-item-d">Crossing round-number active subscriber counts (e.g. 25M, 50M) triggers celebratory marketing resets.</div></div>
<div class="math-item"><div class="math-item-t"><span>San Francisco Working Window</span><span class="num" style="color:var(--muted)">Weight: 5%</span></div><div class="math-item-d">OpenAI engineering team flushes cluster limits predominantly between 09:00 and 17:00 US Pacific time on weekdays.</div></div>
<div class="math-item"><div class="math-item-t"><span>Community Consensus Index</span><span class="num" style="color:var(--muted)">Weight: 4%</span></div><div class="math-item-d">Aggregated developer chatter on GitHub discussions, Reddit, and Discord regarding server congestion.</div></div>
<div class="math-item"><div class="math-item-t"><span>Edge Buffer Headroom</span><span class="num" style="color:var(--muted)">Weight: 3%</span></div><div class="math-item-d">Cluster-level latency benchmarks indicating available inference compute headroom across global data centers.</div></div>
</div>

<!-- Authority Matrix -->
<div class="sec-h" style="margin-top:36px"><span class="sec-kick">SOURCE HIERARCHY</span><h2 class="sec-t">3. Monitored Accounts & Verification Tiers</h2></div>
<div class="monitor-grid" style="margin-bottom:28px">
{render_monitors(code)}
</div>

<!-- Data Ingestion Pipeline -->
<div class="math-card" style="margin-top:36px">
<h2 class="sec-t" style="margin-bottom:8px">4. Realtime Ingestion & Pipeline Architecture</h2>
<p class="sec-s" style="line-height:1.6">Our server runs automated polling tasks every 30 minutes:<br>
1. <strong>X/Twitter Stream</strong>: Ingests real-time posts from monitored accounts via verified scraping proxies.<br>
2. <strong>LLM Semantic Classifier</strong>: Runs zero-shot analysis on candidate tweets to distinguish banter from actual hard quota commitments.<br>
3. <strong>Status Poller</strong>: Checks OpenAI status feeds and API response latency.<br>
4. <strong>Static Compilation</strong>: Re-computes probability and updates all 10 language builds automatically with zero downtime.
</p>
</div>

</div>
</main>
<footer>
<div class="wrap foot-in">
{render_footer_dir(code, f"/{d}/" if d else "/")}
<div class="foot-links"><a href="/llms.txt">llms.txt</a><a href="/llms-full.txt">llms-full.txt</a><a href="/sitemap.xml">sitemap.xml</a></div>
<p class="foot-c">© 2026 CodexReset.live — {esc(t["foot"])}</p>
</div>
</footer>
<script>
var lb=document.getElementById('langBtn'),lp=document.getElementById('langPanel');
lb.addEventListener('click',function(e){{e.stopPropagation();lp.classList.toggle('open');lb.classList.toggle('open');}});
document.addEventListener('click',function(e){{if(!lp.contains(e.target)&&!lb.contains(e.target)){{lp.classList.remove('open');lb.classList.remove('open');}}}});
</script>
</body>'''

    p4_path.write_text(p4_head + "\n" + p4_body_custom, encoding="utf-8")
    SITEMAP_URLS.append((p4_canon, "0.8"))

    print(f"Generated 4 pages for [{code:7s}]: / | /reset-today/ | /history/ | /methodology/")

# --- WRITE COMPREHENSIVE SITEMAP.XML (ALL 40 URLS) ---
sitemap_items = []
for url, prio in SITEMAP_URLS:
    sitemap_items.append(f'''  <url>
    <loc>{url}</loc>
    <lastmod>2026-10-05T09:00:00+00:00</lastmod>
    <changefreq>hourly</changefreq>
    <priority>{prio}</priority>
  </url>''')

full_sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{"\n".join(sitemap_items)}
</urlset>'''

(SITE_DIR / "sitemap.xml").write_text(full_sitemap, encoding="utf-8")
print(f"\nUpdated sitemap.xml with {len(SITEMAP_URLS)} URLs!")
print("ALL 40 PAGES GENERATED AND COMPILED SUCCESSFULLY!")
