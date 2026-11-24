#!/usr/bin/env python3
"""Builds the "20 Quick Wins" lead-magnet guide.

    python3 build_ebook.py          # writes ebook.html next to this file
    node render_pdf.js ebook.html out.pdf   # prints the PDF (Chromium)

To make the next guide, copy this folder, change TITLE / PARTS / WINS below.
"""
import html
from pathlib import Path

HERE = Path(__file__).resolve().parent
esc = html.escape

PHONE = "074 124 2969"
EMAIL = "rian@get-found.co.za"
SITE = "www.get-found.co.za"

PARTS = {
    1: ("Google Business Profile", "Your free shop window on Google Search and Google Maps."),
    2: ("Your website", "Simple fixes that help Google, AI tools and customers understand you."),
    3: ("AI search", "Be the business ChatGPT, Gemini and Perplexity talk about."),
}

# (number, part, title, time, big_impact, steps, why, tip_label, tip)
WINS = [
    (1, 1, "Claim and verify your profile", "15 min", False,
     ["Search your business name on Google, or go to business.google.com.",
      "Click <b>Claim this business</b> (or <b>Add your business</b>) and follow the prompts.",
      "Verify using the method Google offers: video, phone, email or postcard."],
     "Until it's verified, you can't control how you show up on Google Search and Maps.",
     "Tip", "Claimed it years ago? Log in and check the owner email is one you still use."),
    (2, 1, "Pick the right main category", "5 min", True,
     ["In your profile, choose <b>Edit profile</b>, then <b>Business information</b>.",
      "Set your main category to the most specific match, like &ldquo;Car rental agency&rdquo;, not &ldquo;Business&rdquo;.",
      "Add a few extra categories that truly describe what you do."],
     "Your main category is one of the biggest signals telling Google which searches you should show up for.",
     "Tip", "Only pick categories you really offer. Fewer, accurate ones beat a long list."),
    (3, 1, "Make your details perfect", "10 min", False,
     ["Use your real business name, exactly as on your signage. No extra keywords.",
      "Check your address, phone number and website link.",
      "Set your opening hours, plus special hours for public holidays and December."],
     "Wrong hours or numbers cost you customers and trust, and Google compares your details with other websites.",
     "Tip", "Copy your name, address and phone number once, and paste them exactly the same everywhere else."),
    (4, 1, "Write your business description", "10 min", False,
     ["You have up to 750 characters. Put the most important things in the first 250.",
      "Say what you do, where you do it and who you help, in plain English.",
      "Work in a few natural keywords like &ldquo;plumber in Claremont&rdquo;. Don't stuff them or add links."],
     "It's your elevator pitch, and it helps Google and AI tools understand what you do.",
     "Tip", "Read it out loud. If it sounds like a robot wrote it, rewrite it."),
    (5, 1, "Add your services, products and extras", "15 min", True,
     ["Add each service you offer, with a one-line description and a price if you can.",
      "Add your products if you sell any.",
      "Tick every attribute that applies, like &ldquo;online appointments&rdquo; or &ldquo;wheelchair accessible&rdquo;."],
     "Google's AI now answers customer questions using your profile details, so the more complete it is, the better those answers.",
     "Tip", "If a detail is true, add it. Every blank field is a missed chance."),
    (6, 1, "Add 10 or more real photos", "20 min", False,
     ["Take photos on your phone in daylight: outside, inside, your team and your work.",
      "Upload them under <b>Photos</b>, and add your logo and a cover photo.",
      "Add new photos every week or two."],
     "People choose businesses that look real and active, and photos get a lot of attention.",
     "Tip", "Skip stock photos. Real beats pretty."),
    (7, 1, "Ask 5 happy customers for a review", "15 min", True,
     ["In your profile, click <b>Ask for reviews</b> and copy your review link.",
      "WhatsApp it to 5 customers who were happy, with a friendly, personal message.",
      "Put a QR code for your review link on your counter or invoices (free tools can make one)."],
     "Reviews are one of the strongest signals for Google Maps, and AI tools tend to recommend businesses with plenty of good reviews.",
     "Careful", "Never pay for reviews or offer rewards for them. It breaks Google's rules."),
    (8, 1, "Reply to every review", "10 min", False,
     ["Open your reviews and reply to each one, newest first.",
      "Thank happy customers by name and mention something specific.",
      "For a bad review, stay calm, apologise, and offer to fix it offline."],
     "Replies show you care, and customers read them before they choose you.",
     "Tip", "Try to reply within 48 hours."),
    (9, 1, "Post a weekly update", "10 min", False,
     ["In your profile, choose <b>Add update</b> (or <b>Posts</b>).",
      "Share an offer, news, a new product or a recent job, with one photo.",
      "Add a button such as <b>Call now</b> or <b>Learn more</b>."],
     "Fresh posts keep your profile active and give people a reason to click.",
     "Tip", "Write four posts in one sitting and you're covered for a month."),

    (10, 2, "Put your service and town in your page titles", "15 min", True,
     ["In your website's SEO settings, find the <b>page title</b> for each page.",
      "Use this pattern: <i>Service in Town | Business name</i>, for example &ldquo;Plumber in Claremont, Cape Town | Smith Plumbing&rdquo;.",
      "Keep it under about 60 characters, and make every page's title different."],
     "The page title is one of the first things Google reads, and it's what people see in search results.",
     "Tip", "Use the same words in the big heading (H1) at the top of the page."),
    (11, 2, "Match your name, address and phone number", "10 min", False,
     ["Put your business name, address and phone number as <b>text</b> in your website footer.",
      "Copy them exactly from your Google profile.",
      "Add a Google Map to your contact page."],
     "When your details match everywhere, Google and AI tools can trust you're a real, stable business.",
     "Tip", "Use text, not an image. Google can't read words inside pictures."),
    (12, 2, "Make it easy to call or WhatsApp", "15 min", False,
     ["Add a <b>Call now</b> button that opens the phone dialler (a link that starts with tel:).",
      "Add a <b>WhatsApp</b> button (a link like wa.me/27741234567, your number with country code, no spaces or plus).",
      "Check on your own phone that both are easy to tap near the top of the page."],
     "Most local searches happen on phones. Make contacting you a one-tap job.",
     "Tip", "Many South African customers would rather WhatsApp than call."),
    (13, 2, "Make your site fast on a phone", "20 min", False,
     ["Go to pagespeed.web.dev and test your home page.",
      "Shrink big photos with a free tool like Squoosh or TinyPNG before you upload them.",
      "Remove what you don't need, like old plug-ins and auto-playing videos."],
     "Slow pages lose visitors, and speed is part of how Google judges your site.",
     "Tip", "Aim for photos under about 200 KB each."),
    (14, 2, "Give each service its own page", "45 min", True,
     ["Make a separate page for each main service (and each main area you serve).",
      "On each one, explain in your own words what you do, who it's for, your prices or process, and add real photos.",
      "Add a button to call, WhatsApp or book."],
     "One page per service gives Google, and your customers, a clear answer for each search.",
     "Tip", "Start with the service that earns you the most money."),
    (15, 2, "Connect Google Search Console", "15 min", False,
     ["Go to search.google.com/search-console and sign in with your Google account.",
      "Add your website and verify it. The page walks you through it.",
      "Submit your sitemap, usually yourwebsite.com/sitemap.xml."],
     "It's free, it shows how people find you, and it tells you if Google has trouble with your site.",
     "Tip", "Check back once a month to see which searches bring people to you."),

    (16, 3, "Test yourself in AI search", "10 min", False,
     ["Open ChatGPT, Gemini or Perplexity.",
      "Ask: &ldquo;Who is the best [your service] in [your town]?&rdquo; and &ldquo;Tell me about [your business name].&rdquo;",
      "Screenshot what each says: who gets recommended, and what they say about you (right or wrong)."],
     "Now you know where you stand today and what to fix first.",
     "Tip", "Answers change between tools and from day to day. Test a few times and look for patterns."),
    (17, 3, "Answer your customers' questions on your website", "30 min", True,
     ["Write down the 5 to 8 questions customers ask you most.",
      "Add a <b>Frequently Asked Questions</b> section to your site, or to the right service page.",
      "Answer each in 2 or 3 plain sentences, with the direct answer first."],
     "AI tools love clear, direct answers, and so do your customers.",
     "Tip", "Use your customers' own words, not industry jargon."),
    (18, 3, "List your business in more places", "30 min", False,
     ["Claim your free profiles on <b>Bing Places</b> and <b>Apple Business Connect</b>.",
      "Set up a Facebook business page and a LinkedIn page if you don't have them.",
      "Add your business to 2 or 3 directories that suit your industry and area, using exactly the same name, address and phone number each time."],
     "AI tools and search engines gather information from many places, and matching details build trust.",
     "Tip", "Keep a note of where you're listed so you can update everything at once."),
    (19, 3, "Get mentioned by other local sites", "30 min", True,
     ["List 5 local businesses, suppliers, associations or community sites you already know.",
      "Ask each one to mention or link to your business, for example on a &ldquo;partners&rdquo; page or in a newsletter.",
      "Say yes to local events, podcasts and write-ups, and link to them from your site."],
     "Mentions from trusted local sources are strong proof that you're a real, respected business in your area.",
     "Tip", "Offer something back: a quote, a useful tip or a link to them."),
    (20, 3, "Make it a 15-minute monthly habit", "15 min / month", False,
     ["Once a month, reply to new reviews and ask 2 or 3 customers for a fresh one.",
      "Add a post and a few new photos, and check your hours and details.",
      "Re-run your AI test from Win 16 and see what's changed."],
     "Steady, regular activity beats one big burst. Local SEO is a habit, not a one-off job.",
     "Tip", "Put a repeating reminder in your phone calendar right now."),
]


