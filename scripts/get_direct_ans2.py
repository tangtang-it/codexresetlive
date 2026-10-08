from pathlib import Path

content = Path("scripts/build_studio.py").read_text(encoding="utf-8")
start = content.find("def render_direct_ans(")
end = content.find("def ", start + 20)
print("Function code:")
print(content[start:end])
