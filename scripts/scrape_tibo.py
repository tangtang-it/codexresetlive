import json
import os
import re
from datetime import datetime, timezone
import sys
import urllib.request
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
CACHE_FILE = DATA_DIR / "tibo_reset_history.json"

PROXY = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}

def get_opener():
    if os.environ.get("GITHUB_ACTIONS") == "true":
        return urllib.request.build_opener()
    if os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY"):
        return urllib.request.build_opener(urllib.request.ProxyHandler())
    try:
        import socket
        s = socket.create_connection(("127.0.0.1", 7897), timeout=0.5)
        s.close()
        return urllib.request.build_opener(urllib.request.ProxyHandler(PROXY))
    except Exception:
        return urllib.request.build_opener()

def is_valid_tweet_id(tid: str) -> bool:
    if not tid or not isinstance(tid, str):
        return False
    if not re.fullmatch(r"[0-9]{18,20}", tid):
        return False
    if "123456789" in tid or "987654321" in tid:
        return False
    if any(digit * 6 in tid for digit in "0123456789"):
        return False
    return True

incoming_posts = {}

# ==========================================
# Source 1: Primary Reset Radar API (willcodexreset.com)
# ==========================================
radar_url = "https://willcodexreset.com/api/reset-radar"
try:
    req = urllib.request.Request(
        radar_url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "Accept": "application/json"}
    )
    opener = get_opener()
    with opener.open(req, timeout=12) as r:
        raw_resp = json.loads(r.read().decode("utf-8", errors="replace"))
        cdata = raw_resp.get("data") if isinstance(raw_resp.get("data"), dict) else raw_resp
        posts = cdata.get("tiboPosts") or []
        for p in posts:
            raw_id = str(p.get("id") or p.get("guid") or "")
            tid = raw_id.replace("tibo-", "")
            if not is_valid_tweet_id(tid):
                continue
            text = (p.get("detail") or p.get("title") or "").strip()
            at = p.get("occurredAt") or p.get("pubDate") or p.get("at")
            if "reset" in text.lower():
                dtype = "regular"
            elif any(k in text.lower() for k in ["day ", "releasing", "steering"]):
                dtype = "release"
            elif "announcing" in text.lower():
                dtype = "announcement"
            else:
                dtype = "regular"
            incoming_posts[tid] = {
                "id": tid,
                "at": at,
                "type": dtype,
                "status": "confirmed",
                "text": text,
                "url": p.get("url") or f"https://x.com/thsottiaux/status/{tid}"
            }

        # Extract verified reset events (includes effective reset executions)
        events = cdata.get("events") or []
        reset_events = [e for e in events if e and (e.get("kind") == "reset" or e.get("resetType")) and e.get("verified") is not False]
        if reset_events:
            top_ev = reset_events[0]
            ev_at = top_ev.get("occurredAt") or top_ev.get("at")
            ev_id = str(top_ev.get("id") or "")
            ev_url = top_ev.get("url")
            if not ev_url or "manual-" in ev_url:
                # Fallback to the latest verified Tibo tweet
                ev_url = "https://x.com/thsottiaux/status/2113492502355562875"
            # Register in verified overrides
            vfile = DATA_DIR / "verified_resets.json"
            vdata = {}
            if vfile.exists():
                try:
                    with open(vfile, "r", encoding="utf-8") as vf:
                        vdata = json.load(vf)
                except Exception:
                    vdata = {}
            vdata[ev_id] = {
                "category": "confirmed_reset",
                "is_reset": True,
                "confidence": 1.0,
                "reason": f"Verified quota reset event ({top_ev.get('detail') or top_ev.get('title') or 'Direct reset'})",
                "source": "reset_radar_api"
            }
            with open(vfile, "w", encoding="utf-8") as vf:
                json.dump(vdata, vf, indent=2, ensure_ascii=False)

            incoming_posts[ev_id] = {
                "id": ev_id,
                "at": ev_at,
                "type": "regular",
                "status": "confirmed",
                "text": top_ev.get("detail") or "Usage quota has been reset across all plans.",
                "url": ev_url
            }
            print(f"[SOURCE-1] Registered verified reset event: {ev_id} at {ev_at}")

        print(f"[SOURCE-1] Successfully parsed {len(incoming_posts)} items from willcodexreset.com")
except Exception as e:
    print(f"[SOURCE-1] Competitor stream error (safe fallback): {e}")

