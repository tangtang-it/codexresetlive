import os

build_path = r"D:/ZySpace/zy_code/seo/codexlimit/scripts/build_final.py"
with open(build_path, "r", encoding="utf-8") as f:
    code = f.read()

# Replace plain text arrow with SVG arrow in View on X link
old_link = '<a href="%s" target="_blank" rel="noopener nofollow">View on X ↗</a>'
new_link = '<a href="%s" target="_blank" rel="noopener nofollow">View on X <svg class="icon-svg" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg></a>'

if old_link in code:
    code = code.replace(old_link, new_link)
    with open(build_path, "w", encoding="utf-8") as f:
        f.write(code)
    print("Replaced View on X link with SVG icon in build_final.py!")
else:
    print("Link already replaced or pattern changed.")
