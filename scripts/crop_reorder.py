from PIL import Image

img = Image.open("reorder_full_verified.png")
print("Full view size:", img.size)

# 切片 1: 01 Signal Studio 紧随 02 Authority & Proximity (y 轴 600 到 1550)
c1 = img.crop((0, 600, 1280, 1580))
c1.save("reorder_studio_to_monitors.png")

# 切片 2: 后续的 03 Calendar Radar 与 04 Personal Engine (y 轴 1500 到 2300)
c2 = img.crop((0, 1500, 1280, 2300))
c2.save("reorder_cal_engine.png")

print("Generated reordered QA crops successfully!")
