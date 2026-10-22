"""Regenerate the static GitHub Pages site from site-content.json.

    python3 build.py

Standard library only. Writes index.html, resume.html, projects/*.html,
sitemap.xml, robots.txt and TODO_CONTENT.md.
"""
from datetime import date
from html import escape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
C = json.loads((ROOT / 'site-content.json').read_text(encoding='utf-8'))
PROJECTS = C['projects']
P = {p['id']: p for p in PROJECTS}
LAYERS = {layer['id']: layer for layer in C['layers']}
FEATURED = [P[i] for i in C['featured_order']]
SITE = C['site_url'].rstrip('/')
TODAY = date.today().isoformat()


# ---------------------------------------------------------------- helpers

def e(value):
    return escape(str(value), quote=True)


def inline(text):
    """Escape text and turn `code` spans into <code>."""
    return re.sub(r'`([^`]+)`', r'<code>\1</code>', e(text))


def ext(href, label, cls=''):
    """External link: opens in a new tab and carries the ↗ marker."""
    c = f' class="{cls}"' if cls else ''
    return f'<a{c} href="{e(href)}" target="_blank" rel="noopener">{label}<span class="ext" aria-hidden="true">↗</span><span class="sr-only"> (opens in a new tab)</span></a>'


def reading_time(p):
    words = ' '.join([p['summary'], p['problem'], ' '.join(p['implementation']), p['results'], p['learning'], p.get('media_note', '')]).split()
    return max(2, round(len(words) / 160))


def layer_of(p):
    return LAYERS[p['layer']]


# ---------------------------------------------------------------- page shell

def head(title, description, prefix='', path='', extra=''):
    url = f'{SITE}/{path}'
    return f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{e(url)}">
<meta name="theme-color" content="#FBF8F3">
<meta property="og:type" content="website"><meta property="og:url" content="{e(url)}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}">
<meta property="og:image" content="{SITE}/assets/og-image.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(description)}"><meta name="twitter:image" content="{SITE}/assets/og-image.png">
<link rel="icon" type="image/svg+xml" href="{prefix}favicon.svg"><link rel="apple-touch-icon" href="{prefix}assets/apple-touch-icon.png">
<link rel="preload" href="{prefix}assets/fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{prefix}styles.css"><script src="{prefix}script.js" defer></script>{extra}
</head><body><a class="skip" href="#main">Skip to content</a>'''


def header(prefix='', current='', home=None):
    if home is None:
        home = f'{prefix}index.html' if prefix else ''
    def nav(href, label, key):
        cur = ' aria-current="page"' if key == current else ''
        return f'<a href="{href}" data-nav="{key}"{cur}>{label}</a>'
    return f'''<header class="site-header" id="top"><div class="wrap header-inner">
<a class="brand" href="{prefix or './'}{'index.html' if prefix else ''}"><span class="brand-full">{e(C['name'])}</span><span class="brand-short" aria-hidden="true">{e(C['initials'])}</span></a>
<nav class="site-nav" aria-label="Main">{nav(home + '#work', 'Work', 'work')}{nav(home + '#about', 'About', 'about')}{nav(prefix + 'resume.html', 'Resume', 'resume')}{nav(home + '#contact', 'Contact', 'contact')}</nav>
{ext(C['github'], 'GitHub', 'header-cta')}
</div></header>'''


# ---------------------------------------------------------------- hand-drawn icons (inline SVG, ink = currentColor)

ICONS = {
    'peace': '<svg class="ico ico-peace" viewBox="0 0 64 64" aria-hidden="true"><g fill="var(--paper)" stroke="currentColor" stroke-width="4.4" stroke-linejoin="round" stroke-linecap="round"><rect x="15.5" y="4" width="13" height="34" rx="6.5" transform="rotate(-13 22 36)"/><rect x="33" y="3" width="13" height="35" rx="6.5" transform="rotate(12 39.5 36)"/><path d="M14 40c0-6 4-9 10-9h17c6 0 9 4 9 10v6c0 8-6 14-14 14h-8c-8 0-14-6-14-14Z"/><path d="M34 39.5c4-1.6 8.5-1.6 12.5 0" fill="none"/><path d="M9.5 45.5c0-3 2.4-5 5.4-4.6l17 2.4c3 .4 4.8 3 4.3 6-.5 2.8-3.2 4.6-6 4.2l-16.4-2.4c-2.7-.4-4.3-2.8-4.3-5.6Z"/></g></svg>',
    'chip': '<svg class="ico" viewBox="0 0 48 48" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"><rect x="12" y="12" width="24" height="24" rx="4"/><rect x="19" y="19" width="10" height="10" rx="1.5"/><path d="M18 5v7M24 5v7M30 5v7M18 36v7M24 36v7M30 36v7M5 18h7M5 24h7M5 30h7M36 18h7M36 24h7M36 30h7"/></g></svg>',
    'mesh': '<svg class="ico" viewBox="0 0 48 48" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="3.4" stroke-linecap="round"><path d="M10 37 24 11 38 37 10 37M24 11v17M10 37l14-9 14 9"/></g><g fill="var(--paper)" stroke="currentColor" stroke-width="3.4"><circle cx="24" cy="11" r="5"/><circle cx="10" cy="37" r="5"/><circle cx="38" cy="37" r="5"/><circle cx="24" cy="28" r="4"/></g></svg>',
    'braces': '<svg class="ico" viewBox="0 0 48 48" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"><path d="M18 7c-5 0-6.5 2.5-6.5 6.5v6c0 2.8-1.6 4.5-5 4.5 3.4 0 5 1.7 5 4.5v6c0 4 1.5 6.5 6.5 6.5M30 7c5 0 6.5 2.5 6.5 6.5v6c0 2.8 1.6 4.5 5 4.5-3.4 0-5 1.7-5 4.5v6c0 4-1.5 6.5-6.5 6.5"/></g></svg>',
    'spark': '<svg class="ico" viewBox="0 0 48 48" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="3.4" stroke-linejoin="round"><path d="M20 7c1.4 8.6 4.4 11.6 13 13-8.6 1.4-11.6 4.4-13 13-1.4-8.6-4.4-11.6-13-13 8.6-1.4 11.6-4.4 13-13Z"/><path d="M37 29c.7 4 2 5.3 6 6-4 .7-5.3 2-6 6-.7-4-2-5.3-6-6 4-.7 5.3-2 6-6Z"/></g></svg>',
    'cursor': '<svg class="cursor3d" viewBox="0 0 80 80" aria-hidden="true"><defs><filter id="cur-shadow" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="3" dy="6" stdDeviation="3.5" flood-color="#18202E" flood-opacity=".35"/></filter><linearGradient id="cur-fill" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3a4252"/><stop offset="1" stop-color="#0d121b"/></linearGradient></defs><path filter="url(#cur-shadow)" d="M14 8 L14 62 L28 49 L38 70 L48 65 L38 45 L57 45 Z" fill="url(#cur-fill)" stroke="#fff" stroke-width="5" stroke-linejoin="round"/></svg>',
}


def contact(prefix=''):
    return f'''<section class="contact" id="contact" aria-labelledby="contact-title"><div class="wrap contact-inner">
