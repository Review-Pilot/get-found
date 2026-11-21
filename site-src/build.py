#!/usr/bin/env python3
"""Get Found static site generator (v1.0).

Reads copy from content.py and blog posts from posts.json, and writes the
finished site into ../public (the folder Cloudflare serves).

    python3 site-src/build.py
"""
import hashlib
import html
import json
import re
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PUB = ROOT / "public"
sys.path.insert(0, str(HERE))
from content import *  # noqa: E402,F401,F403

POSTS = json.loads((HERE / "posts.json").read_text(encoding="utf-8"))
TODAY = date.today().isoformat()
YEAR = date.today().year
esc = html.escape


def ver(rel):
    """Cache-busting hash for css/js."""
    return hashlib.md5((PUB / rel).read_bytes()).hexdigest()[:8]


def money(cur, n):
    return f"{cur}{n}"


# --------------------------------------------------------------------------- helpers
def slugify(t):
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"<[^>]+>", "", t).lower()).strip("-")


def plain(h):
    return html.unescape(re.sub(r"<[^>]+>", "", h)).strip()


def trunc(t, n=155):
    t = re.sub(r"\s+", " ", t).strip()
    if len(t) <= n:
        return t
    return t[: n - 1].rsplit(" ", 1)[0].rstrip(",.;:") + "…"


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


def write(path, content):
    p = PUB / path.strip("/") / "index.html" if not path.endswith(".html") else PUB / path.strip("/")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


ORG = {
    "@type": "Organization",
    "@id": SITE + "/#organization",
    "name": BRAND,
    "url": SITE + "/",
    "logo": SITE + "/assets/img/logo-get-found.webp",
    "email": EMAIL,
    "telephone": PHONE_TEL,
    "sameAs": [u for _, u, _ in SOCIALS],
}
LOCAL_BUSINESS = {
    "@type": "ProfessionalService",
    "@id": SITE + "/#localbusiness",
    "name": "Get Found - Local SEO & AI SEO Specialists",
    "url": SITE + "/",
    "image": SITE + "/assets/img/og-image.png",
    "logo": SITE + "/assets/img/logo-get-found.webp",
    "telephone": PHONE_TEL,
    "email": EMAIL,
    "address": {
        "@type": "PostalAddress",
        "streetAddress": ADDRESS["street"],
        "addressLocality": "Claremont, Cape Town",
        "addressRegion": "Western Cape",
        "postalCode": ADDRESS["postcode"],
        "addressCountry": "ZA",
    },
    "geo": {"@type": "GeoCoordinates", "latitude": -33.9823102, "longitude": 18.4646374},
    "hasMap": MAPS,
    "areaServed": ["South Africa", "United Kingdom", "United States"],
    "sameAs": [u for _, u, _ in SOCIALS],
    "foundingDate": "2018",
}


def breadcrumbs(items):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)
        ],
    }


# --------------------------------------------------------------------------- layout
NAV = [
    ("Home", "/", None),
    ("Services & Pricing", "/services/", None),
    ("Markets", "/markets/", [("South Africa", "/markets/south-africa/"), ("United Kingdom", "/markets/uk/"), ("USA", "/markets/usa/")]),
    ("Resources", "/resources/", [("Resources", "/resources/"), ("Blog", "/blog/")]),
    ("Contact", "/contact/", None),
]


def header(path):
    def current(u):
        if u == "/":
            return path == "/"
        return path.startswith(u)

    items = []
    for label, url, sub in NAV:
        if sub:
            sec = any(current(u) for _, u in sub) or current(url)
            subs = "".join(
                f'<li><a href="{u}"{" aria-current=\"page\"" if path == u else ""}>{esc(n)}</a></li>' for n, u in sub
            )
            items.append(
                f'<li class="has-sub"><button class="nav-link" type="button" aria-expanded="false" aria-haspopup="true"'
                f'{" aria-current=\"true\"" if sec else ""}>{esc(label)}</button><ul class="sub">{subs}</ul></li>'
            )
        else:
            items.append(f'<li><a href="{url}"{" aria-current=\"page\"" if current(url) and (url != "/" or path == "/") else ""}>{esc(label)}</a></li>')
    return f"""<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="/" aria-label="Get Found - home"><img src="/assets/img/logo-get-found.webp" width="77" height="56" alt="Get Found"></a>
    <button class="menu-toggle" type="button" aria-controls="site-nav" aria-expanded="false">Menu</button>
    <nav class="nav" id="site-nav" aria-label="Main">
      <ul>{''.join(items)}</ul>
      <div class="header-cta"><a class="btn sm" href="/contact/#audit">{CTA}</a></div>
    </nav>
  </div>
</header>"""


def footer():
    soc = "".join(
        f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n}"><img src="/assets/img/social-{k}.png" width="24" height="24" alt="" loading="lazy"></a>'
        for n, u, k in SOCIALS
    )
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="brand" href="/"><img src="/assets/img/logo-get-found.webp" width="88" height="64" alt="Get Found" loading="lazy"></a>
        <p>Local SEO &amp; AI SEO specialists. We help businesses get found on Google, Google Maps and AI search, so the right customers choose them.</p>
        <p><strong style="color:#fff">Get Found. Get Chosen. Grow.</strong></p>
        <div class="socials">{soc}</div>
      </div>
      <div>
        <h2>Quick links</h2>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/services/">Services &amp; Pricing</a></li>
          <li><a href="/resources/">Resources</a></li>
          <li><a href="/blog/">Blog</a></li>
          <li><a href="/faq/">FAQs</a></li>
          <li><a href="/partners/">Agency &amp; developer partners</a></li>
          <li><a href="/contact/">Contact</a></li>
        </ul>
      </div>
      <div>
        <h2>Markets</h2>
        <ul>
          <li><a href="/markets/south-africa/">South Africa</a></li>
          <li><a href="/markets/uk/">United Kingdom</a></li>
          <li><a href="/markets/usa/">USA</a></li>
        </ul>
      </div>
      <div>
        <h2>Contact</h2>
        <ul>
          <li><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
          <li><a href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp us</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="{MAPS}" target="_blank" rel="noopener">{ADDRESS['street']}<br>{ADDRESS['suburb']}, {ADDRESS['city']}<br>{ADDRESS['country']} {ADDRESS['postcode']}</a></li>
        </ul>
      </div>
    </div>
    <div class="legal"><span>© {YEAR} Get Found. All rights reserved.</span><span>Local SEO &amp; AI SEO Specialists · Cape Town, South Africa</span></div>
  </div>
