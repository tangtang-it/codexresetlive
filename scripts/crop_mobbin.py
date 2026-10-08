from PIL import Image

img = Image.open("mobbin_full_view.png")
print("Full shot dimensions:", img.size)

# 切片 1: 顶部悬浮导航 + 答案条 + 双核心卡片
c1 = img.crop((0, 0, 1280, 850))
c1.save("mobbin_crop_hero.png")

# 切片 2: 3列 Studio 控制台 + 5小时滚动计算器
c2 = img.crop((0, 850, 1280, 1750))
c2.save("mobbin_crop_studio.png")

# 切片 3: 月度日历 + Polarity Inversion 纯黑底板
c3 = img.crop((0, 1750, 1280, img.size[1]))
c3.save("mobbin_crop_footer.png")

print("Generated Mobbin visual crops successfully!")
