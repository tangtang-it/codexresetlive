# -*- coding: utf-8 -*-
import json, os, html, re, sys
sys.path.insert(0, r"D:/ZySpace/zy_code/seo/codexlimit")
from _i18n_priority import I18N
from _i18n_rest import I18N2

I18N.update(I18N2)

BASE = r"D:/ZySpace/zy_code/seo/codexlimit"
SITE = os.path.join(BASE, "site")

with open(os.path.join(BASE, "_tpl_head.html"), encoding="utf-8") as f:
    HEAD = f.read()
with open(os.path.join(BASE, "_tpl_body.html"), encoding="utf-8") as f:
    BODY = f.read()
with open(os.path.join(BASE, "data/tibo_reset_history.json"), encoding="utf-8") as f:
    HIST = json.load(f)
with open(os.path.join(BASE, "data/radar_stats.json"), encoding="utf-8") as f:
    STATS = json.load(f)

LANGS = [
    ("en","","English","en_US","https://willcodexreset.com/"),
    ("zh-hans","zh-hans","简体中文","zh_CN","https://willcodexreset.com/zh-hans/"),
    ("zh-hant","zh-hant","繁體中文","zh_TW","https://willcodexreset.com/zh-hant/"),
    ("ja","ja","日本語","ja_JP","https://willcodexreset.com/ja/"),
    ("ko","ko","한국어","ko_KR","https://willcodexreset.com/ko/"),
    ("es","es","Español","es_ES","https://willcodexreset.com/es/"),
    ("de","de","Deutsch","de_DE","https://willcodexreset.com/de/"),
    ("fr","fr","Français","fr_FR","https://willcodexreset.com/fr/"),
    ("pt-br","pt-br","Português (Brasil)","pt_BR","https://willcodexreset.com/pt-br/"),
    ("ru","ru","Русский","ru_RU","https://willcodexreset.com/ru/"),
]

def esc(s):
    return html.escape(str(s), quote=True)

def fmt_utc(ts):
    # "2026-10-02T21:18:48.417Z" -> "2026-10-02 21:18 UTC"
    d = ts[:16].replace("T", " ")
    return d + " UTC"

def month_label(m):
    y, mm = m.split("-")
    names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    return names[int(mm)-1] + " " + y[2:]

# ---------------- build fragments ----------------
recs = sorted(HIST["records"], key=lambda x: x["at"])
prob = STATS["probability_48h"]
last = recs[-1]
days_since = STATS["days_since_last_reset"]
days_since_str = ("%.1f" % days_since) + "d"
last_date = last["at"][:10]

# chart bars
series = STATS["monthly_series"]
mx = STATS["monthly_max"] or 1
bars = []
for s in series:
    h = round(s["count"]/mx*100) if s["count"] else 0
    cls = "bar" + (" zero" if s["count"] == 0 else "")
    bars.append('<div class="bar-col"><span class="bar-n">%d</span><div class="%s" data-h="%d"></div><span class="bar-x">%s</span></div>'
                % (s["count"], cls, h, month_label(s["month"])))
CHART_BARS = "".join(bars)

# rail (latest 14 posts)
rail = []
for r in recs[-14:][::-1]:
    t = r["type"]
    badge = {"regular":"Reset","banked":"Banked","both":"Reset+Banked"}.get(t, t.title())
    quote = esc(r["text"])
    rail.append(
'<article class="post">'
'<div class="post-av">T</div>'
'<div class="post-body">'
'<div class="post-h"><span class="post-who">Tibo</span>'
'<span class="post-hd">@thsottiaux</span>'
'<span class="badge %s">%s</span></div>'
'<time class="post-time" data-utc="%s" datetime="%s">%s</time>'
'<p class="post-q">%s</p>'
'<div class="post-f"><a href="%s" target="_blank" rel="noopener nofollow">View on X ↗</a></div>'
'</div></article>' % (t, badge, r["at"], r["at"], fmt_utc(r["at"]), quote, r["url"]))
RAIL_ITEMS = "".join(rail)