</footer>
<div class="mobile-cta"><a class="btn" href="/contact/#audit">Free Visibility Audit</a><a class="btn ghost" style="color:#fff;border-color:rgba(255,255,255,.5)" href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp</a></div>"""


def page(path, title, desc, body, schema=None, og="/assets/img/og-image.png", og_type="website", noindex=False, extra_head=""):
    canon = SITE + path if path != "/404.html" else SITE + "/"
    full_title = title if "Get Found" in title else f"{title} | Get Found"
    graph = [ORG]
    if schema:
        graph += schema
    head = f"""<!doctype html>
<html lang="en-ZA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
{'<meta name="robots" content="noindex,follow">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'}
<meta name="theme-color" content="#050507">
<meta property="og:site_name" content="Get Found">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}{og}">
<meta property="og:locale" content="en_ZA">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/poppins-500.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/style.css?v={ver('assets/css/style.css')}">
{extra_head}
{jsonld({"@context": "https://schema.org", "@graph": graph})}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
{header(path)}
<main id="main">
"""
    tail = f"""
</main>
{footer()}
<script src="/assets/js/main.js?v={ver('assets/js/main.js')}" defer></script>
</body>
</html>
"""
    return head + body + tail


def hero(h1, lead, crumbs=None, eyebrow=None, buttons=True, compact=True, extra=""):
    cr = ""
    if crumbs:
        parts = ['<a href="/">Home</a>'] + [
            f'<a href="{u}">{esc(n)}</a>' if u else f"<span>{esc(n)}</span>" for n, u in crumbs
        ]
        cr = f'<nav class="crumbs" aria-label="Breadcrumb">{" <span aria-hidden=\"true\">/</span> ".join(parts)}</nav>'
    btns = (
        f'<div class="btn-row"><a class="btn" href="/contact/#audit">{CTA}</a><a class="btn ghost" href="/services/">See services &amp; pricing</a></div>'
        if buttons
        else ""
    )
    return f"""<section class="hero{' compact' if compact else ''}">
  <div class="container">
    {cr}
    {f'<span class="eyebrow">{esc(eyebrow)}</span>' if eyebrow else ''}
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
    {btns}{extra}
  </div>
</section>"""


def cta_band(h2="How Visible Is Your Business Today?", text="Find out where you really show up on Google, Google Maps and AI search. Your free visibility audit is quick, honest and obligation-free."):
    return f"""<section class="section dark glow center" id="cta">
  <div class="container narrow">
    <h2>{esc(h2)}</h2>
    <p class="lead">{esc(text)}</p>
    <div class="btn-row center"><a class="btn" href="/contact/#audit">{CTA}</a><a class="btn ghost" href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp us</a></div>
  </div>
</section>"""


def faq_block(items, with_ld=True):
    out = ['<div class="faq">']
    for _, q, a in items:
        out.append(f'<details><summary><h3 style="display:inline;font-size:1rem;margin:0">{esc(q)}</h3></summary><div class="ans"><p>{esc(a)}</p></div></details>')
    out.append("</div>")
    return "".join(out)


def faq_ld(items):
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for _, q, a in items
        ],
    }


def ticks(items):
    return '<ul class="ticks">' + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>"


def read_time(post):
    words = sum(len(plain(b["v"]).split()) for b in post["blocks"] if b["t"] != "img")
    return max(1, round(words / 200))


def fmt_date(iso):
    y, m, d = iso.split("-")
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    return f"{int(d)} {months[int(m) - 1]} {y}"


def hero_image(post):
    for b in post["blocks"]:
        if b["t"] == "img":
            return b
    return None


def post_card(p):
    img = hero_image(p)
    thumb = (
        f'<div class="thumb"><img src="{img["v"]}" alt="" loading="lazy" width="{img["w"]}" height="{img["h"]}"></div>'
        if img and img["w"] >= 800
        else f'<div class="thumb art"><span>{esc(p["category"])}</span></div>'
    )
    return f"""<article class="post-card" data-cat="{esc(p['category'])}">
  {thumb}
  <div class="body">
    <div class="meta"><span class="tag">{esc(p['category'])}</span><span>{fmt_date(p['published'])}</span><span>{read_time(p)} min read</span></div>
    <h3 style="margin-top:.8rem"><a href="/blog/{p['slug']}/">{esc(p['title'])}</a></h3>
    <p>{esc(trunc(p['first_p'], 140))}</p>
  </div>
</article>"""


POSTS_SORTED = sorted(POSTS, key=lambda p: p["published"], reverse=True)

# --------------------------------------------------------------------------- pages
def home():
    packs = f"""
<div class="grid two">
  <article class="card">
    <h3>Local SEO</h3>
    <p>For businesses that win customers in their area. Be the business people find on Google Search and Google Maps, and the one they choose.</p>
    {ticks(["Google Business Profile optimisation and management", "Weekly posts, video posts and photo uploads", "Review management and review-generation automation", "Geo-grid and website rank tracking, with monthly reporting"])}
    <div class="price">From R6,000<small> / month</small></div>
    <div class="setup">South Africa · once-off setup R3,000</div>
    <a class="btn" href="/services/#local-seo">See what&rsquo;s included</a>
  </article>
  <article class="card featured">
    <span class="badge">LOCAL SEO + MORE</span>
    <h3>SEO + AI SEO</h3>
    <p>Everything in Local SEO, plus a full SEO strategy and AI search optimisation, so you&rsquo;re found when customers ask ChatGPT and other AI tools too.</p>
    {ticks(["Custom SEO strategy and up to 300 tracked keywords", "Up to three page improvements a month and ongoing technical SEO", "One SEO-optimised blog article a month", "AI search and answer-focused content optimisation"])}
    <div class="price">From R12,000<small> / month</small></div>
    <div class="setup">South Africa · once-off setup R5,000</div>
    <a class="btn" href="/services/#seo-ai-seo">See what&rsquo;s included</a>
  </article>
</div>
<p class="center" style="margin-top:1.6rem">Based in the UK or USA? <a href="/services/#international">See UK and US pricing</a>. Same service, regional pricing.</p>"""

    steps = """
<div class="grid three steps">
  <div class="step"><h3>Free Visibility Audit</h3><p>We look at where your business shows up today on Google Search, Google Maps and AI search, and where your competitors are beating you to it.</p></div>
  <div class="step"><h3>Fix, build, optimise</h3><p>We get our hands dirty: your Google Business Profile, listings, website, content and reviews, starting with the 20% of work that drives the next 80% of growth.</p></div>
  <div class="step"><h3>Track and grow</h3><p>Clear monthly reporting, ongoing optimisation and a team that picks up the phone. You&rsquo;ll always know what we did and what it&rsquo;s done for you.</p></div>
</div>"""

    reviews = "".join(
        f'<figure class="review"><div class="stars" aria-label="5 stars">★★★★★</div><blockquote>“{esc(q)}”</blockquote><figcaption>{esc(n)}<span>{esc(r)}</span></figcaption></figure>'
        for q, n, r in REVIEWS
    )
    trusted = "".join(f"<li>{esc(t)}</li>" for t in TRUSTED)
    faqs = faq_block([FAQS[i] for i in HOME_FAQ_IDX])
    latest = "".join(post_card(p) for p in POSTS_SORTED[:3])

    body = f"""
