# -*- coding: utf-8 -*-
import re, json, sys
from pathlib import Path

site_dir = Path("site")
html_files = [f for f in site_dir.rglob("*.html") if "reset-history" not in str(f)]

print(f"Total HTML files verified: {len(html_files)}")
all_ok = True

for hf in sorted(html_files):
    content = hf.read_text(encoding="utf-8")
    rel_path = str(hf.relative_to(site_dir))

    # 1. Check for unreplaced placeholders
    unreplaced = re.findall(r"__[A-Z0-9_]+__", content)
    if unreplaced:
        print(f"FAILED: {hf} has unreplaced placeholders: {set(unreplaced)}")
        all_ok = False

    # 2. Check canonical & hreflang
    canonical = re.search(r'<link rel="canonical" href="(.*?)">', content)
    hreflangs = re.findall(r'<link rel="alternate" hreflang="(.*?)" href="(.*?)">', content)
    if not canonical:
        print(f"FAILED: {hf} missing canonical link")
        all_ok = False

    # 3. Check JSON-LD schema based on page type
    schema_match = re.search(r'<script type="application/ld\+json">\s*({.*?})\s*</script>', content, re.DOTALL)
    if not schema_match:
        print(f"FAILED: {hf} missing schema JSON-LD")
        all_ok = False
    else:
        try:
            schema_obj = json.loads(schema_match.group(1))
            graph = schema_obj.get("@graph", [])
            types = [item.get("@type") for item in graph]
            if "history" in rel_path:
                if "DataCatalog" not in types:
                    print(f"FAILED: {hf} history schema missing DataCatalog: {types}")
                    all_ok = False
            elif "methodology" in rel_path:
                if "TechArticle" not in types:
                    print(f"FAILED: {hf} methodology schema missing TechArticle: {types}")
                    all_ok = False
            elif "reset-today" in rel_path:
                if "WebPage" not in types:
                    print(f"FAILED: {hf} reset-today schema missing WebPage: {types}")
                    all_ok = False
            else:
                if "FAQPage" not in types or "WebApplication" not in types:
                    print(f"FAILED: {hf} home schema missing FAQPage or WebApplication: {types}")
                    all_ok = False
        except Exception as e:
            print(f"FAILED: {hf} schema json decode error: {e}")
            all_ok = False

    # Check key sections for main landing pages
    if not any(sub in rel_path for sub in ["history", "methodology", "reset-today"]):
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
            print(f"FAILED: {hf} missing key home sections!")
            all_ok = False
        else:
            print(f"OK [HOME]: {rel_path:24s} | Size: {len(content):,} B | Canonical: {canonical.group(1)}")
    else:
        print(f"OK [SUB] : {rel_path:24s} | Size: {len(content):,} B | Canonical: {canonical.group(1)}")

if all_ok:
    print("ALL VERIFIED FILES PASSED INTEGRITY, SCHEMA & SECTION AUDIT 100%!")
else:
    print("AUDIT FAILED!")
    sys.exit(1)