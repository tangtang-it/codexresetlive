from PIL import Image

img = Image.open("stamp_full_view.png")
print("Full view size:", img.size)

# 切片 1: 专门特写顶部的 Direct Answer 动态大印章横幅 (y 轴 60 到 440)
c1 = img.crop((0, 60, 1280, 480))
c1.save("stamp_crop_banner.png")

# 切片 2: 包含整个 Hero 区域 (y 轴 0 到 900)
c2 = img.crop((0, 0, 1280, 920))
c2.save("stamp_crop_hero.png")

print("Generated stamp visual QA images successfully!")