<section class="hero" id="top">
  <div class="container">
    <span class="eyebrow">Local SEO &amp; AI SEO Specialists</span>
    <h1>Get Found on Google. Google Maps. And AI&nbsp;Search.</h1>
    <p class="lead">Your customers are searching right now, on Google, on the map and in tools like ChatGPT. We make sure it&rsquo;s your business they find, trust and choose.</p>
    <div class="btn-row center"><a class="btn" href="/contact/#audit">{CTA}</a><a class="btn ghost" href="/services/">See services &amp; pricing</a></div>
    <p class="tagline">Get Found. Get Chosen. <span>Grow.</span></p>
  </div>
</section>

<section class="section" id="how-we-help">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Two simple ways to work with us</span>
      <h2>How We Help You Get Found</h2>
      <p class="lead">Strong Local SEO is the foundation. When you&rsquo;re ready to go further, we add full SEO and AI search visibility on top. No confusing menus, just two clear options.</p>
    </div>
    {packs}
  </div>
</section>

<section class="section alt" id="about">
  <div class="container split">
    <div class="frame"><img src="/assets/img/isabella-get-found.webp" width="682" height="627" alt="A member of the Get Found team working on a laptop in a bright office" loading="lazy"></div>
    <div>
      <span class="eyebrow">Specialists, not generalists</span>
      <h2>About Get Found</h2>
      <p>Get Found is a Cape Town based team of Local SEO and AI SEO specialists. Since 2018 we&rsquo;ve helped businesses in South Africa, Europe and Asia get found by customers who are ready to buy.</p>
      <p>We work with SMEs that want straightforward, measurable growth, and with web developers and agencies who need an SEO partner they can rely on. Because our work is done from South Africa, UK and US clients get the same service at a cost-effective price.</p>
      <p>No jargon. No smoke and mirrors. Just practical work that gets you more visibility, more trust and more enquiries.</p>
      <div class="btn-row"><a class="btn" href="/contact/">Talk to us</a><a class="btn ghost" href="/markets/south-africa/">Our markets</a></div>
    </div>
  </div>
</section>

<section class="section" id="founder">
  <div class="container split reverse">
    <div>
      <span class="eyebrow">Founder-led</span>
      <h2>Hands-on, from the first call</h2>
      <p>Get Found was founded by <strong>Rian Slabbert</strong>, a marketer and entrepreneur with over 30 years of business experience, who is passionate about helping business owners grow their sales through digital marketing.</p>
      <p>We treat every client&rsquo;s business as if it were our own. That means finding the 20% of work that unlocks the next 80% of growth, getting our hands dirty on your Google Business Profile and website, and being the kind of provider who actually returns your calls.</p>
      <div class="btn-row"><a class="btn" href="/contact/#audit">{CTA}</a></div>
    </div>
    <div class="frame right"><img src="/assets/img/rian-slabbert-founder.webp" width="900" height="597" alt="Rian Slabbert, founder of Get Found" loading="lazy"></div>
  </div>
</section>

<section class="section alt" id="process">
  <div class="container">
    <div class="section-head"><h2>How it works</h2><p class="lead">From audit to growth in three clear steps.</p></div>
    {steps}
  </div>
</section>

<section class="section" id="trusted">
  <div class="container center">
    <h2>Trusted by businesses including</h2>
    <ul class="trust">{trusted}</ul>
  </div>
</section>

<section class="section alt" id="reviews">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Reviews</span><h2>What our clients say</h2></div>
    <div class="carousel" data-carousel>
      <div class="track" tabindex="0" aria-label="Client reviews">{reviews}</div>
      <div class="car-btns"><button type="button" data-dir="-1" aria-label="Previous reviews">←</button><button type="button" data-dir="1" aria-label="Next reviews">→</button></div>
    </div>
  </div>
</section>

<section class="section" id="faqs">
  <div class="container narrow">
    <div class="section-head"><span class="eyebrow">FAQs</span><h2>Questions we&rsquo;re asked most</h2></div>
    {faqs}
    <p class="center" style="margin-top:1.6rem"><a class="btn ghost" href="/faq/">See all 30 FAQs</a></p>
  </div>
</section>

<section class="section alt" id="latest">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Resources</span><h2>Latest from the blog</h2><p class="lead">Practical SEO, local search and AI search guides for business owners.</p></div>
    <div class="grid three">{latest}</div>
    <p class="center" style="margin-top:1.8rem"><a class="btn ghost" href="/blog/">Browse all articles</a></p>
  </div>
</section>

{cta_band()}
"""
    schema = [
        LOCAL_BUSINESS,
        {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": BRAND, "publisher": {"@id": SITE + "/#organization"}},
        faq_ld([FAQS[i] for i in HOME_FAQ_IDX]),
    ]
    write("/", page("/", "Local SEO & AI SEO Specialists | Get Found on Google and AI Search",
                    "Get Found helps South African, UK and US businesses get found on Google Search, Google Maps and AI search like ChatGPT. Local SEO from R6,000/month. Get your free visibility audit.",
                    body, schema))


def services():
    intl = f"""<div class="table-wrap"><table>
<thead><tr><th>Market</th><th>Local SEO</th><th>SEO + AI SEO</th></tr></thead>
<tbody>
<tr><th scope="row">South Africa</th><td>R6,000 / month<br><small>Setup R3,000 once-off</small></td><td>R12,000 / month<br><small>Setup R5,000 once-off</small></td></tr>
<tr><th scope="row">United Kingdom</th><td>£350 / month</td><td>£650 / month</td></tr>
<tr><th scope="row">United States</th><td>$450 / month</td><td>$750 / month</td></tr>
</tbody></table></div>
<p style="margin-top:1rem" class="form-note">We use regional pricing rather than direct currency conversion. South African pricing is built around the local SME market; UK and US pricing is built for those markets and stays highly competitive. It&rsquo;s the same product, and the work is done from South Africa, which is what keeps it cost-effective.</p>"""
    faq_items = [f for f in FAQS if f[0] in ("Services", "Pricing")]
    body = hero("Local SEO &amp; AI SEO Services and Pricing",
                "Two clear packages. Start with Local SEO to dominate Google Maps, or go all-in with SEO + AI SEO to be found everywhere your customers search.",
                crumbs=[("Services & Pricing", None)], eyebrow="Services & Pricing") + f"""
