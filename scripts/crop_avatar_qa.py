from PIL import Image
import os

img = Image.open("tibo_avatar_full.png")
# 我们裁切 Studio 区域从 y=500 到 y=1400，看一下
studio_crop = img.crop((40, 650, 1240, 1280))
studio_crop.save("tibo_avatar_studio_crop.png")

# 针对中间列（Col 2: x 从 400 到 880，y 从 660 到 760）
header_crop = img.crop((420, 690, 860, 770))
header_crop.save("tibo_avatar_header_detail.png")
print("Cropped successfully.")