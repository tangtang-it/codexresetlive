from PIL import Image
import numpy as np

img = Image.open("tibo_avatar_col2_header.png")
arr = np.array(img)
print("Shape:", arr.shape)
print("Min pixel:", arr.min(), "Max pixel:", arr.max(), "Mean pixel:", arr.mean())

# 检查头像大致区域（左侧约 x: 10~50, y: 15~55）的方差，确认不是空白占位
avatar_patch = arr[10:60, 10:60]
print("Avatar patch std dev:", avatar_patch.std(), "mean:", avatar_patch.mean())

full_img = Image.open("tibo_avatar_full.png")
# 获取绝对路径供输出
import os
print("Full path:", os.path.abspath("tibo_avatar_col2_header.png"))
print("3col path:", os.path.abspath("tibo_avatar_studio_3col.png"))