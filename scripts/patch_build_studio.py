from pathlib import Path

path = Path("scripts/build_studio.py")
content = path.read_text(encoding="utf-8")

# 1. 替换全新的 Linear pulse_svg
new_pulse_svg = """pulse_svg = f'''<svg viewBox="0 0 740 180" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="histAreaGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#27a644" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#27a644" stop-opacity="0.00"/>
    </linearGradient>
    <linearGradient id="projAreaGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#5e6ad2" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#5e6ad2" stop-opacity="0.00"/>
    </linearGradient>
    <filter id="glowGreen" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glowIndigo" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Horizontal Hairline Grid Lines (Linear System) -->
  <line x1="40" y1="30" x2="710" y2="30" stroke="#23252a" stroke-width="1" stroke-dasharray="2 3"/>
  <line x1="40" y1="80" x2="710" y2="80" stroke="#23252a" stroke-width="1" stroke-dasharray="2 3"/>
  <line x1="40" y1="130" x2="710" y2="130" stroke="#23252a" stroke-width="1"/>

  <!-- Y-Axis Tabular Labels -->
  <text x="15" y="34" fill="#8a8f98" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="9.5">80%</text>
  <text x="15" y="84" fill="#8a8f98" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="9.5">40%</text>
  <text x="15" y="134" fill="#8a8f98" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="9.5">0%</text>

  <!-- X-Axis Timeline Labels -->
  <text x="70" y="156" fill="#8a8f98" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="10" text-anchor="middle">Sep 30</text>
  <text x="170" y="156" fill="#8a8f98" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="10" text-anchor="middle">Oct 2</text>
  <text x="280" y="156" fill="#8a8f98" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="10" text-anchor="middle">Oct 4</text>
  <text x="400" y="156" fill="#8a8f98" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="10" text-anchor="middle">Oct 7</text>
  <text x="500" y="156" fill="#34d399" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="10" font-weight="600" text-anchor="middle">{p_now_lbl}</text>
  <text x="590" y="156" fill="#8a8f98" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="10" text-anchor="middle">{p_t1_lbl}</text>
  <text x="670" y="156" fill="#8a8f98" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="10" text-anchor="middle">{p_t2_lbl}</text>

  <!-- Historical Filled Area -->
  <path d="M 70 48 C 105 75, 135 65, 170 38 C 210 40, 245 95, 280 95 C 320 95, 360 40, 400 36 C 435 36, 465 110, 500 116 L 500 130 L 70 130 Z" fill="url(#histAreaGrad)"/>
  
  <!-- Projected Filled Area -->
  <path d="M 500 116 C 535 116, 565 95, 590 85 C 615 75, 645 60, 670 55 L 670 130 L 500 130 Z" fill="url(#projAreaGrad)"/>

  <!-- Verified Historical Trajectory (Emerald Wave with Glow) -->
  <path d="M 70 48 C 105 75, 135 65, 170 38 C 210 40, 245 95, 280 95 C 320 95, 360 40, 400 36 C 435 36, 465 110, 500 116" stroke="#27a644" stroke-width="2.4" fill="none" stroke-linecap="round" filter="url(#glowGreen)"/>

  <!-- 48-Hour Projection Line (Linear Signature Lavender-Blue Dash) -->
  <path d="M 500 116 C 535 116, 565 95, 590 85 C 615 75, 645 60, 670 55" stroke="#5e6ad2" stroke-width="2.2" stroke-dasharray="4 3" fill="none" stroke-linecap="round" filter="url(#glowIndigo)"/>

  <!-- Event Marker 1: Sep 30 Banked Reset (Amber Capsule) -->
  <line x1="70" y1="48" x2="70" y2="130" stroke="#f59e0b" stroke-width="1" stroke-opacity="0.35"/>
  <circle cx="70" cy="48" r="4" fill="#f59e0b"/>
  <rect x="47" y="23" width="46" height="16" rx="4" fill="#141516" stroke="#f59e0b" stroke-width="1"/>
  <text x="70" y="34.5" fill="#fbbf24" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="8.5" font-weight="600" text-anchor="middle">Banked</text>

  <!-- Event Marker 2: Oct 2 Hard Reset (Emerald Capsule) -->
  <line x1="170" y1="38" x2="170" y2="130" stroke="#27a644" stroke-width="1" stroke-opacity="0.35"/>
  <circle cx="170" cy="38" r="4" fill="#27a644"/>
  <rect x="151" y="14" width="38" height="16" rx="4" fill="#141516" stroke="#27a644" stroke-width="1"/>
  <text x="170" y="25.5" fill="#34d399" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="8.5" font-weight="600" text-anchor="middle">Reset</text>

  <!-- Event Marker 3: Oct 7 Double Event (Hard Reset + Banked Credit) -->
  <line x1="400" y1="36" x2="400" y2="130" stroke="#27a644" stroke-width="1" stroke-opacity="0.4"/>
  <circle cx="400" cy="36" r="6" stroke="#f59e0b" stroke-width="1.2" fill="none"/>
  <circle cx="400" cy="36" r="3.5" fill="#27a644"/>
  <rect x="355" y="12" width="90" height="16" rx="4" fill="#141516" stroke="#34343a" stroke-width="1"/>
  <text x="378" y="23.5" fill="#34d399" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="8.5" font-weight="600" text-anchor="middle">Reset</text>
  <text x="399" y="23.5" fill="#8a8f98" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="8" text-anchor="middle">+</text>
  <text x="424" y="23.5" fill="#fbbf24" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="8" font-weight="600" text-anchor="middle">Banked</text>

  <!-- Current Status Anchor: Now Point (Linear Dual Ring) -->
  <line x1="500" y1="116" x2="500" y2="130" stroke="#5e6ad2" stroke-width="1.2" stroke-opacity="0.6"/>
  <circle cx="500" cy="116" r="7.5" stroke="#5e6ad2" stroke-width="1.5" stroke-opacity="0.5"/>
  <circle cx="500" cy="116" r="4" fill="#5e6ad2"/>
  <rect x="472" y="92" width="56" height="18" rx="4" fill="#5e6ad2"/>
  <text x="500" y="104.5" fill="#ffffff" font-family="'JetBrains Mono', ui-monospace, monospace" font-size="8.5" font-weight="700" text-anchor="middle">Now {prob}%</text>
</svg>'''"""

# 查找并精准替换 pulse_svg 块
pulse_start = content.find("pulse_svg = f'''<svg viewBox=\"0 0 740 180\"")
pulse_end = content.find("</svg>'''", pulse_start) + len("</svg>'''")

if pulse_start != -1 and pulse_end != -1:
    content = content[:pulse_start] + new_pulse_svg + content[pulse_end:]
    print("Replaced pulse_svg successfully")
else:
    print("WARN: Could not locate pulse_svg boundaries:", pulse_start, pulse_end)

# 2. 替换白皮书页面 (p4_body_custom) 中的 Brand Mark SVG 与色彩
content = content.replace('stroke="#FCD535"', 'stroke="#5e6ad2"')
content = content.replace('fill="#FCD535"', 'fill="#828fff"')
content = content.replace('stroke="#0ecb81"', 'stroke="#27a644"')
content = content.replace('background:#1e2329', 'background:#141516')
content = content.replace('border:1px solid #2b3139', 'border:1px solid #23252a')
content = content.replace('color:#707a8a', 'color:#8a8f98')
content = content.replace('color:#0ecb81', 'color:#34d399')
content = content.replace('color:#FCD535', 'color:#fbbf24')

path.write_text(content, encoding="utf-8")
print("Updated scripts/build_studio.py successfully")
