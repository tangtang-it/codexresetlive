from pathlib import Path

head_path = Path("_tpl_head_v2.html")
c = head_path.read_text(encoding="utf-8")

c = c.replace("linear-gradient(135deg,#FCD535,#f0b90b)", "linear-gradient(135deg,#5e6ad2,#828fff)")
c = c.replace("#FCD535", "#5e6ad2")
c = c.replace("#f0b90b", "#4f5bb5")

head_path.write_text(c, encoding="utf-8")
print("Cleaned .post-av gradient in _tpl_head_v2.html")