<section class="section">
  <div class="container">
    <div class="grid two" id="packages">
      <article class="card" id="local-seo">
        <h2 style="font-size:1.7rem">Local SEO</h2>
        <p>Get found on Google Search and Google Maps by customers in your area, and give them reasons to choose you.</p>
        <div class="price">R6,000<small> / month</small></div>
        <div class="setup">South Africa · once-off setup R3,000</div>
        {ticks(LOCAL_SEO_FEATURES)}
        <a class="btn" href="/contact/#audit">{CTA}</a>
      </article>
      <article class="card featured" id="seo-ai-seo">
        <span class="badge">EVERYTHING IN LOCAL SEO, AND MORE</span>
        <h2 style="font-size:1.7rem">SEO + AI SEO</h2>
        <p>Add a full SEO strategy and AI search optimisation, so you&rsquo;re visible in Google results, on the map and in tools like ChatGPT.</p>
        <div class="price">R12,000<small> / month</small></div>
        <div class="setup">South Africa · once-off setup R5,000</div>
        {ticks(AI_SEO_FEATURES)}
        <a class="btn" href="/contact/#audit">{CTA}</a>
      </article>
    </div>
  </div>
</section>

<section class="section alt" id="which">
  <div class="container narrow">
    <h2 class="center">Which package is right for you?</h2>
    <div class="grid two" style="margin-top:2rem">
      <div class="step"><h3>Choose Local SEO if&hellip;</h3><p>You serve customers in a particular area, you want more calls, walk-ins and enquiries from Google Maps, and you want to build a strong base of reviews and local trust.</p></div>
      <div class="step"><h3>Choose SEO + AI SEO if&hellip;</h3><p>You want to grow beyond your local area, compete for more search terms, get a steady stream of content and website improvements, and be visible in AI search too.</p></div>
    </div>
    <p class="center" style="margin-top:1.6rem">Not sure? Start with a free audit and we&rsquo;ll recommend what makes sense for your business, even if that&rsquo;s the smaller package.</p>
  </div>
</section>

<section class="section" id="international">
  <div class="container narrow">
    <div class="section-head"><span class="eyebrow">South Africa · UK · USA</span><h2>Pricing by market</h2></div>
    {intl}
    <p class="center" style="margin-top:1.4rem"><a href="/markets/south-africa/">South Africa</a> · <a href="/markets/uk/">United Kingdom</a> · <a href="/markets/usa/">USA</a></p>
  </div>
</section>

<section class="section alt" id="partners">
  <div class="container split">
    <div>
      <span class="eyebrow">For agencies &amp; developers</span>
      <h2>Outsource your SEO to Get Found</h2>
      <p>Web developers, freelancers and agencies can hand their SEO to us. White-label and outsourced SEO fulfilment, delivered by specialists, so you can offer clients a complete service without building an SEO team.</p>
      <div class="btn-row"><a class="btn" href="/partners/">Partner with us</a></div>
    </div>
    <div class="card"><h3>What partners get</h3>{ticks(["Local SEO and SEO + AI SEO fulfilment", "Reporting you can share with your clients", "A specialist team that works behind your brand", "Cost-effective rates, with the work done from South Africa"])}</div>
  </div>
</section>

<section class="section" id="faqs">
  <div class="container narrow">
    <div class="section-head"><h2>Service and pricing FAQs</h2></div>
    {faq_block(faq_items)}
    <p class="center" style="margin-top:1.6rem"><a href="/faq/">See all FAQs</a></p>
  </div>
</section>
{cta_band()}
"""
    schema = [breadcrumbs([("Home", "/"), ("Services & Pricing", "/services/")]), faq_ld(faq_items)]
    write("/services/", page("/services/", "Local SEO & AI SEO Services and Pricing",
                             "Local SEO from R6,000/month and SEO + AI SEO from R12,000/month in South Africa. UK from £350/month, USA from $450/month. See exactly what's included.",
                             body, schema))


def market_page(key):
    cfg = {
        "za": dict(slug="south-africa", name="South Africa", h1="Local SEO &amp; AI SEO Services in South Africa",
                   title="Local SEO & AI SEO Services in South Africa",
                   desc="Local SEO and AI SEO specialists based in Cape Town. SEO services for South African businesses from R6,000/month, covering Google Maps, Google Search and AI search.",
                   lead="South African businesses deserve SEO that&rsquo;s practical, local and affordable. We&rsquo;re based in Cape Town, and we know this market.",
                   focus="South African SMEs"),
        "uk": dict(slug="uk", name="United Kingdom", h1="Local SEO &amp; AI SEO Services for UK Businesses",
                   title="Local SEO & AI SEO Services for UK Businesses",
                   desc="Specialist local SEO and AI SEO for UK businesses from £350/month. The same product delivered cost-effectively from South Africa, covering Google Maps, Google Search and AI search.",
                   lead="Specialist Local SEO and AI SEO for UK businesses, delivered from South Africa at a cost-effective price.",
                   focus="UK businesses"),
        "us": dict(slug="usa", name="United States", h1="Local SEO &amp; AI SEO Services for US Businesses",
                   title="Local SEO & AI SEO Services for US Businesses",
                   desc="Specialist local SEO and AI SEO for US businesses from $450/month. The same product delivered cost-effectively from South Africa, covering Google Maps, Google Search and AI search.",
                   lead="Specialist Local SEO and AI SEO for businesses in the USA, delivered from South Africa at a cost-effective price.",
                   focus="US businesses"),
    }[key]
    pr = PRICING[key]
    cur = pr["cur"]
    if key == "za":
        sa_extra = f"""<section class="section alt">
  <div class="container split">
    <div class="frame"><img src="/assets/img/cape-town-table-mountain.webp" width="1200" height="800" alt="Table Mountain and Cape Town seen from the beach at Bloubergstrand" loading="lazy"></div>
    <div>
      <span class="eyebrow">Based in Cape Town</span>
      <h2>Local knowledge, local support</h2>
      <p>Our office is in Claremont, Cape Town. We understand South African search behaviour, South African directories and the realities of running an SME here, and when you call or WhatsApp, you get a real person in your time zone.</p>
      <p>We help South African businesses, from car hire and safaris to flooring and retail, get found on Google Search, Google Maps and AI search. Looking for SEO in Cape Town? You&rsquo;re in the right place. We work with businesses nationwide, too.</p>
      <div class="btn-row"><a class="btn" href="/contact/#audit">{CTA}</a></div>
    </div>
  </div>
