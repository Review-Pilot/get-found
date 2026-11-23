"""Shared content for the Get Found site (v1.0).
Edit copy here, then run:  python3 site-src/build.py
"""

SITE = "https://www.get-found.co.za"
BRAND = "Get Found"
PHONE_DISPLAY = "074 124 2969"
PHONE_TEL = "+27741242969"
WHATSAPP = "https://wa.me/27741242969?text=Hi%20Get%20Found%2C%20I%27d%20like%20a%20free%20visibility%20audit."
EMAIL = "rian@get-found.co.za"
MAPS = "https://www.google.com/maps/place/?q=place_id:ChIJge67A14Z-AERnN5AxlZBpkI"
ADDRESS = {
    "street": "11 Grove Avenue",
    "suburb": "Claremont",
    "city": "Cape Town",
    "country": "South Africa",
    "postcode": "7708",
}
SOCIALS = [
    ("Facebook", "https://www.facebook.com/GetfoundKenilworth", "facebook"),
    ("LinkedIn", "https://www.linkedin.com/in/rian-slabbert-2582ab188/", "linkedin"),
    ("Instagram", "https://www.instagram.com/getfound.za/", "instagram"),
    ("YouTube", "https://www.youtube.com/@get-found6025", "youtube"),
    ("TikTok", "https://www.tiktok.com/@getfound2?lang=en", "tiktok"),
    ("X", "https://x.com/RianSlabbe19436", "x"),
    ("Google Business Profile", MAPS, "google"),
]
CTA = "Get Your Free Visibility Audit"

LOCAL_SEO_FEATURES = [
    "Google Business Profile optimisation and management",
    "Two Google Business Profile posts per week",
    "One Google Business Profile video post per week",
    "Regular photo uploads",
    "Local keyword optimisation",
    "Geo-grid local rank tracking",
    "Website rank tracking",
    "Review management and review-generation automation",
    "Automated / customised review responses",
    "Citation building and local business listings",
    "Competitor monitoring",
    "Comprehensive reporting",
    "Ongoing optimisation",
    "Website chatbot setup",
]
AI_SEO_FEATURES = [
    "Everything in Local SEO",
    "Custom SEO strategy",
    "Up to 300 tracked keywords",
    "Up to three website-page improvements per month",
    "Ongoing technical SEO",
    "One SEO-optimised blog article per month",
    "AI Search optimisation",
    "Conversational search and answer-focused content optimisation",
    "Business listings across 50+ relevant directories and platforms",
    "AI-related traffic reporting",
    "Competitor analysis and ongoing testing",
]

PRICING = {
    "za": {"name": "South Africa", "cur": "R", "local": "6,000", "ai": "12,000", "setup_local": "R3,000", "setup_ai": "R5,000"},
    "uk": {"name": "United Kingdom", "cur": "£", "local": "350", "ai": "650", "setup_local": "£200", "setup_ai": "£300"},
    "us": {"name": "United States", "cur": "$", "local": "450", "ai": "750", "setup_local": "$300", "setup_ai": "$400"},
}

REVIEWS = [
    ("GF and Samantha has given us excellent service and increased our traffic exponentially over the last 12 months.", "Warren Jeppe", "Owner, MJ Flooring"),
    ("Rian and Get-Found have been amazing and are constantly making a significant positive improvement to my business. Really appreciate the lengths they go to to achieve results. Professional and fun guys, highly recommended.", "Chris Ryder", "Owner, The Wholesome Dog Co"),
    ("Such a profound experience working with Rian, he really knows his stuff when it comes to SEO and optimizing all your platforms to be more visible online. What inspires me is that he is also constantly working on staying on top of the latest trends and technology to really give you the best value for your money. I highly recommend working with him!", "Amanda Ferreira", "Owner, B Inspired Digital"),
    ("I am super thrilled with Get-Found's SEO service. Rian is friendly and easy to work with, making the onboarding process effortless. Although I've been a customer for a short time, I've already noticed a significant improvement in my business, with a stronger online presence and increased interest. Thank you!", "Lisa King", "Owner, The Lisa King Collection"),
]

TRUSTED = ["Vineyard Car Hire", "African Welcome Safaris", "MJ Flooring"]

