import subprocess, json, time, urllib.request

# 启动带 remote-debugging-port 的 Edge 实例测量高度
port = 9222
cmd = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "--headless",
    "--disable-gpu",
    f"--remote-debugging-port={port}",
    "http://localhost:8080/zh-hans/"
]

proc = subprocess.Popen(cmd)
time.sleep(1.5)

try:
    # 获取 targets
    resp = urllib.request.urlopen(f"http://127.0.0.1:{port}/json").read().decode("utf-8")
    targets = json.loads(resp)
    ws_url = targets[0]["webSocketDebuggerUrl"]
    print("Edge CDP ready, targets:", len(targets))
except Exception as e:
    print("CDP Connect error:", e)
finally:
    proc.terminate()