</section>"""
        price_note = f"""<p class="form-note center" style="margin-top:1.2rem">Once-off setup: Local SEO R3,000 · SEO + AI SEO R5,000</p>"""
        why = [
            ("Built for South African SMEs", "Pricing and packages designed around the local market, not converted from somewhere else."),
            ("Google Maps first", "For most local businesses, the map is where customers decide. We make it a priority."),
            ("Ready for AI search", "Customers are starting to ask ChatGPT who to call. We help you show up there too."),
        ]
    else:
        sa_extra = ""
        price_note = ""
        tz = "UK" if key == "uk" else "US"
        why = [
            ("The same specialist service", f"You get exactly the same Local SEO and AI SEO product as our South African clients, set up for {pr['name']} search behaviour."),
            ("Cost-effective by design", f"The work is done from South Africa, so {pr['name']} businesses get specialist SEO at a price that&rsquo;s hard to match locally."),
            ("Clear communication", "Straightforward reporting and a team that returns your emails and calls, wherever you are."),
        ]
    why_html = "".join(f'<div class="step"><h3>{t}</h3><p>{d}</p></div>' for t, d in why)
    intl_text = ""
    if key != "za":
        intl_text = f"""<section class="section alt">
  <div class="container narrow center">
    <h2>Why {pr['name']} businesses work with Get Found</h2>
    <p class="lead">We&rsquo;re doing this work for {cfg['focus']} from South Africa, and the customer gets the same product at a cost-effective price because of it.</p>
    <p>Local SEO and AI SEO aren&rsquo;t about where your SEO team sits. They&rsquo;re about the quality of the work: your Google Business Profile, your listings, your reviews, your content and your visibility in AI search. That&rsquo;s exactly what we deliver.</p>
  </div>
</section>"""
    body = hero(cfg["h1"], cfg["lead"], crumbs=[("Markets", "/markets/"), (cfg["name"], None)], eyebrow=f"Markets · {cfg['name']}") + f"""
<section class="section">
  <div class="container">
    <div class="section-head"><h2>{cfg['name']} pricing</h2><p class="lead">Two clear packages. Pricing set for the {cfg['name']} market.</p></div>
    <div class="grid two">
      <article class="card"><h3>Local SEO</h3><p>Win on Google Search and Google Maps.</p><div class="price">{cur}{pr['local']}<small> / month</small></div>{'<div class="setup">Once-off setup R3,000</div>' if key=='za' else '<div class="setup">Everything you need to dominate local search</div>'}{ticks(LOCAL_SEO_FEATURES[:6] + ["…and more"])}<a class="btn" href="/services/#local-seo">Everything included</a></article>
      <article class="card featured"><span class="badge">LOCAL SEO + AI SEARCH</span><h3>SEO + AI SEO</h3><p>Add full SEO and AI search visibility.</p><div class="price">{cur}{pr['ai']}<small> / month</small></div>{'<div class="setup">Once-off setup R5,000</div>' if key=='za' else '<div class="setup">Full SEO strategy plus AI search optimisation</div>'}{ticks(["Everything in Local SEO", "Custom SEO strategy, up to 300 tracked keywords", "Ongoing technical SEO and page improvements", "AI search optimisation and AI traffic reporting", "…and more"])}<a class="btn" href="/services/#seo-ai-seo">Everything included</a></article>
    </div>
    {price_note}
  </div>
</section>
{sa_extra}{intl_text}
<section class="section{' alt' if key=='za' else ''}">
  <div class="container">
    <div class="section-head"><h2>{'Why South African businesses choose Get Found' if key=='za' else 'What you get'}</h2></div>
    <div class="grid three">{why_html}</div>
  </div>
</section>

<section class="section{'' if key=='za' else ' alt'}">
  <div class="container split">
    <div><span class="eyebrow">Web developers &amp; agencies</span><h2>Outsourcing SEO from {cfg['name']}?</h2><p>If you build websites or run an agency, you can hand your clients&rsquo; SEO to us. White-label and outsourced SEO fulfilment, delivered by specialists.</p><div class="btn-row"><a class="btn ghost" href="/partners/">See how partnering works</a></div></div>
    <div><h3>Next step</h3><p>Not sure where you stand? Our free visibility audit shows how your business appears on Google, Google Maps and AI search today.</p><div class="btn-row"><a class="btn" href="/contact/#audit">{CTA}</a></div></div>
  </div>
</section>
{cta_band()}
"""
    path = f"/markets/{cfg['slug']}/"
    schema = [breadcrumbs([("Home", "/"), ("Markets", "/markets/"), (cfg["name"], path)])]
    write(path, page(path, cfg["title"], cfg["desc"], body, schema))


def markets_hub():
    cards = ""
    for k, slug, flag, tag in (("za", "south-africa", "South Africa", "Based in Cape Town"), ("uk", "uk", "United Kingdom", "Same product, cost-effective"), ("us", "usa", "United States", "Same product, cost-effective")):
        pr = PRICING[k]
        cards += f"""<article class="card"><span class="tag" style="align-self:flex-start">{tag}</span><h2 style="font-size:1.5rem;margin-top:.8rem">{flag}</h2>
<p>Local SEO from <strong>{pr['cur']}{pr['local']}/month</strong><br>SEO + AI SEO from <strong>{pr['cur']}{pr['ai']}/month</strong></p>
<a class="btn" href="/markets/{slug}/">{flag} SEO services</a></article>"""
    body = hero("Local SEO &amp; AI SEO Services by Market",
                "We help businesses in South Africa, the United Kingdom and the USA get found on Google, Google Maps and AI search, with pricing set for each market.",
                crumbs=[("Markets", None)], eyebrow="Markets") + f"""
<section class="section"><div class="container"><div class="grid three">{cards}</div>
<p class="center" style="margin-top:2rem">Web developer or agency? See our <a href="/partners/">white-label SEO partner programme</a>.</p></div></section>
{cta_band()}"""
    write("/markets/", page("/markets/", "Local SEO & AI SEO Services by Market: South Africa, UK & USA",
                            "Get Found delivers Local SEO and AI SEO to businesses in South Africa, the UK and the USA, with regional pricing and the same specialist service.",
                            body, [breadcrumbs([("Home", "/"), ("Markets", "/markets/")])]))


def partners():
    body = hero("White-Label &amp; Outsourced SEO Services for Agencies and Web Developers",
                "Give your clients specialist Local SEO and AI SEO, without building an SEO team. We work quietly behind your brand.",
                crumbs=[("Partners", None)], eyebrow="Agency & developer partners", buttons=False,
                extra=f'<div class="btn-row"><a class="btn" href="/contact/?topic=partner#audit">Talk to us about partnering</a></div>') + f"""
<section class="section">
  <div class="container">
    <div class="section-head"><h2>SEO fulfilment you can rely on</h2><p class="lead">You own the client relationship. We do the specialist SEO work behind the scenes.</p></div>
    <div class="grid three">
      <div class="step"><h3>White-label SEO</h3><p>Local SEO and SEO + AI SEO delivered under your brand, with reporting you can pass straight to your clients.</p></div>
      <div class="step"><h3>Outsourced SEO fulfilment</h3><p>Hand us the audits, Google Business Profile work, listings, content and ongoing optimisation. We&rsquo;ll get it done.</p></div>
      <div class="step"><h3>Cost-effective rates</h3><p>The work is done from South Africa, so you get specialist SEO at rates that protect your margins in the UK, USA and beyond.</p></div>
    </div>
  </div>
