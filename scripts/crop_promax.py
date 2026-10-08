from PIL import Image

img = Image.open("promax_full_view.png")
print("Full view size:", img.size)

# 切片 1: 顶部导航 + Direct Answer + Dual Hero (上部 0 到 850)
c1 = img.crop((0, 0, 1280, 850))
c1.save("promax_crop_hero.png")

# 切片 2: 3列 Studio 控制台 + 5小时滚动恢复计算器 (850 到 1750)
c2 = img.crop((0, 850, 1280, 1750))
c2.save("promax_crop_studio.png")

# 切片 3: 月度日历 + FAQ + 底部 (1750 到底部)
c3 = img.crop((0, 1750, 1280, img.size[1]))
c3.save("promax_crop_calendar.png")

print("Generated Pro Max visual QA images successfully!")