def win_card(w):
    n, part, title, time, big, steps, why, tip_label, tip = w
    steps_html = "".join(f"<li><span class='sn'>{i}</span><span>{s}</span></li>" for i, s in enumerate(steps, 1))
    tag = "<span class='chip hot'>Big impact</span>" if big else "<span class='chip'>Easy win</span>"
    warn = " warn" if tip_label == "Careful" else ""
    return f"""
<article class="win">
  <div class="num">{n}</div>
  <div class="body">
    <div class="top"><h3>{title}</h3><div class="chips">{tag}<span class="chip time">{time}</span></div></div>
    <ol class="steps">{steps_html}</ol>
    <div class="foot">
      <p class="why"><b>Why it works:</b> {why}</p>
      <p class="tip{warn}"><b>{tip_label}:</b> {tip}</p>
    </div>
  </div>
</article>"""


def part_band(p, with_map=False):
    name, sub = PARTS[p]
    mp = '<img class="band-map" src="assets/local-seo-map.jpg" alt="">' if with_map else ""
    return f"""
<div class="band">
  <div class="band-text"><span class="kicker">Part {p} &middot; Wins {'1&ndash;9' if p == 1 else '10&ndash;15' if p == 2 else '16&ndash;20'}</span><h2>{name}</h2><p>{sub}</p></div>
  {mp}
</div>"""


