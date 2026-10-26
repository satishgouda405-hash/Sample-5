#!/usr/bin/env python3
"""Generates the static homestay website. Edit CONFIG below, then run: python3 build.py"""
import os, html, urllib.parse

CONFIG = {
    "name": "Misty Hills Homestay",
    "short": "Misty Hills",
    "tagline": "Slow mornings. Mountain air. Home-cooked meals.",
    "city": "Your Town, Karnataka",
    "address": "Misty Hills Homestay, Your Village Road, Your Town, Karnataka 000000",
    "phone": "+91 99999 99999",
    "phone_tel": "+919999999999",
    "whatsapp": "919999999999",  # country code + number, no + or spaces
    "email": "stay@example.com",
    "instagram": "https://instagram.com/yourproperty",
    "facebook": "https://facebook.com/yourproperty",
    "youtube": "https://youtube.com/@yourproperty",
    "site_url": "https://www.example.com",
}

ROOMS = [
    dict(name="Garden View Room", g="g1", img="room-1.jpg", guests="2 adults", bed="1 Queen bed",
         price="₹2,500 / night", desc="A calm, bright room opening onto the garden. Wake up to birdsong and fresh air.",
         am=["Attached bath", "Hot water", "Wi-Fi", "Garden view"]),
    dict(name="Family Suite", g="g2", img="room-2.jpg", guests="4 adults", bed="1 King + 1 Double bed",
         price="₹4,200 / night", desc="Spacious suite with a sitting area, ideal for families and small groups.",
         am=["Attached bath", "Sitting area", "Wi-Fi", "Private balcony"]),
    dict(name="Cottage Villa", g="g3", img="room-3.jpg", guests="3 adults", bed="1 King bed + 1 Single",
         price="₹3,600 / night", desc="A private stand-alone cottage with its own veranda for a quiet getaway.",
         am=["Private veranda", "Hot water", "Wi-Fi", "Parking"]),
]

REVIEWS = [  # REPLACE with the client's real guest reviews before launch
    ("Beautiful, peaceful property. The food felt like a home meal and the hosts were wonderful.", "Guest name", "Bengaluru"),
    ("Clean rooms, great views and very easy to reach. We will definitely come back.", "Guest name", "Mysuru"),
    ("Perfect weekend break with family. Kids loved the garden and the bonfire evening.", "Guest name", "Hyderabad"),
    ("Warm hospitality and honest pricing. Booking over WhatsApp was quick and simple.", "Guest name", "Pune"),
]

AMENITIES = [
    ("🍲", "Home-style meals", "Fresh, local, cooked with care.", "span2"),
    ("📶", "Free Wi-Fi", "Stay connected when you need to.", ""),
    ("🌄", "Scenic surroundings", "Hills, greenery and open skies.", ""),
    ("🔥", "Bonfire evenings", "Warm nights under the stars.", ""),
    ("🚗", "Free parking", "Safe, easy parking on site.", ""),
    ("🚿", "Hot water 24x7", "Comfort, always on.", "span2"),
]

PAGES = [("index.html", "Home"), ("about.html", "About"), ("rooms.html", "Stay"),
         ("gallery.html", "Gallery"), ("contact.html", "Contact")]

C = CONFIG
e = html.escape
wa_base = f"https://wa.me/{C['whatsapp']}"
wa_hello = f"{wa_base}?text=" + urllib.parse.quote(f"Hello {C['name']}, I would like to know more about staying with you.")


def photo(img, g="g1", label="", cls=""):
    return (f'<div class="photo {g} {cls}" style="--img:url(\'images/{img}\')" role="img" '
            f'aria-label="{e(label)}"></div>')


def words(text):
    out = []
    for i, w in enumerate(text.split()):
        out.append(f'<span class="w"><span style="--i:{i}">{e(w)}</span></span>')
    return " ".join(out)


def head(title, desc, page, extra=""):
    return f"""<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#09090b">
<link rel="canonical" href="{C['site_url']}/{page if page != 'index.html' else ''}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{C['site_url']}/images/hero.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
<script>document.documentElement.className='js'</script>
{extra}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"></div>
<div class="glow glow-a" aria-hidden="true"></div>
<div class="glow glow-b" aria-hidden="true"></div>
"""


