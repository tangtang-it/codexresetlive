from pathlib import Path

path = Path("scripts/build_studio.py")
content = path.read_text(encoding="utf-8")

# 打造超越竞品 OpenTheRank 的极致吸睛的大徽章设计
# 包含：环形文字轨道 textPath、内圈精细刻度、超大醒目的 Yes.、柔和深邃发光微动效
new_direct_ans_func = '''def render_direct_ans(code):
    reset_recs = [r for r in recs if any(k in r.get("text", "").lower() for k in ["reset", "banked", "propagated"])]
    l_rec = reset_recs[-1] if reset_recs else recs[-1]
    l_dt = datetime.strptime(l_rec["at"][:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
    now_u = datetime.now(timezone.utc)
    h_diff = max(0.1, (now_u - l_dt).total_seconds() / 3600.0)
    is_today_reset = (h_diff < 24.0)
    h_round = int(round(h_diff))
    l_type = l_rec.get("type", "banked").upper()
    badge_cls = l_rec.get("type", "banked")
    type_badge = render_banked_badge(code, l_type) if badge_cls == "banked" else f'<span class="badge {badge_cls}">{l_type}</span>'

    tz_icon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:13px;height:13px"><circle cx="12" cy="12" r="10"/><line x1="2" x2="22" y1="12" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>'

    # 超越大印章设计：SVG 环形文字轨道 + 优雅微旋转 + 超大醒目 Yes.
    yes_stamp_svg = f"""<div class="openthe-stamp-wrap yes">
      <svg class="stamp-svg" viewBox="0 0 220 220" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <path id="circleTextPath" d="M 110, 110 m -82, 0 a 82,82 0 1,1 164,0 a 82,82 0 1,1 -164,0" />
          <filter id="glowGreenBig" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="6" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>
        
        <!-- 外部缓慢旋转轮盘轨道 -->
        <g class="stamp-spinning-track">
          <!-- 外层细线同心圆 -->
          <circle cx="110" cy="110" r="98" stroke="#0ecb81" stroke-width="1.2" stroke-opacity="0.35"/>
          <circle cx="110" cy="110" r="82" stroke="#0ecb81" stroke-width="1.8" stroke-dasharray="4 3" stroke-opacity="0.7"/>
          <circle cx="110" cy="110" r="68" stroke="#0ecb81" stroke-width="1.2" stroke-opacity="0.4"/>
          <!-- 沿圆周环绕的雷达核验文字 (Curved Text) -->
          <text fill="#0ecb81" font-size="9" font-family="'JetBrains Mono', ui-monospace, monospace" font-weight="700" letter-spacing="2.8" opacity="0.85">
            <textPath href="#circleTextPath" startOffset="0%">
              OPENAI CODEX RESET  VERIFIED FLUSH  
            </textPath>
          </text>
        </g>

        <!-- 静态中心焦点：超大醒目的 Yes. 与下划虚线 -->
        <g class="stamp-center-focus" filter="url(#glowGreenBig)">
          <text x="110" y="118" fill="#0ecb81" font-size="52" font-weight="900" text-anchor="middle" font-family="'Inter', system-ui, -apple-system, sans-serif" letter-spacing="-1">Yes.</text>
          <!-- 水平分割虚线 -->
          <line x1="68" y1="132" x2="152" y2="132" stroke="#0ecb81" stroke-width="2" stroke-dasharray="3 3" stroke-opacity="0.85"/>
          <!-- 底部小微标 -->
          <text x="110" y="148" fill="#0ecb81" font-size="9.5" font-weight="800" text-anchor="middle" font-family="'JetBrains Mono', ui-monospace, monospace" letter-spacing="2">CONFIRMED</text>
        </g>
      </svg>
    </div>"""

    # 备用状态：未重置时的大金印章 (Soon / Probable)
    soon_stamp_svg = f"""<div class="openthe-stamp-wrap soon">
      <svg class="stamp-svg" viewBox="0 0 220 220" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <path id="circleTextPathSoon" d="M 110, 110 m -82, 0 a 82,82 0 1,1 164,0 a 82,82 0 1,1 -164,0" />
          <filter id="glowGoldBig" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="6" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>
        
        <g class="stamp-spinning-track">
          <circle cx="110" cy="110" r="98" stroke="#FCD535" stroke-width="1.2" stroke-opacity="0.35"/>
          <circle cx="110" cy="110" r="82" stroke="#FCD535" stroke-width="1.8" stroke-dasharray="4 3" stroke-opacity="0.7"/>
          <circle cx="110" cy="110" r="68" stroke="#FCD535" stroke-width="1.2" stroke-opacity="0.4"/>
          <text fill="#FCD535" font-size="9" font-family="'JetBrains Mono', ui-monospace, monospace" font-weight="700" letter-spacing="2.8" opacity="0.85">
            <textPath href="#circleTextPathSoon" startOffset="0%">
              PREDICTION RADAR  PROBABILITY PULSE  
            </textPath>
          </text>
        </g>

        <g class="stamp-center-focus" filter="url(#glowGoldBig)">
          <text x="110" y="118" fill="#FCD535" font-size="44" font-weight="900" text-anchor="middle" font-family="'Inter', system-ui, -apple-system, sans-serif" letter-spacing="-1">{prob}%</text>
          <line x1="68" y1="132" x2="152" y2="132" stroke="#FCD535" stroke-width="2" stroke-dasharray="3 3" stroke-opacity="0.85"/>
          <text x="110" y="148" fill="#FCD535" font-size="9.5" font-weight="800" text-anchor="middle" font-family="'JetBrains Mono', ui-monospace, monospace" letter-spacing="2">PROBABLE</text>
        </g>
      </svg>
    </div>"""

    if is_today_reset:
        if "zh" in code:
            return f'''<div class="direct-ans-banner yes-theme">
  <div class="dab-left">
    <div class="dab-kicker">
      <span class="dt-dot-live"></span>
      <span class="kicker-txt">CODEX RESET RADAR  ʵʱң</span>
    </div>
    <div class="dab-h">Codex  <strong>ǵģã(Yes.)</strong></div>
    <div class="dab-p">һιٷע뷢 <strong data-ago-utc="{l_rec['at']}">{h_round} Сʱǰ</strong>Ѳϣٵȴ</div>
    <div class="dab-rec-line">
      <span>һμ¼</span>
      <span class="dab-rec-dt" data-local-dt="{l_rec['at']}">2026108 03:19</span>
      <span class="dab-rec-tz">(ʱ)</span>
      {type_badge}
    </div>
    <div class="tz-indicator">{tz_icon} <span data-tz-display>ʱʾ</span></div>
  </div>
  <div class="dab-right-wrap">
    {yes_stamp_svg}
    <a href="#calculator" class="dab-btn">˽ </a>
  </div>
