from pathlib import Path

content = Path("scripts/build_studio.py").read_text(encoding="utf-8")

# 检查 render_direct_ans 的完整返回结构
start = content.find("def render_direct_ans(")
end = content.find("def build_lang_items", start)
print(content[start:end])
