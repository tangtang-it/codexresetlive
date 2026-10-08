from pathlib import Path

content = Path("_tpl_body_v2.html").read_text(encoding="utf-8")
start = content.find('<section id="studio">')
end = content.find('</section>', start) + len('</section>')
print(content[start:end])