# (group, question, answer)  — 30 FAQs, in the order of the site strategy document.
FAQS = [
    ("Local SEO", "What is Local SEO?",
     "Local SEO is the work of making your business visible when people nearby search for what you offer: in Google Search, in Google Maps and in local directories. It combines an optimised Google Business Profile, accurate business listings, reviews and locally relevant content so customers find you first."),
    ("Local SEO", "Who needs Local SEO?",
     "Any business that serves customers in a particular town, city or region, or that customers visit in person. Think trades, clinics, restaurants, retailers, accommodation, car hire and professional services. If your customers search for “[service] near me” or “[service] in [city]”, Local SEO matters to you."),
    ("Local SEO", "What is Google Business Profile optimisation?",
     "Your Google Business Profile is the listing that appears on Google Maps and in the panel beside search results. Optimising it means complete and accurate details, the right categories and services, quality photos, regular posts and proper review handling, so Google understands your business and customers trust it."),
    ("Local SEO", "Can Local SEO help my business rank in Google Maps?",
     "Yes. Google Maps rankings are driven by relevance, distance and prominence. We work on relevance (your profile and keywords) and prominence (reviews, citations and website strength). We can’t change where your customer is standing, which is why we track your visibility with geo-grid reports."),
    ("Local SEO", "What is geo-grid rank tracking?",
     "Your Google Maps ranking changes depending on where the searcher is. Geo-grid tracking checks your ranking from a grid of points around your business and shows it as a heat map, so you can see exactly where you’re strong and where competitors are winning."),
    ("Local SEO", "How long does Local SEO take to work?",
     "Many businesses see movement in Google Maps within the first few months, with stronger results building over time. How quickly depends on your competition, your starting point and your industry. We report monthly so you can see progress for yourself."),
    ("Local SEO", "Do Google reviews help Local SEO?",
     "Yes. The number, quality and freshness of your reviews, and how you respond to them, influence local visibility. Just as importantly, reviews influence whether people choose you. We help you ask for reviews consistently and respond to every one."),
    ("Local SEO", "What are local citations?",
     "Citations are mentions of your business name, address and phone number on directories and other websites. Consistent, accurate listings build trust with search engines and give customers more places to find you."),
    ("Local SEO", "How often will my Google Business Profile be updated?",
     "Our Local SEO package includes two Google Business Profile posts and one video post every week, plus regular photo uploads and ongoing optimisation, so your profile stays active and fresh."),
    ("Local SEO", "Does Local SEO include competitor tracking?",
     "Yes. We monitor your competitors so we can see what they’re doing, where they’re gaining ground and where there are opportunities for you to move ahead."),
    ("AI SEO", "What is AI SEO?",
     "AI SEO is optimising your business so it is found, understood and recommended in AI-powered search, such as ChatGPT and Google’s AI features. It builds on strong SEO fundamentals: clear helpful content, consistent listings, trust signals and direct answers to the questions your customers ask."),
    ("AI SEO", "What is the difference between traditional SEO and AI SEO?",
     "Traditional SEO helps your pages rank in a list of results. AI SEO helps your business get understood, trusted and mentioned inside an answer. Both rely on the same foundations, which is why we treat AI SEO as an extension of good SEO and not a replacement for it."),
    ("AI SEO", "What are GEO and AEO?",
     "GEO (Generative Engine Optimisation) and AEO (Answer Engine Optimisation) are industry terms for optimising content so AI tools and answer engines can find, understand and reference it. We use them as supporting terms. What matters to you is simple: clear, structured, trustworthy content wins."),
    ("AI SEO", "Can you get my business listed in ChatGPT?",
     "No one can guarantee a mention in ChatGPT or any AI tool. What we can do is strengthen the signals those tools rely on: consistent listings, strong website content, reviews and clear answers to your customers’ questions. Our work with Vineyard Car Hire is a practical example of AI-search visibility. It’s an example, not a guaranteed outcome."),
    ("AI SEO", "Which AI search platforms do you optimise for?",
     "We focus on the platforms your customers actually use, including ChatGPT, Google’s AI features, Gemini, Perplexity and Microsoft Copilot. Much of the optimisation work is common across all of them."),
    ("AI SEO", "Does AI SEO replace normal Google SEO?",
     "No. Strong Google SEO and Local SEO remain the foundation, and AI tools draw on many of the same sources. That’s why our SEO + AI SEO package starts with everything in Local SEO and builds from there."),
    ("Services", "What is included in your SEO + AI SEO package?",
     "Everything in Local SEO, plus a custom SEO strategy, up to 300 tracked keywords, up to three website-page improvements a month, ongoing technical SEO, one SEO-optimised blog article a month, AI Search optimisation, conversational and answer-focused content optimisation, listings across 50+ directories and platforms, AI-related traffic reporting, and competitor analysis with ongoing testing."),
    ("Services", "Do you create SEO content?",
     "Yes. Our SEO + AI SEO package includes one SEO-optimised blog article every month, plus up to three improvements to your website pages."),
    ("Services", "Do you fix technical SEO problems?",
     "Yes. Ongoing technical SEO is part of our SEO + AI SEO package, covering the behind-the-scenes issues that stop search engines and AI tools reading your site properly."),
    ("Services", "How many keywords do you track?",
     "Our SEO + AI SEO package tracks up to 300 keywords. Our Local SEO package focuses on local keywords, with geo-grid rank tracking and website rank tracking."),
    ("Pricing", "How much does Local SEO cost in South Africa?",
     "In South Africa, Local SEO is R6,000 per month with a once-off setup fee of R3,000. In the UK it’s £350 per month with a once-off £200 setup fee, and in the USA it’s $450 per month with a once-off $300 setup fee."),
    ("Pricing", "How much does SEO + AI SEO cost?",
     "In South Africa, SEO + AI SEO is R12,000 per month with a once-off setup fee of R5,000. In the UK it’s £650 per month with a once-off £300 setup fee, and in the USA it’s $750 per month with a once-off $400 setup fee."),
    ("Pricing", "Why are your UK and US prices different from your South African prices?",
     "We use regional pricing rather than a straight currency conversion. South African pricing is structured around the local SME market, while UK and US pricing is structured for those markets and stays very competitive. UK and US clients get exactly the same product at a cost-effective price because the work is done from South Africa."),
    ("Working with us", "Do I have to learn any SEO software?",
     "No. We use the tools so you don’t have to. You simply get clear reports and a straight conversation about what’s working."),
    ("Working with us", "Will I receive reports?",
     "Yes. You receive comprehensive reporting that covers rankings, Google Business Profile activity, reviews and traffic, and for SEO + AI SEO clients, AI-related traffic reporting too."),
    ("Working with us", "Do you guarantee number-one Google rankings?",
     "No, and you should be cautious of anyone who does. No one controls Google. What we offer is focused, transparent work on the things that move the needle, backed by monthly reporting so you can see exactly what you’re getting."),
    ("Working with us", "Do you work with businesses outside South Africa?",
     "Yes. We work with businesses in the UK and USA, and we have clients across Europe and Asia as well as South Africa."),
    ("Partners", "Can web developers outsource SEO to Get Found?",
     "Yes. Web developers, freelancers and agencies can hand their SEO to us, so you can offer your clients a complete service without building an SEO team."),
    ("Partners", "Do you offer white-label SEO?",
     "Yes. We provide white-label and outsourced SEO fulfilment for agencies and web developers. Get in touch and we’ll talk you through how it works."),
    ("Partners", "Do you have an affiliate or referral programme?",
     "If you’d like to refer clients or partner with us, get in touch and we’ll walk you through the options."),
]

