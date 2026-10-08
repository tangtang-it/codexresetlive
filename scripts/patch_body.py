import re
from pathlib import Path

# 1. 更新 _tpl_body_v2.html
body_path = Path("_tpl_body_v2.html")
b = body_path.read_text(encoding="utf-8")

# 替换 Brand Mark 里的 SVG 颜色
b = b.replace('stroke="#FCD535"', 'stroke="#5e6ad2"')
b = b.replace('fill="#FCD535"', 'fill="#828fff"')

# 替换 JS 内联函数中的旧颜色
b = b.replace('stroke="#f6465d"', 'stroke="#ef4444"')
b = b.replace('stroke="#0ecb81"', 'stroke="#27a644"')
# 时钟和铃铛使用 Linear 蓝紫与琥珀金
b = b.replace("if(k==='clock') return '<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"#FCD535\"", "if(k==='clock') return '<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"#5e6ad2\"")
b = b.replace("if(k==='bell') return '<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"#FCD535\"", "if(k==='bell') return '<svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"#f59e0b\"")

body_path.write_text(b, encoding="utf-8")
print("Updated _tpl_body_v2.html successfully")
