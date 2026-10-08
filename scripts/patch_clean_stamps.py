from pathlib import Path

# 1. 精准升级 scripts/build_studio.py
path_bs = Path("scripts/build_studio.py")
content = path_bs.read_text(encoding="utf-8")

# 替换 yes_stamp 为专业的官方遥测卡 (去除生硬假印章)
old_yes_start = content.find("yes_stamp = f'''")
old_yes_end = content.find("'''", old_yes_start + 16) + 3

new_yes_stamp = '''yes_stamp = f"""<div class="dab-telemetry-badge yes">
      <div class="dt-top">
        <span class="dot-live"></span>
        <span class="dt-label">OFFICIAL TELEMETRY</span>
      </div>
      <div class="dt-source">Source: <strong>@thsottiaux</strong></div>
      <div class="dt-time num">Landed {h_round}h ago</div>
      <div class="dt-prob-pill yes"><span class="num">100%</span> CONFIRMED</div>
    </div>"""'''

if old_yes_start != -1 and old_yes_end != -1:
    content = content[:old_yes_start] + new_yes_stamp + content[old_yes_end:]
    print("Successfully replaced yes_stamp with Official Telemetry Badge")

# 替换 soon_stamp 为备用遥测卡
old_soon_start = content.find("soon_stamp = f'''")
old_soon_end = content.find("'''", old_soon_start + 17) + 3

new_soon_stamp = '''soon_stamp = f"""<div class="dab-telemetry-badge standby">
      <div class="dt-top">
        <span class="dot-amber"></span>
        <span class="dt-label">RADAR STANDBY</span>
      </div>
      <div class="dt-source">Last: <strong>{last_date}</strong></div>
      <div class="dt-time num">{days_since_str} ago</div>
      <div class="dt-prob-pill yellow"><span class="num">{prob}%</span> PROBABILITY</div>
    </div>"""'''

if old_soon_start != -1 and old_soon_end != -1:
    content = content[:old_soon_start] + new_soon_stamp + content[old_soon_end:]
    print("Successfully replaced soon_stamp with Telemetry Standby Badge")

path_bs.write_text(content, encoding="utf-8")
print("Updated scripts/build_studio.py cleanly!")