def header(active):
    links = "".join(
        f'<a href="{h}"{" class=\"active\" aria-current=\"page\"" if h == active else ""}>{t}</a>'
        for h, t in PAGES)
    return f"""<header class="site-header">
  <div class="container bar">
    <a class="brand" href="index.html" aria-label="{e(C['name'])} home"><span class="dot"></span>{e(C['short'])}</a>
    <nav class="nav" id="nav" aria-label="Main"><span class="pill" aria-hidden="true"></span>{links}</nav>
    <a class="btn btn-sm magnetic hide-sm" href="contact.html">Enquire Now</a>
    <button class="burger" aria-label="Open menu" aria-expanded="false" aria-controls="nav"><i></i><i></i></button>
  </div>
</header>
<main id="main">
"""


def footer():
    return f"""</main>
<footer class="footer">
  <div class="container foot-grid">
    <div>
      <a class="brand" href="index.html"><span class="dot"></span>{e(C['name'])}</a>
      <p class="muted">{e(C['tagline'])}</p>
    </div>
    <div>
      <h4>Explore</h4>
      {''.join(f'<a href="{h}">{t}</a>' for h, t in PAGES)}
    </div>
    <div>
      <h4>Contact</h4>
      <a href="tel:{C['phone_tel']}">{e(C['phone'])}</a>
      <a href="mailto:{C['email']}">{e(C['email'])}</a>
      <a href="{wa_hello}" target="_blank" rel="noopener">WhatsApp us</a>
    </div>
    <div>
      <h4>Follow</h4>
      <a href="{C['instagram']}" target="_blank" rel="noopener">Instagram</a>
      <a href="{C['facebook']}" target="_blank" rel="noopener">Facebook</a>
      <a href="{C['youtube']}" target="_blank" rel="noopener">YouTube</a>
    </div>
  </div>
  <div class="container foot-bottom">
    <span>© <span id="year">2026</span> {e(C['name'])}. All rights reserved.</span>
    <!-- Add Privacy / Terms links here if the client supplies them -->
  </div>
</footer>

<div class="fab" aria-label="Quick contact">
  <a class="fab-wa" href="{wa_hello}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">
    <svg viewBox="0 0 24 24" width="26" height="26" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.200-1.200l-.3-.2-3 .8.8-2.900-.2-.3A8.200 8.200 0 1 1 12 20.200zm4.500-6.100c-.2-.1-1.500-.7-1.700-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.200-.3.200-.5.100-1.500-.7-2.500-1.300-3.400-2.900-.3-.4.300-.4.800-1.300.1-.2 0-.3 0-.5l-.8-1.800c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.5.100-.7.300-.2.300-1 1-1 2.400s1 2.700 1.200 2.900c.1.200 2 3.100 4.800 4.300 1.800.7 2.500.8 3.400.7.500-.1 1.700-.7 1.900-1.400.2-.6.200-1.200.2-1.300-.1-.1-.3-.2-.6-.3z"/></svg>
  </a>
  <a class="fab-call" href="tel:{C['phone_tel']}" aria-label="Call us">
    <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.800a15.100 15.100 0 0 0 6.600 6.600l2.200-2.200a1 1 0 0 1 1-.25c1.100.37 2.300.57 3.600.57a1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.500a1 1 0 0 1 1 1c0 1.300.2 2.500.57 3.600a1 1 0 0 1-.25 1z"/></svg>
  </a>
</div>
<script src="js/main.js" defer></script>
</body>
</html>
"""


def room_card(r, i):
    am = "".join(f"<li>{e(a)}</li>" for a in r["am"])
    q = urllib.parse.quote(r["name"])
    return f"""<article class="room card reveal spot">
  {photo(r['img'], r['g'], r['name'] + ' photo', 'room-img')}
  <div class="room-body">
    <h3>{e(r['name'])}</h3>
    <p class="muted">{e(r['desc'])}</p>
    <dl class="facts"><div><dt>Guests</dt><dd>{e(r['guests'])}</dd></div><div><dt>Beds</dt><dd>{e(r['bed'])}</dd></div></dl>
    <ul class="chips">{am}</ul>
    <div class="room-foot">
      <span class="price">{e(r['price'])}</span>
      <a class="btn btn-sm magnetic" href="contact.html?room={q}">Enquire</a>
    </div>
  </div>
</article>"""


