import os
import json
import urllib.request

api_key = os.environ.get("AGNES_API_KEY")
if not api_key:
    print("ERROR: AGNES_API_KEY is not set")
    exit(1)

out_dir = r"D:/ZySpace/zy_code/seo/codexlimit/site/assets"
os.makedirs(out_dir, exist_ok=True)

tasks = [
    {
        "filename": "radar-core-3d.png",
        "prompt": "A modern 3D icon of a futuristic quantum radar scanner with glowing concentric yellow rings, floating tech gyroscope, Binance dark theme, obsidian black background #0b0e11, vibrant yellow #FCD535 neon accents, emerald green pulse dot, premium financial trading terminal 3D asset, octane render, smooth lighting, centered isolated subject"
    },
    {
        "filename": "signal-tower-3d.png",
        "prompt": "A futuristic 3D icon of a satellite signal antenna broadcasting data pulse waves, dark cyberpunk finance theme, matte black metal chassis with glowing Binance yellow #FCD535 accents, isolated on deep dark background #0b0e11, high resolution 3D render, minimalist tech badge"
    }
]

for task in tasks:
    target_path = os.path.join(out_dir, task["filename"])
    print(f"Generating {task['filename']} via Agnes Image 2.5 Flash...")
    payload = {
        "model": "agnes-image-2.5-flash",
        "prompt": task["prompt"],
        "size": "1K",
        "ratio": "1:1",
        "extra_body": {
            "response_format": "url"
        }
    }
    
    req = urllib.request.Request(
        "https://apihub.agnes-ai.com/v1/images/generations",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            res_data = json.loads(resp.read().decode("utf-8"))
            img_url = res_data["data"][0]["url"]
            print(f"Success! Downloading from {img_url} to {target_path}...")
            
            # Download image
            img_req = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(img_req, timeout=60) as img_resp:
                with open(target_path, "wb") as f:
                    f.write(img_resp.read())
            print(f"Saved {task['filename']} ({os.path.getsize(target_path)} bytes)")
    except Exception as e:
        print(f"Failed to generate {task['filename']}: {e}")

print("AGNES_GENERATION_DONE")
