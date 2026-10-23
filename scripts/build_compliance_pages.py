# -*- coding: utf-8 -*-
import json, html
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SITE_DIR = ROOT_DIR / "site"

with open(ROOT_DIR / "_tpl_head_v2.html", encoding="utf-8") as f:
    HEAD = f.read()

def esc(s):
    return html.escape(str(s), quote=True)

def build_compliance_page(slug, title, desc, h1, sub_p, content_html, schema_type):
    canon_url = f"https://codexresetlive.com/{slug}/"
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": "https://codexresetlive.com/#organization",
                "name": "CodexReset Radar Team",
                "url": "https://codexresetlive.com/",
                "logo": "https://codexresetlive.com/favicon-32x32.png"
            },
            {
                "@type": schema_type,
                "@id": f"{canon_url}#{slug}",
                "url": canon_url,
                "name": title,
                "description": desc,
                "isPartOf": {
                    "@type": "WebSite",
                    "@id": "https://codexresetlive.com/#website",
                    "url": "https://codexresetlive.com/",
                    "name": "CodexReset.live"
                },
                "breadcrumb": {
                    "@type": "BreadcrumbList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://codexresetlive.com/"},
                        {"@type": "ListItem", "position": 2, "name": h1, "item": canon_url}
                    ]
                }
            }
        ]
    }

    hreflang_tags = f'<link rel="alternate" hreflang="x-default" href="{canon_url}">\n<link rel="alternate" hreflang="en" href="{canon_url}">'

    head = HEAD.replace("__LANG__", "en").replace("__TITLE__", esc(title)).replace("__DESC__", esc(desc))
    head = head.replace("__CANONICAL__", canon_url).replace("__LOCALE__", "en_US")
    head = head.replace("__HREFLANG__", hreflang_tags)
    head = head.replace("__SCHEMA__", json.dumps(schema, ensure_ascii=False, indent=2))

    body = f'''<header class="hdr">
<div class="wrap hdr-in">
<a class="brand" href="/">
<span class="brand-mark" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none"><path d="M12 2.75C6.89 2.75 2.75 6.89 2.75 12C2.75 14.54 3.78 16.84 5.45 18.5" stroke="#FCD535" stroke-width="2"/><path d="M21.25 12C21.25 17.11 17.11 21.25 12 21.25" stroke="#FCD535" stroke-width="2"/><circle cx="12" cy="12" r="5.2" stroke="#FCD535" stroke-width="1.6"/><circle cx="12" cy="2.2" fill="#FCD535"/></svg></span>
<span class="brand-txt"><span class="brand-name">CodexReset<span style="color:var(--primary)">.live</span></span><span class="brand-sub">Independent Quota Radar</span></span>
</a>
<nav class="hdr-nav" aria-label="Main Navigation">
<a class="nav-item" href="/">Radar</a>
<a class="nav-item" href="/reset-today/">Reset Today</a>
<a class="nav-item" href="/history/">History</a>
<a class="nav-item" href="/methodology/">Methodology</a>
</nav>
<div class="hdr-r">
<div class="theme-toggle" role="button" aria-label="Toggle theme" id="themeToggle" tabindex="0">
<span class="theme-sun"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:13px;height:13px"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg></span>
<span class="theme-moon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:13px;height:13px"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg></span>
</div>
</div>
</div>
</header>

<main class="main" style="padding-top:24px;padding-bottom:56px">
<div class="wrap">
<div class="sub-header" style="margin-bottom:28px">
<div class="sub-badge">Official Compliance & Documentation</div>
<h1 class="sub-h1">{esc(h1)}</h1>
<p class="sub-p">{esc(sub_p)}</p>
</div>

<div class="card-box" style="padding:28px;background:var(--card);border:1px solid var(--hairline);border-radius:var(--r-xl);line-height:1.75;font-size:14px;color:var(--muted-strong)">
{content_html}
</div>

</div>
</main>

<footer>
<div class="wrap foot-in">
<div class="foot-links">
<a href="/about/">About</a>
<a href="/privacy/">Privacy Policy</a>
<a href="/terms/">Terms of Service</a>
<a href="/contact/">Contact</a>
<a href="https://github.com/tangtang-it/codexresetlive" target="_blank" rel="noopener nofollow">GitHub ↗</a>
<a href="/llms.txt">llms.txt</a>
<a href="/llms-full.txt">llms-full.txt</a>
<a href="/sitemap.xml">sitemap.xml</a>
</div>
<p class="foot-c">© 2026 CodexReset.live — Independent tracker for OpenAI Codex quota resets. Not affiliated with OpenAI.</p>
</div>
</footer>
<script>
var savedTheme = localStorage.getItem('codex_theme') || 'dark';
document.documentElement.setAttribute('data-theme', savedTheme);
var tt = document.getElementById('themeToggle');
if(tt){{
  tt.addEventListener('click', function(){{
    var current = document.documentElement.getAttribute('data-theme') || 'dark';
    var next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('codex_theme', next);
  }});
}}
</script>
</body>'''

    out_dir = SITE_DIR / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "index.html"
    full_doc = head + chr(10) + body
    out_file.write_text(full_doc, encoding="utf-8")
    print(f"Generated compliance page: /{slug}/ (Size: {len(full_doc):,} B)")
    return canon_url