# ---------------------------------------------------------------- HOME
def home():
    ld = f"""<script type="application/ld+json">{{"@context":"https://schema.org","@type":"LodgingBusiness","name":"{C['name']}","description":"{C['tagline']}","telephone":"{C['phone_tel']}","email":"{C['email']}","address":"{C['address']}","url":"{C['site_url']}"}}</script>"""
    s = head(f"{C['name']} | Homestay & Stay in {C['city']}",
             f"{C['name']} offers comfortable rooms, home-cooked meals and warm hospitality in {C['city']}. Enquire on WhatsApp or call today.",
             "index.html", ld)
    s += header("index.html")
    s += f"""<section class="hero">
  {photo('hero.jpg', 'g0', C['name'] + ' main view', 'hero-bg')}
  <div class="hero-shade"></div>
  <div class="container hero-inner">
    <p class="eyebrow reveal">Welcome to {e(C['city'])}</p>
    <h1>{words(C['tagline'])}</h1>
    <p class="lead reveal" style="transition-delay:.5s">A warm, family-run stay where you can unwind, eat well and wake up to a view. Tell us your dates and we will take care of the rest.</p>
    <div class="cta-row reveal" style="transition-delay:.65s">
      <a class="btn btn-lg magnetic" href="contact.html">Enquire Now</a>
      <a class="btn btn-lg btn-ghost magnetic" href="{wa_hello}" target="_blank" rel="noopener">WhatsApp</a>
    </div>
  </div>
  <a class="scroll-cue" href="#about" aria-label="Scroll down"><span></span></a>
</section>

<section class="section" id="about">
  <div class="container split">
    <div class="reveal">
      <p class="eyebrow">The property</p>
      <h2>A quiet corner to slow down</h2>
      <p class="muted">{e(C['name'])} is a small, welcoming stay in {e(C['city'])}. Comfortable rooms, fresh home-style food and friendly hosts who make you feel like family. It is the kind of place you come to rest and leave wanting to return.</p>
      <a class="link" href="about.html">Our story →</a>
    </div>
    <div class="stats reveal" style="transition-delay:.15s">
      <div class="card spot"><b data-count="3">0</b><span>Room types</span></div>
      <div class="card spot"><b data-count="10">0</b><span>Guests hosted daily*</span></div>
      <div class="card spot"><b data-count="24">0</b><span>Hour hot water</span></div>
      <div class="card spot"><b data-count="100" data-suffix="%">0</b><span>Home-cooked</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="sec-head reveal"><p class="eyebrow">Amenities</p><h2>Everything for an easy stay</h2></div>
    <div class="bento">
      {''.join(f'<div class="card spot bento-item {sp} reveal" style="transition-delay:{i*0.07}s"><span class="ico">{ic}</span><h3>{e(t)}</h3><p class="muted">{e(d)}</p></div>' for i,(ic,t,d,sp) in enumerate(AMENITIES))}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="sec-head reveal"><p class="eyebrow">Accommodation</p><h2>Choose your stay</h2></div>
    <div class="rooms-grid">
      {''.join(room_card(r, i) for i, r in enumerate(ROOMS))}
    </div>
    <p class="center reveal"><a class="btn btn-ghost magnetic" href="rooms.html">See all rooms</a></p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="sec-head reveal"><p class="eyebrow">Gallery</p><h2>A glimpse of the place</h2></div>
    <div class="mosaic">
      {photo('gallery-1.jpg','g1','Property photo 1','m1 reveal zoom')}
      {photo('gallery-2.jpg','g2','Property photo 2','m2 reveal zoom')}
      {photo('gallery-3.jpg','g3','Property photo 3','m3 reveal zoom')}
      {photo('gallery-4.jpg','g4','Property photo 4','m4 reveal zoom')}
      {photo('gallery-5.jpg','g5','Property photo 5','m5 reveal zoom')}
    </div>
    <p class="center reveal"><a class="link" href="gallery.html">View full gallery →</a></p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="sec-head reveal"><p class="eyebrow">Guest reviews</p><h2>Loved by our guests</h2></div>
    <!-- REPLACE with the client's real reviews before launch -->
    <div class="reviews">
      {''.join(f'<figure class="card spot review reveal" style="transition-delay:{i*0.08}s"><div class="stars" aria-label="5 out of 5 stars">★★★★★</div><blockquote>{e(q)}</blockquote><figcaption>{e(n)} · {e(c)}</figcaption></figure>' for i,(q,n,c) in enumerate(REVIEWS))}
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="cta-card reveal">
      <h2>Ready to plan your stay?</h2>
      <p class="muted">Send us your dates. We usually reply within a few hours.</p>
      <div class="cta-row center-row">
        <a class="btn btn-lg magnetic" href="contact.html">Enquire Now</a>
        <a class="btn btn-lg btn-ghost magnetic" href="{wa_hello}" target="_blank" rel="noopener">WhatsApp</a>
        <a class="btn btn-lg btn-ghost magnetic" href="tel:{C['phone_tel']}">Call</a>
      </div>
    </div>
  </div>
</section>
"""
    s += footer()
    return s


