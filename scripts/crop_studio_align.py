from PIL import Image

img = Image.open("studio_align_verified.png")
print("Full view size:", img.size)

# 裁切 01 - Signal Studio 的完整区域 (y 轴 620 到 1380)
crop = img.crop((0, 620, 1280, 1380))
crop.save("aligned_studio_crop.png")

print("Cropped aligned studio visual QA snapshot successfully!")