# ==============================================================================
# 1. ABOUT PAGE
# ==============================================================================
about_content = '''
<h2 style="font-size:20px;color:var(--on-dark);margin-top:0;margin-bottom:12px">1. Our Mission</h2>
<p><strong>CodexReset.live</strong> is an open-access, independent observability radar built for developers, AI engineers, and teams building on OpenAI Codex and ChatGPT Work. We monitor public rate limit recovery signals, calculate personal 5-hour rolling limit replenishment countdowns, and maintain a permanent archive of verified global quota resets.</p>

<h2 style="font-size:20px;color:var(--on-dark);margin-top:28px;margin-bottom:12px">2. Why We Built CodexReset.live</h2>
<p>Hitting a rate limit wall in the middle of a complex coding session can bring productivity to a sudden halt. While OpenAI operates a 5-hour rolling recovery window for ChatGPT Plus and Pro accounts, platform leadership occasionally executes spontaneous global resets or awards promotional banked resets during major feature launches, model updates, or infrastructure recovery events.</p>
<p>Before CodexReset.live, developers had to scour social media feeds, check obscure incident reports, or constantly restart sessions to discover whether their limits had been lifted. CodexReset.live centralizes these signals into a single, high-fidelity radar updated every 30 seconds.</p>

<h2 style="font-size:20px;color:var(--on-dark);margin-top:28px;margin-bottom:12px">3. How Our Signals Are Sourced</h2>
<p>All event data displayed on CodexReset.live is derived from verified, publicly accessible sources:</p>
<ul style="padding-left:20px;margin-bottom:16px">
  <li><strong>Executive Leadership Statements</strong>: Public announcements and status updates from Thibault Sottiaux (@thsottiaux, Head of Codex at OpenAI) and official OpenAI engineering channels.</li>
  <li><strong>Official Infrastructure Feeds</strong>: Incident reports, degradation notices, and resolution logs published on <a href="https://status.openai.com" target="_blank" rel="noopener nofollow" style="color:var(--primary)">status.openai.com</a>.</li>
  <li><strong>Ecosystem Validation</strong>: Timestamped reports and corroborating telemetry from cross-verified developer communities.</li>
</ul>
<p>For a detailed mathematical explanation of our 48-hour probability formula and signal scoring, inspect our <a href="/methodology/" style="color:var(--primary)">Prediction Methodology Whitepaper</a>.</p>

<h2 style="font-size:20px;color:var(--on-dark);margin-top:28px;margin-bottom:12px">4. Editorial & Legal Independence</h2>
<p><strong>Strict Non-Affiliation Disclosure</strong>: CodexReset.live is an independent open-source developer project maintained by <code>tangtang-it</code> and community contributors. It is not affiliated with, endorsed by, sponsored by, or operated in partnership with OpenAI, Inc. "OpenAI", "Codex", and "ChatGPT" are registered trademarks of OpenAI, Inc.</p>

<h2 style="font-size:20px;color:var(--on-dark);margin-top:28px;margin-bottom:12px">5. Get in Touch</h2>
<p>We welcome community feedback, correction submissions with public evidence, and partnership inquiries. Visit our <a href="/contact/" style="color:var(--primary)">Contact Page</a> or submit an issue directly on our <a href="https://github.com/tangtang-it/codexresetlive" target="_blank" rel="noopener nofollow" style="color:var(--primary)">GitHub repository</a>.</p>
'''