<h2 id="contact-title" class="contact-title"><span class="ct-line">Interested in {ICONS['peace']}</span><span class="ct-line">building together?</span></h2>
<p class="contact-lead">Contact me:</p>
<p class="contact-mail-row"><a class="contact-mail" href="mailto:{e(C['email'])}">{e(C['email']).replace('@', '<wbr>@')}</a>{ICONS['cursor']}</p>
<div class="contact-actions"><button class="btn btn-dark" type="button" data-copy-email="{e(C['email'])}">Copy email</button><a class="btn btn-outline" href="{prefix}{e(C['cv_pdf'])}" download>Download CV (PDF)</a></div>
<p class="copy-status" id="copy-status" role="status" aria-live="polite"></p>
</div></section>'''


def footer(prefix=''):
    return f'''<footer class="site-footer"><div class="wrap footer-inner">
<p class="footer-made">Designed &amp; built<br>by {e(C['name'])}</p>
<p class="footer-pills">{ext(C['linkedin'], 'LinkedIn', 'pill-link')}{ext(C['github'], 'GitHub', 'pill-link')}{ext(C['github'] + '/TitovMykhailo.github.io', 'Site source', 'pill-link')}</p>
<p class="footer-end">© <span data-year>{date.today().year}</span> {e(C['name'])}<br><a href="#top">Back to top ↑</a></p>
</div></footer>
</body></html>'''


# ---------------------------------------------------------------- diagrams
# Every diagram is drawn from facts in the project's public repository
# (or is clearly captioned as a textbook illustration).

# simulator/scenario.json in TitovMykhailo/Kizuna-v2 (default field scenario)
KIZUNA_SCENARIO = [
    ('GW-01', 'gateway', 80, 80, 'r'), ('RTR-02', 'router', 310, 150, 'r'), ('RTR-03', 'router', 620, 160, 'r'),
    ('MOD-04', 'module', 1350, 220, 'r'), ('RTR-05', 'router', 190, 360, 'r'), ('RTR-06', 'router', 760, 420, 'r'),
    ('MOD-07', 'module', 1180, 480, 'r'), ('RTR-08', 'router', 130, 690, 'r'), ('RTR-09', 'router', 930, 690, 'r'),
    ('GW-10', 'gateway', 1520, 820, 'l'), ('RTR-11', 'standby', 740, 380, 'l'), ('RTR-12', 'standby', 810, 460, 'br'),
]


def kizuna_map():
    grid = ''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="900"/>' for x in range(200, 1600, 200))
    grid += ''.join(f'<line x1="0" y1="{y}" x2="1600" y2="{y}"/>' for y in range(150, 900, 150))
    nodes = ''
    for name, kind, x, y, side in KIZUNA_SCENARIO:
        if kind == 'gateway':
            shape = f'<circle class="k-ring" cx="{x}" cy="{y}" r="42"/><circle class="k-gw" cx="{x}" cy="{y}" r="26"/>'
        elif kind == 'module':
            shape = f'<rect class="k-mod" x="{x - 19}" y="{y - 19}" width="38" height="38" transform="rotate(45 {x} {y})"/>'
        elif kind == 'standby':
            shape = f'<circle class="k-standby" cx="{x}" cy="{y}" r="21"/>'
        else:
            shape = f'<circle class="k-rtr" cx="{x}" cy="{y}" r="21"/><circle class="k-core" cx="{x}" cy="{y}" r="7"/>'
        if side == 'l':
            label = f'<text x="{x - 36}" y="{y + 11}" text-anchor="end">{name}</text>'
        elif side == 'br':
            label = f'<text x="{x + 30}" y="{y + 46}">{name}</text>'
        else:
            label = f'<text x="{x + (50 if kind == "gateway" else 34)}" y="{y + 11}">{name}</text>'
        nodes += shape + label
    svg = f'''<svg class="kizuna-map" viewBox="0 0 1600 900" role="img" aria-labelledby="kmap-t"><title id="kmap-t">Default KIZUNA field scenario: 2 gateways, 7 routers, 2 modules and 2 standby routers over 1600 × 900 m</title>