HOME_FAQ_IDX = [0, 10, 11, 13, 5, 20, 24, 25]   # 8 strongest FAQs for the homepage preview

RESOURCE_CATEGORIES = [
    ("Free & Low-Cost Tools", "Roundups aimed at cost-conscious entrepreneurs and SMEs.", None),
    ("SEO & Local SEO Tools", "Keyword tools, local rank trackers, GBP tools, citation tools, Search Console and GA4 guides.", "Local SEO"),
    ("AI Tools for Business", "AI writing, research, chatbots, customer service and workflow tools.", "AI SEO"),
    ("Automation", "WhatsApp automation, CRM workflows, email automation and integrations.", None),
    ("Reviews & Reputation", "Review generation, reputation management, widgets and QR/NFC.", None),
    ("Marketing & Lead Generation", "Meta lead generation, click-to-WhatsApp, Google Ads and outreach.", "Lead Generation"),
    ("Website & Conversion Tools", "Landing pages, forms, chatbots, analytics and call-to-action tools.", None),
    ("Productivity & Operations", "Low-cost software for scheduling, documentation, projects and admin.", None),
    ("Guides & How-Tos", "Step-by-step practical guides for small business owners.", "SEO Strategy"),
    ("Comparisons & Alternatives", "Tool A vs Tool B, best alternatives, free vs paid, DIY vs managed.", None),
]

# Nicer <title> tags than the old Wix ones, keyed by the new slug.
POST_SEO_TITLES = {
    "local-seo-vs-ai-seo-how-search-is-evolving": "Local SEO vs AI SEO: How Search Is Evolving",
    "local-seo-tips-to-boost-local-visibility": "Local SEO Tips to Boost Your Local Visibility",
    "intent-focused-ai-ready-seo-strategy-2026": "Intent-Focused, AI-Ready SEO Strategy for 2026",
    "mastering-seo-ranking-strategies-that-work": "Mastering SEO: Ranking Strategies That Work",
    "lead-generation-systems-for-small-businesses-2026": "Best Lead Generation Systems for Small Businesses (2026)",
    "impact-of-local-seo-on-small-businesses": "The Impact of Local SEO on Small Businesses",
    "local-seo-strategies-cape-town-south-africa": "Local SEO Strategies for Cape Town & South Africa",
    "growth-strategies-for-small-businesses": "Growth Strategies Every Small Business Should Know",
    "local-vs-global-seo-south-african-market": "Local vs Global SEO in the South African Market",
}
