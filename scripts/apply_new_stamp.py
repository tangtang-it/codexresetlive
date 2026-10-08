from pathlib import Path

path = Path("scripts/build_studio.py")
content = path.read_text(encoding="utf-8")

# 找到 yes_stamp 的起始位置
start = content.find("yes_stamp = f")
end = content.find("tz_icon = ", start)

new_stamps = '''yes_stamp = f"""<div class="openthe-stamp-wrap yes">
      <svg class="stamp-svg" viewBox="0 0 220 220" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <path id="circleTextPathYes" d="M 110, 110 m -82, 0 a 82,82 0 1,1 164,0 a 82,82 0 1,1 -164,0" />
          <filter id="glowGreenBig" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="5" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>
        
        <!-- 环形自转轨道与文字 -->
        <g class="stamp-spin-orbit">
          <circle cx="110" cy="110" r="98" stroke="#0ecb81" stroke-width="1.2" stroke-opacity="0.35"/>
          <circle cx="110" cy="110" r="82" stroke="#0ecb81" stroke-width="1.6" stroke-dasharray="4 3" stroke-opacity="0.75"/>
          <circle cx="110" cy="110" r="68" stroke="#0ecb81" stroke-width="1.2" stroke-opacity="0.4"/>
          <text fill="#0ecb81" font-size="9" font-family="'JetBrains Mono', ui-monospace, monospace" font-weight="700" letter-spacing="2.6" opacity="0.85">
            <textPath href="#circleTextPathYes" startOffset="0%">
              OPENAI CODEX RESET &bull; VERIFIED FLUSH &bull; 
            </textPath>
          </text>
        </g>

        <!-- 超大醒目的 Yes. 与下划虚线 -->
        <g class="stamp-center" filter="url(#glowGreenBig)">
          <text x="110" y="118" fill="#0ecb81" font-size="54" font-weight="900" text-anchor="middle" font-family="'Inter', system-ui, -apple-system, sans-serif" letter-spacing="-1">Yes.</text>
          <line x1="68" y1="132" x2="152" y2="132" stroke="#0ecb81" stroke-width="2" stroke-dasharray="3 3" stroke-opacity="0.85"/>
          <text x="110" y="148" fill="#0ecb81" font-size="9.5" font-weight="800" text-anchor="middle" font-family="'JetBrains Mono', ui-monospace, monospace" letter-spacing="2">CONFIRMED</text>
        </g>
      </svg>
    </div>"""

    soon_stamp = f"""<div class="openthe-stamp-wrap soon">
      <svg class="stamp-svg" viewBox="0 0 220 220" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <path id="circleTextPathSoon" d="M 110, 110 m -82, 0 a 82,82 0 1,1 164,0 a 82,82 0 1,1 -164,0" />
          <filter id="glowGoldBig" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="5" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>
        
        <g class="stamp-spin-orbit">
          <circle cx="110" cy="110" r="98" stroke="#FCD535" stroke-width="1.2" stroke-opacity="0.35"/>
          <circle cx="110" cy="110" r="82" stroke="#FCD535" stroke-width="1.6" stroke-dasharray="4 3" stroke-opacity="0.75"/>
          <circle cx="110" cy="110" r="68" stroke="#FCD535" stroke-width="1.2" stroke-opacity="0.4"/>
          <text fill="#FCD535" font-size="9" font-family="'JetBrains Mono', ui-monospace, monospace" font-weight="700" letter-spacing="2.6" opacity="0.85">
            <textPath href="#circleTextPathSoon" startOffset="0%">
              PREDICTION RADAR &bull; PROBABILITY PULSE &bull; 
            </textPath>
          </text>
        </g>

        <g class="stamp-center" filter="url(#glowGoldBig)">
          <text x="110" y="118" fill="#FCD535" font-size="44" font-weight="900" text-anchor="middle" font-family="'Inter', system-ui, -apple-system, sans-serif" letter-spacing="-1">{prob}%</text>
          <line x1="68" y1="132" x2="152" y2="132" stroke="#FCD535" stroke-width="2" stroke-dasharray="3 3" stroke-opacity="0.85"/>
          <text x="110" y="148" fill="#FCD535" font-size="9.5" font-weight="800" text-anchor="middle" font-family="'JetBrains Mono', ui-monospace, monospace" letter-spacing="2">PROBABLE</text>
        </g>
      </svg>
    </div>"""

    '''

if start != -1 and end != -1:
    content = content[:start] + new_stamps + content[end:]
    print("Replaced yes_stamp and soon_stamp cleanly!")
else:
    print("WARN: Could not locate start/end:", start, end)

path.write_text(content, encoding="utf-8")
print("Saved scripts/build_studio.py")