<g class="k-grid">{grid}</g><g class="k-nodes">{nodes}</g></svg>'''
    legend = '<ul class="k-legend"><li><i class="lg-gw"></i>Gateway</li><li><i class="lg-rtr"></i>Router</li><li><i class="lg-mod"></i>Module</li><li><i class="lg-sb"></i>Standby router</li></ul>'
    return f'<div class="diagram diagram-map">{svg}{legend}</div>'


def codeword():
    labels = ['P0', 'P1', 'P2', 'D1', 'P4', 'D2', 'D3', 'D4']
    bits = ['0', '0', '1', '1', '0', '1', '1', '1']
    cells = ''.join(
        f'<li class="{"flipped" if i == 5 else ("parity" if l.startswith("P") else "")}"><small>{l}</small><b>{b}</b><span>{i}</span></li>'
        for i, (l, b) in enumerate(zip(labels, bits)))
    return f'''<div class="diagram diagram-code" role="img" aria-label="Extended Hamming (8,4) codeword with bit 5 flipped; syndrome 101 points to position 5.">
<p class="d-title">Received codeword</p><ol class="bits">{cells}</ol>
<dl class="checks"><div><dt>Syndrome</dt><dd><code>1 0 1</code> → position 5</dd></div><div><dt>Overall parity</dt><dd>fails → single error, flip bit 5</dd></div><div><dt>Two errors?</dt><dd>parity passes, syndrome ≠ 0 → detect, don’t correct</dd></div></dl></div>'''


def document_review():
    return '''<div class="diagram diagram-doc" role="img" aria-label="Illustration of a doctor's record next to a proposed REDCap form; one field is flagged because two sources disagree.">
<div class="doc-sheet"><p class="d-title">Doctor’s records</p><i></i><i></i><i class="hl"></i><i></i><i class="short"></i><i></i><i class="hl"></i><i class="short"></i><i></i></div>
<div class="doc-review"><p class="d-title">REDCap form</p>
<div class="doc-row"><span>Diagnosis date</span><em class="ok">filled</em></div>
<div class="doc-row"><span>PSA value</span><em class="ok">filled</em></div>
<div class="doc-row"><span>Tumour grade</span><em class="warn">2 sources disagree</em></div>
<div class="doc-row"><span>Diagram region</span><em class="ok">filled</em></div>
<div class="doc-actions"><span class="d-btn d-primary">Confirm</span><span class="d-btn">Show source</span></div></div></div>'''


def agent_pipeline():
    sources = ''.join(f'<li>{s}</li>' for s in ['Profesia.sk', 'Worki.sk', 'LinkedIn', 'Jobs.sk', 'Reddit'])
    return f'''<div class="diagram diagram-flow" role="img" aria-label="Job listings from five sources are filtered, scored by Azure OpenAI and written to two Google Sheets.">
<div class="flow-step"><p class="d-title">Collect</p><ul class="d-chips">{sources}</ul></div>
<div class="flow-arrow" aria-hidden="true"></div>
<div class="flow-step"><p class="d-title">Pre-filter</p><ul class="d-list"><li>“for hire” posts</li><li>discussions</li><li>senior-only roles</li><li>already seen</li></ul></div>
<div class="flow-arrow" aria-hidden="true"></div>
<div class="flow-step flow-model"><p class="d-title">Azure OpenAI</p><p class="d-big">0–10</p><p class="d-small">relevance score</p></div>
<div class="flow-arrow" aria-hidden="true"></div>
<div class="flow-step"><p class="d-title">Google Sheets</p><p class="d-out d-primary">Shortlist · score ≥ 7</p><p class="d-out">Full log · every listing</p></div></div>'''


def video_pipeline():
    steps = ['Voiceover', 'Transcribe', 'Trim silence & fillers', 'Captions', 'Match clips & sound', 'Colour grade', 'Resolve timeline', 'Draft render']
    clips = ''.join(f'<li style="--w:{w}"><span>{s}</span></li>' for s, w in zip(steps, [1.1, 1, 1.5, 1, 1.5, 1.1, 1.3, 1.1]))
    return f'''<div class="diagram diagram-timeline" role="img" aria-label="Editing pipeline: {', '.join(steps)}.">
<p class="d-title">Pipeline</p><ol class="clips">{clips}</ol>
<div class="tracks" aria-hidden="true"><div class="playhead"></div><span>V1</span><div class="track"><i style="left:4%;width:30%"></i><i style="left:36%;width:34%"></i><i style="left:72%;width:25%"></i></div><span>A1</span><div class="track"><i class="a" style="left:2%;width:96%"></i></div></div></div>'''


def study_arch():
    return '''<div class="diagram diagram-arch" role="img" aria-label="React SPA talks to a Spring Boot API over REST and WebSocket; the API uses Cloud SQL PostgreSQL and Cloud Storage; both run on Cloud Run.">
