import json

data = json.load(open("D:/ZySpace/zy_code/seo/codexlimit/audit_result.json", encoding="utf-8"))

for lang, p in data["pages"].items():
    print(f"==================================================")
    print(f"=== Language: {lang.upper()} ===")
    print(f"Title ({p['title_len']} chars): {p['title']}")
    print(f"Description ({p['description_len']} chars): {p['description']}")
    print(f"Keywords ({p['keywords_count']}): {p['keywords']}")
    print(f"Canonical: {p['canonical']}")
    print(f"H1 Count: {p['h1_count']} -> {p['h1_texts']}")
    print("Hreflangs:")
    for hl, url in p["hreflangs"].items():
        print(f"  {hl} -> {url}")
    print("Headings hierarchy:")
    for h in p["headings"]:
        print(f"  {h['tag']}: {h['text'][:40]}")
    print(f"External scripts: {p['external_scripts']}")
    print(f"External styles: {p['external_styles']}")
    print(f"JSON-LD Count: {len(p['json_lds'])}")
    for i, j in enumerate(p["json_lds"]):
        if j["valid"]:
            d = j["data"]
            t = d.get("@type", "Unknown") if isinstance(d, dict) else [item.get("@type") for item in d] if isinstance(d, list) else "Raw"
            print(f"  [{i}] @type: {t}")
        else:
            print(f"  [{i}] Invalid JSON-LD: {j['error']}")
    print("OpenGraph:")
    for k, v in p["og"].items():
        print(f"  {k}: {v}")

print("
==================================================")
print("=== ROBOTS.TXT ===")
print(data["robots"].get("raw", ""))

print("
==================================================")
print("=== SITEMAP.XML ===")
print(data["sitemap"].get("raw", ""))
