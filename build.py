#!/usr/bin/env python3
"""Builds index.html + services/*.html + about/*.html from src/partials and the content below.
Run: python3 build.py"""
import math, re, os, json
P={f[:-5]: open(f'src/partials/{f}',encoding='utf-8').read() for f in os.listdir('src/partials') if f.endswith('.html')}
WA='https://wa.me/918637721112?text='
EMAIL='info@kuberestate.co.in'
INSTAGRAM='https://www.instagram.com/kuberrproperty'
V='M16 28A98 98 0 0 1 84 28L68 77A46 46 0 0 0 32 77Z'
def Rmark(color): return f'<g fill="none" stroke="{color}" stroke-width="4.6" stroke-linejoin="miter"><path d="M42.5 38.5v27"/><path d="M42.5 40.5h7.5a6.5 6.5 0 0 1 0 13h-7.5"/><path d="M49 53.5l9 11.5"/></g>'
BRAND=f'<svg class="brand__mark" viewBox="14 26 72 53" aria-hidden="true"><path d="{V}" fill="currentColor"/>{Rmark("var(--brand-bg,#e5e5e5)")}</svg>'
FAV="data:image/svg+xml,"+(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="22" fill="#000"/><g transform="translate(50 50) scale(.72) translate(-50 -52)"><path d="{V}" fill="#fff"/>{Rmark("#000")}</g></svg>').replace('#','%23').replace('"',"'").replace('<','%3C').replace('>','%3E')
VER='v=3'
WAI=lambda t: WA+t

# ------------------------------------------------------------------ chrome
def head(title, desc, path, og='/assets/og.png'):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="https://kuberestate.co.in{path}">
  <meta name="theme-color" content="#e5e5e5">
  <meta property="og:type" content="website"><meta property="og:site_name" content="Kuber Estate">
  <meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
  <meta property="og:url" content="https://kuberestate.co.in{path}"><meta property="og:image" content="https://kuberestate.co.in{og}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="{FAV}">
  <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400..600&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
  <link rel="preconnect" href="https://images.unsplash.com">
  <link rel="stylesheet" href="/styles.css?{VER}">
'''
LD='''  <script type="application/ld+json">
  {"@context":"https://schema.org","@type":"RealEstateAgent","name":"Kuber Estate","url":"https://kuberestate.co.in/","email":"'+EMAIL+'","telephone":"+91-86377-21112",
   "description":"Global real estate investment consultancy born in Pune, India — property selection, legal and government verification, valuation and deal closure for investors in India and international markets.",
   "areaServed":[{"@type":"City","name":"Pune"},{"@type":"Country","name":"India"},"Worldwide"],
   "address":{"@type":"PostalAddress","addressLocality":"Pune","addressRegion":"Maharashtra","addressCountry":"IN"},
   "sameAs":["https://www.instagram.com/kuberrproperty"]}
  </script>
</head>
'''
def nav(back=None):
    b = f'<a class="back" href="{back}" id="backBtn"><svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg><span>Back</span></a>' if back else ''
    return f'''<body class="{'page' if back else 'home'}">
  <header class="nav" id="nav">
    <div class="wrap nav__inner">
      <div class="nav__left">{b}
      <a class="brand" href="/" aria-label="Kuber Estate home">
        {BRAND}
        <span class="brand__word">Kuber Estate</span>
      </a></div>
      <a class="btn btn--fill btn--sm" href="{WAI('Hi%20Kuber%20Estate%2C%20I%27d%20like%20to%20discuss%20a%20property%20investment.')}" target="_blank" rel="noopener">WhatsApp us</a>
    </div>
  </header>
'''
WAPATH='<path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>'
def dock(active=''):
    items=[('home','/#home','Home','<path d="M4 11l8-7 8 7v9a1 1 0 01-1 1h-5v-6h-4v6H5a1 1 0 01-1-1z"/>'),
           ('offer','/#offer','What we offer','<path d="M4 7h16v13H4zM9 7V4h6v3M4 12h16"/>'),
           ('properties','/properties.html','Properties','<path d="M3 21h18M5 21V8l7-5 7 5v13M9 21v-6h6v6"/>'),
           ('about','/about.html','About','<path d="M5 7h14l-3 11H8z"/>')]
    a=''.join(f'<a href="{h}" data-p="{k}"{" class=is-active" if k==active else ""}><svg viewBox="0 0 24 24">{ic}</svg><span>{t}</span></a>' for k,h,t,ic in items)
    return f'''
  <nav class="dock" id="dock" aria-label="Sections" data-active="{active}">{a}
    <div class="connect" id="connect">
      <button class="connect__btn" type="button" id="connectBtn" aria-expanded="false" aria-haspopup="true" aria-label="Connect with us">
        <svg viewBox="0 0 24 24" class="connect__ico"><path d="M20 12a8 8 0 01-11.6 7.1L4 20l1-4.2A8 8 0 1120 12z"/><path d="M8.5 12h.01M12 12h.01M15.5 12h.01" stroke-width="2.4"/></svg>
      </button>
      <div class="connect__menu" id="connectMenu" role="menu">
        <a role="menuitem" href="{WAI('Hi%20Kuber%20Estate%2C%20I%27d%20like%20to%20discuss%20a%20property%20investment.')}" target="_blank" rel="noopener"><span class="connect__ic connect__ic--wa"><svg viewBox="0 0 24 24" class="wa">{WAPATH}</svg></span><span><strong>WhatsApp</strong><small>+91 86377 21112</small></span></a>
        <a role="menuitem" href="{INSTAGRAM}" target="_blank" rel="noopener"><span class="connect__ic connect__ic--ig"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="0.9" fill="currentColor" stroke="none"/></svg></span><span><strong>Instagram</strong><small>@kuberrproperty</small></span></a>
        <a role="menuitem" href="/#contact" class="connect__contact"><span class="connect__ic connect__ic--mail"><svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg></span><span><strong>Contact us</strong><small>Send an enquiry</small></span></a>
      </div>
    </div>
  </nav>
'''
def footer():
    f=P['footer']
    f=re.sub(r'<svg class="brand__mark".*?</svg>', BRAND, f, count=1, flags=re.S)
    f=f.replace('Real estate investment consultants, Pune. We find, verify, evaluate and close — on your side of the table.','Global real estate investment consultants, born in Pune. We find, verify, evaluate and close — on your side of the table, anywhere in the world.')
    links='''          <h4>Company</h4>
          <ul>
            <li><a href="/services.html">Services</a></li>
            <li><a href="/products/kubercrm.html">Products</a></li>
            <li><a href="/properties.html">Properties</a></li>
            <li><a href="/about.html">About us</a></li>
            <li><a href="/about.html#difference">The difference</a></li>
            <li><a href="/about.html#founders">Founders</a></li>

          </ul>'''
    f=re.sub(r'<h4>Company</h4>\s*<ul>.*?</ul>', links, f, count=1, flags=re.S)
    f=re.sub(r'<h4>Properties</h4>\s*<ul>.*?</ul>', '''<h4>Services</h4>
          <ul>
            <li><a href="/services.html#investment-advisory">Investment advisory</a></li>
            <li><a href="/services.html#overseas-investors">Overseas &amp; NRI investors</a></li>
            <li><a href="/services.html#buying-your-home">Buying your home</a></li>
            <li><a href="/services.html#commercial-retail">Commercial &amp; retail</a></li>
            <li><a href="/services.html#plots-land">Plots &amp; land</a></li>
            <li><a href="/services.html#sell-or-list">Sell or list a project</a></li>
          </ul>''', f, count=1, flags=re.S)
    f=f.replace('<li>Pune, Maharashtra, India</li>','<li>Global · HQ Pune, India</li>')
    return f
def tail(): return f'''
  <script src="/script.js?{VER}" defer></script>
</body>
</html>
'''

# ------------------------------------------------------------------ content
SERVICES=[
 dict(slug='investment-advisory', n='01', title='Investment advisory', short='Where to put your money and why — matched to your horizon, purpose and appetite for risk.',
   icon='<path d="M3 17l5-5 4 4 8-8"/><path d="M14 8h6v6"/>',
   hero='Where to put your money, and why.',
   lead='Residential, commercial, plots or pre‑launch — every asset class behaves differently. We help you decide which one fits your goals, timeline and appetite for risk, and then find the specific property that proves it.',
   who=['First‑time investors who want a clear, defensible plan', 'Families building a property portfolio over years', 'Business owners parking capital in real assets', 'Anyone who has been pitched a project and wants an independent second opinion'],
   included=['A written investment brief: purpose, budget, horizon, target yield and appreciation', 'Asset‑class recommendation with the reasoning, not just the answer', 'A shortlist of specific properties that fit — with site visits arranged', 'Full document verification and a price & return estimate on the one you choose', 'Negotiation, closure and handover managed end to end'],
   gets=['A written investment brief','A matched shortlist & site visits','A document verification report','A price & return estimate','A closed deal, registered & handed over'],
   wa='Hi%20Kuber%20Estate%2C%20I%27d%20like%20advice%20on%20a%20property%20investment.'),
 dict(slug='overseas-investors', n='02', title='Overseas &amp; NRI investors', short='Invest across borders. We do the ground work; you decide.',
   icon='<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 010 18M12 3a14 14 0 000 18"/>',
   hero='Invest across borders, with someone on the ground.',
   lead='Distance is the biggest risk in real estate — you can\'t walk the site, read the file or sit across the table. We do exactly that on your behalf, whether you\'re investing into India from abroad or from India into an international market: verification, valuation, negotiation and registration, with everything documented in KuberCRM so you see what we see.',
   who=['NRIs and OCI holders buying a home or an investment in India', 'International investors looking at Indian cities — and Indian investors looking abroad', 'Families managing property in India from abroad', 'Anyone who needs a trusted pair of eyes on the ground'],
   included=['Requirement brief built over video calls in your time zone', 'Shortlist with walk‑through videos and site‑visit reports', 'Title, RERA, approvals, encumbrances and dues verified — the report is yours', 'Guidance on FEMA/RBI rules, repatriation and power of attorney (with your legal advisor)', 'Negotiation, agreement, registration and possession handled on the ground; every document uploaded to KuberCRM'],
   gets=['A written requirement brief','A shortlist with video walk‑throughs','A document verification report','A price & return estimate','A closed deal, registered — documents in your CRM'],
   wa='Hi%20Kuber%20Estate%2C%20I%27m%20based%20abroad%20and%20want%20to%20invest%20in%20property%20in%20India.'),
 dict(slug='buying-your-home', n='03', title='Buying your home', short='End‑to‑end representation for a home you\'ll live in — shortlist to keys.',
   icon='<path d="M3 21h18"/><path d="M5 21V8l7-5 7 5v13"/><path d="M9 21v-6h6v6"/>',
   hero='The home you\'ll live in, bought properly.',
   lead='A home is the largest cheque most people ever write, and it\'s usually written under pressure. We slow the process down where it matters — the paperwork and the price — and speed it up everywhere else.',
   who=['First‑time buyers who want someone on their side of the table', 'Families upgrading and juggling a sale and a purchase', 'Buyers relocating to a new city — or a new country — who don\'t know the micro‑markets', 'Anyone who wants the papers checked before the token, not after'],
   included=['Requirement brief: areas, size, budget, timeline, must‑haves', 'Curated shortlist and accompanied site visits', 'Verification of title, RERA, approvals and dues before you pay anything', 'Fair‑value estimate and negotiation on your behalf', 'Agreement, loan coordination, registration and possession'],
   gets=['A written requirement brief','A matched shortlist & site visits','A document verification report','A fair‑value estimate','Keys in your hand — registered'],
   wa='Hi%20Kuber%20Estate%2C%20I%27m%20looking%20to%20buy%20a%20home.'),
 dict(slug='commercial-retail', n='04', title='Commercial &amp; retail', short='Offices and high‑street units evaluated on yield, tenant demand and exit.',
   icon='<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M8 7h2M14 7h2M8 11h2M14 11h2M8 15h2M14 15h2M10 21v-3h4v3"/>',
   hero='Commercial property, judged on the numbers.',
   lead='Offices, retail units and high‑street shops in business corridors — in India and abroad — bought for the rent they will earn and the price they will fetch, not for the brochure.',
   who=['Investors targeting rental yield rather than appreciation', 'Businesses buying their own premises', 'Professionals and clinics looking for the right frontage', 'Portfolio investors diversifying out of residential'],
   included=['Micro‑market study: tenant demand, vacancy, rents achieved', 'Shortlist with realistic yield and exit assumptions', 'Verification of title, approvals, occupancy certificate and society dues', 'Lease and tenant assessment where the unit is pre‑leased', 'Negotiation, documentation and registration'],
   gets=['A written investment brief','A shortlist with yield assumptions','A document verification report','A yield & exit estimate','A closed deal, registered'],
   wa='Hi%20Kuber%20Estate%2C%20I%27m%20interested%20in%20commercial%20or%20retail%20property.'),
 dict(slug='plots-land', n='05', title='Plots &amp; land', short='NA plots and land parcels with title, zoning and access verified.',
   icon='<path d="M3 6l6-2 6 2 6-2v14l-6 2-6-2-6 2z"/><path d="M9 4v14M15 6v14"/>',
   hero='Land is where the paperwork matters most.',
   lead='Plots carry the highest upside and the highest documentation risk in real estate. Title chains, zoning, NA status, access roads and boundaries — we check all of it before you commit a rupee.',
   who=['Investors buying for long‑term appreciation', 'Families buying a plot to build on', 'Buyers in growth corridors — around Indian cities and in international markets', 'Anyone who has been offered "a great deal" on land'],
   included=['Title chain and 7/12 extract verification', 'NA order, zoning, reservations and development plan check', 'Physical survey: boundaries, access, encroachments', 'Fair‑value estimate against recent transactions', 'Agreement, registration and mutation'],
   gets=['A written requirement brief','A shortlist of verified parcels','A title & zoning verification report','A fair‑value estimate','A registered plot, mutation done'],
   wa='Hi%20Kuber%20Estate%2C%20I%27m%20interested%20in%20plots%20or%20land.'),
 dict(slug='sell-or-list', n='06', title='Selling or listing a project', short='We evaluate it, verify it and place it with the buyers who need it.',
   icon='<circle cx="8" cy="8" r="3"/><circle cx="16" cy="16" r="3"/><path d="M11 8h5a2 2 0 012 2v1"/><path d="M13 16H8a2 2 0 01-2-2v-1"/>',
   hero='The right buyer for your property.',
   lead='Own a property, or developing a project? We take on select listings, verify them to our own standard, and bring them to clients who are actually looking for what you have — in India and abroad.',
   who=['Owners selling a home, office or plot', 'Developers with inventory in a specific project', 'NRIs selling property in India from overseas', 'Landowners exploring a sale or a joint development'],
   included=['Honest valuation and a pricing strategy', 'Document check so the listing survives a buyer\'s diligence', 'Placement with matched buyers from our own requirement pipeline', 'Negotiation and buyer qualification', 'Agreement, registration and handover'],
   gets=['A valuation & pricing brief','Matched buyers from our pipeline','A clean, verified listing file','A negotiated offer','A closed sale, registered'],
   wa='Hi%20Kuber%20Estate%2C%20I%20have%20a%20property%20%2F%20project%20I%27d%20like%20to%20sell%20or%20list.'),
 dict(slug='kubercrm', n='07', title='KuberCRM', short='The real estate CRM we built to run our own firm.', product=True,
   icon='<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
   hero='Consulting, powered by our own software.',
   lead='KuberCRM is the real estate CRM we built to run Kuber Estate — every enquiry, property, document and follow‑up in one place. It\'s why nothing falls through the cracks, and why we can tell you exactly where your deal stands, any day, from anywhere.',
   who=['Our own clients — every engagement runs on it', 'Brokerages and consultancies that want the same discipline', 'Developers tracking enquiries across projects', 'Teams tired of deals living in WhatsApp chats'],
   included=['Requirement tracking — captured once, matched against every new project', 'Property and document vault — title, approvals, verification reports per property', 'Deal pipeline — shortlist → visit → verify → negotiate → close', 'Client view — your clients see the same stages you do', 'Follow‑ups and reminders so nothing slips'],
   gets=['Requirements captured & matched','Shortlists shared with clients','Documents stored & verified per property','Estimates attached to the deal','Closure tracked to handover'],
   wa='Hi%20Kuber%20Estate%2C%20I%27d%20like%20to%20know%20more%20about%20KuberCRM.'),
]
STEPS=[('Understand','A conversation about your goals, budget, timeline, preferred areas and what "right" looks like for you.'),
       ('Shortlist','We match the brief against the market and our own criteria, then arrange site visits — only for properties worth your time.'),
       ('Verify','Title, RERA registration, sanctioned plans and approvals, encumbrances, government records, dues and litigation — checked before any money moves.'),
       ('Evaluate','Fair price against comparable deals, expected yield, appreciation outlook and the risks — assessed purely in your interest. If it doesn\'t hold up, we say so.'),
       ('Finalise','We negotiate on your side, then manage the agreement, payment schedule, registration and possession — one point of contact until it\'s done.')]

def keystone_static():
    cx,cy,Ro,ri=100,96,66,44; n=9; parts=[]
    for i in range(n):
        a0=math.pi-i*math.pi/n; a1=math.pi-(i+1)*math.pi/n
        p=lambda rad,a:(cx+rad*math.cos(a), cy-rad*math.sin(a))
        x0,y0=p(Ro,a0); x1,y1=p(Ro,a1); x2,y2=p(ri,a1); x3,y3=p(ri,a0)
        d=f'M{x0:.1f} {y0:.1f}A{Ro} {Ro} 0 0 1 {x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}A{ri} {ri} 0 0 0 {x3:.1f} {y3:.1f}Z'
        if i==n//2:
            key=(f'<g transform="translate(100 14) scale(1.9) translate(-100 -40)"><path d="{d}" fill="currentColor"/>'
                 f'<g transform="translate(100 44) scale(.42) translate(-50 -52)"><g fill="none" stroke="var(--ksbg,#000)" stroke-width="5" stroke-linejoin="miter"><path d="M42.5 38.5v27"/><path d="M42.5 40.5h7.5a6.5 6.5 0 0 1 0 13h-7.5"/><path d="M49 53.5l9 11.5"/></g></g></g>')
        else: parts.append(f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="1.2" opacity=".45"/>')
    return f'<svg class="ks-static" viewBox="0 -40 200 170" aria-hidden="true"><path d="M12 22H188M12 28H188" fill="none" stroke="currentColor" stroke-width="1.4" opacity=".45"/><path d="M{cx-Ro} {cy}V118M{cx+Ro} {cy}V118M{cx-ri} {cy}V118M{cx+ri} {cy}V118" fill="none" stroke="currentColor" stroke-width="1.2" opacity=".45"/><path d="M6 118H194" stroke="currentColor" stroke-width="1" opacity=".3"/>{"".join(parts)}{key}</svg>'

# ------------------------------------------------------------------ what we offer (main page tiles)
SVC=[s for s in SERVICES if not s.get('product')]
PRODUCT=[s for s in SERVICES if s.get('product')][0]
def icon(svg, cls='mini__icon'): return f'<span class="{cls}"><svg viewBox="0 0 24 24">{svg}</svg></span>'
def offer_tiles():
    minis=''.join(f'<a class="mini" href="/services.html#{s["slug"]}">{icon(s["icon"])}<span>{s["title"]}</span></a>' for s in SVC)
    prod=f'<a class="mini" href="/products/kubercrm.html">{icon(PRODUCT["icon"])}<span>KuberCRM — real estate CRM</span></a>'
    return f'''        <div class="tiles">
          <div class="tile2 tile2--inv">
            <div class="tile2__head">
              <span class="tile2__icon"><svg viewBox="0 0 24 24"><path d="M4 7h16v13H4zM9 7V4h6v3M4 12h16"/></svg></span>
              <div><span class="mono">Services</span><h3 class="h">Advisory, buying, selling.</h3></div>
            </div>
            <p>Six ways to work with us — for investors, home buyers, NRIs, owners and developers. Every engagement runs on the same five‑step process.</p>
            <div class="minis">{minis}</div>
            <a class="tile2__more" href="/services.html">All services &amp; the five steps <svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
          </div>
          <div class="tile2">
            <div class="tile2__head">
              <span class="tile2__icon"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg></span>
              <div><span class="mono">Products</span><h3 class="h">Software we built.</h3></div>
            </div>
            <p>The tools that run our own firm — now available to other brokerages, consultancies and developers.</p>
            <div class="minis">{prod}</div>
            <a class="tile2__more" href="/products/kubercrm.html">See the product <svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
          </div>
        </div>'''

# ------------------------------------------------------------------ services page (combined, starts with the five steps)
def build_services_page():
    GEN=['A written requirement brief','A matched shortlist & site visits','A document verification report','A price & return estimate','A closed deal, registered & handed over']
    secs=[]
    for i,s in enumerate(SVC):
        who=''.join(f'<li>{w}</li>' for w in s['who'])
        inc=''.join(f'<li><span class="mono">0{k+1}</span><span>{w}</span></li>' for k,w in enumerate(s['included']))
        gets=''.join(f'<li><span class="mono">0{k+1}</span><span>{g}</span></li>' for k,g in enumerate(s['gets']))
        cls=' svc--alt' if i%2 else ''
        secs.append(f'''    <section class="svc{cls}" id="{s['slug']}">
      <div class="wrap">
        <div class="svc__grid">
          <div class="svc__intro">
            <span class="mono panel__num">Service {s['n']}</span>
            {icon(s['icon'],'svc__icon')}
            <h2 class="display">{s['title']}</h2>
            <p class="sub-lg">{s['hero']}</p>
            <p class="sub">{s['lead']}</p>
            <div class="btn-row"><a class="btn btn--fill" href="{WAI(s['wa'])}" target="_blank" rel="noopener">Enquire on WhatsApp</a></div>
          </div>
          <div class="svc__detail">
            <div class="svc__box"><span class="tag">Who it's for</span><ul class="plain">{who}</ul></div>
            <div class="svc__box"><span class="tag">What's included</span><ol class="included">{inc}</ol></div>
            <div class="svc__box"><span class="tag tag--mist">What you get, step by step</span><ol class="gets">{gets}</ol></div>
          </div>
        </div>
      </div>
    </section>
''')
    jump=''.join(f'<a href="#{s["slug"]}">{icon(s["icon"])}<span>{s["title"]}</span></a>' for s in SVC)
    body=f'''
  <main class="page__main">
    <section class="page-hero">
      <div class="wrap">
        <span class="mono panel__num">02 · Services</span>
        <h1 class="display">Six ways to work with us. One way we work.</h1>
        <p class="sub-lg">Whatever you come to us for, the engagement runs through the same five steps — and each step ends with something concrete in your hands. The process first; the services below it.</p>
        <nav class="jump" aria-label="Services">{jump}</nav>
      </div>
    </section>

    <section class="panel panel--inv" id="process">
      <div class="wrap">
        <div class="panel__head"><span class="mono panel__num">The process</span><h2 class="display">Five steps. No shortcuts.</h2><p class="sub">The same sequence on every engagement — a first home, a commercial portfolio, a plot, a sale. Tracked in <a href="/products/kubercrm.html">KuberCRM</a>, so you always know where your deal stands.</p></div>
        <ol class="ptimeline">
{process_timeline(GEN)}
        </ol>
      </div>
    </section>

{''.join(secs)}
    <section class="panel">
      <div class="wrap">
        <div class="card card--lg cta-block">
          <span class="tag">Not sure which one?</span>
          <h2 class="display">Tell us what you're trying to do.</h2>
          <p class="sub">A first conversation costs nothing. We'll point you to the right service — or tell you honestly if we're not the right fit.</p>
          <div class="btn-row"><a class="btn btn--fill" href="{WAI('Hi%20Kuber%20Estate%2C%20I%27d%20like%20to%20discuss%20a%20property%20investment.')}" target="_blank" rel="noopener">Enquire on WhatsApp</a><a class="btn btn--ghost" href="/#contact">Use the form</a></div>
        </div>
      </div>
    </section>
  </main>

'''
    html=head('Services — Kuber Estate','Investment advisory, overseas & NRI investors, home buying, commercial & retail, plots & land, selling or listing — all on the same five-step process.','/services.html')+LD+nav('/#offer')+body+footer()+dock('offer')+tail()
    open('services.html','w',encoding='utf-8').write(html)

# ------------------------------------------------------------------ product page (KuberCRM, no five steps)
def build_product_page():
    s=PRODUCT
    feats=[('Requirement tracking','Every client\'s purpose, budget, areas and timeline captured once — and matched automatically against every new property that comes in.','<circle cx="12" cy="12" r="9"/><path d="M12 8v4l3 2"/>'),
           ('Property & document vault','Title, approvals, verification reports and photos stored per property. Nothing lost in a chat, nothing unchecked.','<path d="M9 3h6l4 4v14H5V3h4z"/><path d="M9 13l2 2 4-4"/>'),
           ('Deal pipeline','Shortlist → visit → verify → negotiate → close. Every deal on one board, every stage visible to the whole team.','<path d="M4 6h16M4 12h10M4 18h6"/>'),
           ('Client view','Clients see the same stages, documents and next steps you do — from anywhere in the world.','<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0116 0"/>'),
           ('Follow‑ups & reminders','Site visits, callbacks, payment schedules and registration dates — nudged before they slip.','<path d="M6 8a6 6 0 0112 0v5l2 3H4l2-3z"/><path d="M10 20a2 2 0 004 0"/>'),
           ('Reports','Enquiries by source, conversion by stage, time to close — the numbers a firm actually runs on.','<path d="M4 19V5M4 19h16"/><path d="M7 15l4-5 3 3 5-6"/>')]
    fgrid=''.join(f'<div class="feat">{icon(ic,"feat__icon")}<h3 class="h-sm">{t}</h3><p>{d}</p></div>' for t,d,ic in feats)
    who=''.join(f'<li>{w}</li>' for w in s['who'])
    body=f'''
  <main class="page__main">
    <section class="page-hero page-hero--inv prod-hero">
      <div class="wrap prod-hero__grid">
        <div>
          <span class="tag">Product</span>
          <h1 class="display" style="margin-top:20px">KuberCRM.</h1>
          <p class="sub-lg">{s['hero']}</p>
          <p class="sub">{s['lead']}</p>
          <div class="btn-row"><a class="btn btn--white" href="{WAI('Hi%20Kuber%20Estate%2C%20I%27d%20like%20a%20demo%20of%20KuberCRM.')}" target="_blank" rel="noopener">Request a demo</a><a class="btn btn--ghost-light" href="/#contact">Send an enquiry</a></div>
        </div>
        <div class="prod-hero__shot">
          <!-- PLACEHOLDER IMAGE: replace with a KuberCRM screenshot (assets/kubercrm.png) -->
          <div class="device"><img src="https://images.unsplash.com/photo-1551434678-e076c223a692?w=1200&q=75&auto=format&fit=crop" alt="KuberCRM in use" width="1200" height="900" loading="eager" decoding="async"></div>
        </div>
      </div>
    </section>

    <section class="panel panel--white">
      <div class="wrap">
        <div class="panel__head"><span class="mono panel__num">What it does</span><h2 class="display">Everything a deal needs, in one place.</h2></div>
        <div class="feats">{fgrid}</div>
      </div>
    </section>

    <section class="panel">
      <div class="wrap two">
        <div><span class="tag">Who it's for</span><ul class="plain">{who}</ul></div>
        <div>
          <span class="tag">Why we built it</span>
          <p class="sub" style="margin-top:24px">We couldn't find a CRM that thought the way a property consultancy works — requirement first, documents per property, one pipeline from shortlist to keys. So we built one, ran our own firm on it, and kept what survived real deals. That's KuberCRM.</p>
          <p class="sub">It's the reason our clients always know where their deal stands, and the reason nothing falls through the cracks between a site visit and a registration.</p>
        </div>
      </div>
    </section>

    <section class="panel panel--inv">
      <div class="wrap">
        <div class="cta-block">
          <span class="tag">Get started</span>
          <h2 class="display">See it on your own deals.</h2>
          <p class="sub">A 30‑minute walkthrough with your real pipeline. No slides.</p>
          <div class="btn-row"><a class="btn btn--white" href="{WAI('Hi%20Kuber%20Estate%2C%20I%27d%20like%20a%20demo%20of%20KuberCRM.')}" target="_blank" rel="noopener">Request a demo</a><a class="btn btn--ghost-light" href="{WAI(s['wa'])}" target="_blank" rel="noopener">Ask a question</a></div>
        </div>
      </div>
    </section>
  </main>

'''
    html=head('KuberCRM — real estate CRM by Kuber Estate','The real estate CRM Kuber Estate built to run its own firm: requirements, documents, deal pipeline, client view.','/products/kubercrm.html')+LD+nav('/#offer')+body+footer()+dock('offer')+tail()
    open('products/kubercrm.html','w',encoding='utf-8').write(html)

def offer_cards():
    out=[]
    for s in SERVICES:
        tag = '<span class="tag tag--mist">Product</span>' if s.get('product') else ''
        out.append(f'''          <a class="offer" href="/services/{s['slug']}.html">
            <div class="offer__top"><span class="offer__icon"><svg viewBox="0 0 24 24">{s['icon']}</svg></span><span class="mono smoke">{s['n']}</span></div>
            <h3 class="h-sm">{s['title']}</h3>
            <p>{s['short']}</p>
            <span class="offer__more">{tag}<span class="offer__arrow">Learn more <svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></span>
          </a>''')
    return '\n'.join(out)

def process_timeline(gets):
    out=[]
    for i,(t,d) in enumerate(STEPS):
        out.append(f'''        <li class="pstep">
          <div class="pstep__ig">{P[f'ig{i+1}']}</div>
          <div class="pstep__body">
            <span class="mono smoke">Step 0{i+1}</span>
            <h3 class="h-sm">{t}</h3>
            <p>{d}</p>
            <div class="pstep__out"><span class="mono">You get</span><strong>{gets[i]}</strong></div>
          </div>
        </li>''')
    return '\n'.join(out)

# ------------------------------------------------------------------ shared blocks
def hero_block():
    hero=P['hero']
    hero=hero.replace('Pune · Real estate investment consultants','Global real estate investment consultants · Born in Pune')
    hero=hero.replace('Kuber Estate is a Pune‑based real estate investment consultancy. We find the property that fits you, verify every paper, and negotiate the deal on your side.',
                      'Kuber Estate is a global real estate investment consultancy, born in Pune. We find the property that fits you — in India or anywhere in the world — verify every paper, and negotiate the deal on your side.')
    trust=P['trust']
    trust=trust.replace('<span class="mono">01 — Where</span><strong>Pune, Maharashtra</strong><span>Hinjewadi, Baner–Balewadi, Wakad, Kharadi, Wagholi, Talegaon–Chakan</span>',
                        '<span class="mono">01 — Where</span><strong>Global, born in Pune</strong><span>Clients and properties across India, the Gulf, the UK and beyond</span>')
    trust=trust.replace('<span class="mono">02 — Who for</span><strong>Investors &amp; home buyers</strong><span>First homes to portfolio plays — and owners &amp; developers on the other side</span>',
                        '<span class="mono">02 — Who for</span><strong>Investors &amp; home buyers</strong><span>Indian residents, NRIs and international investors — and owners &amp; developers on the other side</span>')
    trust=trust.replace('<span>Ready, under‑construction and pre‑launch</span>','<span>Ready, under‑construction and pre‑launch — in India and international markets</span>')
    return hero, trust

def know_more(href, label='Know more'):
    return f'<a class="btn btn--fill know" href="{href}">{label} <svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>'

ABOUT_INTRO = """            <span class="tag">The keystone</span>
            <h3 class="display" style="margin-top:20px">That stone is us.</h3>
            <p class="sub">Every arch stands because of one stone — the wedge at the top that locks all the others in place. In a property deal, that's the verification and the judgement that make everything else hold. That's what we do, and it's why our mark is a keystone with an R cut into it.</p>
            <p class="sub">Kuber Estate is a global firm that was born in Pune. We work with investors and properties across India and international markets, and we're independent — engaged to get you the right property, not to move inventory — and every step of every deal is documented in KuberCRM, the software we built to run our own firm.</p>"""

def about_block(with_button=True):
    btn = ('<div class="btn-row" style="margin-top:32px">' + know_more('/about.html') + '</div>') if with_button else ''
    return f"""        <div class="about">
          <div class="about__art">{keystone_static()}</div>
          <div class="about__copy">
{ABOUT_INTRO}
            {btn}
          </div>
        </div>"""

def props_grid(limit=None):
    g=P['properties']
    tiles=re.findall(r'<article class="card tile">.*?</article>', g, re.S)
    if limit: tiles=tiles[:limit]
    arrow_l='<svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg>'
    arrow_r='<svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg>'
    return ('        <div class="carousel" data-carousel>\n'
            '          <div class="carousel__bar"><span class="mono carousel__count" data-count>01 / %02d</span>'
            '<div class="carousel__nav"><button type="button" class="carousel__btn" data-prev aria-label="Previous property">%s</button>'
            '<button type="button" class="carousel__btn" data-next aria-label="Next property">%s</button></div></div>\n'
            '          <div class="properties" data-track>\n' % (len(tiles), arrow_l, arrow_r)
            + '\n'.join(tiles) + '\n          </div>\n        </div>')

OWNERS_ROW = f"""        <div class="card owners-row">
          <div><span class="tag">For owners &amp; developers</span><h3 class="h-sm" style="margin-top:12px">Have a property or a project? We'll find the right buyer.</h3></div>
          <div class="btn-row"><a class="btn btn--fill" href="/services.html#sell-or-list">How it works</a><a class="btn btn--ghost" href="{WAI('Hi%20Kuber%20Estate%2C%20I%20have%20a%20project%20%2F%20property%20I%27d%20like%20you%20to%20evaluate%20and%20find%20investors%20for.')}" target="_blank" rel="noopener">WhatsApp us</a></div>
        </div>"""

# ------------------------------------------------------------------ index
def build_index():
    hero,trust=hero_block()
    contact=P['contact'].replace('<li><span class="mono">Location</span><span class="val">Pune, Maharashtra</span></li>','<li><span class="mono">Location</span><span class="val">Global · headquartered in Pune, India</span></li>')
    body=f"""
  <main id="top">

    <!-- 01 HOME -->
    <section class="panel panel--home" id="home">
      <div class="wrap">
        <div class="hero">
{hero}      </div>
{trust}    </section>

    <!-- 02 WHAT WE OFFER -->
    <section class="panel panel--white" id="offer">
      <div class="wrap">
        <div class="panel__head">
          <span class="mono panel__num">02</span>
          <h2 class="display">What we offer.</h2>
          <p class="sub">Services for people buying, investing and selling — and the software we built to run them. Tap any item to go straight to its details.</p>
        </div>
{offer_tiles()}
      </div>
    </section>

    <!-- 03 PROPERTIES -->
    <section class="panel" id="properties">
      <div class="wrap explain">
        <div class="panel__head">
          <span class="mono panel__num">03</span>
          <h2 class="display">Properties we offer.</h2>
        </div>
        <div class="explain__text explain__text--wide">
          <p class="sub-lg">Shreepal Green City — our first listed project.</p>
          <p>A gated plotted township at Malegaon Khurd, Baramati (Pune district): cemented 20 and 30 ft roads, underground water, sewage and wiring, a garden and an open gym. Buy an open plot from ₹18 lakh, or a built‑to‑order 2 BHK (₹32 lakh) or 3 BHK (₹41.6 lakh) — plot and construction included. Verified to our own standard before we listed it.</p>
        </div>
{offer_tiles_carousel()}
        <div class="btn-row" style="margin-top:32px">{know_more('/properties.html','See the project')}<a class="btn btn--ghost" href="#contact">Tell us your requirement</a></div>
      </div>
    </section>

    <!-- 04 ABOUT -->
    <section class="panel panel--inv" id="about">
      <div class="wrap">
        <div class="panel__head">
          <span class="mono panel__num">04</span>
          <h2 class="display">About us.</h2>
        </div>
{about_block(True)}
      </div>
    </section>

    <!-- 05 CONTACT -->
    <section class="panel" id="contact">
      <div class="wrap">
        <div class="panel__head">
          <span class="mono panel__num">05</span>
          <h2 class="display">Contact us.</h2>
        </div>
{contact}
      </div>
    </section>

  </main>

"""
    html=head('Kuber Estate — Global Real Estate Investment Consultants','Kuber Estate is a global real estate investment consultancy born in Pune. We shortlist verified properties in India and international markets, check every document, evaluate returns and close the deal — on your side.','/')+LD+nav()+body+footer()+dock('home')+tail()
    html=html.replace('src="assets/','src="/assets/').replace('poster="assets/','poster="/assets/').replace('href="assets/','href="/assets/')
    open('index.html','w',encoding='utf-8').write(html)

# ------------------------------------------------------------------ overview pages
# ------------------------------------------------------------------ project: Shreepal Green City
PROJECT=dict(
  name='Shreepal Green City', slug='shreepal-green-city',
  place='Malegaon Khurd, Baramati · Pune district, Maharashtra 413115',
  map='https://maps.app.goo.gl/Z6JB9nNkFTmxgm1y5',
  embed='https://www.google.com/maps?q=Shrilal+green+city,+Malegaon+Khurd,+Malegaon+Bk,+Maharashtra+413115&output=embed',
  lead='A gated plotted township with ready‑to‑build plots and built‑to‑order 2 and 3 BHK homes — cemented roads, underground services, a garden and an open gym. Our first listed project, verified to our own standard.',
  plan='assets/shreepal-plan.jpg',
)
OFFERS=[
 dict(key='2bhk', tag='Home · Built to order', title='2 BHK home', area='1,000 sq ft', price='₹32 lakh', breakdown=[('Plot (1,000 sq ft)','₹18 lakh'),('Construction','₹14 lakh')], note='All‑inclusive: plot + construction.',
   icon='<path d="M3 21h18"/><path d="M5 21V8l7-5 7 5v13"/><path d="M9 21v-6h6v6"/>', wa='Hi%20Kuber%20Estate%2C%20I%27m%20interested%20in%20a%202%20BHK%20at%20Shreepal%20Green%20City.'),
 dict(key='3bhk', tag='Home · Built to order', title='3 BHK home', area='1,300 sq ft', price='₹41.6 lakh', breakdown=[('Plot (1,300 sq ft)','₹23.4 lakh'),('Construction','₹18.2 lakh')], note='Same per‑sq‑ft basis as the 2 BHK.',
   icon='<path d="M3 21h18"/><path d="M4 21V9l8-6 8 6v12"/><path d="M8 21v-7h8v7M12 14v7"/>', wa='Hi%20Kuber%20Estate%2C%20I%27m%20interested%20in%20a%203%20BHK%20at%20Shreepal%20Green%20City.'),
 dict(key='plot', tag='Open plot · Build later', title='Open plots', area='from 1,000 sq ft', price='from ₹18 lakh', breakdown=[('Rate','₹1,800 per sq ft'),('1,000 sq ft plot','₹18 lakh')], note='Larger plots priced pro‑rata. Coloured plots on the plan are sold; uncoloured are available.',
   icon='<path d="M3 6l6-2 6 2 6-2v14l-6 2-6-2-6 2z"/><path d="M9 4v14M15 6v14"/>', wa='Hi%20Kuber%20Estate%2C%20I%27m%20interested%20in%20an%20open%20plot%20at%20Shreepal%20Green%20City.'),
]
AMENITIES=[
 ('Gated society','<rect x="3" y="10" width="18" height="11" rx="2"/><path d="M7 10V7a5 5 0 0110 0v3"/>'),
 ('Garden','<path d="M12 22V12"/><path d="M12 12c-5 0-8-3-8-8 5 0 8 3 8 8zM12 12c5 0 8-3 8-8-5 0-8 3-8 8z"/>'),
 ('Open gym','<path d="M6 8v8M18 8v8M3 10v4M21 10v4M6 12h12"/>'),
 ('20 & 30 ft cemented roads','<path d="M4 20L9 4h6l5 16"/><path d="M12 8v2M12 13v2M12 18v2"/>'),
 ('Underground water supply','<path d="M12 3s6 6 6 11a6 6 0 01-12 0c0-5 6-11 6-11z"/><path d="M4 21h16"/>'),
 ('Underground sewage','<path d="M4 6h10a4 4 0 014 4v10"/><path d="M4 12h6"/><path d="M2 20h20"/>'),
 ('Underground wiring','<path d="M13 2L5 13h6l-1 9 8-11h-6z"/><path d="M2 22h20"/>'),
]
# ------------------------------------------------------------------ amenities, explained (with infographics)
A='fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
MONO='font-family="JetBrains Mono, ui-monospace, monospace" font-size="9" letter-spacing=".04em" fill="#000" stroke="none"'
def lbl(x,y,t,anchor='middle',fill='#000'):
    attrs=MONO.replace('fill="#000"', 'fill="%s"' % fill)
    return '<text x="%s" y="%s" text-anchor="%s" %s>%s</text>' % (x,y,anchor,attrs,t)
def soil(y=110, x0=10, x1=310):
    # ground line + hatch marks that read as "underground"
    ticks=''.join(f'<path d="M{x} {y+6}l-6 8"/>' for x in range(x0+8, x1, 18))
    return f'<g class="ig-row" style="--d:0s"><path d="M{x0} {y}h{x1-x0}" stroke-width="2.5"/><g opacity=".35">{ticks}</g></g>'
def ig_gate():
    return f'''<svg class="ig" viewBox="0 0 320 180"><g {A}>
<g class="ig-row" style="--d:0s"><path d="M8 150h304" stroke-width="2.5"/></g>
<g class="ig-row" style="--d:.1s"><path d="M8 118h60v32M252 118h60v32"/><path d="M20 118v32M32 118v32M44 118v32M276 118v32M288 118v32M300 118v32" opacity=".5"/></g>
<g class="ig-row" style="--d:.25s"><rect x="68" y="70" width="26" height="80" rx="4" class="ig-chip"/><rect x="226" y="70" width="26" height="80" rx="4" class="ig-chip"/><path d="M94 70h132" stroke-width="4"/><path d="M94 84h132" opacity=".5"/></g>
<g class="ig-pop" style="--d:.45s"><rect x="100" y="34" width="120" height="26" rx="13" class="ig-mint" stroke="#000" stroke-width="2"/>{lbl(160,51,'SHREEPAL GREEN CITY')}</g>
<g class="ig-row" style="--d:.55s"><path d="M108 150V96h18v54M122 96h18v54"/><path d="M108 118h50"/><path d="M108 132h50" opacity=".6"/><path d="M162 150V96h18v54M176 96h18v54"/><path d="M162 118h50"/><path d="M162 132h50" opacity=".6"/></g>
<g class="ig-pop" style="--d:.7s"><rect x="254" y="100" width="42" height="50" rx="4" class="ig-chip"/><rect x="262" y="110" width="12" height="12" rx="2" class="ig-mint"/><path d="M275 150v-14h12v14"/>{lbl(275,168,'CABIN')}</g>
<g class="ig-pop" style="--d:.85s"><circle cx="272" cy="30" r="12" class="ig-mint" stroke="#000" stroke-width="2"/><path d="M272 23v7l5 3" stroke="#000"/>{lbl(272,52,'24 / 7','middle','#595959')}</g>
</g></svg>'''
def ig_garden():
    return f'''<svg class="ig" viewBox="0 0 320 180"><g {A}>
<g class="ig-row" style="--d:0s"><path d="M8 150c40-18 80-18 120 0s80 18 120 0" stroke-width="2.5"/><path d="M8 150h304" opacity=".3"/></g>
<g class="ig-row" style="--d:.1s"><path d="M30 92c-10 22 4 40 24 40s34-18 24-40c-8-16-40-16-48 0z" class="ig-mint"/><path d="M54 132v18"/></g>
<g class="ig-row" style="--d:.25s"><path d="M120 150V70"/><path d="M120 72c-18 0-30-12-30-30 18 0 30 12 30 30zM120 72c18 0 30-12 30-30-18 0-30 12-30 30z" class="ig-mint"/></g>
<g class="ig-row" style="--d:.4s"><circle cx="230" cy="76" r="30" class="ig-mint"/><circle cx="212" cy="96" r="18" class="ig-mint"/><path d="M230 106v44"/></g>
<g class="ig-pop" style="--d:.55s"><rect x="160" y="122" width="44" height="6" rx="3" fill="#000"/><path d="M164 128v16M200 128v16M164 116h36" /><rect x="160" y="110" width="44" height="6" rx="3" fill="#000"/>{lbl(182,164,'BENCH','middle','#595959')}</g>
<g class="ig-row" style="--d:.7s"><path d="M270 150c4-10 8-10 12 0M286 150c4-8 8-8 12 0M300 148c3-6 6-6 9 0"/><path d="M268 122l4-6 4 6M284 118l4-6 4 6"/></g>
<g class="ig-pop" style="--d:.85s"><circle cx="286" cy="30" r="14" class="ig-mint"/><path d="M286 8v6M286 46v6M264 30h6M302 30h6M270 14l4 4M298 42l4 4M302 14l-4 4M274 42l-4 4"/></g>
</g></svg>'''
def ig_gym():
    return f'''<svg class="ig" viewBox="0 0 320 180"><g {A}>
<g class="ig-row" style="--d:0s"><path d="M8 150h304" stroke-width="2.5"/><path d="M40 150v6M120 150v6M200 150v6M280 150v6" opacity=".4"/></g>
<g class="ig-row" style="--d:.15s"><path d="M40 150V60M84 150V60"/><path d="M36 60h52" stroke-width="4"/>{lbl(62,168,'PULL-UP','middle','#595959')}</g>
<g class="ig-pop" style="--d:.35s"><circle cx="62" cy="78" r="8" class="ig-chip"/><path d="M62 86v28M62 96l-14 10M62 96l14 10M62 114l-10 20M62 114l10 20"/><path d="M50 66l-6-6M74 66l6-6"/></g>
<g class="ig-row" style="--d:.45s"><path d="M130 150V94h40l14 18"/><path d="M130 122h40"/><circle cx="196" cy="100" r="8" class="ig-chip"/><path d="M196 108v42"/><path d="M150 94V70"/><rect x="138" y="58" width="24" height="12" rx="6" class="ig-mint"/>{lbl(165,168,'CYCLE','middle','#595959')}</g>
<g class="ig-row" style="--d:.6s"><path d="M228 150V96h60v54"/><path d="M228 112h60M228 128h60" opacity=".6"/><path d="M258 96V76"/><rect x="236" y="62" width="44" height="14" rx="7" class="ig-mint"/><rect x="228" y="58" width="8" height="22" rx="2" fill="#000"/><rect x="280" y="58" width="8" height="22" rx="2" fill="#000"/>{lbl(258,168,'PRESS','middle','#595959')}</g>
<g class="ig-pop" style="--d:.8s"><rect x="104" y="16" width="112" height="24" rx="12" class="ig-mint" stroke="#000" stroke-width="2"/>{lbl(160,32,'FREE · OPEN AIR')}</g>
</g></svg>'''
def ig_roads():
    return f'''<svg class="ig" viewBox="0 0 320 180"><g {A}>
<g class="ig-row" style="--d:0s"><path d="M40 160L130 30h60l90 130z" fill="#f3f3f3"/><path d="M160 40v12M160 66v16M160 98v20M160 134v26" stroke-dasharray="6 6"/></g>
<g class="ig-row" style="--d:.2s"><rect x="18" y="60" width="44" height="30" rx="3" class="ig-chip"/><rect x="10" y="104" width="52" height="36" rx="3" class="ig-chip"/><rect x="258" y="60" width="44" height="30" rx="3" class="ig-chip"/><rect x="258" y="104" width="52" height="36" rx="3" class="ig-chip"/>{lbl(40,79,'PLOT')}{lbl(36,126,'PLOT')}{lbl(280,79,'PLOT')}{lbl(284,126,'PLOT')}</g>
<g class="ig-row" style="--d:.35s"><path d="M100 96h120" opacity=".5"/><path d="M96 92l4 4-4 4M224 92l-4 4 4 4"/></g>
<g class="ig-pop" style="--d:.5s"><rect x="126" y="80" width="68" height="22" rx="11" class="ig-mint" stroke="#000" stroke-width="2"/>{lbl(160,95,'30 FT MAIN')}</g>
<g class="ig-pop" style="--d:.65s"><rect x="8" y="150" width="76" height="22" rx="11" class="ig-mint" stroke="#000" stroke-width="2"/>{lbl(46,165,'20 FT CROSS')}<path d="M84 161h30" opacity=".6"/></g>
<g class="ig-pop" style="--d:.8s"><rect x="190" y="10" width="122" height="22" rx="11" class="ig-chip"/>{lbl(251,25,'CONCRETE · NOT TAR')}</g>
</g></svg>'''
def ig_water():
    return f'''<svg class="ig" viewBox="0 0 320 180"><g {A}>
{soil(104)}
<g class="ig-row" style="--d:.15s"><path d="M52 104V72h44v32M52 80l22-16 22 16M172 104V72h44v32M172 80l22-16 22 16"/><rect x="68" y="88" width="12" height="16" fill="#000"/><rect x="188" y="88" width="12" height="16" fill="#000"/></g>
<g class="ig-row" style="--d:.3s"><path d="M8 134h304" stroke-width="8" opacity=".9"/><path d="M8 134h304" stroke="#d1ffca" stroke-width="4"/><path d="M74 134v-24M194 134v-24" stroke-width="4"/><path d="M74 134v-24M194 134v-24" stroke="#d1ffca" stroke-width="2"/></g>
<g class="ig-row" style="--d:.5s"><path d="M30 134l6-3 6 3M130 134l6-3 6 3M240 134l6-3 6 3" stroke="#000" stroke-width="1.5"/>{lbl(160,160,'UNDERGROUND MAIN · EVERY PLOT CONNECTED','middle','#595959')}</g>
<g class="ig-pop" style="--d:.7s"><path d="M270 18s16 18 16 30a16 16 0 01-32 0c0-12 16-30 16-30z" class="ig-mint" stroke="#000" stroke-width="2"/></g>
<g class="ig-pop" style="--d:.85s"><rect x="8" y="14" width="140" height="22" rx="11" class="ig-chip"/>{lbl(78,29,'NO TANKERS · NO PIPES')}</g>
</g></svg>'''
def ig_sewage():
    return f'''<svg class="ig" viewBox="0 0 320 180"><g {A}>
{soil(100)}
<g class="ig-row" style="--d:.15s"><path d="M40 100V68h40v32M40 76l20-14 20 14M140 100V68h40v32M140 76l20-14 20 14M240 100V68h40v32M240 76l20-14 20 14"/></g>
<g class="ig-row" style="--d:.3s"><path d="M60 100v22M160 100v22M260 100v22" stroke-width="3"/><path d="M20 130h280" stroke-width="8"/><path d="M296 126l10 4-10 4" stroke="#fff" stroke-width="2"/></g>
<g class="ig-pop" style="--d:.5s"><rect x="50" y="118" width="20" height="20" rx="3" class="ig-mint" stroke="#000" stroke-width="2"/><rect x="150" y="118" width="20" height="20" rx="3" class="ig-mint" stroke="#000" stroke-width="2"/><rect x="250" y="118" width="20" height="20" rx="3" class="ig-mint" stroke="#000" stroke-width="2"/>{lbl(160,160,'INSPECTION CHAMBER AT EVERY PLOT','middle','#595959')}</g>
<g class="ig-pop" style="--d:.7s"><rect x="204" y="14" width="108" height="22" rx="11" class="ig-chip"/>{lbl(258,29,'NO OPEN DRAINS')}</g>
</g></svg>'''
def ig_wiring():
    return f'''<svg class="ig" viewBox="0 0 320 180"><g {A}>
{soil(100)}
<g class="ig-row" style="--d:.15s"><path d="M64 100V66h40v34M64 74l20-14 20 14M200 100V66h40v34M200 74l20-14 20 14"/><rect x="92" y="80" width="10" height="12" rx="1" class="ig-mint" stroke="#000" stroke-width="1.5"/><rect x="228" y="80" width="10" height="12" rx="1" class="ig-mint" stroke="#000" stroke-width="1.5"/>{lbl(97,76,'METER','middle','#595959')}{lbl(233,76,'METER','middle','#595959')}</g>
<g class="ig-row" style="--d:.3s"><rect x="8" y="70" width="34" height="30" rx="3" class="ig-chip"/><path d="M14 80h22M14 88h14"/>{lbl(25,66,'FEEDER','middle','#595959')}</g>
<g class="ig-row" style="--d:.45s"><path d="M25 100v28h272" stroke-width="5"/><path d="M97 128v-36M233 128v-36" stroke-width="3"/></g>
<g class="ig-pop" style="--d:.65s"><path d="M168 108l-9 16h8l-3 14 10-16h-8z" class="ig-mint" stroke="#000" stroke-width="1.8"/></g>
<g class="ig-pop" style="--d:.8s"><g opacity=".9"><path d="M276 100V30M266 40h20" /><path d="M254 24l44 44" stroke="#000" stroke-width="4"/><path d="M298 24l-44 44" stroke="#000" stroke-width="4"/></g>{lbl(276,166,'NO POLES · NO OVERHEAD LINES','middle','#595959')}</g>
</g></svg>'''
AMEN=[
 dict(t='Gated society', s='One entry, one exit, a watchman\'s cabin and a boundary wall around the whole township.', why='Security is the first thing every buyer asks about — and the thing most plotted schemes leave until "later". Here it\'s built in from day one, so your plot is protected even before you build on it.', ig=ig_gate()),
 dict(t='Garden', s='A landscaped garden in the open space, with walking paths and seating.', why='A township with a garden becomes a neighbourhood, not a grid of plots. It\'s where evenings happen — and it holds resale value in a way an empty "open space" never does.', ig=ig_garden()),
 dict(t='Open gym', s='Outdoor fitness equipment in the amenity space, free to every resident.', why='A gym in the open space means you use it: no fees, no membership, thirty seconds from your door. For families, it\'s the difference between an amenity on paper and one in daily life.', ig=ig_gym()),
 dict(t='20 & 30 ft cemented roads', s='Concrete internal roads — 30 ft on the main spine, 20 ft on the cross roads — laid before plots are handed over.', why='The road is the township. Cement roads don\'t wash out in the monsoon, cost nothing to maintain, and let a truck reach your plot the day you start building. Tar or mud roads are where most small townships fail.', ig=ig_roads()),
 dict(t='Underground water supply', s='Piped water to every plot through underground lines, with individual connections.', why='No tankers, no overhead pipes running past your gate, no fights over supply. You connect on the day you build — and the street stays clean.', ig=ig_water()),
 dict(t='Underground sewage', s='A proper drainage network with underground sewer lines and inspection chambers for every plot.', why='Open drains are what make a colony smell in five years. Underground sewage is expensive to add later and impossible to retrofit well — which is why it matters that it\'s done now, before the first house.', ig=ig_sewage()),
 dict(t='Underground wiring', s='Electrical distribution through underground cables to a metered point at every plot.', why='No poles, no overhead lines, no outages every time the wind picks up. It\'s safer for children, it looks like a planned town rather than a village extension — and it keeps the skyline yours.', ig=ig_wiring()),
]
def amenities_block():
    rows=[]
    for i,a in enumerate(AMEN):
        rows.append(f'''          <article class="amenx{' amenx--alt' if i%2 else ''}">
            <div class="amenx__ig">{a['ig']}</div>
            <div class="amenx__body">
              <span class="mono">Amenity 0{i+1}</span>
              <h3 class="display amenx__title">{a['t']}</h3>
              <p class="amenx__what">{a['s']}</p>
              <p class="amenx__why"><strong>Why it matters.</strong> {a['why']}</p>
            </div>
          </article>''')
    return '        <div class="amenities">\n'+'\n'.join(rows)+'\n        </div>'
def offer_tiles_carousel():
    tiles=[]
    for o in OFFERS:
        rows=''.join(f'<div><span>{k}</span><strong>{v}</strong></div>' for k,v in o['breakdown'])
        tiles.append(f'''          <article class="card tile tile--offer">
            <div class="tile__img tile__ico"><svg viewBox="0 0 24 24">{o['icon']}</svg><span class="mono">{o['area']}</span></div>
            <div class="tile__body">
              <div class="tile__tags"><span class="tag">{PROJECT['name']}</span><span class="tag tag--mist">{o['tag']}</span></div>
              <h3 class="h-sm">{o['title']}</h3>
              <p class="tile__loc">{o['price']} · {PROJECT['place'].split(' ·')[0]}</p>
              <div class="tile__meta mono">{rows}</div>
              <a class="btn btn--fill btn--sm" href="properties.html#{o['key']}">View details</a>
            </div>
          </article>''')
    arrow_l='<svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg>'; arrow_r='<svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg>'
    return ('        <div class="carousel" data-carousel>\n'
            '          <div class="carousel__bar"><span class="mono carousel__count" data-count>01 / %02d</span>'
            '<div class="carousel__nav"><button type="button" class="carousel__btn" data-prev aria-label="Previous">%s</button>'
            '<button type="button" class="carousel__btn" data-next aria-label="Next">%s</button></div></div>\n'
            '          <div class="properties" data-track>\n' % (len(tiles), arrow_l, arrow_r) + '\n'.join(tiles) + '\n          </div>\n        </div>')

def build_properties():
    import os
    offers=''
    for o in OFFERS:
        rows=''.join(f'<li><span>{k}</span><strong>{v}</strong></li>' for k,v in o['breakdown'])
        offers+=f'''          <article class="offercard" id="{o['key']}">
            <div class="offercard__top"><span class="offer__icon"><svg viewBox="0 0 24 24">{o['icon']}</svg></span><span class="tag tag--mist">{o['tag']}</span></div>
            <h3 class="display offercard__title">{o['title']}</h3>
            <p class="mono">{o['area']}</p>
            <p class="offercard__price">{o['price']}</p>
            <ul class="offercard__rows">{rows}</ul>
            <p class="offercard__note">{o['note']}</p>
            <a class="btn btn--fill" href="{WAI(o['wa'])}" target="_blank" rel="noopener">Enquire on WhatsApp</a>
          </article>'''
    amen=''.join(f'<li><span class="amen__icon"><svg viewBox="0 0 24 24">{ic}</svg></span><span>{t}</span></li>' for t,ic in AMENITIES)
    has_plan=os.path.exists(PROJECT['plan'])
    plan_block = (f'''<figure class="plan"><img src="{PROJECT['plan']}" alt="Shreepal Green City layout plan" loading="lazy" decoding="async"><figcaption class="plan__legend"><span><i class="sw sw--sold"></i>Coloured plots — sold</span><span><i class="sw sw--free"></i>Uncoloured plots — available</span><span><i class="sw sw--green"></i>Open space &amp; amenities</span></figcaption></figure>'''
                  if has_plan else
                  '''<div class="plan plan--pending"><p class="sub">Layout plan — coming soon. Ask us on WhatsApp for the current availability map.</p></div>''')
    body=f'''
  <main class="page__main">
    <section class="page-hero">
      <div class="wrap">
        <span class="mono panel__num">03 · Project 01</span>
        <h1 class="display">{PROJECT['name']}.</h1>
        <p class="sub-lg">{PROJECT['lead']}</p>
        <p class="mono" style="margin-top:16px">{PROJECT['place']}</p>
        <div class="btn-row"><a class="btn btn--fill" href="{WAI('Hi%20Kuber%20Estate%2C%20I%27d%20like%20to%20know%20more%20about%20Shreepal%20Green%20City.')}" target="_blank" rel="noopener">Enquire on WhatsApp</a><a class="btn btn--ghost" href="{PROJECT['map']}" target="_blank" rel="noopener">Open in Google Maps</a></div>
      </div>
    </section>

    <section class="panel panel--inv" id="amenities">
      <div class="wrap">
        <div class="panel__head"><span class="mono panel__num">01 · Amenities — the reason to buy here</span><h2 class="display">The services are underground. The living is above.</h2><p class="sub">Most plotted schemes sell you a boundary line and a promise. Shreepal Green City is finished before you build: roads, water, drainage and power are already in the ground, and the garden, gym and gate are already there. Here is what each one is, and why it changes what your plot is worth.</p></div>
{amenities_block()}
      </div>
    </section>

    <section class="panel" id="offerings">
      <div class="wrap">
        <div class="panel__head"><span class="mono panel__num">02 · What's on offer</span><h2 class="display">Three ways to own here.</h2><p class="sub">Plot first, then build — or buy the plot alone and build when you're ready. Prices are all‑inclusive as shown; registration and taxes extra.</p></div>
        <div class="offercards">
{offers}
        </div>
      </div>
    </section>

    <section class="panel panel--white" id="plan">
      <div class="wrap">
        <div class="panel__head"><span class="mono panel__num">03 · Layout &amp; availability</span><h2 class="display">Pick your plot.</h2><p class="sub">Coloured plots are sold. Uncoloured plots are available — availability changes weekly, so confirm on WhatsApp before you decide.</p></div>
        {plan_block}
        <div class="btn-row" style="margin-top:24px"><a class="btn btn--fill" href="{WAI('Hi%20Kuber%20Estate%2C%20which%20plots%20are%20currently%20available%20at%20Shreepal%20Green%20City%3F')}" target="_blank" rel="noopener">Ask which plots are available</a></div>
      </div>
    </section>

    <section class="panel" id="location">
      <div class="wrap">
        <div class="panel__head"><span class="mono panel__num">04 · Location</span><h2 class="display">{PROJECT['place'].split(' ·')[0]}.</h2><p class="sub">{PROJECT['place']}</p></div>
        <div class="map"><iframe src="{PROJECT['embed']}" title="Shreepal Green City on Google Maps" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>
        <div class="btn-row" style="margin-top:16px"><a class="btn btn--ghost" href="{PROJECT['map']}" target="_blank" rel="noopener">Get directions</a></div>
      </div>
    </section>

    <section class="panel">
      <div class="wrap">
{OWNERS_ROW}
      </div>
    </section>
  </main>

'''
    html=head(f'{PROJECT["name"]} — Kuber Estate', 'Gated plotted township at Malegaon Khurd, Baramati: 2 BHK from ₹32 lakh, 3 BHK from ₹41.6 lakh, open plots from ₹18 lakh per 1,000 sq ft.', '/properties.html')+LD+nav('/#properties')+body+footer()+dock('properties')+tail()
    open('properties.html','w',encoding='utf-8').write(html)

# ------------------------------------------------------------------ team
S='fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
def ig_ceo():
    return f'''<svg class="ig" viewBox="0 0 200 120"><g {S}>
<path class="ig-dash" style="--d:.1s" d="M100 60L46 40M100 60l54-20M100 60L46 90M100 60l54 30"/>
<g class="ig-pop" style="--d:.25s"><rect x="30" y="26" width="32" height="26" rx="8" class="ig-chip"/><path d="M40 39h12M40 45h8"/></g>
<g class="ig-pop" style="--d:.35s"><rect x="138" y="26" width="32" height="26" rx="8" class="ig-chip"/><path d="M148 34l-4 5 4 5M160 34l4 5-4 5"/></g>
<g class="ig-pop" style="--d:.45s"><rect x="30" y="76" width="32" height="26" rx="8" class="ig-chip"/><path d="M36 95l6-8 5 4 9-9"/></g>
<g class="ig-pop" style="--d:.55s"><rect x="138" y="76" width="32" height="26" rx="8" class="ig-chip"/><circle cx="154" cy="86" r="4"/><path d="M146 100a8 8 0 0116 0"/></g>
</g><g class="ig-pop" style="--d:0s"><path d="M84 42h32l-6 32H90z" fill="#d1ffca" stroke="#000" stroke-width="2.5"/><g fill="none" stroke="#000" stroke-width="2.4"><path d="M96.5 51v13"/><path d="M96.5 52h4a3 3 0 010 6h-4"/><path d="M99.5 58l4.5 6"/></g></g></svg>'''
def ig_sourcing():
    return f'''<svg class="ig" viewBox="0 0 200 120"><g {S}>
<g class="ig-row" style="--d:0s"><rect x="20" y="20" width="22" height="30" rx="3"/><rect x="50" y="12" width="22" height="38" rx="3"/><rect x="80" y="26" width="22" height="24" rx="3"/><rect x="110" y="16" width="22" height="34" rx="3"/><rect x="140" y="22" width="22" height="28" rx="3"/><path d="M16 50h150"/></g>
<path class="ig-dash" style="--d:.3s" d="M100 58v14"/><path class="ig-row" style="--d:.4s" d="M93 66l7 7 7-7"/>
<g class="ig-pop" style="--d:.55s"><rect x="72" y="80" width="56" height="30" rx="8" class="ig-mint"/><rect x="88" y="86" width="8" height="18" fill="#000"/><rect x="100" y="90" width="8" height="14" fill="#000" opacity=".6"/><circle cx="118" cy="95" r="4" fill="#000"/></g>
</g></svg>'''
def ig_sales():
    return f'''<svg class="ig" viewBox="0 0 200 120"><g {S}>
<path d="M22 100h156M22 100V24"/>
<path class="ig-sign" style="--d:.1s" d="M30 88c20-4 34-10 48-24s28-30 48-38 30-8 42-8" stroke-dasharray="230" stroke-dashoffset="230"/>
<g class="ig-pop" style="--d:.7s"><circle cx="168" cy="18" r="7" class="ig-mint" stroke="#000" stroke-width="2"/></g>
<g class="ig-pop" style="--d:.4s"><circle cx="56" cy="74" r="6" class="ig-chip"/><path d="M46 92a10 10 0 0120 0"/></g>
<g class="ig-pop" style="--d:.55s"><circle cx="108" cy="52" r="6" class="ig-chip"/><path d="M98 70a10 10 0 0120 0"/></g>
</g></svg>'''
def ig_people():
    return f'''<svg class="ig" viewBox="0 0 200 120"><g {S}>
<path class="ig-dash" style="--d:.1s" d="M100 60L60 30M100 60l40-30M100 60L54 74M100 60l46 14M100 60v34"/>
<g class="ig-pop" style="--d:.2s"><circle cx="60" cy="24" r="8" class="ig-chip"/></g>
<g class="ig-pop" style="--d:.3s"><circle cx="140" cy="24" r="8" class="ig-chip"/></g>
<g class="ig-pop" style="--d:.4s"><circle cx="48" cy="78" r="8" class="ig-chip"/></g>
<g class="ig-pop" style="--d:.5s"><circle cx="152" cy="78" r="8" class="ig-chip"/></g>
<g class="ig-pop" style="--d:.6s"><circle cx="100" cy="100" r="8" class="ig-chip"/></g>
<g class="ig-pop" style="--d:0s"><circle cx="100" cy="58" r="16" class="ig-mint" stroke="#000" stroke-width="2"/><path d="M100 64c-6-4-8-8-4-11 2-1 4 0 4 2 0-2 2-3 4-2 4 3 2 7-4 11z" fill="#000" stroke="none"/></g>
</g></svg>'''
def ig_finance():
    return f'''<svg class="ig" viewBox="0 0 200 120"><g {S}>
<g class="ig-pop" style="--d:0s"><circle cx="62" cy="60" r="34"/><path d="M62 60V26A34 34 0 0196 60z" fill="#d1ffca"/><path d="M62 60l24 24"/></g>
<g class="ig-row" style="--d:.3s"><path d="M116 36h60M116 36v0"/><rect x="116" y="34" width="60" height="4" rx="2" class="ig-line"/></g>
<g class="ig-row" style="--d:.4s"><rect x="116" y="52" width="44" height="4" rx="2" class="ig-line"/></g>
<g class="ig-row" style="--d:.5s"><rect x="116" y="70" width="52" height="4" rx="2" class="ig-line"/></g>
<g class="ig-row" style="--d:.6s"><rect x="116" y="88" width="36" height="4" rx="2" class="ig-line"/><path d="M164 82l4 4 8-8"/></g>
</g></svg>'''
def ig_talent():
    return f'''<svg class="ig" viewBox="0 0 200 120"><g {S}>
<g class="ig-row" style="--d:0s"><circle cx="40" cy="40" r="8" class="ig-chip"/><path d="M28 60a12 12 0 0124 0"/></g>
<g class="ig-row" style="--d:.1s"><circle cx="84" cy="40" r="8" class="ig-chip"/><path d="M72 60a12 12 0 0124 0"/></g>
<g class="ig-row" style="--d:.2s"><circle cx="128" cy="40" r="8" class="ig-chip"/><path d="M116 60a12 12 0 0124 0"/></g>
<g class="ig-row" style="--d:.3s"><circle cx="172" cy="40" r="8" class="ig-chip"/><path d="M160 60a12 12 0 0124 0"/></g>
<g class="ig-pop" style="--d:.55s"><circle cx="128" cy="46" r="24" class="ig-mint" stroke="#000" stroke-width="2.5" fill-opacity=".85"/><path d="M146 64l18 18" stroke="#000" stroke-width="5"/><circle cx="128" cy="40" r="8" fill="#000"/><path d="M116 60a12 12 0 0124 0" stroke="#000" stroke-width="2.5"/></g>
<g class="ig-row" style="--d:.7s"><path d="M28 96h144" stroke-dasharray="4 5"/></g>
</g></svg>'''
TEAM=[
 dict(n='01', name='Aniket Vohra', init='AV', role='Co‑founder & CEO · Business and technology', founder=True, ig=ig_ceo(),
   desc='The brain of the organisation. Sets the direction, runs the business and leads the technology — including KuberCRM, which he built to run the firm and now offers to others.',
   focus=['Strategy','Business','Technology']),
 dict(n='02', name='Aniket Bhalerao', init='AB', role='Co‑founder & Managing Director · Project sourcing', founder=True, ig=ig_sourcing(),
   desc='Finds and secures the projects we take on — developer relationships, site assessment and the first honest call on whether a project deserves our clients\' money.',
   focus=['Developer relations','Site assessment','Project pipeline']),
 dict(n='03', name='Mukund Bansode', init='MB', role='Head of Sales · New investor acquisition', ig=ig_sales(),
   desc='Brings new investors into the firm and matches them to the right opportunity — the first conversation, and the honest one about fit.',
   focus=['Investor outreach','Requirement mapping','Deal matching']),
 dict(n='04', name='Nidhi Trivedi', init='NT', role='Co‑founder · Human Resources & investor management', founder=True, ig=ig_people(),
   desc='Looks after the people — the team inside and the investors outside: onboarding, communication, and making sure every client always knows where things stand.',
   focus=['People','Investor relations','Communication']),
 dict(n='05', name='Mansi More', init='MM', role='Head of Finance', ig=ig_finance(),
   desc='Runs the numbers: valuations, payment schedules, transaction accounting and the return estimates that go into every recommendation we make.',
   focus=['Valuations','Payment schedules','Reporting']),
 dict(n='06', name='Yuga Joshi', init='YJ', role='Talent Acquisition (TAG)', ig=ig_talent(),
   desc='Builds the team. Finds and brings in the people who can hold our standard — consultants, analysts and engineers — and helps them grow into it.',
   focus=['Hiring','Team growth','Culture']),
]
def team_grid():
    rows=[]
    for k,t in enumerate(TEAM):
        chips=''.join(f'<span class="tag tag--mist">{f}</span>' for f in t['focus'])
        founder = '<span class="tag tcard__founder">Founder</span>' if t.get('founder') else ''
        rows.append(f'''          <article class="tcard{' tcard--alt' if k%2 else ''}" id="team-{t['n']}">
            <div class="tcard__ig">{t['ig']}</div>
            <div class="tcard__body">
              <div class="tcard__meta"><span class="mono smoke">{t['n']} / 06</span>{founder}</div>
              <div class="tcard__head">
                <div class="tcard__avatar" aria-hidden="true">{t['init']}</div>
                <div><h3 class="display tcard__name">{t['name']}</h3><p class="tcard__role mono">{t['role']}</p></div>
              </div>
              <p class="sub">{t['desc']}</p>
              <div class="tcard__chips">{chips}</div>
            </div>
          </article>''')
    return '        <div class="team">\n'+'\n'.join(rows)+'\n        </div>'

# ------------------------------------------------------------------ about page (single)
def build_about():
    crm=P['crm'].replace('<a class="btn btn--ghost-light" href="#contact">Request a demo</a>','<a class="btn btn--ghost-light" href="/products/kubercrm.html">See the product page</a>')
    body=f"""
  <main class="page__main">
    <section class="page-hero page-hero--inv">
      <div class="wrap">
        <span class="mono panel__num">04 · About us</span>
{about_block(False)}
      </div>
    </section>

    <section class="panel" id="difference">
      <div class="wrap">
        <div class="panel__head"><span class="mono panel__num">4.1</span><h2 class="display">The difference.</h2><p class="sub">What working with us looks like, next to how property usually gets bought.</p></div>
{P['why']}
      </div>
    </section>

    <section class="panel panel--white" id="vision">
      <div class="wrap">
        <div class="panel__head"><span class="mono panel__num">4.2</span><h2 class="display">Why we exist.</h2></div>
{P['vision']}
      </div>
    </section>

    <section class="panel" id="founders">
      <div class="wrap">
        <div class="panel__head"><span class="mono panel__num">4.3</span><h2 class="display">The people behind Kuber Estate.</h2><p class="sub">Three founders and the team around them. Six people, one standard — every deal passes through more than one of them.</p></div>
{team_grid()}
      </div>
    </section>

    <section class="panel panel--inv" id="crm">
      <div class="wrap">
        <div class="panel__head"><span class="mono panel__num">4.4</span></div>
{crm}
      </div>
    </section>

    <section class="panel">
      <div class="wrap">
        <div class="card card--lg cta-block">
          <span class="tag">Work with us</span>
          <h2 class="display">Tell us what you're looking for.</h2>
          <p class="sub">A first conversation costs nothing. We'll tell you honestly whether we're the right fit.</p>
          <div class="btn-row"><a class="btn btn--fill" href="{WAI('Hi%20Kuber%20Estate%2C%20I%27d%20like%20to%20discuss%20a%20property%20investment.')}" target="_blank" rel="noopener">Enquire on WhatsApp</a><a class="btn btn--ghost" href="/#contact">Use the form</a></div>
        </div>
      </div>
    </section>
  </main>

"""
    html=head('About us — Kuber Estate','The keystone of your deal: who we are, how we are different, our vision and principles, and the founders.','/about.html')+LD+nav('/#about')+body+footer()+dock('about')+tail()
    open('about.html','w',encoding='utf-8').write(html)

import re as _re
def relativize(html, base):
    html=html.replace('aniket.vohra@kuberestate.co.in', EMAIL)
    html=html.replace('href="/#', 'href="'+base+'index.html#').replace('href="/"', 'href="'+base+'index.html"')
    html=_re.sub(r'(href|src|poster)="/(?!/)', lambda m: m.group(1)+'="'+base, html)
    return html
_open=open
def open(path, mode='r', **kw):
    if mode=='w' and path.endswith('.html'):
        class W:
            def __init__(s,p): s.p=p
            def write(s,html):
                base='../' if '/' in s.p else ''
                _open(s.p,'w',encoding='utf-8').write(relativize(html, base))
        return W(path)
    return _open(path, mode, **kw)
build_index(); build_services_page(); build_product_page(); build_properties(); build_about()
print('built: index, services, products/kubercrm, properties, about')