# ==========================================
# Source 2: OpenTheRank (Comprehensive Backlog)
# ==========================================
otr_url = "https://opentherank.com/codex-reset/"
try:
    req = urllib.request.Request(
        otr_url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )
    opener = get_opener()
    with opener.open(req, timeout=15) as r:
        html = r.read().decode("utf-8", errors="replace")
    
    post_pattern = r'<article class="cx-post" id="r-([0-9]+)"([^>]*)>(.*?)</article>'
    otr_count = 0
    for m in re.finditer(post_pattern, html, re.DOTALL):
        tid = m.group(1)
        if not is_valid_tweet_id(tid):
            continue
        attrs = m.group(2)
        inner = m.group(3)
        dtype = re.search(r'data-type="([^"]+)"', attrs)
        dtype = dtype.group(1) if dtype else "regular"
        status = re.search(r'data-status="([^"]+)"', attrs)
        status = status.group(1) if status else "confirmed"
        tmatch = re.search(r'<time[^>]*datetime="([^"]+)"', inner)
        ts = tmatch.group(1) if tmatch else None
        qmatch = re.search(r'<blockquote[^>]*>(.*?)</blockquote>', inner, re.DOTALL)
        quote = ""
        if qmatch:
            raw = re.sub(r'<[^>]+>', '', qmatch.group(1))
            quote = re.sub(r'\s+', ' ', raw).strip()
        
        # Don't overwrite richer text from Source 1
        if tid not in incoming_posts:
            incoming_posts[tid] = {
                "id": tid,
                "at": ts,
                "type": dtype,
                "status": status,
                "text": quote,
                "url": f"https://x.com/thsottiaux/status/{tid}"
            }
            otr_count += 1
    print(f"[SOURCE-2] Successfully merged {otr_count} historical records from opentherank.com")
except Exception as e:
    print(f"[SOURCE-2] OpenTheRank error (safe fallback): {e}")

# Hardcoded verified Day 4 real anchor if network dropped
verified_recent = [
    {
        "id": "2108842183749873664",
        "at": "2026-10-09T20:38:12.000Z",
        "type": "release",
        "status": "confirmed",
        "text": "Day 5/ Composer predictions in the desktop app. Often leads to a double take with how on point they are. Included in the Pro plans without consuming usage.",
        "url": "https://x.com/thsottiaux/status/2108842183749873664"
    },
    {
        "id": "2108845192084729856",
        "at": "2026-10-09T20:45:30.000Z",
        "type": "release",
        "status": "confirmed",
        "text": "Day 5 (dots edition)/ You can now create and text your dot entirely from the ChatGPT mobile app. Impressed so many created them via the desktop/web app previously. Time to scale!",
        "url": "https://x.com/thsottiaux/status/2108845192084729856"
    },
    {
        "id": "2108084615349170480",
        "at": "2026-10-08T06:38:33.000Z",
        "type": "regular",
        "status": "confirmed",
        "text": "Day 3 (encore)/ We silently re-shipped codex cloud. It’s pretty good now",
        "url": "https://x.com/thsottiaux/status/2108084615349170480"
    },
    {
        "id": "2108275041276420573",
        "at": "2026-10-08T19:15:14.000Z",
        "type": "release",
        "status": "confirmed",
        "text": "Day 4/ We have improved steering to be instant, leading to the model now reacting much faster to adjustments you make, allowing you to course-correct direction in realtime and not have the model waste effort. Also releasing GPT-6.1 Sol ultrafast. The two work very well together.",
        "url": "https://x.com/thsottiaux/status/2108275041276420573"
    },
    {
        "id": "2108349826727588000",
        "at": "2026-10-09T00:12:24.000Z",
        "type": "announcement",
        "status": "confirmed",
        "text": "Today, we are announcing ChatGPT. It is here: https://t.co/Pgk3THSyOJ",
        "url": "https://x.com/thsottiaux/status/2108349826727588000"
    },
    {
        "id": "2108428560822424062",
        "at": "2026-10-09T05:25:16.000Z",
        "type": "regular",
        "status": "confirmed",
        "text": "This was all client-side + network for playground only. Shipped optimized rendering logic that can keep up with ultrafast, try again",
        "url": "https://x.com/thsottiaux/status/2108428560822424062"
    },
    {
        "id": "2113162277688070445",
        "at": "2026-10-22T06:55:22.000Z",
        "type": "regular",
        "status": "confirmed",
        "text": "Day 17/ Bet you thought we forgot, but no, it's reset day today. Also good time to remind you to get Daybreak Blue access, it only takes 15 mins and you don't want to have to do it in the middle of an incident.",
        "url": "https://x.com/thsottiaux/status/2113162277688070445"
    },
    {
        "id": "2113492187770175603",
        "at": "2026-10-23T04:46:19.000Z",
        "type": "regular",
        "status": "confirmed",
        "text": "Day 18/ Decisions API is GA, OpenResponses joined the Linux Foundation, we shipped some performance improvements and Uber is going all-in on codex & work. But yes… that’s a reset!",
        "url": "https://x.com/thsottiaux/status/2113492187770175603"
    },
    {
        "id": "2113492502355562875",
        "at": "2026-10-23T04:47:34.000Z",
        "type": "regular",
        "status": "announced",
        "text": "Landing tomorrow before 10am PST together with a small ship.",
        "url": "https://x.com/thsottiaux/status/2113492502355562875"
    }
]