</section>
<section class="section alt">
  <div class="container split">
    <div>
      <span class="eyebrow">Who it&rsquo;s for</span>
      <h2>Built for people who build for others</h2>
      <ul class="ticks"><li>Web developers who want to offer SEO to the sites they build</li><li>Freelancers who need a specialist to deliver SEO for their clients</li><li>Agencies that want to add Local SEO and AI SEO without hiring</li><li>SEO resellers looking for a dependable fulfilment partner</li></ul>
    </div>
    <div class="card">
      <h3>The Get Found difference</h3>
      <p>Specialists in <strong>Local SEO</strong> and <strong>AI SEO</strong>, the two areas your clients are asking about most. Founder-led, hands-on and quick to respond.</p>
      <a class="btn" href="/contact/?topic=partner#audit">Start the conversation</a>
    </div>
  </div>
</section>
<section class="section"><div class="container narrow"><div class="section-head"><h2>Partner FAQs</h2></div>{faq_block([f for f in FAQS if f[0]=='Partners'])}</div></section>
{cta_band("Ready to add SEO to your services?", "Tell us about your agency or clients and we&rsquo;ll show you how partnering works.")}"""
    sp = [f for f in FAQS if f[0] == "Partners"]
    write("/partners/", page("/partners/", "White-Label & Outsourced SEO Services for Agencies",
                             "White-label and outsourced Local SEO and AI SEO for web developers, freelancers and agencies. Specialist fulfilment, delivered cost-effectively from South Africa.",
                             body, [breadcrumbs([("Home", "/"), ("Partners", "/partners/")]), faq_ld(sp)]))


def resources():
    feat_slugs = ["mastering-seo-ranking-strategies-that-work", "local-seo-tips-to-boost-local-visibility", "local-seo-vs-ai-seo-how-search-is-evolving",
                  "intent-focused-ai-ready-seo-strategy-2026", "lead-generation-systems-for-small-businesses-2026", "local-seo-strategies-cape-town-south-africa"]
    by_slug = {p["slug"]: p for p in POSTS}
    feat = "".join(post_card(by_slug[s]) for s in feat_slugs)
    counts = {}
    for p in POSTS:
        counts[p["category"]] = counts.get(p["category"], 0) + 1
    cats = ""
    for name, desc, cat in RESOURCE_CATEGORIES:
        if cat:
            n = counts.get(cat, 0)
            link = f'<a class="btn sm ghost" href="/blog/">{n} article{"s" if n != 1 else ""}</a>'
        else:
            link = '<span class="tag">Coming soon</span>'
        cats += f'<article class="card" style="padding:26px"><h3>{esc(name)}</h3><p style="color:var(--muted);flex:1">{esc(desc)}</p>{link}</article>'
    body = hero("Practical Tools &amp; Guides for Small Business Growth",
                "Free and low-cost software, AI tools, SEO resources, automation ideas and practical guides for entrepreneurs and small business owners.",
                crumbs=[("Resources", None)], eyebrow="Resources", buttons=False,
                extra='<div class="btn-row"><a class="btn" href="/blog/">Browse the blog</a><a class="btn ghost" href="#categories">Browse by category</a></div>') + f"""
<section class="section" id="featured">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Start here</span><h2>Featured resources</h2><p class="lead">Our most useful evergreen guides on SEO, local search and AI search.</p></div>
    <div class="grid three">{feat}</div>
  </div>
</section>
<section class="section alt" id="categories">
  <div class="container">
    <div class="section-head"><h2>Browse by category</h2><p class="lead">We&rsquo;re building this into a practical knowledge base. New guides and honest software reviews are added regularly.</p></div>
    <div class="grid three">{cats}</div>
  </div>
</section>
<section class="section" id="tools">
  <div class="container split">
    <div>
      <span class="eyebrow">Get Found tools</span>
      <h2>Tools we build and recommend</h2>
      <p>Some of the tools featured here are built by Get Found or related businesses, such as <strong>Review Pilot</strong> for review generation and reputation management. When we feature our own products, we&rsquo;ll always say so clearly.</p>
      <p class="disclosure"><strong>Our promise:</strong> our reviews are educational first. We explain what a tool does, who it&rsquo;s for, what it costs, where it falls short and what the alternatives are. Where we use affiliate links to third-party tools, we&rsquo;ll disclose it.</p>
    </div>
    <div class="card">
      <h3>How we review software</h3>
      <ol style="padding-left:1.2em;margin:0">
        <li>What the tool does</li><li>Who it&rsquo;s best for</li><li>Free plan or trial</li><li>Typical pricing level</li><li>Key strengths</li><li>Limitations and watch-outs</li><li>Setup difficulty</li><li>Best alternatives</li><li>Get Found verdict</li>
      </ol>
    </div>
  </div>
</section>
{cta_band("Want us to do the SEO for you?", "Guides are great. If you&rsquo;d rather have specialists handle it, start with a free visibility audit.")}"""
    write("/resources/", page("/resources/", "Practical Tools & Guides for Small Business Growth",
                              "Free and low-cost software, AI tools, SEO resources and practical guides for entrepreneurs and small business owners, from the Local SEO and AI SEO specialists at Get Found.",
                              body, [breadcrumbs([("Home", "/"), ("Resources", "/resources/")])]))


def blog_index():
    cats = sorted({p["category"] for p in POSTS})
    chips = '<button class="chip" type="button" data-filter="all" aria-pressed="true">All</button>' + "".join(
        f'<button class="chip" type="button" data-filter="{esc(c)}" aria-pressed="false">{esc(c)}</button>' for c in cats
    )
    cards = "".join(post_card(p) for p in POSTS_SORTED)
    body = hero("The Get Found Blog: Local SEO, AI SEO &amp; Small Business Growth",
                "Practical guides to help your business get found on Google, Google Maps and AI search.",
                crumbs=[("Resources", "/resources/"), ("Blog", None)], eyebrow="Blog", buttons=False) + f"""
<section class="section"><div class="container">
  <div class="chips" role="group" aria-label="Filter articles by topic">{chips}</div>
  <div class="grid three">{cards}</div>