# ==============================================================================
# 2. PRIVACY POLICY PAGE
# ==============================================================================
privacy_content = '''
<p style="font-size:12px;color:var(--muted);margin-bottom:20px">Effective Date: October 23, 2026 | Version 2.0</p>

<h2 style="font-size:20px;color:var(--on-dark);margin-top:0;margin-bottom:12px">1. Introduction & Philosophy</h2>
<p>At <strong>CodexReset.live</strong>, we respect developer privacy. We believe that tracking tools and rate limit countdowns should not require you to surrender your personal information. Our core architecture is built around client-side execution, zero account registrations, and strict adherence to international privacy standards.</p>

<h2 style="font-size:20px;color:var(--on-dark);margin-top:28px;margin-bottom:12px">2. Information We Do NOT Collect</h2>
<ul style="padding-left:20px;margin-bottom:16px">
  <li><strong>No User Code or Prompts</strong>: We never inspect, upload, log, or store your code snippets, prompt history, model outputs, or repository files.</li>
  <li><strong>No API Keys or Credentials</strong>: We never ask for or process your OpenAI API keys, session tokens, or authentication credentials.</li>
  <li><strong>No User Accounts</strong>: We do not require usernames, passwords, or profile registrations.</li>
</ul>

<h2 style="font-size:20px;color:var(--on-dark);margin-top:28px;margin-bottom:12px">3. Information We Collect Automatically</h2>
<p>When you visit CodexReset.live, certain standard technical data is collected automatically to maintain server uptime, guard against malicious attacks, and deliver cached assets at the edge:</p>
<ul style="padding-left:20px;margin-bottom:16px">
  <li><strong>Server & CDN Logs</strong>: Our website is deployed across Cloudflare edge infrastructure. Standard HTTP access logs temporarily record non-personally identifiable technical information, including your masked IP address, browser type, operating system version, referring page URL, and request timestamps. These logs are used solely for DDoS mitigation, edge caching, and service reliability.</li>
  <li><strong>Local Browser Storage (HTML5 localStorage)</strong>: We use local storage strictly on your client device for UI preferences:
    <br><code>codex_theme</code>: Saves your preferred theme ('dark' or 'light').
    <br>This information remains exclusively within your local browser and is never transmitted to our servers.</li>
</ul>

<h2 style="font-size:20px;color:var(--on-dark);margin-top:28px;margin-bottom:12px">4. Advertising & Google AdSense / DoubleClick Cookie Disclosure</h2>
<p>We may display advertisements served by Google AdSense and third-party advertising networks to help cover high-concurrency edge hosting costs and ongoing server maintenance. In connection with these services:</p>
<ul style="padding-left:20px;margin-bottom:16px">
  <li>Third-party vendors, including Google, use cookies (such as the DoubleClick cookie) to serve ads based on a user's prior visits to this website or other websites on the Internet.</li>
  <li>Google's use of advertising cookies enables it and its partners to serve ads to our users based on their visit to our site and/or other sites on the Internet.</li>
  <li>Users may opt out of personalized advertising by visiting <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener nofollow" style="color:var(--primary)">Google Ads Settings</a>.</li>
  <li>Alternatively, users can opt out of a third-party vendor's use of cookies for personalized advertising by visiting <a href="https://www.aboutads.info/choices/" target="_blank" rel="noopener nofollow" style="color:var(--primary)">www.aboutads.info</a> or <a href="https://www.networkadvertising.org/choices/" target="_blank" rel="noopener nofollow" style="color:var(--primary)">networkadvertising.org</a>.</li>
</ul>

<h2 style="font-size:20px;color:var(--on-dark);margin-top:28px;margin-bottom:12px">5. Third-Party Services & Links</h2>
<p>Our website contains links to external developer tools, official documentation, and partner services (such as Cursor, Windsurf, status.openai.com, and x.com). These external sites have separate and independent privacy policies. We encourage you to review their policies upon visiting.</p>

<h2 style="font-size:20px;color:var(--on-dark);margin-top:28px;margin-bottom:12px">6. Data Rights (GDPR & CCPA/CPRA)</h2>
<p>Depending on your jurisdiction (such as the European Economic Area, United Kingdom, or California), you may hold statutory rights regarding data transparency and access. Because CodexReset.live does not maintain user databases, personal profiles, or individual browsing dossiers, we do not sell or share personal information.</p>
<p>If you have any questions or data requests, you can contact our privacy point of contact at <a href="mailto:privacy@codexresetlive.com" style="color:var(--primary)">privacy@codexresetlive.com</a>.</p>

<h2 style="font-size:20px;color:var(--on-dark);margin-top:28px;margin-bottom:12px">7. Changes to This Policy</h2>
<p>We may update this Privacy Policy periodically to reflect infrastructure modifications or evolving regulatory standards. Any revisions will be published immediately on this page with an updated effective date.</p>
'''