</div>'''
        else:
            return f'''<div class="direct-ans-banner yes-theme">
  <div class="dab-left">
    <div class="dab-kicker">
      <span class="dt-dot-live"></span>
      <span class="kicker-txt">CODEX RESET TRACKER  OFFICIAL TELEMETRY</span>
    </div>
    <div class="dab-h">Will Codex reset today? <strong>Yes. Quota replenished today.</strong></div>
    <div class="dab-p">The latest verified quota flush from OpenAI leadership landed <strong data-ago-utc="{l_rec['at']}">{h_round} hours ago</strong>. Global limits cleared &mdash; optimal window to build with confidence.</div>
    <div class="dab-rec-line">
      <span>Latest recorded reset:</span>
      <span class="dab-rec-dt" data-local-dt="{l_rec['at']}">Thu, Oct 8, 2026, 03:19</span>
      <span class="dab-rec-tz">(your local time)</span>
      {type_badge}
    </div>
    <div class="tz-indicator">{tz_icon} <span data-tz-display>Displayed in your local browser timezone</span></div>
  </div>
  <div class="dab-right-wrap">
    {yes_stamp_svg}
    <a href="#calculator" class="dab-btn">Check 5h Window </a>
  </div>
</div>'''
    else:
        if "zh" in code:
            return f'''<div class="direct-ans-banner soon-theme">
  <div class="dab-left">
    <div class="dab-kicker soon">
      <span class="dt-dot-amber"></span>
      <span class="kicker-txt">CODEX RESET RADAR  Ԥģʽ</span>
    </div>
    <div class="dab-h">Codex ȫ <strong>޷ˮ ({prob}% )</strong></div>
    <div class="dab-p">δ⵽ٷȫü¼һιٷˮ <strong>{days_since_str} ǰ</strong>{last_date}鱣࣬·ɲ 5 Сʱʱ</div>
  </div>
  <div class="dab-right-wrap">
    {soon_stamp_svg}
    <a href="#calculator" class="dab-btn">˽ </a>
  </div>
</div>'''
        else:
            return f'''<div class="direct-ans-banner soon-theme">
  <div class="dab-left">
    <div class="dab-kicker soon">
      <span class="dt-dot-amber"></span>
      <span class="kicker-txt">CODEX RESET TRACKER  PROBABILITY ENGINE</span>
    </div>
    <div class="dab-h">Will Codex reset today? <strong>High probability ({prob}% chance)</strong></div>
    <div class="dab-p">No global reset recorded yet today. The last verified reset landed <strong>{days_since_str} ago</strong> ({last_date}). Calculate your personal 5-hour rolling limit recovery window below.</div>
  </div>
  <div class="dab-right-wrap">
    {soon_stamp_svg}
    <a href="#calculator" class="dab-btn">Check Recovery </a>
  </div>
</div>'''
'''

start = content.find("def render_direct_ans(")
end = content.find("def build_lang_items", start)
if start != -1 and end != -1:
    content = content[:start] + new_direct_ans_func + "\n\n" + content[end:]
    print("Replaced render_direct_ans with Eye-Catching Stamp Design")
else:
    print("WARN: Could not locate render_direct_ans")

path.write_text(content, encoding="utf-8")
print("Updated scripts/build_studio.py successfully")