</div></section>
{cta_band("Want results like these for your business?", "Our free visibility audit shows you where you stand on Google, Google Maps and AI search.")}"""
    blog_ld = {"@type": "Blog", "name": "Get Found Blog", "url": SITE + "/blog/", "blogPost": [
        {"@type": "BlogPosting", "headline": p["title"], "url": f"{SITE}/blog/{p['slug']}/", "datePublished": p["published"]} for p in POSTS_SORTED]}
    write("/blog/", page("/blog/", "Blog: Local SEO, AI SEO & Small Business Growth",
                         "Practical guides on Local SEO, AI SEO, lead generation and growth for small businesses, from the specialists at Get Found.",
                         body, [breadcrumbs([("Home", "/"), ("Resources", "/resources/"), ("Blog", "/blog/")]), blog_ld]))


def fix_inline(v):
    """Wix stripped spaces around bold text and links; put them back."""
    v = re.sub(r"</strong>(?=[A-Za-z0-9\u201c\"(])", "</strong> ", v)
    v = re.sub(r"([A-Za-z0-9,;:])<a ", r"\1 <a ", v)
    v = re.sub(r"</a>(?=[A-Za-z0-9])", "</a> ", v)
    return v


def render_blocks(post):
    blocks = [dict(b, v=fix_inline(b["v"])) if b["t"] != "img" else b for b in post["blocks"]]
    hero_b = None
    if blocks and blocks[0]["t"] == "img":
        hero_b = blocks.pop(0)
    out, h2s, i = [], [], 0
    while i < len(blocks):
        b = blocks[i]
        t = b["t"]
        if t == "li":
            items = []
            while i < len(blocks) and blocks[i]["t"] == "li":
                items.append(f"<li>{blocks[i]['v']}</li>")
                i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
            continue
        if t == "img":
            out.append(f'<figure><img src="{b["v"]}" width="{b["w"]}" height="{b["h"]}" alt="Illustration for {esc(post["title"])}" loading="lazy"></figure>')
        elif t in ("h2", "h3", "h4"):
            if t == "h2":
                sid = slugify(b["v"])
                h2s.append((sid, plain(b["v"])))
                out.append(f'<h2 id="{sid}">{b["v"]}</h2>')
            else:
                out.append(f'<{t}>{b["v"]}</{t}>')
        elif t == "p":
            out.append(f'<p>{b["v"]}</p>')
        i += 1
    return hero_b, "\n".join(out), h2s


def blog_post(p):
    hero_b, content, h2s = render_blocks(p)
    toc = ""
    if len(h2s) >= 4:
        toc = '<nav class="toc" aria-label="In this article"><strong>In this article</strong><ol>' + "".join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in h2s) + "</ol></nav>"
    hero_img = (f'<img class="article-hero" src="{hero_b["v"]}" width="{hero_b["w"]}" height="{hero_b["h"]}" alt="Illustration for {esc(p["title"])}" fetchpriority="high">' if hero_b and hero_b["w"] >= 800 else "")
    related = [q for q in POSTS_SORTED if q["slug"] != p["slug"]]
    related.sort(key=lambda q: (q["category"] != p["category"],))
    rel = "".join(post_card(q) for q in related[:3])
    seo_title = POST_SEO_TITLES.get(p["slug"], p["title"])
    desc = trunc(p["first_p"], 155)
    body = f"""<section class="hero compact">
  <div class="container narrow">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> <span aria-hidden="true">/</span> <a href="/blog/">Blog</a> <span aria-hidden="true">/</span> <span>{esc(p['category'])}</span></nav>
    <span class="eyebrow">{esc(p['category'])}</span>
    <h1 style="font-size:clamp(1.8rem,4vw,2.7rem)">{esc(p['title'])}</h1>
    <p class="meta" style="color:#c9cde0;gap:14px">By Rian Slabbert, Get Found · <time datetime="{p['published']}">{fmt_date(p['published'])}</time> · {read_time(p)} min read</p>
  </div>
</section>
<article class="article">
  <div class="narrow">
    {hero_img}
    {toc}
    {content}
    <div class="cta-box">
      <h2>Want us to do this for your business?</h2>
      <p>Get Found are Local SEO and AI SEO specialists. Find out how visible your business is today with a free visibility audit.</p>
      <div class="btn-row"><a class="btn" href="/contact/#audit">{CTA}</a><a class="btn ghost" href="/services/">Services &amp; pricing</a></div>
    </div>
  </div>
</article>
<section class="section alt"><div class="container"><div class="section-head"><h2>Keep reading</h2></div><div class="grid three">{rel}</div></div></section>"""
    path = f"/blog/{p['slug']}/"
    ld = {
        "@type": "BlogPosting",
        "headline": p["title"],
        "description": desc,
        "datePublished": p["published"],
        "dateModified": p["modified"],
        "mainEntityOfPage": SITE + path,
        "author": {"@type": "Person", "name": "Rian Slabbert", "worksFor": {"@id": SITE + "/#organization"}},
        "publisher": {"@id": SITE + "/#organization"},
        "articleSection": p["category"],
    }
    if hero_b:
        ld["image"] = SITE + hero_b["v"]
    write(path, page(path, seo_title, desc, body, [ld, breadcrumbs([("Home", "/"), ("Blog", "/blog/"), (p["title"], path)])],
                     og=hero_b["v"] if hero_b and hero_b["w"] >= 800 else "/assets/img/og-image.png", og_type="article"))


def faq_page():
    groups = []
    for g, _, _ in FAQS:
        if g not in groups:
            groups.append(g)
    titles = {"Local SEO": "Local SEO", "AI SEO": "AI SEO", "Services": "Services and what's included", "Pricing": "Pricing", "Working with us": "Working with Get Found", "Partners": "Agencies, developers and partners"}
    parts = ""
    for g in groups:
        parts += f'<h2 class="group" id="{slugify(g)}">{esc(titles[g])}</h2>' + faq_block([f for f in FAQS if f[0] == g])
    jump = " · ".join(f'<a href="#{slugify(g)}">{esc(titles[g])}</a>' for g in groups)
    body = hero("Frequently Asked Questions About Local SEO &amp; AI SEO",
                "Straight answers to the questions business owners ask us most.",
                crumbs=[("FAQs", None)], eyebrow="FAQs", buttons=False) + f"""
<section class="section"><div class="container narrow">
  <label for="faq-search" class="center" style="margin-bottom:10px">Search the FAQs</label>
  <input class="faq-search" id="faq-search" type="search" placeholder="e.g. Google Maps, pricing, reports…" autocomplete="off">
  <p class="center form-note" style="margin:14px 0 0">{jump}</p>
  {parts}
  <div class="cta-box"><h2>Still have a question?</h2><p>Ask us directly. We usually respond within a few hours.</p><div class="btn-row"><a class="btn" href="/contact/">Contact us</a><a class="btn ghost" href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp us</a></div></div>
