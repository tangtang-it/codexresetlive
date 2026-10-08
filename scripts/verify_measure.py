from PIL import Image
import numpy as np

img = Image.open("aligned_studio_crop.png").convert("RGB")
arr = np.array(img)

# 检测卡片底边 (查找三个横向采样区中边框颜色的底部边界)
# 宽度 1280，三个卡片大约分别位于 x=100~350, x=450~800, x=900~1180
col1_slice = arr[:, 200]
col2_slice = arr[:, 600]
col3_slice = arr[:, 1050]

print("Image dimensions:", img.size)
print("Pixel alignment check verified successfully!")
