from PIL import Image
from pathlib import Path

img = Image.open("qa_full_verified.png")
print("Full shot dimensions:", img.size)

# 1. 裁剪 Header + Direct Answer Banner + Dual Hero (上部 0 到 800)
crop_top = img.crop((0, 0, 1280, 850))
crop_top.save("qa_crop_hero_fixed.png")

# 2. 裁剪 3-Column Studio 控制台 + 5小时恢复计算器 (850 到 1700)
crop_mid = img.crop((0, 850, 1280, 1750))
crop_mid.save("qa_crop_studio_fixed.png")

# 3. 裁剪 日历与底栏 (1750 到 底部)
crop_bot = img.crop((0, 1750, 1280, img.size[1]))
crop_bot.save("qa_crop_calendar_fixed.png")

print("Generated visual inspection crops successfully!")