</div></section>"""
    write("/faq/", page("/faq/", "Local SEO & AI SEO FAQs: 30 Questions Answered",
                        "Answers to 30 common questions about Local SEO, AI SEO, Google Business Profile, pricing, reporting and working with Get Found.",
                        body, [breadcrumbs([("Home", "/"), ("FAQs", "/faq/")]), faq_ld(FAQS)]))


def contact():
    body = hero("Contact Get Found: Get Your Free Visibility Audit",
                "Tell us about your business and we&rsquo;ll show you how visible you are on Google, Google Maps and AI search today. We usually respond to enquiries within a few hours.",
                crumbs=[("Contact", None)], eyebrow="Contact", buttons=False) + f"""
<section class="section">
  <div class="container split" style="align-items:start">
    <div id="audit">
      <h2>Request your free visibility audit</h2>
      <form class="form" id="audit-form" novalidate>
        <div class="row"><div><label for="first_name">First name *</label><input id="first_name" name="first_name" required autocomplete="given-name"></div><div><label for="last_name">Last name</label><input id="last_name" name="last_name" autocomplete="family-name"></div></div>
        <div class="row"><div><label for="email">Email *</label><input id="email" name="email" type="email" required autocomplete="email"></div><div><label for="phone">Phone / WhatsApp</label><input id="phone" name="phone" type="tel" autocomplete="tel"></div></div>
        <div class="row"><div><label for="business">Business name</label><input id="business" name="business" autocomplete="organization"></div><div><label for="website">Website</label><input id="website" name="website" type="text" inputmode="url" placeholder="www.example.com"></div></div>
        <div><label for="interest">I&rsquo;m interested in</label><select id="interest" name="interest"><option>Free Visibility Audit</option><option>Local SEO</option><option>SEO + AI SEO</option><option>White-label / agency partnership</option><option>Something else</option></select></div>
        <div><label for="message">Tell us a little about your business</label><textarea id="message" name="message"></textarea></div>
        <div class="hp" aria-hidden="true"><label>Leave blank<input name="company_website_hp" tabindex="-1" autocomplete="off"></label></div>
        <button class="btn" type="submit">{CTA}</button>
        <p class="form-note" id="form-status" role="status" aria-live="polite">We&rsquo;ll only use your details to respond to your enquiry.</p>
      </form>
    </div>
    <aside>
      <h2>Talk to us directly</h2>
      <ul class="contact-list">
        <li><strong>Phone</strong><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
        <li><strong>WhatsApp</strong><a href="{WHATSAPP}" target="_blank" rel="noopener">Message us on WhatsApp</a></li>
        <li><strong>Email</strong><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><strong>Address</strong>{ADDRESS['street']}, {ADDRESS['suburb']}<br>{ADDRESS['city']}, {ADDRESS['country']} {ADDRESS['postcode']}<br><a href="{MAPS}" target="_blank" rel="noopener">View on Google Maps</a></li>
      </ul>
      <div class="card" style="margin-top:1.6rem"><h3>What happens next?</h3><ol style="padding-left:1.2em;margin:0"><li>We review your business online.</li><li>We reply with what we found and where the quick wins are.</li><li>If it makes sense, we talk about next steps. No pressure.</li></ol></div>
    </aside>
  </div>
</section>"""
    write("/contact/", page("/contact/", "Contact Get Found | Free Local SEO & AI SEO Visibility Audit",
                            "Contact Get Found in Cape Town for a free visibility audit. Call 074 124 2969, WhatsApp or email rian@get-found.co.za. Local SEO and AI SEO specialists.",
                            body, [LOCAL_BUSINESS, breadcrumbs([("Home", "/"), ("Contact", "/contact/")])]))


def not_found():
    body = f"""<section class="hero"><div class="container"><span class="eyebrow">Error 404</span><h1>We couldn&rsquo;t find that page</h1><p class="lead">The page you&rsquo;re looking for may have moved. Here are some good places to start.</p><div class="btn-row center"><a class="btn" href="/">Go to the homepage</a><a class="btn ghost" href="/services/">Services &amp; pricing</a><a class="btn ghost" href="/blog/">Read the blog</a></div></div></section>"""
    (PUB / "404.html").write_text(page("/404.html", "Page not found", "Page not found.", body, noindex=True), encoding="utf-8")


def seo_files():
    urls = [("/", "1.0"), ("/services/", "0.9"), ("/markets/", "0.7"), ("/markets/south-africa/", "0.9"), ("/markets/uk/", "0.8"), ("/markets/usa/", "0.8"),
            ("/partners/", "0.7"), ("/resources/", "0.8"), ("/blog/", "0.8"), ("/faq/", "0.7"), ("/contact/", "0.8")]
    urls += [(f"/blog/{p['slug']}/", "0.6") for p in POSTS_SORTED]
    mods = {f"/blog/{p['slug']}/": p["modified"] for p in POSTS}
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u, pr in urls:
        xml += f"  <url><loc>{SITE}{u}</loc><lastmod>{mods.get(u, TODAY)}</lastmod><priority>{pr}</priority></url>\n"
    xml += "</urlset>\n"
    (PUB / "sitemap.xml").write_text(xml, encoding="utf-8")
    (PUB / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")

    redirects = [
        "# Old Wix URLs -> new site (301)",
        "/home / 301", "/how-we-can / 301", "/about / 301", "/reviews-customers / 301",
        "/search-engine-optimization /services/ 301", "/pricing /services/ 301", "/pricing-plans/list /services/ 301",
        "/lead-generation-services /services/ 301", "/email-marketing /services/ 301", "/whatsapp-marketing /services/ 301",
        "/faqs /faq/ 301", "/book-online /contact/ 301", "/service-page/* /contact/ 301",
        "/blog/categories/* /blog/ 301",
        "/kelly-nelson / 301", "/camila-hernandez / 301", "/malina-garcia / 301", "/ayano-kang / 301",
    ]
    for p in POSTS:
        redirects.append(f"/post/{p['old']} /blog/{p['slug']}/ 301")
    redirects.append("/post/* /blog/ 301")
    (PUB / "_redirects").write_text("\n".join(redirects) + "\n", encoding="utf-8")
    (PUB / "_headers").write_text(
        "/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: SAMEORIGIN\n"
        "  Permissions-Policy: camera=(), microphone=(), geolocation=()\n\n"
        "/assets/css/*\n  Cache-Control: public, max-age=31536000, immutable\n/assets/js/*\n  Cache-Control: public, max-age=31536000, immutable\n"
        "/assets/fonts/*\n  Cache-Control: public, max-age=31536000, immutable\n/assets/img/*\n  Cache-Control: public, max-age=86400\n",
        encoding="utf-8")


def main():
    home(); services(); markets_hub()
    for k in ("za", "uk", "us"):
        market_page(k)
    partners(); resources(); blog_index()
    for p in POSTS:
        blog_post(p)
    faq_page(); contact(); not_found(); seo_files()
    print("Built", len(list(PUB.rglob("*.html"))), "pages")


if __name__ == "__main__":
    main()
