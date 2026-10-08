from PIL import Image

img = Image.open("binance_restored_full.png")
print("Full view size:", img.size)

# 切片 1: 顶部 + Direct Answer + Dual Hero
c1 = img.crop((0, 0, 1280, 850))
c1.save("binance_crop_hero.png")

# 切片 2: Studio 3列 + 计算器
c2 = img.crop((0, 850, 1280, 1750))
c2.save("binance_crop_studio.png")

# 切片 3: 月度日历 + FAQ + 底部
c3 = img.crop((0, 1750, 1280, img.size[1]))
c3.save("binance_crop_calendar.png")

print("Generated restored visual QA images successfully!")