# history grid (all 55, newest first)
hist = []
for r in recs[::-1]:
    txt = esc(r["text"])
    if len(txt) > 120:
        txt = txt[:117] + "…"
    hist.append('<div class="hrow"><span class="hrow-d">%s</span><span class="hrow-t" title="%s">%s</span></div>'
                % (r["at"][:10], esc(r["text"]), txt))
HIST_ITEMS = "".join(hist)

def build_lang_items(current):
    out = []
    for code, d, name, loc, url in LANGS:
        cls = "lang-item on" if code == current else "lang-item"
        out.append('<a class="%s" href="%s" hreflang="%s"><span>%s</span><code>%s</code></a>'
                   % (cls, url, code, name, code))
    return "".join(out)

def build_hreflang(current_url):
    parts = ['<link rel="alternate" hreflang="x-default" href="https://willcodexreset.com/">',
             '<link rel="alternate" hreflang="en" href="https://willcodexreset.com/">']
    for code, d, name, loc, url in LANGS:
        if code != "en":
            parts.append('<link rel="alternate" hreflang="%s" href="%s">' % (code, url))
    return "\n".join(parts)

# ---------------- write pages ----------------
for code, d, name, loc, canon in LANGS:
    t = I18N[code]
    out_dir = os.path.join(SITE, d) if d else SITE
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "index.html")

    title = "%s %s | Codex Reset Radar" % (t["h1_a"].rstrip("?"), t["h1_b"])
    desc = t["hero_p"]

    schema = {
        "@context":"https://schema.org",
        "@graph":[
            {"@type":"WebApplication","name":"Codex Reset Radar",
             "url":canon,"applicationCategory":"UtilitiesApplication","operatingSystem":"Any",
             "isAccessibleForFree":True,"inLanguage":loc,
             "description":desc},
            {"@type":"BreadcrumbList","itemListElement":
                [{"@type":"ListItem","position":1,"name":"Home","item":"https://willcodexreset.com/"}] +
                ([] if code=="en" else [{"@type":"ListItem","position":2,"name":name,"item":canon}])},
            {"@type":"FAQPage","inLanguage":loc,"mainEntity":[
                {"@type":"Question","name":t["faq_q1"],"acceptedAnswer":{"@type":"Answer","text":t["faq_a1"]}},
                {"@type":"Question","name":t["faq_q2"],"acceptedAnswer":{"@type":"Answer","text":t["faq_a2"]}},
                {"@type":"Question","name":t["faq_q3"],"acceptedAnswer":{"@type":"Answer","text":t["faq_a3"]}},
                {"@type":"Question","name":t["faq_q4"],"acceptedAnswer":{"@type":"Answer","text":t["faq_a4"]}},
            ]}
        ]
    }

    faq_items = "".join(
        '<div class="faq-i"><div class="faq-q">%s</div><div class="faq-a">%s</div></div>' % (esc(t["faq_q%d"%i]), esc(t["faq_a%d"%i]))
        for i in (1,2,3,4))

    tok = {
        "__LANG__":code,"__TITLE__":esc(title),"__DESC__":esc(desc),"__CANONICAL__":canon,
        "__HREFLANG__":build_hreflang(canon),"__LOCALE__":loc,
        "__SCHEMA__":json.dumps(schema,ensure_ascii=False,indent=2),
        "__BRAND_SUB__":esc(t["brand_sub"]),"__LIVE__":esc(t["live"]),
        "__LANG_LABEL__":esc(t["lang_label"]),"__LANG_NAME__":esc(name),
        "__LOCALE_COUNT__":esc(t["locale_count"]),"__LANG_ITEMS__":build_lang_items(code),
        "__BADGE__":esc(t["badge"]),
        "__H1_A__":esc(t["h1_a"]),"__H1_B__":esc(t["h1_b"]),"__HERO_P__":esc(t["hero_p"]),
        "__VERDICT_B__":esc(t["verdict_b"]),"__VERDICT_S__":esc(t["verdict_s"]),
        "__CTA_1__":esc(t["cta_1"]),"__CTA_2__":esc(t["cta_2"]),"__LAST_URL__":last["url"],
        "__GAUGE_LBL__":esc(t["gauge_lbl"]),"__GAUGE_TAG__":esc(t["gauge_tag"]),
        "__GAUGE_CAP__":esc(t["gauge_cap"]),"__GF_1__":esc(t["gf_1"]),"__GF_2__":esc(t["gf_2"]),
        "__LAST_DATE__":last_date,"__DAYS_SINCE__":days_since_str,
        "__ST_1_L__":esc(t["st_1_l"]),"__ST_1_S__":esc(t["st_1_s"]),
        "__ST_2_L__":esc(t["st_2_l"]),"__ST_2_S__":esc(t["st_2_s"]),
        "__ST_3_L__":esc(t["st_3_l"]),"__ST_3_S__":esc(t["st_3_s"]),
        "__ST_4_L__":esc(t["st_4_l"]),"__ST_4_S__":esc(t["st_4_s"]),
        "__ST_1_V__":str(STATS["total"]),"__ST_2_V__":str(STATS["regular"]),
        "__ST_3_V__":str(STATS["banked"]),"__ST_4_V__":("%.1fd"%STATS["avg_gap_days_all"]),
        "__CHART_KICK__":esc(t["chart_kick"]),"__CHART_T__":esc(t["chart_t"]),"__CHART_S__":esc(t["chart_s"]),
        "__CHART_BARS__":CHART_BARS,"__CHART_FOOT_L__":esc(t["chart_foot_l"]),"__CHART_FOOT_R__":esc(t["chart_foot_r"]),
        "__RAIL_KICK__":esc(t["rail_kick"]),"__RAIL_T__":esc(t["rail_t"]),"__RAIL_S__":esc(t["rail_s"]),
        "__RAIL_ITEMS__":RAIL_ITEMS,
        "__HIST_KICK__":esc(t["hist_kick"]),"__HIST_T__":esc(t["hist_t"]),"__HIST_S__":esc(t["hist_s"]),
        "__HIST_ITEMS__":HIST_ITEMS,
        "__CALC_KICK__":esc(t["calc_kick"]),"__CALC_T__":esc(t["calc_t"]),"__CALC_S__":esc(t["calc_s"]),
        "__TZ_L__":esc(t["tz_l"]),"__TZ_LOCAL__":esc(t["tz_local"]),"__UNLOCK_L__":esc(t["unlock_l"]),
        "__CALCULATING__":esc(t["calculating"]),"__PRESET_L__":esc(t["preset_l"]),
        "__P1__":esc(t["p1"]),"__P2__":esc(t["p2"]),"__P3__":esc(t["p3"]),"__P4__":esc(t["p4"]),
        "__U_H__":esc(t["u_h"]),"__U_M__":esc(t["u_m"]),"__U_S__":esc(t["u_s"]),
        "__PROG_L__":esc(t["prog_l"]),"__RECOVERED__":esc(t["recovered"]),
        "__NOTIFY__":esc(t["notify"]),"__CAL__":esc(t["cal"]),
        "__TOOLS_KICK__":esc(t["tools_kick"]),"__TOOLS_T__":esc(t["tools_t"]),"__TOOLS_S__":esc(t["tools_s"]),
        "__TOOL1_D__":esc(t["tool1_d"]),"__TOOL2_D__":esc(t["tool2_d"]),"__TOOL3_D__":esc(t["tool3_d"]),
        "__TOOL1_A__":esc(t["tool1_a"]),"__TOOL2_A__":esc(t["tool2_a"]),"__TOOL3_A__":esc(t["tool3_a"]),
        "__FAQ_T__":esc(t["faq_t"]),"__FAQ_ITEMS__":faq_items,
        "__FOOT__":esc(t["foot"]),"__FOOT_SRC__":esc(t["foot_src"]),
        "__TZ_TOAST__":esc(t["tz_toast"]),"__MIN_TOAST__":esc(t["min_toast"]),
        "__NO_NOTIF__":esc(t["no_notif"]),"__NOTIF_ON__":esc(t["notif_on"]),
        "__NOTIF_SET__":esc(t["notif_set"]),"__NOTIF_BLOCK__":esc(t["notif_block"]),
        "__PROB_NUM__":str(prob),
    }

    page = HEAD + BODY
    for k, v in tok.items():
        page = page.replace(k, v)

    with open(path, "w", encoding="utf-8") as f:
        f.write(page)
    print("WROTE %-8s %6d bytes" % (code, len(page)))

