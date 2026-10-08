from pathlib import Path

path = Path("scripts/build_studio.py")
content = path.read_text(encoding="utf-8")

# Mobbin 风格纯净白底墨水脉冲波形 SVG (Monochrome Ink + Electric Blue)
mobbin_pulse_svg = """pulse_svg = f'''<svg viewBox="0 0 740 180" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="mobbinHistGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#141414" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="#141414" stop-opacity="0.00"/>
    </linearGradient>
    <linearGradient id="mobbinProjGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0066ff" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#0066ff" stop-opacity="0.00"/>
    </linearGradient>
  </defs>

  <!-- Horizontal Hairline Grid Lines (Mobbin Hairline Soft) -->
  <line x1="40" y1="30" x2="710" y2="30" stroke="#f0f0f0" stroke-width="1" stroke-dasharray="2 3"/>
  <line x1="40" y1="80" x2="710" y2="80" stroke="#f0f0f0" stroke-width="1" stroke-dasharray="2 3"/>
  <line x1="40" y1="130" x2="710" y2="130" stroke="#e0e0e0" stroke-width="1"/>

  <!-- Y-Axis Tabular Labels (Saans/Inter) -->
  <text x="15" y="34" fill="#707070" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="9.5" font-weight="600">80%</text>
  <text x="15" y="84" fill="#707070" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="9.5" font-weight="600">40%</text>
  <text x="15" y="134" fill="#707070" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="9.5" font-weight="600">0%</text>

  <!-- X-Axis Timeline Labels -->
  <text x="70" y="156" fill="#707070" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="10.5" font-weight="500" text-anchor="middle">Sep 30</text>
  <text x="170" y="156" fill="#707070" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="10.5" font-weight="500" text-anchor="middle">Oct 2</text>
  <text x="280" y="156" fill="#707070" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="10.5" font-weight="500" text-anchor="middle">Oct 4</text>
  <text x="400" y="156" fill="#707070" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="10.5" font-weight="500" text-anchor="middle">Oct 7</text>
  <text x="500" y="156" fill="#141414" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="10.5" font-weight="700" text-anchor="middle">{p_now_lbl}</text>
  <text x="590" y="156" fill="#707070" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="10.5" font-weight="500" text-anchor="middle">{p_t1_lbl}</text>
  <text x="670" y="156" fill="#707070" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="10.5" font-weight="500" text-anchor="middle">{p_t2_lbl}</text>

  <!-- Historical Filled Area (Soft Ink Wash) -->
  <path d="M 70 48 C 105 75, 135 65, 170 38 C 210 40, 245 95, 280 95 C 320 95, 360 40, 400 36 C 435 36, 465 110, 500 116 L 500 130 L 70 130 Z" fill="url(#mobbinHistGrad)"/>
  
  <!-- Projected Filled Area (Electric Blue Wash) -->
  <path d="M 500 116 C 535 116, 565 95, 590 85 C 615 75, 645 60, 670 55 L 670 130 L 500 130 Z" fill="url(#mobbinProjGrad)"/>

  <!-- Verified Historical Trajectory (Ink Black Solid Line) -->
  <path d="M 70 48 C 105 75, 135 65, 170 38 C 210 40, 245 95, 280 95 C 320 95, 360 40, 400 36 C 435 36, 465 110, 500 116" stroke="#141414" stroke-width="2.5" fill="none" stroke-linecap="round"/>

  <!-- 48-Hour Projection Line (Mobbin Electric Blue #0066ff Dash) -->
  <path d="M 500 116 C 535 116, 565 95, 590 85 C 615 75, 645 60, 670 55" stroke="#0066ff" stroke-width="2.2" stroke-dasharray="4 3" fill="none" stroke-linecap="round"/>

  <!-- Event Marker 1: Sep 30 Banked Reset (Mobbin White Stadium Pill) -->
  <line x1="70" y1="48" x2="70" y2="130" stroke="#e0e0e0" stroke-width="1"/>
  <circle cx="70" cy="48" r="4" fill="#141414"/>
  <rect x="47" y="21" width="46" height="18" rx="9" fill="#ffffff" stroke="#e0e0e0" stroke-width="1"/>
  <text x="70" y="33.5" fill="#141414" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="8.5" font-weight="600" text-anchor="middle">Banked</text>

  <!-- Event Marker 2: Oct 2 Hard Reset (Mobbin Ink Stadium Pill) -->
  <line x1="170" y1="38" x2="170" y2="130" stroke="#e0e0e0" stroke-width="1"/>
  <circle cx="170" cy="38" r="4" fill="#141414"/>
  <rect x="150" y="12" width="40" height="18" rx="9" fill="#ffffff" stroke="#e0e0e0" stroke-width="1"/>
  <text x="170" y="24.5" fill="#141414" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="8.5" font-weight="600" text-anchor="middle">Reset</text>

  <!-- Event Marker 3: Oct 7 Double Event (Hard Reset + Banked Credit) -->
  <line x1="400" y1="36" x2="400" y2="130" stroke="#e0e0e0" stroke-width="1"/>
  <circle cx="400" cy="36" r="6" stroke="#0066ff" stroke-width="1.2" fill="none"/>
  <circle cx="400" cy="36" r="3.5" fill="#141414"/>
  <rect x="353" y="10" width="94" height="18" rx="9" fill="#ffffff" stroke="#e0e0e0" stroke-width="1"/>
  <text x="378" y="22.5" fill="#141414" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="8.5" font-weight="600" text-anchor="middle">Reset</text>
  <text x="399" y="22.5" fill="#adadad" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="8.5" text-anchor="middle">+</text>
  <text x="424" y="22.5" fill="#141414" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="8.5" font-weight="600" text-anchor="middle">Banked</text>

  <!-- Current Status Anchor: Now Point (Mobbin Electric Blue Pill) -->
  <line x1="500" y1="116" x2="500" y2="130" stroke="#0066ff" stroke-width="1.2"/>
  <circle cx="500" cy="116" r="7" stroke="#0066ff" stroke-width="1.5" fill="none"/>
  <circle cx="500" cy="116" r="4" fill="#0066ff"/>
  <rect x="470" y="90" width="60" height="20" rx="10" fill="#0066ff"/>
  <text x="500" y="103.5" fill="#ffffff" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="9" font-weight="700" text-anchor="middle">Now {prob}%</text>
</svg>'''"""

# 查找并替换 pulse_svg 块
pulse_start = content.find("pulse_svg = f'''<svg viewBox=\"0 0 740 180\"")
pulse_end = content.find("</svg>'''", pulse_start) + len("</svg>'''")

if pulse_start != -1 and pulse_end != -1:
    content = content[:pulse_start] + mobbin_pulse_svg + content[pulse_end:]
    print("Replaced with Mobbin pulse_svg successfully")
else:
    print("WARN: Could not locate pulse_svg boundaries:", pulse_start, pulse_end)

# 白皮书页面中的 Brand Mark 与边框
content = content.replace('stroke="#FCD535"', 'stroke="#141414"')
content = content.replace('fill="#FCD535"', 'fill="#141414"')
content = content.replace('stroke="#5e6ad2"', 'stroke="#141414"')
content = content.replace('stroke="#27a644"', 'stroke="#141414"')

path.write_text(content, encoding="utf-8")
print("Updated build_studio.py for Mobbin successfully")