# ---------------------------------------------------------------- ABOUT
def about():
    s = head(f"About | {C['name']}", f"The story, philosophy and what makes {C['name']} special.", "about.html")
    s += header("about.html")
    s += f"""<section class="page-hero"><div class="container">
  <p class="eyebrow reveal">About us</p><h1>{words('Our story, our home')}</h1>
  <p class="lead reveal">A small property with a big heart.</p></div></section>

<section class="section"><div class="container split">
  <div class="reveal">
    <h2>How it began</h2>
    <p class="muted">Write the property's real story here: who started it, why, and what the place means to the family. Two or three short paragraphs are enough. Guests like knowing the people behind the stay.</p>
    <p class="muted">{e(C['name'])} was created so that travellers could enjoy comfort, good food and quiet surroundings without the feel of a big hotel.</p>
  </div>
  {photo('about.jpg','g2','The hosts or the property','tall reveal zoom')}
</div></section>

<section class="section"><div class="container">
  <div class="sec-head reveal"><p class="eyebrow">Philosophy</p><h2>How we look after guests</h2></div>
  <div class="bento three">
    <div class="card spot bento-item reveal"><span class="ico">🤝</span><h3>Genuine warmth</h3><p class="muted">You are a guest first, a booking never. We greet you like family.</p></div>
    <div class="card spot bento-item reveal" style="transition-delay:.08s"><span class="ico">🧼</span><h3>Clean and simple</h3><p class="muted">Tidy rooms, fresh linen and no unnecessary extras.</p></div>
    <div class="card spot bento-item reveal" style="transition-delay:.16s"><span class="ico">🌿</span><h3>Local and fresh</h3><p class="muted">Food and experiences rooted in the place we live.</p></div>
  </div>
</div></section>

<section class="section"><div class="container">
  <div class="cta-card reveal">
    <h2>What makes us special</h2>
    <p class="muted">Add 3 to 4 honest points: the view, the food, the location, the hosts. Then invite guests to get in touch.</p>
    <div class="cta-row center-row"><a class="btn btn-lg magnetic" href="contact.html">Enquire Now</a>
    <a class="btn btn-lg btn-ghost magnetic" href="{wa_hello}" target="_blank" rel="noopener">WhatsApp</a></div>
  </div>
</div></section>
"""
    return s + footer()


# ---------------------------------------------------------------- ROOMS
def rooms():
    s = head(f"Rooms & Stay | {C['name']}", f"Rooms and accommodation at {C['name']}, with guest capacity, beds, amenities and prices.", "rooms.html")
    s += header("rooms.html")
    s += f"""<section class="page-hero"><div class="container">
  <p class="eyebrow reveal">Stay</p><h1>{words('Rooms & accommodation')}</h1>
  <p class="lead reveal">Pick what suits you. Send an enquiry and we will confirm availability.</p></div></section>
<section class="section"><div class="container">
  <div class="rooms-grid">{''.join(room_card(r, i) for i, r in enumerate(ROOMS))}</div>
  <p class="note reveal">Prices are indicative and may change by season. Availability is confirmed on enquiry.</p>
</div></section>
"""
    return s + footer()