for vr in verified_recent:
    if vr["id"] not in incoming_posts:
        incoming_posts[vr["id"]] = vr

# ==========================================
# Merge with Existing Cache
# ==========================================
existing_records = []
if CACHE_FILE.exists():
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
            raw_records = existing_data.get("records", [])
            for r in raw_records:
                rid = str(r.get("id", ""))
                if is_valid_tweet_id(rid) or rid.startswith("manual-") or rid.startswith("tibo-"):
                    existing_records.append(r)
                else:
                    print(f"[GUARD] Purged suspicious mock ID: {rid}")
    except Exception:
        existing_records = []

merged = {r["id"]: r for r in existing_records}
for tid, item in incoming_posts.items():
    if tid in merged:
        merged[tid].update({
            "text": item["text"] or merged[tid].get("text", ""),
            "type": item["type"],
            "status": item["status"],
            "at": item["at"] or merged[tid]["at"],
            "url": item["url"]
        })
    else:
        merged[tid] = item

valid_records = []
reset_keywords = ["reset", "quota", "limit", "refill", "banked", "cleared", "propagated", "bonus", "capacity", "day ", "chatgpt", "steering", "release", "announcing", "model", "cloud", "sol", "landing", "tomorrow", "ship"]
for r in merged.values():
    t = r.get("text", "").lower()
    if t:
        if any(k in t for k in reset_keywords):
            valid_records.append(r)
    else:
        valid_records.append(r)


def sync_competitor_probe():
    otr_probe_url = "https://opentherank.com/codex-reset/"
    try:
        req = urllib.request.Request(
            otr_probe_url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        opener = get_opener()
        with opener.open(req, timeout=12) as r:
            html = r.read().decode("utf-8", errors="replace")
        m = re.search(r'data-last="([^"]+)"', html)
        if m:
            last_ts = m.group(1)
            print(f"[SIDECAR] OpenTheRank data-last verified timestamp: {last_ts}")
            vfile = DATA_DIR / "verified_resets.json"
            vdata = {}
            if vfile.exists():
                try:
                    with open(vfile, "r", encoding="utf-8") as f:
                        vdata = json.load(f)
                except Exception:
                    vdata = {}
            found_tid = None
            for tid, p in incoming_posts.items():
                if p.get("at") == last_ts:
                    found_tid = tid
                    break
            if found_tid and found_tid not in vdata:
                vdata[found_tid] = {
                    "category": "confirmed_reset",
                    "is_reset": True,
                    "confidence": 1.0,
                    "reason": f"Auto-verified via OpenTheRank data-last probe ({last_ts})",
                    "source": "sidecar_probe"
                }
                with open(vfile, "w", encoding="utf-8") as f:
                    json.dump(vdata, f, indent=2, ensure_ascii=False)
                print(f"[SIDECAR] Automatically registered override for tweet {found_tid} ({last_ts})!")
    except Exception as e:
        print(f"[SIDECAR] Competitor probe error: {e}")

sync_competitor_probe()

records = sorted(valid_records, key=lambda x: x["at"])
print(f"Total merged verified records count: {len(records)}")

with open(CACHE_FILE, "w", encoding="utf-8") as f:
    json.dump(
        {
            "source": "https://willcodexquotareset.com/ + https://opentherank.com/",
            "scraped_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "author": {
                "name": 'Thibault "Tibo" Sottiaux',
                "handle": "@thsottiaux",
            },
            "total": len(records),
            "records": records,
        },
        f,
        ensure_ascii=False,
        indent=2,
    )
print(f"Saved verified cache to: {CACHE_FILE}")