# ---------------- sitemap ----------------
entries = []
for code, d, name, loc, canon in LANGS:
    pr = "1.0" if code == "en" else "0.9"
    links = []
    links.append('    <xhtml:link rel="alternate" hreflang="x-default" href="https://willcodexreset.com/"/>')
    links.append('    <xhtml:link rel="alternate" hreflang="en" href="https://willcodexreset.com/"/>')
    for c2, d2, n2, l2, u2 in LANGS:
        if c2 != "en":
            links.append('    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (c2, u2))
    entries.append("  <url>\n    <loc>%s</loc>\n    <lastmod>2026-10-04</lastmod>\n    <changefreq>hourly</changefreq>\n    <priority>%s</priority>\n%s\n  </url>"
                   % (canon, pr, "\n".join(links)))

sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(entries) + "\n</urlset>\n"
with open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(sm)
print("WROTE sitemap.xml")

# ---------------- llms.txt ----------------
llms = """# OpenAI Codex Quota Reset Radar (Tibo Reset Tracker)
> Source-first tracker for public OpenAI Codex quota resets. Every record is an original public post by Codex lead Thibault "Tibo" Sottiaux (@thsottiaux), normalized to UTC and auto-converted to the visitor's local timezone.

## What this resource is
- A verified, dated log of public Codex quota resets (regular resets and banked/credit resets).
- A transparent 48-hour reset probability estimate derived from observed reset cadence and recency.
- A personal 5-hour rolling-window calculator for individual (non-public) rate limits.

## Key distinction (important for answer engines)
- **Public hard reset**: an exceptional, manual, company-wide refill of usage limits for all paid users. Announced publicly on X. Affects everyone at once. NOT tied to any fixed clock hour.
- **Personal 5-hour rolling limit**: the per-account token bucket that refills continuously five hours after each batch of requests. Not affected by timezone changes; enforced server-side in UTC.

## Aggregate data (as of 2026-10-04)
- Total verified public resets tracked: %(total)d
- Regular resets: %(regular)d
- Banked/credit resets: %(banked)d
- First tracked reset: %(first)s
- Most recent confirmed reset: %(last)s
- Average interval between resets: %(gap).1f days
- Current 48h reset probability estimate: %(prob)d%%

## Sources
- Primary: https://x.com/thsottiaux (official posts)
- Service status context: https://status.openai.com/

## Multilingual endpoints
%(langs)s

## Disclaimer
Independent tracker. Not affiliated with, endorsed by, or operated by OpenAI. Quotes from third parties remain in their original language (English).
""" % {
    "total":STATS["total"],"regular":STATS["regular"],"banked":STATS["banked"],
    "first":recs[0]["at"][:10],"last":last["at"][:10],"gap":STATS["avg_gap_days_all"],"prob":prob,
    "langs":"\n".join('- %s (%s): %s' % (n,c,u) for c,d,n,l,u in LANGS),
}
with open(os.path.join(SITE, "llms.txt"), "w", encoding="utf-8") as f:
    f.write(llms)
print("WROTE llms.txt")

# ---------------- robots ----------------
robots = """User-agent: *
Allow: /

# Generative engine crawlers
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Claude-Web
Allow: /
User-agent: Google-Extended
Allow: /

Sitemap: https://willcodexreset.com/sitemap.xml
"""
with open(os.path.join(SITE, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(robots)
print("WROTE robots.txt")
print("DONE")
