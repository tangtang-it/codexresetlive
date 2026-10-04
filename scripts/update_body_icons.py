import os

body_path = r"D:/ZySpace/zy_code/seo/codexlimit/_tpl_body.html"
with open(body_path, "r", encoding="utf-8") as f:
    body = f.read()

# 1. Replace 🌐 with Globe SVG in language button
globe_svg = '''<svg class="icon-svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>'''
body = body.replace('🌐 <span>__LANG_NAME__</span>', f'{globe_svg} <span>__LANG_NAME__</span>')

# 2. Replace ✓ with Shield-Check SVG in verdict card
shield_check = '''<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>'''
body = body.replace('<span class="verdict-ic">✓</span>', f'<span class="verdict-ic">{shield_check}</span>')

# 3. Embed Agnes 3D Quantum Radar Badge into gauge-top
gauge_top_old = '''<div class="gauge-top">
<span class="gauge-lbl">__GAUGE_LBL__</span>
<span class="gauge-tag">__GAUGE_TAG__</span>
</div>'''

gauge_top_new = '''<div class="gauge-top">
<div>
<span class="gauge-lbl">__GAUGE_LBL__</span>
<div style="margin-top:4px"><span class="gauge-tag">__GAUGE_TAG__</span></div>
</div>
<img src="/assets/radar-core-3d.png" alt="Quantum Radar Scanner Badge" class="deco-3d-badge" loading="lazy" width="48" height="48">
</div>'''
body = body.replace(gauge_top_old, gauge_top_new)

# 4. Embed Agnes 3D Satellite Antenna into Evidence / Signal Desk section header
evidence_sec_old = '''<section id="evidence">
<div class="sec-h">
<span class="sec-kick">02 — __RAIL_KICK__</span>
<h2 class="sec-t">__RAIL_T__</h2>
<p class="sec-s">__RAIL_S__</p>
</div>'''

evidence_sec_new = '''<section id="evidence">
<div class="sec-h section-deco-header">
<div>
<span class="sec-kick">02 — __RAIL_KICK__</span>
<h2 class="sec-t">__RAIL_T__</h2>
<p class="sec-s">__RAIL_S__</p>
</div>
<img src="/assets/signal-tower-3d.png" alt="Signal Monitoring Dish" class="deco-satellite" loading="lazy" width="56" height="56">
</div>'''
body = body.replace(evidence_sec_old, evidence_sec_new)

# 5. Add Clock SVG before Timezone Selector
clock_svg = '''<svg class="icon-svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'''
body = body.replace('<span>__TZ_L__</span>', f'<span>{clock_svg} __TZ_L__</span>')

# 6. Replace Bell and Calendar buttons with SVG
bell_svg = '''<svg class="icon-svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>'''
cal_svg = '''<svg class="icon-svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/><line x1="12" x2="12" y1="14" y2="18"/><line x1="10" x2="14" y1="16" y2="16"/></svg>'''

body = body.replace('🔔 __NOTIFY__', f'{bell_svg} __NOTIFY__')
body = body.replace('📅 __CAL__', f'{cal_svg} __CAL__')

# 7. Replace Alternative Tool Emojis with bespoke SVGs
cursor_svg = '''<svg width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M5.5 3.5L18.5 12L12 13.5L8.5 20L5.5 3.5Z" fill="#FCD535" stroke="#181a20" stroke-width="1.6" stroke-linejoin="round"/></svg>'''
windsurf_svg = '''<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#2dbdb6" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12c2.5-4 6-4 8.5 0s6 4 8.5 0 3-2 3-2"/><path d="M2 17c2.5-4 6-4 8.5 0s6 4 8.5 0 3-2 3-2"/><path d="M12 3v6"/></svg>'''
claude_svg = '''<svg width="22" height="22" viewBox="0 0 24 24" fill="#D97706"><path d="M12 2l2.4 6.6L21 11l-6.6 2.4L12 20l-2.4-6.6L3 11l6.6-2.4L12 2z"/></svg>'''

body = body.replace('<span class="tool-ic">🖱️</span>', f'<span class="tool-ic">{cursor_svg}</span>')
body = body.replace('<span class="tool-ic">🏄</span>', f'<span class="tool-ic">{windsurf_svg}</span>')
body = body.replace('<span class="tool-ic">⚡</span>', f'<span class="tool-ic">{claude_svg}</span>')

# 8. Toast Icons with SVG
body = body.replace('<span id="toastI">✅</span>', '<span id="toastI"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#0ecb81" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg></span>')

with open(body_path, "w", encoding="utf-8") as f:
    f.write(body)

print("Body template successfully updated with SVG icons and Agnes 3D assets!")
