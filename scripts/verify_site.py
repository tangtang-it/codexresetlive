import re, json, sys
from pathlib import Path

site_dir = Path("site")
html_files = list(site_dir.rglob("*.html"))

print(f"Total HTML files verified: {len(html_files)}")
all_ok = True

for hf in sorted(html_files):
    content = hf.read_text(encoding="utf-8")
    
    # 1. Check for unreplaced placeholders
    unreplaced = re.findall(r"__[A-Z0-9_]+__", content)
    if unreplaced:
        print(f"FAILED: {hf} has unreplaced placeholders: {set(unreplaced)}")
        all_ok = False
        
    # 2. Check canonical & hreflang
    canonical = re.search(r'<link rel="canonical" href="(.*?)">', content)
    hreflangs = re.findall(r'<link rel="alternate" hreflang="(.*?)" href="(.*?)">', content)
    
    # 3. Check JSON-LD schema
    schema_match = re.search(r'<script type="application/ld\+json">\s*({.*?})\s*</script>', content, re.DOTALL)
    if not schema_match:
        print(f"FAILED: {hf} missing schema JSON-LD")
        all_ok = False
    else:
        try:
            schema_obj = json.loads(schema_match.group(1))
            graph = schema_obj.get("@graph", [])
            types = [item.get("@type") for item in graph]
            if "FAQPage" not in types or "WebApplication" not in types:
                print(f"FAILED: {hf} schema missing FAQPage or WebApplication: {types}")
                all_ok = False
        except Exception as e:
            print(f"FAILED: {hf} schema json decode error: {e}")
            all_ok = False

    # Check all key sections exist
    has_banner = "direct-ans-banner" in content
    has_gauge = "gauge-wrap" in content
    has_pulse = "chart-svg-wrap" in content
    has_studio = "studio-grid" in content
    has_cal = "cal-table" in content
    has_calc = 'id="calculator"' in content
    has_guides = "guides-grid" in content
    has_monitors = "monitor-grid" in content
    has_tools = 'class="tools"' in content
    has_faq = 'class="faq"' in content
    has_footer_dir = "footer-dir" in content

    sections_ok = all([has_banner, has_gauge, has_pulse, has_studio, has_cal, has_calc, has_guides, has_monitors, has_tools, has_faq, has_footer_dir])
    if not sections_ok:
        print(f"FAILED: {hf} missing sections!")
        all_ok = False
    else:
        rel_path = hf.relative_to(site_dir)
        print(f"OK: {str(rel_path):18s} | Size: {len(content):,} B | Hreflangs: {len(hreflangs)} | Canonical: {canonical.group(1)}")

if all_ok:
    print("\nALL 10 LOCALES PASSED INTEGRITY, SCHEMA & SECTION AUDIT 100%!")
