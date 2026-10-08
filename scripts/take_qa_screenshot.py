import subprocess
import time
import os
import shutil
from PIL import Image

chrome_exe = "C:/Program Files/Google/Chrome/Application/chrome.exe"
if not os.path.exists(chrome_exe):
    chrome_exe = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"

out_png = "tibo_avatar_full.png"
temp_profile = os.path.join(os.environ.get("TEMP", "C:/temp"), "browser_qa_temp").replace("\\", "/")
if os.path.exists(temp_profile):
    shutil.rmtree(temp_profile, ignore_errors=True)

cmd = [
    chrome_exe,
    "--headless=new",
    "--disable-gpu",
    f"--user-data-dir={temp_profile}",
    "--window-size=1280,1800",
    f"--screenshot={os.path.abspath(out_png)}",
    "http://localhost:8080/"
]

print("Running screenshot command with:", chrome_exe)
res = subprocess.run(cmd, capture_output=True, text=True)
print("Exit code:", res.returncode)
time.sleep(1)

if os.path.exists(out_png):
    print("Screenshot captured successfully:", out_png)
    img = Image.open(out_png)
    print("Full image size:", img.size)
    
    # 裁切 studio 区域
    crop_studio = img.crop((0, 600, 1280, 1300))
    crop_studio.save("tibo_avatar_studio_crop.png")
    
    # 裁切 Col 2 header 区域
    crop_col2 = img.crop((380, 700, 850, 780))
    crop_col2.save("tibo_avatar_header_detail.png")
    print("Cropped views saved.")
else:
    print("Screenshot failed! stderr:", res.stderr)