# ---------------------------------------------------------------- GALLERY
def gallery():
    s = head(f"Gallery | {C['name']}", f"Photos of rooms, food and surroundings at {C['name']}.", "gallery.html")
    s += header("gallery.html")
    gs = ["g1", "g2", "g3", "g4", "g5", "g6"]
    tall = {1, 4, 7, 10}
    items = "".join(photo(f"gallery-{i}.jpg", gs[i % 6], f"Property photo {i}",
                          f"gal reveal zoom {'gt' if i in tall else ''}") for i in range(1, 13))
    s += f"""<section class="page-hero"><div class="container">
  <p class="eyebrow reveal">Gallery</p><h1>{words('See the place')}</h1>
  <p class="lead reveal">Tap any photo to view it larger.</p></div></section>
<section class="section"><div class="container"><div class="gallery">{items}</div></div></section>
<div class="lightbox" role="dialog" aria-modal="true" aria-label="Photo viewer" hidden>
  <button class="lb-close" aria-label="Close">×</button>
  <div class="lb-img photo"></div>
</div>
"""
    return s + footer()


# ---------------------------------------------------------------- CONTACT
def contact():
    mapq = urllib.parse.quote(C["address"])
    s = head(f"Contact & Enquiry | {C['name']}", f"Call, WhatsApp or send an enquiry to {C['name']}.", "contact.html")
    s += header("contact.html")
    s += f"""<section class="page-hero"><div class="container">
  <p class="eyebrow reveal">Contact</p><h1>{words("Let's plan your stay")}</h1>
  <p class="lead reveal">Fastest reply: WhatsApp or call. Or fill the form below.</p></div></section>

<section class="section"><div class="container contact-grid">
  <div class="info">
    <a class="card spot info-card reveal" href="tel:{C['phone_tel']}"><span class="ico">📞</span><div><h3>Call</h3><p class="muted">{e(C['phone'])}</p></div></a>
    <a class="card spot info-card reveal" href="{wa_hello}" target="_blank" rel="noopener"><span class="ico">💬</span><div><h3>WhatsApp</h3><p class="muted">Chat with us now</p></div></a>
    <a class="card spot info-card reveal" href="mailto:{C['email']}"><span class="ico">✉️</span><div><h3>Email</h3><p class="muted">{e(C['email'])}</p></div></a>
    <div class="card spot info-card reveal"><span class="ico">📍</span><div><h3>Address</h3><p class="muted">{e(C['address'])}</p></div></div>
  </div>

  <form class="card form reveal" id="enquiry" novalidate>
    <h2>Send an enquiry</h2>
    <div class="row">
      <label>Name<input name="name" required autocomplete="name"></label>
      <label>Phone<input name="phone" type="tel" required autocomplete="tel"></label>
    </div>
    <div class="row">
      <label>Check-in<input name="checkin" type="date" required></label>
      <label>Check-out<input name="checkout" type="date" required></label>
    </div>
    <label>Guests<input name="guests" type="number" min="1" max="30" value="2" required></label>
    <label>Message<textarea name="message" rows="4" placeholder="Room preference, special requests..."></textarea></label>
    <button class="btn btn-lg magnetic" type="submit">Send on WhatsApp</button>
    <p class="note" id="form-note" role="status">Your enquiry opens in WhatsApp, ready to send.</p>
  </form>
</div></section>

<section class="section"><div class="container reveal">
  <div class="map"><iframe title="Map showing {e(C['name'])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
    src="https://www.google.com/maps?q={mapq}&output=embed"></iframe></div>
</div></section>
<script>window.WA_NUMBER="{C['whatsapp']}";window.PROP_NAME="{C['name']}";</script>
"""
    return s + footer()


if __name__ == "__main__":
    out = os.path.dirname(os.path.abspath(__file__))
    for fn, fnc in [("index.html", home), ("about.html", about), ("rooms.html", rooms),
                    ("gallery.html", gallery), ("contact.html", contact)]:
        with open(os.path.join(out, fn), "w", encoding="utf-8") as f:
            f.write(fnc())
    os.makedirs(os.path.join(out, "images"), exist_ok=True)
    print("built")