# ==============================================================================
# 3. TERMS OF SERVICE PAGE
# ==============================================================================
terms_content = '''
<p style="font-size:12px;color:var(--muted);margin-bottom:20px">Effective Date: October 23, 2026 | Version 2.0</p>

<h2 style="font-size:20px;color:var(--on-dark);margin-top:0;margin-bottom:12px">1. Acceptance of Terms</h2>
<p>By accessing and utilizing <strong>CodexReset.live</strong>, you acknowledge and agree to comply with these Terms of Service. If you disagree with any portion of these terms, please discontinue use of the site immediately.</p>

<h2 style="font-size:20px;color:var(--on-dark);margin-top:28px;margin-bottom:12px">2. Observability & Estimative Purpose Only</h2>
<p>All probability scores, 48-hour refill chances, rolling recovery countdown clocks, and signal switches provided on CodexReset.live are statistical models and observational telemetry based on publicly verifiable historical events. They are provided strictly for developer convenience and planning.</p>
<p><strong>No Service Guarantee</strong>: CodexReset.live does NOT guarantee that OpenAI will execute a quota reset at any specified date, time, or frequency. Rate limit policies and operational flushes remain entirely at the sole discretion of OpenAI leadership.</p>

<h2 style="font-size:20px;color:var(--on-dark);margin-top:28px;margin-bottom:12px">3. Trademarks & Nominative Fair Use</h2>
<p>"OpenAI", "Codex", and "ChatGPT" are trademarks of OpenAI, Inc. References to these names and products on CodexReset.live are made solely under nominative fair use principles to identify compatible technologies and report on third-party service status. CodexReset.live is an independent website and is NOT affiliated with, authorized, maintained, sponsored, or endorsed by OpenAI.</p>

<h2 style="font-size:20px;color:var(--on-dark);margin-top:28px;margin-bottom:12px">4. Acceptable Use Policy</h2>
<p>You agree to use our website and public API endpoints responsibly:</p>
<ul style="padding-left:20px;margin-bottom:16px">
  <li>You may not subject our edge infrastructure to denial-of-service attempts or abusive rapid-fire polling.</li>
  <li>If you consume our edge JSON feeds (e.g. <code>/api/radar</code>), please implement a minimum 30-second client-side polling interval and respect HTTP cache-control directives.</li>
  <li>You may freely share screenshots, link to our forecast charts, or quote our statistics with proper attribution to CodexReset.live.</li>
</ul>

<h2 style="font-size:20px;color:var(--on-dark);margin-top:28px;margin-bottom:12px">5. Affiliate & Sponsorship Disclosures</h2>
<p>Certain links on CodexReset.live to alternative developer tools (such as Cursor IDE or Windsurf) may include referral or affiliate parameters. If you choose to subscribe to these services through our links, we may earn an affiliate commission at no additional cost to you. This helps fund server infrastructure and domain maintenance.</p>

<h2 style="font-size:20px;color:var(--on-dark);margin-top:28px;margin-bottom:12px">6. Disclaimer of Warranties & Limitation of Liability</h2>
<p>THE SERVICE IS PROVIDED ON AN "AS IS" AND "AS AVAILABLE" BASIS WITHOUT WARRANTIES OF ANY KIND, WHETHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR TIMELINESS. UNDER NO CIRCUMSTANCES SHALL CODEXRESET.LIVE OR ITS MAINTAINERS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL LOSSES RESULTING FROM SERVICE LIMITS OR RELIANCE ON DISPLAYED PREDICTIONS.</p>

<h2 style="font-size:20px;color:var(--on-dark);margin-top:28px;margin-bottom:12px">7. Contact</h2>
<p>Questions regarding these Terms may be directed via our <a href="/contact/" style="color:var(--primary)">Contact Page</a> or by writing to <a href="mailto:contact@codexresetlive.com" style="color:var(--primary)">contact@codexresetlive.com</a>.</p>
'''

