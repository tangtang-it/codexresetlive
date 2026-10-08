from PIL import Image

img = Image.open("studio_compact_full.png")
print("Full view size:", img.size)

# 裁切 01 - Signal Studio 的完整紧凑区域 (y 轴 600 到 1300)
crop = img.crop((0, 600, 1280, 1300))
crop.save("compact_studio_crop.png")

print("Cropped compact studio visual QA snapshot successfully!")