<div class="arch-box"><p class="d-title">React SPA</p><p class="d-small">Vite, served by nginx</p></div>
<div class="arch-link"><code>REST /api/**</code><code>WS /ws/chat</code></div>
<div class="arch-box arch-core"><p class="d-title">Spring Boot API</p><p class="d-small">JWT and Google OAuth2</p></div>
<div class="arch-split"><div class="arch-box"><p class="d-title">Cloud SQL</p><p class="d-small">PostgreSQL, 8 tables</p></div><div class="arch-box"><p class="d-title">Cloud Storage</p><p class="d-small">shared files</p></div></div>
<p class="arch-note">Both services deploy to Cloud Run via Cloud Build</p></div>'''


DIAGRAMS = {'kizuna-map': kizuna_map, 'codeword': codeword, 'document-review': document_review,
            'agent-pipeline': agent_pipeline, 'video-pipeline': video_pipeline, 'study-arch': study_arch}


def media(p, prefix='', large=False, eager=False):
    m = p['media'] if large else p.get('card_media', p['media'])
    cls = f'media tint-{e(p["color"])}' + (' media-large' if large else '')
    if m['kind'] == 'image':
        loading = 'eager' if eager else 'lazy'
        inner = f'<div class="shot"><img src="{prefix}{e(m["src"])}" width="{m["width"]}" height="{m["height"]}" alt="{e(m["alt"])}" loading="{loading}" decoding="async"></div>'
        cls += ' media-shot'
    else:
        inner = DIAGRAMS[m['diagram']]()
    return f'<div class="{cls}">{inner}</div>'


# ---------------------------------------------------------------- home page parts

# ---------------------------------------------------------------- playful hero + intro

def hero_dots():
    import random
    rnd = random.Random(7)
    dots = ''.join(f'<circle cx="{rnd.uniform(0, 1600):.0f}" cy="{rnd.uniform(0, 760):.0f}" r="{rnd.choice((1.6, 2, 2.4, 3))}"/>' for _ in range(150))
    return f'<svg class="hero-dots" viewBox="0 0 1600 760" preserveAspectRatio="none" aria-hidden="true">{dots}</svg>'


def hero_type():
    return f'''<section class="hero" aria-labelledby="hero-title">
{hero_dots()}
<div class="wrap hero-stage">
<h1 id="hero-title" class="sr-only">{e(C['name'])}, {e(C['hero_words'][0].lower())} {e(C['hero_words'][1].lower())} {e(C['hero_words'][2].lower())}</h1>
<div class="hero-type" aria-hidden="true">
<span class="ht-line ht-dots">{e(C['hero_words'][0])}</span>
<span class="ht-line ht-orange">S<button class="ht-toggle" type="button" tabindex="-1" aria-pressed="false" data-toggle><span class="ht-knob"></span></button>FTWARE</span>
<span class="ht-line ht-black">ENG<span class="ht-capsule"><img src="{e(C['hero_capsule'])}" alt="" width="360" height="986" decoding="async"></span>NEER<span class="ht-sticker"><span>&lt;/&gt;</span></span></span>

</div>
</div>
<div class="wrap hero-foot">
<p class="hero-places-label"><span class="status-dot" aria-hidden="true"></span>{e(C['status'])}. Studying and building at</p>
<div class="marquee" aria-label="Places">{names_track()}{names_track(hidden=True)}</div>
<div class="hero-actions"><a class="btn btn-signal" href="#work">See the projects</a><a class="btn btn-outline" href="{e(C['cv_pdf'])}" download>Download CV (PDF)</a></div>
</div>
</section>'''


def names_track(hidden=False):
    items = ''.join(f'<li class="nm-{e(n["style"])}">{e(n["name"])}</li>' for n in C['places'])
    attr = ' aria-hidden="true"' if hidden else ''
    return f'<ul class="marquee-track"{attr}>{items}</ul>'


def intro():
    i = C['intro']
    avatar = (f'<img class="intro-avatar" src="{e(C["photo"])}" alt="" width="96" height="96">' if C.get('photo')
              else f'<span class="intro-avatar intro-avatar-mono" aria-hidden="true">{e(C["initials"])}</span>')
    text = (f'Hi, I’m {avatar} {e(C["short_name"])}{ICONS["peace"]}, an ICT student at <span class="intro-pill">{e(i["pill"])}</span> '
            f'building software from bits{ICONS["chip"]}, networks{ICONS["mesh"]} and APIs{ICONS["braces"]} to AI agents{ICONS["spark"]}.')
    skills = ''
    for sk in i['skills']:
        style = f' style="--r:{sk["rotate"]}deg"' if sk.get('rotate') else ''
        skills += f'<li class="sk sk-{e(sk["style"])}"{style}>{e(sk["name"])}</li>'
    return f'''<section class="intro" id="about-intro" aria-label="Introduction"><div class="wrap intro-inner">
<p class="intro-text">{text}</p>
<svg class="scroll-badge" viewBox="0 0 120 120" aria-hidden="true"><defs><path id="badge-circle" d="M60 60 m-44 0 a44 44 0 1 1 88 0 a44 44 0 1 1 -88 0"/></defs><text><textPath href="#badge-circle">SCROLL ✦ SCROLL ✦ SCROLL ✦ </textPath></text></svg>
<p class="skills-label">with my skills in:</p>
<ul class="skill-cloud">{skills}</ul>
</div></section>'''


def metrics(p, cls='metrics'):
    if not p['metrics']:
        return ''
    return f'<ul class="{cls}">' + ''.join(f'<li><b>{e(m["value"])}</b><span>{e(m["label"])}</span></li>' for m in p['metrics']) + '</ul>'


def chips(items, limit=None):
    items = items[:limit] if limit else items
    return '<ul class="chips">' + ''.join(f'<li>{e(i)}</li>' for i in items) + '</ul>'


def case_card(p, index):
    layer = layer_of(p)
    code = ext(p['repo'], 'Code on GitHub', 'text-link') if p['repo'] else ''
    context = f'<span>{e(p["team"])}</span>' if p.get('team') else ''
    facts = ''
    if not p['metrics'] and p['facts']:
        facts = '<ul class="metrics metrics-facts">' + ''.join(f'<li><b>{e(f["items"][0])}</b><span>{e(", ".join(f["items"][1:]) or f["label"])}</span></li>' for f in p['facts'][:2]) + '</ul>'
    return f'''<article class="case" aria-labelledby="case-{e(p['id'])}">
<div class="case-text">
<p class="case-meta"><span class="layer-tag tint-{e(layer['color'])}">{e(layer['name'])}</span><span>{e(p['year'])}</span>{context}</p>
<h3 id="case-{e(p['id'])}">{e(p['title'])}</h3>
<p class="case-outcome">{e(p['outcome'])}</p>
{metrics(p) or facts}
{chips(p['stack'], 5)}
<div class="case-actions"><a class="btn btn-dark" href="projects/{e(p['id'])}.html">Read the case study<span class="sr-only">: {e(p['title'])}</span></a><span class="read-time">{reading_time(p)} min read</span>{code}</div>
</div>
<a class="case-media" href="projects/{e(p['id'])}.html" tabindex="-1" aria-hidden="true">{media(p, eager=index == 0)}</a>
</article>'''


def projects_table():
    order = FEATURED + [p for p in PROJECTS if p not in FEATURED]
    rows = ''
    for p in order:
        layer = layer_of(p)
        code = ext(p['repo'], 'Code', 'text-link') if p['repo'] else '<span class="muted">Private</span>'
        rows += f'''<tr><th scope="row"><a href="projects/{e(p['id'])}.html">{e(p['title'])}</a></th><td>{e(p['subtitle'])}</td><td><span class="layer-tag tint-{e(layer['color'])}">{e(layer['name'])}</span></td><td class="num">{e(p['year'])}</td><td>{code}</td></tr>'''
    return f'''<div class="table-wrap"><table class="projects-table"><caption class="sr-only">All projects</caption>
<thead><tr><th scope="col">Project</th><th scope="col">What it is</th><th scope="col">Layer</th><th scope="col">Year</th><th scope="col">Source</th></tr></thead>
<tbody>{rows}</tbody></table></div>'''


def hackathons():
    cards = ''
    for h in C.get('hackathons', []):
        badge = f'<span class="badge">{e(h["result"])}</span>' if h.get('result') else ''
        meta = [x for x in (h.get('where'), h.get('year'), h.get('team')) if x]
        meta_html = ''.join(f'<span>{e(m)}</span>' for m in meta)
        note = f'<p class="hack-note">{e(h["note"])}</p>' if h.get('note') else ''
        points = '<ul class="hack-points">' + ''.join(f'<li>{e(pt)}</li>' for pt in h['points']) + '</ul>' if h.get('points') else ''
        link = f'<a class="text-link hack-link" href="projects/{e(h["project"])}.html">Read the case study<span class="sr-only">: {e(P[h["project"]]["title"])}</span></a>' if h.get('project') else ''
        cards += f'''<li class="hack{' hack-award' if h.get('result') else ''}"><div class="hack-top"><h3>{e(h['event'])}</h3>{badge}</div>
<p class="hack-meta">{meta_html}</p>{note}<p class="hack-title">{e(h['title'])}</p><p class="hack-summary">{e(h['summary'])}</p>{points}{link}</li>'''
    return f'''<section class="section hackathons" id="hackathons" aria-labelledby="hackathons-title"><div class="wrap">
<h2 id="hackathons-title">Hackathons</h2><p class="section-lead">Team projects built against the clock, from a hospital’s documentation to a university’s heating bill.</p>
<ul class="hack-grid">{cards}</ul></div></section>'''


def portrait(prefix=''):
    if C.get('photo'):
        return f'<img class="portrait" src="{prefix}{e(C["photo"])}" width="480" height="560" alt="Portrait of {e(C["name"])}">'
    return f'<div class="portrait portrait-mono" aria-hidden="true"><span>{e(C["initials"])}</span></div>'


def about():
    a = C['about']
    edu = ''.join(f'<li><b>{e(x["school"])}</b><span>{e(x["program"])}{(" · " + e(x["years"])) if x.get("years") else ""}</span></li>' for x in C['education'])
    langs = ''
    if a.get('languages'):
        langs = '<div class="about-block"><h3>Languages</h3><ul class="plain-list">' + ''.join(f'<li><b>{e(l["name"])}</b><span>{e(l["level"])}</span></li>' for l in a['languages']) + '</ul></div>'
    timeline = ''.join(f'<li><span class="t-year">{e(t["year"])}</span><div><a href="projects/{e(t["project"])}.html">{e(t["title"])}</a><p>{e(t["text"])}</p></div></li>' for t in C['timeline'])
    return f'''<section class="section about" id="about" aria-labelledby="about-title"><div class="wrap about-grid">
<div class="about-side">{portrait()}<p class="about-name">{e(C['name'])}</p><p class="muted">{e(C['location'])}</p></div>
<div class="about-main">
<h2 id="about-title">About me</h2>
{''.join(f'<p class="{"about-lead" if i == 0 else ""}">{e(t)}</p>' for i, t in enumerate(a['bio']))}
<div class="about-block looking"><h3>What I’m looking for</h3><p>{e(a['looking_for'])}</p></div>
<div class="about-block"><h3>Education</h3><ul class="plain-list">{edu}</ul></div>
{langs}
<div class="about-block"><h3>Recent work</h3><ol class="timeline">{timeline}</ol></div>
</div></div></section>'''


def toolbox():
    groups = ''
    for g in C['toolbox']:
        used = ''
        if g['used_in']:
            used = '<p class="used-in">Used in ' + ', '.join(f'<a href="projects/{u}.html">{e(P[u]["title"])}</a>' for u in g['used_in']) + '</p>'
        groups += f'<li class="tool"><h3>{e(g["group"])}</h3>{chips(g["items"])}{used}</li>'
    return f'''<section class="section toolbox" aria-labelledby="toolbox-title"><div class="wrap">
<h2 id="toolbox-title">Toolbox</h2><p class="section-lead">What I work with, and where you can see it in use.</p>
<ul class="tool-grid">{groups}</ul></div></section>'''


# ---------------------------------------------------------------- index

def json_ld():
    data = {
        '@context': 'https://schema.org', '@type': 'Person', 'name': C['name'], 'url': SITE,
        'jobTitle': C['role'], 'email': f"mailto:{C['email']}",
        'address': {'@type': 'PostalAddress', 'addressLocality': 'Bratislava', 'addressCountry': 'SK'},
        'alumniOf': [{'@type': 'CollegeOrUniversity', 'name': x['school']} for x in C['education']],
        'sameAs': [C['github'], C['linkedin']],
        'award': [f"{h['result']}, {h['event']}" for h in C.get('hackathons', []) if h.get('result')],
        'knowsAbout': ['Java', 'Spring Boot', 'React', 'Python', 'Network protocols', 'IPv6', 'Verilog', 'LLM automation'],
    }
    return f'\n<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def build_index():
    out = head(f"{C['name']} — {C['role']}", C['meta_description'], extra=json_ld())
    out += header()
    out += f'''<main id="main">
{hero_type()}
{intro()}
<section class="section work" id="work" aria-labelledby="work-title"><div class="wrap">
<h2 id="work-title">Selected work</h2><p class="section-lead">Four projects in depth. Screens and numbers come from the code itself.</p>
<div class="cases">{''.join(case_card(p, i) for i, p in enumerate(FEATURED))}</div>
</div></section>
<section class="section all-projects" id="projects" aria-labelledby="projects-title"><div class="wrap">
<h2 id="projects-title">All projects</h2><p class="section-lead">Each one has a case study page with what I built and how.</p>
{projects_table()}
</div></section>
{hackathons()}
{about()}
{toolbox()}
</main>'''
    out += contact() + footer()
    (ROOT / 'index.html').write_text(out, encoding='utf-8')


# ---------------------------------------------------------------- project pages

def facts_block(p):
    if not p['facts']:
        return ''
    items = ''
    for f in p['facts']:
        if f.get('code'):
            items += f'<div class="fact fact-code"><h3>{e(f["label"])}</h3><pre><code>{e(f["code"])}</code></pre></div>'
        else:
            items += f'<div class="fact"><h3>{e(f["label"])}</h3>{chips(f["items"])}</div>'
    return f'<section id="facts" aria-labelledby="facts-h"><h2 id="facts-h">At a glance</h2><div class="facts">{items}</div></section>'


def gallery(p):
    if not p['gallery']:
        return ''
    figs = ''.join(f'<figure class="gallery-item"><div class="media tint-{e(p["color"])} media-shot"><div class="shot"><img src="../{e(g["src"])}" width="{g["width"]}" height="{g["height"]}" alt="{e(g["alt"])}" loading="lazy" decoding="async"></div></div><figcaption>{e(g["caption"])}</figcaption></figure>' for g in p['gallery'])
    return f'<section id="screens" aria-labelledby="screens-h"><h2 id="screens-h">Screens</h2>{figs}</section>'


def build_project(p, i):
    layer = layer_of(p)
    prev_p = PROJECTS[(i - 1) % len(PROJECTS)]
    next_p = PROJECTS[(i + 1) % len(PROJECTS)]
    rows = f'<div><dt>Year</dt><dd>{e(p["year"])}</dd></div><div><dt>Layer</dt><dd>{e(layer["name"])}</dd></div>'
    if p.get('role'):
        rows += f'<div><dt>My role</dt><dd>{e(p["role"])}</dd></div>'
    if p.get('team'):
        rows += f'<div><dt>Team</dt><dd>{e(p["team"])}</dd></div>'
    links = []
    if p['repo']:
        links.append(ext(p['repo'], 'Code on GitHub', 'text-link'))
    if p.get('demo'):
        links.append(ext(p['demo'], 'Live demo', 'text-link'))
    if not links:
        links.append(f'<a class="text-link" href="mailto:{e(C["email"])}?subject={e(p["title"])}">Ask me about it</a>')
    rows += f'<div><dt>Links</dt><dd class="dd-links">{"".join(links)}</dd></div>'
    toc = [('problem', 'The problem'), ('built', 'What I built'), ('how', 'How it works')]
    if p['facts']:
        toc.append(('facts', 'At a glance'))
    if p['gallery']:
        toc.append(('screens', 'Screens'))
    toc += [('results', 'Results'), ('learned', 'What I learned')]
    toc_html = ''.join(f'<li><a href="#{a}">{t}</a></li>' for a, t in toc)
    steps = ''.join(f'<li><span>{j + 1}</span>{e(s)}</li>' for j, s in enumerate(p['architecture']))
    out = head(f"{p['title']} — {C['name']}", p['outcome'] + '. ' + p['summary'], '../', f"projects/{p['id']}.html")
    out += header('../', 'work')
    out += f'''<main id="main" class="case-page">
<div class="wrap">
<nav class="breadcrumb" aria-label="Breadcrumb"><a href="../index.html#work">Work</a><span aria-hidden="true">/</span><span aria-current="page">{e(p['title'])}</span></nav>
<header class="case-head">
<p class="case-meta"><span class="layer-tag tint-{e(layer['color'])}">{e(layer['name'])}</span><span>{reading_time(p)} min read</span></p>
<h1 class="case-title">{e(p['title'])}</h1>
<p class="case-outcome case-outcome-lg">{e(p['outcome'])}</p>
</header>
<div class="tldr"><dl class="tldr-list">{rows}</dl>{metrics(p, 'metrics metrics-lg')}<div class="tldr-stack"><h2 class="tldr-h">Stack</h2>{chips(p['stack'])}</div></div>
<figure class="case-hero">{media(p, '../', large=True, eager=True)}<figcaption>{e(p.get('media_note', ''))}</figcaption></figure>
<div class="case-body">
<aside class="toc" aria-label="On this page"><p class="toc-title">On this page</p><ol>{toc_html}</ol></aside>
<article class="prose">
<p class="prose-lead">{e(p['summary'])}</p>
<section id="problem" aria-labelledby="problem-h"><h2 id="problem-h">The problem</h2><p>{e(p['problem'])}</p></section>
<section id="built" aria-labelledby="built-h"><h2 id="built-h">What I built</h2><ul>{''.join(f'<li>{inline(x)}</li>' for x in p['implementation'])}</ul></section>
<section id="how" aria-labelledby="how-h"><h2 id="how-h">How it works</h2><ol class="steps">{steps}</ol></section>
{facts_block(p)}
{gallery(p)}
<section id="results" aria-labelledby="results-h"><h2 id="results-h">Results</h2><p>{inline(p['results'])}</p></section>
<section id="learned" aria-labelledby="learned-h"><h2 id="learned-h">What I learned</h2><p>{inline(p['learning'])}</p></section>
</article>
</div>
<nav class="pager" aria-label="More projects"><a class="pager-prev" href="{e(prev_p['id'])}.html"><span>Previous project</span><b>{e(prev_p['title'])}</b></a><a class="pager-next" href="{e(next_p['id'])}.html"><span>Next project</span><b>{e(next_p['title'])}</b></a></nav>
</div></main>'''
    out += contact('../') + footer('../')
    (ROOT / 'projects' / f"{p['id']}.html").write_text(out, encoding='utf-8')


# ---------------------------------------------------------------- CV
# resume.html (public) and tailored variants such as cv/treehacks.html (unlisted).
# make_assets.py prints each variant to its PDF.

def cv_project(p):
    layer = layer_of(p)
    src = f' · <a href="{e(p["repo"])}">{e(p["repo"].replace("https://", ""))}</a>' if p['repo'] else ''
    points = ''.join(f'<li>{e(x)}</li>' for x in p['cv_points'])
    return f'''<li class="cv-item"><div class="cv-row"><h3>{e(p['title'])}</h3><span class="cv-tag tint-{e(layer['color'])}">{e(layer['name'])}</span><span class="cv-year">{e(p['year'])}</span></div>
<p class="cv-outcome">{e(p['outcome'])}.</p><ul class="cv-points">{points}</ul><p class="cv-foot">{e(', '.join(p['stack'][:5]))}{src}</p></li>'''


def cv_hackathon(h):
    badge = f'<span class="cv-badge">{e(h["result"])}</span>' if h.get('result') else ''
    return f'''<li class="cv-item"><div class="cv-row"><h3>{e(h['event'])}</h3>{badge}<span class="cv-year">{e(h.get('year') or '')}</span></div>
<p class="cv-text">{e(h['cv'])}</p></li>'''


def cv_sections(v):
    out = {}
    out['projects'] = f'<section class="cv-section"><h2>{e(v["projects_title"])}</h2><ul class="cv-list">{"".join(cv_project(P[i]) for i in v["projects"])}</ul></section>'
    out['hackathons'] = f'<section class="cv-section"><h2>Hackathons</h2><ul class="cv-list">{"".join(cv_hackathon(h) for h in C.get("hackathons", []))}</ul></section>'
    out['more'] = '<section class="cv-section"><h2>More projects</h2><ul class="cv-more">' + ''.join(
        f'<li><b>{e(P[i]["title"])}</b> — {e(P[i]["subtitle"])}</li>' for i in v['more']) + '</ul></section>'
    return ''.join(out[k] for k in v['order'])


def cv_sidebar(v):
    a = C['about']
    blocks = {}
    blocks['education'] = '<div class="cv-block"><h2>Education</h2><ul class="cv-plain">' + ''.join(
        f'<li><b>{e(x["school"])}</b><span>{e(x["program"])}{(", " + e(x["years"])) if x.get("years") else ""}</span></li>' for x in C['education']) + '</ul></div>'
    blocks['skills'] = '<div class="cv-block"><h2>Skills</h2><ul class="cv-plain">' + ''.join(
        f'<li><b>{e(g["group"])}</b><span>{e(", ".join(g["items"]))}</span></li>' for g in C['toolbox']) + '</ul></div>'
    blocks['languages'] = ('<div class="cv-block"><h2>Languages</h2><ul class="cv-plain">' + ''.join(
        f'<li><b>{e(l["name"])}</b><span>{e(l["level"])}</span></li>' for l in a['languages']) + '</ul></div>') if a.get('languages') else ''
    blocks['now'] = (f'<div class="cv-block"><h2>Right now</h2><p class="cv-now">{e(v["now"])}</p></div>') if v.get('now') else ''
    blocks['tools'] = ('<div class="cv-block"><h2>Tools</h2><ul class="cv-chips">' + ''.join(f'<li>{e(x)}</li>' for x in v['tools']) + '</ul></div>') if v.get('tools') else ''
    blocks['team'] = ('<div class="cv-block"><h2>What I bring</h2><ul class="cv-plain">' + ''.join(
        f'<li><b>{e(t["title"])}</b><span>{e(t["text"])}</span></li>' for t in v['team']) + '</ul></div>') if v.get('team') else ''
    blocks['tracks'] = ('<div class="cv-block"><h2>Tracks I’d build for</h2><ul class="cv-chips">' + ''.join(
        f'<li>{e(t)}</li>' for t in v['tracks']) + '</ul></div>') if v.get('tracks') else ''
    return ''.join(blocks[k] for k in v['sidebar'])


def cv_article(v):
    site = SITE.replace('https://', '')
    layers = ''.join(f'<span class="tint-{e(l["color"])}">{e(l["name"])}</span>' for l in reversed(C['layers']))
    return f'''<article class="cv" aria-label="Resume of {e(C['name'])}">
<header class="cv-head"><div class="cv-id"><span class="cv-mark" aria-hidden="true">{e(C['initials'])}</span><div><h1>{e(C['name'])}</h1><p class="cv-headline">{e(v['headline'])}</p></div></div>
<ul class="cv-contacts"><li><a href="mailto:{e(C['email'])}">{e(C['email'])}</a></li><li><a href="{e(SITE)}">{e(site)}</a></li><li><a href="{e(C['github'])}">{e(C['github'].replace('https://', ''))}</a></li><li><a href="{e(C['linkedin'])}">{e(C['linkedin'].replace('https://www.', ''))}</a></li><li>{e(C['location'])}</li></ul></header>
<div class="cv-layers" aria-hidden="true">{layers}</div>
<div class="cv-body"><div class="cv-main"><section class="cv-section"><h2>Profile</h2><p class="cv-profile">{e(v['profile'])}</p></section>{cv_sections(v)}</div>
<aside class="cv-side">{cv_sidebar(v)}</aside></div>
</article>'''


def build_resume():
    for key, v in C['cv_variants'].items():
        depth = v['page'].count('/')
        prefix = '../' * depth
        tools = f'<div class="resume-tools"><p>{"One page. The PDF has the same content." if key == "main" else "Tailored resume. The PDF has the same content."}</p><div><a class="btn btn-dark" href="{prefix}{e(v["pdf"])}" download>Download PDF</a><button class="btn btn-outline" type="button" data-print>Print</button></div></div>'
        if key == 'main':
            out = head(f"Resume — {C['name']}", f"Resume of {C['name']}, {C['role']} in Bratislava.", prefix, v['page'])
            out += header(prefix, 'resume', home=f'{prefix}index.html')
            out += f'<main id="main" class="resume-page"><div class="wrap">{tools}{cv_article(v)}</div></main>' + footer(prefix)
        else:
            out = head(f"Resume — {C['name']}", f"Resume of {C['name']}.", prefix, v['page'], extra='\n<meta name="robots" content="noindex">')
            out += f'<main id="main" class="resume-page resume-solo"><div class="wrap">{tools}{cv_article(v)}</div></main></body></html>'
        target = ROOT / v['page']
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(out, encoding='utf-8')


# ---------------------------------------------------------------- extras

def build_extras():
    urls = ['', 'resume.html'] + [f"projects/{p['id']}.html" for p in PROJECTS]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += ''.join(f'  <url><loc>{SITE}/{u}</loc><lastmod>{TODAY}</lastmod></url>\n' for u in urls) + '</urlset>\n'
    (ROOT / 'sitemap.xml').write_text(sitemap, encoding='utf-8')
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n', encoding='utf-8')

    todo = ['# Content to add', '', 'Generated by `build.py` from empty fields in `site-content.json`. Fill them in, run `python3 build.py`, then `python3 make_assets.py` to refresh the PDF and preview image.', '']
    if not C.get('photo'):
        todo.append('- [ ] **Photo** — add a portrait (e.g. `assets/photo.webp`, about 480×560) and set `"photo"` to its path. Until then the site shows an "MT" monogram.')
    if not C['about'].get('languages'):
        todo.append('- [ ] **Languages** — add `"languages": [{"name": "English", "level": "C1"}, …]` under `about`.')
    for x in C['education']:
        if not x.get('years'):
            todo.append(f'- [ ] **Education years** — `{x["school"]}`: add `"years"`, e.g. `"2024 – 2028 (expected)"`.')
    for h in C.get('hackathons', []):
        if not h.get('year'):
            todo.append(f'- [ ] **{h["event"]}** — add `"year"` (and `"where"` if useful) under `hackathons`.')
    todo.append('- [ ] **Status and target role** — check `"status"` and `about.looking_for`; they were written from your GitHub profile and may not match what you want.')
    for p in PROJECTS:
        missing = []
        if not p.get('role'):
            missing.append('`role` (what you personally did)')
        if p.get('team') and 'size' not in p.get('team', ''):
            missing.append('team size in `team`')
        if not p.get('demo') and p['layer'] == 'backend':
            missing.append('`demo` URL if it is deployed')
        if p['media']['kind'] == 'diagram' and p['id'] in ('prostapaper', 'secded', 'study-group'):
            missing.append('real screenshots or result plots for `gallery`')
        if not p['metrics']:
            missing.append('1–3 real numbers for `metrics`')
        if missing:
            todo.append(f'- [ ] **{p["title"]}** — ' + ', '.join(missing) + '.')
    (ROOT / 'TODO_CONTENT.md').write_text('\n'.join(todo) + '\n', encoding='utf-8')


if __name__ == '__main__':
    (ROOT / 'projects').mkdir(exist_ok=True)
    build_index()
    for i, p in enumerate(PROJECTS):
        build_project(p, i)
    build_resume()
    build_extras()
    print(f'Generated index.html, resume.html and {len(PROJECTS)} project pages.')