# ==============================================================================
# 4. CONTACT PAGE
# ==============================================================================
contact_content = '''
<h2 style="font-size:20px;color:var(--on-dark);margin-top:0;margin-bottom:12px">1. How to Reach Us</h2>
<p>We value communication from developers, engineering teams, and community researchers. Whether you have noticed an unrecorded quota reset, want to report a bug, or have an editorial suggestion, here are the most effective ways to reach our maintainers:</p>

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;margin:24px 0">
  <div style="background:var(--canvas);border:1px solid var(--hairline);border-radius:var(--r-lg);padding:20px">
    <div style="font-weight:700;color:var(--on-dark);font-size:16px;margin-bottom:6px">GitHub Repository</div>
    <p style="font-size:13px;color:var(--muted);margin-bottom:12px">Preferred for bug reports, radar false positive audits, and public evidence submissions.</p>
    <a href="https://github.com/tangtang-it/codexresetlive" target="_blank" rel="noopener nofollow" class="btn btn-primary" style="height:34px;padding:0 14px;font-size:12px;text-decoration:none;display:inline-flex;align-items:center;gap:6px">
      <span>Open GitHub Issues ↗</span>
    </a>
  </div>
  <div style="background:var(--canvas);border:1px solid var(--hairline);border-radius:var(--r-lg);padding:20px">
    <div style="font-weight:700;color:var(--on-dark);font-size:16px;margin-bottom:6px">Editorial & General Email</div>
    <p style="font-size:13px;color:var(--muted);margin-bottom:12px">For sponsorship inquiries, privacy notices, and non-public technical correspondence.</p>
    <a href="mailto:contact@codexresetlive.com" class="btn btn-primary" style="height:34px;padding:0 14px;font-size:12px;text-decoration:none;display:inline-flex;align-items:center;gap:6px">
      <span>Email Maintainer ↗</span>
    </a>
  </div>
</div>

<h2 style="font-size:20px;color:var(--on-dark);margin-top:28px;margin-bottom:12px">2. Verified Reset Submissions & Corrections</h2>
<p>Our radar relies on strict verification criteria before logging any reset into our permanent dataset. If you have witnessed an unrecorded global refill or a banked reset distribution:</p>
<ul style="padding-left:20px;margin-bottom:16px">
  <li>Provide a direct link to the public post or announcement on X/Twitter (from @thsottiaux, @OpenAI, or official leadership).</li>
  <li>Include the UTC timestamp and whether the refill applied to ChatGPT Plus, Pro, Business, or Enterprise tiers.</li>
  <li>All verified submissions are reviewed and integrated into our open repository within 24 hours.</li>
</ul>

<h2 style="font-size:20px;color:var(--on-dark);margin-top:28px;margin-bottom:12px">3. Response Times</h2>
<p>We typically review public GitHub issues within 12–24 hours, and respond to direct email correspondence within 24–48 business hours.</p>
'''

urls = []
urls.append(build_compliance_page("about", "About CodexReset.live: Independent Radar for OpenAI Codex Quota Resets", "Learn about CodexReset.live, our mission to provide source-verified Codex rate limit observability, and our independent developer team.", "About CodexReset.live", "Transparent developer observability, source-verified reset tracking, and independent research.", about_content, "AboutPage"))
urls.append(build_compliance_page("privacy", "Privacy Policy | CodexReset.live", "Read our complete Privacy Policy, covering our zero-PII architecture, Google AdSense cookies, edge server logs, and user rights.", "Privacy Policy", "Transparent privacy standards, zero PII collection, and advertising cookie disclosures.", privacy_content, "WebPage"))
urls.append(build_compliance_page("terms", "Terms of Service | CodexReset.live", "Terms of Service governing the use of CodexReset.live rate limit radar, prediction estimates, and developer utilities.", "Terms of Service", "Informational radar terms, non-affiliation disclosures, and acceptable use policies.", terms_content, "WebPage"))
urls.append(build_compliance_page("contact", "Contact & Support | CodexReset.live", "Contact the CodexReset.live maintainers for data corrections, verified reset submissions, bug reports, and editorial inquiries.", "Contact & Support", "Direct channels for verified evidence submissions, bug reports, and editorial inquiries.", contact_content, "ContactPage"))

print("All 4 compliance pages built successfully!")