def page(inner, num, label, cls=""):
    return f"""
<section class="page {cls}">
  <div class="runhead"><span>{label}</span><span>20 Quick Wins</span></div>
  <div class="content">{inner}</div>
  <div class="runfoot"><span>Get Found &middot; Local SEO &amp; AI SEO &middot; Cape Town</span><span>{num}</span></div>
</section>"""


def build():
    W = {w[0]: win_card(w) for w in WINS}
    cards = lambda *ns: "".join(W[n] for n in ns)
    pages = []

    # 1 cover
    pages.append(f"""
<section class="page cover">
  <div class="glow"></div>
  <img class="logo" src="assets/logo.png" alt="Get Found">
  <div class="cover-main">
    <span class="pill">Free guide</span>
    <h1><span class="big20">20</span><br>Quick Wins</h1>
    <p class="sub">to get your local business found on <b>Google</b>, <b>Google Maps</b> and <b>AI&nbsp;search</b></p>
    <div class="cover-parts"><span>Google Business Profile</span><span>Your website</span><span>AI search</span></div>
  </div>
  <div class="cover-author">
    <div class="ring"><img src="assets/rian-square.jpg" alt="Rian, founder of Get Found"></div>
    <p><b>A quick-start guide by Rian</b><br>Founder, Get Found &middot; Cape Town</p>
  </div>
  <div class="cover-tag">Get Found. Get Chosen. Grow.</div>
</section>""")

    # 2 intro
    pages.append(page(f"""
  <div class="intro-grid">
    <div class="frame"><img src="assets/rian-wide.jpg" alt="Rian"></div>
    <div>
      <span class="eyebrow">Welcome</span>
      <h2>Hi, I&rsquo;m Rian.</h2>
      <p>I&rsquo;ve spent over 30 years in business, and today I help local businesses get found online.</p>
      <p>Most businesses don&rsquo;t need anything fancy to start winning. They need the basics done properly. So I&rsquo;ve put the 20 quickest, easiest wins into one short guide.</p>
      <p><b>No jargon. No tech degree needed.</b> Pick one, do it today, tick it off.</p>
    </div>
  </div>
  <h3 class="sec">How to use this guide</h3>
  <div class="trio">
    <div class="mini"><b>1</b><h4>One win a day</h4><p>Do one a day for 20 days, or knock out a few on a quiet afternoon.</p></div>
    <div class="mini"><b>2</b><h4>10 to 20 minutes each</h4><p>Most wins are quick. The time is shown on every card.</p></div>
    <div class="mini"><b>3</b><h4>Start with the big ones</h4><p>Wins marked <span class="chip hot inline">Big impact</span> move the needle most.</p></div>
  </div>
  <h3 class="sec">Before you start, grab these</h3>
  <ul class="ticks">
    <li>Your <b>Google account</b> login (the one you use for your business)</li>
    <li>Your <b>website login</b>, or the person who looks after your site</li>
    <li>Your <b>smartphone</b>, for photos and for testing your site</li>
  </ul>
  <div class="reality"><b>A reality check:</b> no one can promise you the number-one spot, not us and not anyone else. Every business and every area is different. But these 20 steps cover what matters most, and the sooner you start, the sooner you can start seeing results.</div>
""", 2, "Welcome"))

    pages.append(page(part_band(1, with_map=True) + cards(1, 2, 3), 3, "Part 1 · Google Business Profile"))
    pages.append(page(cards(4, 5, 6), 4, "Part 1 · Google Business Profile"))
    pages.append(page(cards(7, 8, 9), 5, "Part 1 · Google Business Profile"))
    pages.append(page(part_band(2) + cards(10, 11, 12), 6, "Part 2 · Your website"))
    pages.append(page(cards(13, 14, 15), 7, "Part 2 · Your website"))
    pages.append(page(part_band(3) + cards(16, 17, 18), 8, "Part 3 · AI search"))
    pages.append(page(cards(19, 20) + """
  <div class="explain">
    <h3>How AI tools pick who to recommend (in plain English)</h3>
    <div class="ex-grid">
      <div><b>Strong Google Maps presence</b><p>Businesses that show up well on Maps tend to be recommended more often.</p></div>
      <div><b>Plenty of good reviews</b><p>Lots of recent, positive reviews are a powerful signal.</p></div>
      <div><b>Matching details everywhere</b><p>The same name, address and phone number across the web builds trust.</p></div>
      <div><b>Mentions by trusted sites</b><p>Local sites, directories and news pieces that name you add proof.</p></div>
      <div><b>Clear answers on your site</b><p>Plain, direct answers to real customer questions are easy for AI to use.</p></div>
    </div>
    <p class="fine">AI answers change from day to day and between tools, so no one can control them. But doing these things well puts you in the best position.</p>
  </div>""", 9, "Part 3 · AI search"))

    # 10 checklist
    def chk(rng, label):
        items = "".join(f"<li><span class='box'></span><span><b>{w[0]}.</b> {w[2]}</span></li>" for w in WINS if w[1] == rng)
        return f"<div><h4>{label}</h4><ul class='check'>{items}</ul></div>"
    pages.append(page(f"""
  <span class="eyebrow">Your cheat sheet</span>
  <h2>The 20-win checklist</h2>
  <p class="lead">Print this page, stick it on the wall, and tick them off as you go.</p>
  <div class="check-grid">{chk(1, 'Part 1 · Google Business Profile')}{chk(2, 'Part 2 · Your website')}{chk(3, 'Part 3 · AI search')}</div>
  <div class="notes"><h4>My notes: what to fix first</h4><div class="lines"></div></div>
  <div class="reality"><b>Made it to 20?</b> Nice work. You&rsquo;ve done more for your local visibility than most of your competitors. Repeat Win 20 every month to keep the momentum going.</div>
  <p class="fine">These are general tips. Google and AI tools change often, so check Google&rsquo;s own help pages if something looks different on your screen.</p>
""", 10, "Checklist"))

    # 11 CTA
    pages.append(f"""
<section class="page cta">
  <div class="glow"></div>
  <img class="logo" src="assets/logo.png" alt="Get Found">
  <div class="cta-main">
    <span class="pill">Want a hand?</span>
    <h2>Rather have us<br>do it for you?</h2>
    <p class="sub">We&rsquo;re customer-driven and customer-focused. Once you&rsquo;ve paid and we have your information, we get started straight away and turn the job around in under 7 days.</p>
    <div class="cta-box">
      <b>Get your free visibility audit</b>
      <span>See how visible your business is on Google, Google Maps and AI search today.</span>
      <a>{SITE}</a>
    </div>
    <div class="contact"><span>WhatsApp / call <b>{PHONE}</b></span><span>{EMAIL}</span><span>11 Grove Avenue, Claremont, Cape Town</span></div>
  </div>
  <div class="cta-photos">
    <div class="ring small"><img src="assets/rian-square.jpg" alt="Rian"></div>
    <img class="map" src="assets/local-seo-map.jpg" alt="Local SEO">
  </div>
  <div class="cover-tag">Get Found. Get Chosen. Grow.</div>
</section>""")

    css = (HERE / "ebook.css").read_text()
    doc = f"""<!doctype html><html lang="en-ZA"><head><meta charset="utf-8"><title>20 Quick Wins | Get Found</title><style>{css}</style></head><body>{''.join(pages)}</body></html>"""
    (HERE / "ebook.html").write_text(doc, encoding="utf-8")
    print("wrote ebook.html,", len(pages), "pages")


if __name__ == "__main__":
    build()
