"""Regenerate the static GitHub Pages site: python3 build.py (standard library only)."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parent
CONTENT = json.loads((ROOT / 'site-content.json').read_text())
PROJECTS = CONTENT['projects']

def e(value):
    return escape(str(value), quote=True)

def head(title, description, prefix=''):
    return f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(description)}">
<meta name="theme-color" content="#fffaf1"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}"><meta property="og:type" content="website">
<link rel="icon" type="image/svg+xml" href="{prefix}favicon.svg"><link rel="stylesheet" href="{prefix}styles.css"><script src="{prefix}script.js" defer></script>
</head><body><a class="skip" href="#main">Skip to content</a>'''

def header(prefix=''):
    home = prefix + 'index.html' if prefix else ''
    return f'''<header class="site-header shell">
<a class="brand" href="{home or '#top'}" aria-label="Mykhailo Titov home"><span class="brand-mark" aria-hidden="true">✳</span><span>MYKHAILO<br>TITOV</span></a>
<nav class="site-nav" aria-label="Main navigation"><a href="{home}#work">Work</a><a href="{home}#about">About</a><a href="{home}#contact">Contact</a></nav>
<a class="header-link" href="{e(CONTENT['github'])}">GitHub ↗</a></header>'''

def footer(prefix=''):
    home = prefix + 'index.html' if prefix else ''
    return f'''<section class="contact-section" id="contact" aria-labelledby="contact-title"><div class="shell">
<div class="contact-top"><p class="eyebrow">HAVE A PROJECT OR AN INTERESTING PROBLEM?</p><span>BASED IN BRATISLAVA, SK</span></div>
<h2 class="contact-title" id="contact-title">Let’s make<br><em>something</em> work. ↗</h2>
<div class="contact-links"><a class="contact-mail" href="mailto:{e(CONTENT['email'])}">{e(CONTENT['email'])} ↗</a><div class="socials"><a href="{e(CONTENT['github'])}">GitHub ↗</a><a href="{e(CONTENT['linkedin'])}">LinkedIn ↗</a></div><button class="copy-email" type="button" data-copy-email="{e(CONTENT['email'])}">Copy email</button></div>
<p class="contact-copied" id="copy-status" role="status" aria-live="polite"></p></div></section>
<footer class="footer shell"><p>© <span data-year>2026</span> Mykhailo Titov</p><a href="{e(CONTENT['github'])}/TitovMykhailo.github.io">Site source ↗</a><a class="back-top" href="#top">BACK TO TOP ↑</a></footer>
<p class="contact-print shell" hidden>Mykhailo Titov · {e(CONTENT['email'])} · github.com/TitovMykhailo</p></body></html>'''

def toolbar(label):
    return f'<div class="mock-toolbar"><i></i><i></i><i></i><span>{label}</span></div>'

def graphic(kind):
    if kind == 'network':
        nodes = [(64,70,'A'),(305,48,'B'),(417,133,'C'),(336,235,'D'),(103,225,'E')]
        lines = ''.join(f'<line class="network-edge" x1="240" y1="140" x2="{x}" y2="{y}"/>' for x,y,_ in nodes)
        points = ''.join(f'<circle class="node" cx="{x}" cy="{y}" r="20"/><circle class="node-core" cx="{x}" cy="{y}" r="4"/><text x="{x-3}" y="{y+38}">{label}</text>' for x,y,label in nodes)
        return f'''<svg class="network-graphic" viewBox="0 0 480 290" aria-hidden="true"><ellipse cx="240" cy="145" rx="204" ry="109" fill="none" stroke="#a9c9b6" stroke-dasharray="3 7"/>{lines}<path class="network-route" d="M64 70 240 140 336 235 417 133"/><circle class="hub" cx="240" cy="140" r="49"/><text class="hub-text" x="206" y="147">KIZU</text>{points}<text class="link-label" x="104" y="100">DISCOVER</text><text class="link-label" x="285" y="190">ADAPT</text><text x="174" y="278" letter-spacing="2">ROUTE. ADAPT. REPEAT.</text></svg>'''
    if kind == 'bits':
        return '''<div class="bits-object" aria-hidden="true"><div class="bits-title"><small>EXTENDED HAMMING (8,4)</small>Make every bit count.</div><div class="bit-row"><span>1</span><span>0</span><span>1</span><span class="error-bit">?</span><span>0</span><span>1</span><span>1</span><span>0</span></div><div class="bits-note">ENCODE → TRANSMIT → CHECK → CORRECT</div></div>'''
    if kind == 'tasks':
        return f'''<div class="browser-mock" aria-hidden="true">{toolbar('TASK TRACKER')}<div class="task-layout"><div class="mock-sidebar"><strong>task.</strong><span class="selected">Overview</span><span>Projects</span><span>Calendar</span><span>Analytics</span><span>Time tracker</span></div><div class="mock-main"><p class="mock-overline">YOUR WORKSPACE</p><p class="mock-title">A little more organized.</p><div class="mock-stats"><div class="mock-stat"><b>Build</b><small>PROJECTS</small></div><div class="mock-stat"><b>Plan</b><small>TASKS</small></div><div class="mock-stat"><b>Track</b><small>TIME</small></div></div><div class="mock-board"><div>TO DO<div class="mini-task">Sketch the idea<i></i></div></div><div>IN PROGRESS<div class="mini-task">Make it work<i class="purple"></i></div></div><div>DONE<div class="mini-task">Ship a first step<i class="green"></i></div></div></div></div></div></div>'''
    if kind == 'document':
        return '''<div class="document-preview" aria-hidden="true"><div class="paper-sheet"><b>Source document</b><i></i><i></i><i></i><i class="highlight"></i><i></i><i></i><i></i><i class="highlight"></i><i></i><i></i></div><div class="review-sheet"><h4>Review the record.</h4><div class="review-row"><span>Source field</span><span>Review ↗</span></div><div class="review-row"><span>Proposed value</span><span>Check ↗</span></div><div class="review-row"><span>Diagram</span><span>Compare ↗</span></div><div class="review-button">Human review comes first</div></div></div>'''
    if kind == 'agent':
        return '''<div class="agent-pipeline" aria-hidden="true"><span>⌕</span><i>→</i><span>AI</span><i>→</i><span>✓</span></div>'''
    if kind == 'video':
        return '''<div class="simple-visual-title" aria-hidden="true"><small>VOICE → TIMELINE</small>A workflow<br>with a rhythm.</div><div class="video-timeline" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div>'''
    if kind == 'clinic':
        return f'''<div class="browser-mock" aria-hidden="true">{toolbar('APPOINTMENT SYSTEM')}<div class="mock-main"><p class="mock-overline">FIND A TIME THAT WORKS</p><p class="mock-title">Your next appointment.</p><div class="clinic-slots"><span>09:00</span><span>09:30</span><span>10:00</span><span>10:30</span><span>11:00</span><span>11:30</span></div><div class="mock-chat-row">Your booking has its own conversation.</div></div></div>'''
    return f'''<div class="browser-mock" aria-hidden="true">{toolbar('STUDY GROUP')}<div class="mock-main"><p class="mock-overline">A LITTLE LESS SCATTERED</p><p class="mock-title">Learn, together.</p><div class="mock-chat-row">Share a useful resource.</div><div class="mock-chat-row">Plan the next task.</div><div class="mock-chat-row">Keep the conversation going.</div></div></div>'''

def visual(p, large=False):
    label = 'CONCEPT DIAGRAM' if p['visual'] in ('network','bits','agent','video') else 'INTERFACE ILLUSTRATION'
    return f'''<div class="project-visual {e(p['color'])}{' case-hero-visual' if large else ''}"><span class="visual-label">{e(p['title'] if p['id'] != 'secded' else 'SEC-DED / VERILOG')}</span>{'' if large else '<span class="preview-arrow" aria-hidden="true">↗</span>'}{graphic(p['visual'])}<span class="visual-footnote">{label}</span></div>'''

def card(p, i):
    return f'''<article class="work-card reveal"><a href="projects/{p['id']}.html" aria-label="Explore {e(p['title'])}">{visual(p)}<div class="project-caption"><div><h3>{e(p['title'])}</h3><p>{e(p['subtitle'])}</p></div><span class="index">0{i}</span></div></a><div class="project-tags">{''.join(f'<span>{e(t)}</span>' for t in p['stack'])}</div></article>'''

def catalog_row(p,i):
    return f'''<a class="catalog-item" href="projects/{p['id']}.html" data-category="{e(p['category'])}"><span class="catalog-number">0{i}</span><div><h3>{e(p['title'])}</h3><p>{e(p['subtitle'])}</p></div><span class="catalog-stack">{e(' · '.join(p['stack'][:3]))}</span><span class="catalog-arrow" aria-hidden="true">↗</span></a>'''

featured = [p for p in PROJECTS if p['featured']]
more = [p for p in PROJECTS if not p['featured']]
home = head('Mykhailo Titov — Software, Networks & Digital Systems', 'A portfolio of software, AI automation, mesh networking and Verilog research by Mykhailo Titov.')
home += '<div id="top"></div>' + header()
home += '''<main id="main"><section class="hero shell" aria-labelledby="hero-title"><div class="hero-meta"><p class="eyebrow"><span class="dot"></span>MYKHAILO TITOV / ICT STUDENT</p><p class="eyebrow">BRATISLAVA, SK<br>ALWAYS LEARNING. ALWAYS BUILDING.</p></div><div class="hero-heading"><p class="hero-kicker">Curious by nature.</p><div class="hero-art" aria-hidden="true"><span class="chip">&lt;/&gt;</span><span class="tiny-star">✳</span></div><h1 id="hero-title"><span class="orange">BUILDING</span><br>REAL THINGS.</h1></div><div class="hero-bottom"><p class="hero-description">I’m <strong>Mykhailo</strong>, an ICT student exploring how software, networks and digital systems fit together. I turn ideas into projects I can build, test and keep improving.</p><div class="hero-bottom-right"><p>PYTHON & JAVA · AI AUTOMATION<br>NETWORKS · VERILOG RESEARCH</p><a class="round-link" href="#work" aria-label="Explore selected work">↘</a></div></div></section><div class="topics"><div class="shell"><span>Software</span><i aria-hidden="true">✳</i><span>AI & automation</span><i aria-hidden="true">✳</i><span>Networks</span><i aria-hidden="true">✳</i><span>Digital systems</span></div></div>
<section class="section shell" id="work" aria-labelledby="work-title"><div class="section-heading"><div><p class="eyebrow">01 / IDEAS INTO IMPLEMENTATIONS</p><h2 class="section-title" id="work-title">Selected <em>work.</em></h2></div><p>A few things I’ve been building.<br>Open a project to see the thinking behind it.</p></div><div class="work-grid">'''
home += ''.join(card(p,i+1) for i,p in enumerate(featured))
home += '''</div></section><section class="section shell catalog-section" aria-labelledby="catalog-title"><div class="filter-row"><h2 id="catalog-title">More to explore ↗</h2><div class="filters" role="group" aria-label="Filter more projects"><button class="filter active" data-filter="all" aria-pressed="true">Everything</button><button class="filter" data-filter="software" aria-pressed="false">Full-stack</button><button class="filter" data-filter="ai" aria-pressed="false">AI & tools</button></div></div><p class="sr-only" id="filter-status" aria-live="polite">Showing 4 projects.</p><div class="catalog-list">'''
home += ''.join(catalog_row(p,i+1) for i,p in enumerate(more))
home += '''</div></section><section class="about-section" id="about" aria-labelledby="about-title"><div class="shell section"><div class="about-layout"><div class="about-copy"><p class="eyebrow">02 / THE PERSON BEHIND THE PROJECTS</p><h2 class="section-title" id="about-title">A curious mind.<br>An <em>engineering</em> habit.</h2><p class="about-lead">I like understanding what happens underneath the interface.</p><p>That curiosity takes me from Java backends and Python automation to network protocols and error correction in Verilog. I enjoy connecting the theory to something I can actually implement and inspect.</p><p>I study Information and Communication Technologies at STU FEI in Bratislava and Computer Science at Dnipro University of Technology. Team projects and hackathons give me a place to put those ideas into practice.</p><span class="about-sticker"><span aria-hidden="true">✳</span> MAKE → TEST → LEARN → REPEAT</span></div><div class="skills-block"><h3>My current toolbox.</h3><div class="skill-row"><strong>SOFTWARE</strong><span>Java · Spring Boot · Python · C · SQL<br>REST APIs · React · TypeScript</span></div><div class="skill-row"><strong>AI & TOOLS</strong><span>Azure OpenAI · LLM workflows<br>Filtering · scoring · process automation</span></div><div class="skill-row"><strong>NETWORKS</strong><span>IPv4 / IPv6 · UDP · routing<br>Mesh networks · Docker simulations</span></div><div class="skill-row"><strong>DIGITAL</strong><span>Verilog · error-correcting codes<br>Testbenches · MATLAB · channel modeling</span></div><div class="skill-row"><strong>WORKFLOW</strong><span>Git & GitHub · Linux · Docker<br>Documentation · collaborative development</span></div><button class="print-control" data-print type="button">Print / save portfolio as PDF ↗</button></div></div><div class="education"><div><p class="eyebrow">EDUCATION / BRATISLAVA</p><h3>Slovak University of Technology</h3><p>Faculty of Electrical Engineering and Information Technology<br>Information and Communication Technologies · Bachelor’s studies</p></div><div><p class="eyebrow">EDUCATION / DNIPRO</p><h3>Dnipro University of Technology</h3><p>Computer Science<br>Parallel bachelor’s studies</p></div></div></div></section></main>'''
home += footer()
(ROOT / 'index.html').write_text(home)

for i,p in enumerate(PROJECTS):
    prefix = '../'
    page = head(f"{p['title']} — Mykhailo Titov", p['summary'], prefix)
    page += '<div id="top"></div>' + header(prefix)
    page += f'''<main id="main" class="shell"><p class="case-breadcrumb"><a href="../index.html#work">← All work</a> / {e(p['title'])}</p><div class="case-heading"><p class="eyebrow">{e(p['label'])}</p><h1>{e(p['title'])}</h1><p class="case-summary">{e(p['summary'])}</p></div><div class="case-meta"><div><small>FOCUS</small><strong>{e(p['category'].capitalize())}</strong></div><div><small>TOOLS</small><strong>{e(' · '.join(p['stack']))}</strong></div><div><small>SOURCE</small><strong>{'Public GitHub repository' if p['repo'] else 'Project shared directly'}</strong></div></div>{visual(p,True)}<div class="case-columns"><aside class="case-aside" aria-label="Project page sections"><a href="#problem">01 / The problem</a><a href="#implementation">02 / Implementation</a><a href="#architecture">03 / How it fits together</a><a href="#status">04 / Current state</a></aside><div class="case-content"><section id="problem"><h2>The problem.</h2><p>{e(p['problem'])}</p></section><section id="implementation"><h2>Inside the project.</h2><ul>{''.join(f'<li>{e(item)}</li>' for item in p['implementation'])}</ul></section><section id="architecture"><h2>How it fits together.</h2><div class="architecture">{''.join(f'<div><small>0{j+1}</small><strong>{e(step)}</strong></div>' for j,step in enumerate(p['architecture']))}</div><p>{e(p['learning'])}</p></section><section id="status"><h2>Current state.</h2><div class="status-note"><p>{e(p['status'])}</p></div><div class="case-actions">'''
    if p['repo']:
        page += f'<a class="pill-button dark" href="{e(p["repo"])}">Explore the repository ↗</a>'
    else:
        page += f'<a class="pill-button dark" href="mailto:{e(CONTENT["email"])}?subject={e(p["id"])}">Ask me about this project ↗</a>'
    page += '<a class="pill-button" href="../index.html#work">Back to selected work</a></div></section></div></div>'
    next_p = PROJECTS[(i+1)%len(PROJECTS)]
    page += f'<a class="case-next" href="{next_p["id"]}.html"><div><p class="eyebrow">KEEP EXPLORING</p><h2>{e(next_p["title"])}</h2></div><span class="round-link" aria-hidden="true">↗</span></a></main>'
    page += footer(prefix)
    (ROOT / 'projects' / f'{p["id"]}.html').write_text(page)

notes = '''# Content sources and editing

This is a buildless static site ready for GitHub Pages. No server, npm install or API keys are required.

## Editing

- Edit `site-content.json` for projects and public contact details.
- Run `python3 build.py` to regenerate `index.html` and `projects/*.html`.
- Edit `styles.css` for colors and layout; edit `script.js` for progressive enhancements.
- Upload the generated pages and assets to the root of `TitovMykhailo.github.io`.
- Keep `CNAME` as `titovmykhailo.me` and configure GitHub Pages to serve `main` / root.
- The zip already contains generated pages. Running the generator is optional unless you edit project data.

## Research notes

Project copy was checked against the following public repository files on 21 October 2026. The underlying applications were not run or independently benchmarked while building this portfolio.

'''
for p in PROJECTS:
    notes += f'- {p["title"]}: {p["repo"] or "User-supplied project details"}; {p["source"]}.\n'
notes += '''
Public contact details and the current software/AI focus came from `TitovMykhailo/TitovMykhailo/README.md`.

16-QAM Mapper is excluded at Mykhailo’s explicit request; it is not his project.

All project previews are original code-native diagrams or interface illustrations, labelled as such. They are not copied screenshots, working application demos, measured results or evidence of production use. No real medical documents or patient data are included.

Design references: junhyungpark.com (spacious project-led structure) and whyramachandran.design (warm background, orange accent, expressive typography). The implementation is original and uses no images, brand marks or authored case-study content from those sites.

## Checks and browser support

The site uses semantic HTML, visible keyboard focus, native links/buttons, responsive CSS, reduced-motion support and a printable layout. External Google Fonts are optional; system fallbacks are provided. Project descriptions and links remain available without JavaScript. JavaScript adds filters, reveal transitions, print and copy-email controls.
'''
(ROOT / 'SOURCE_NOTES.md').write_text(notes)
print(f'Generated index and {len(PROJECTS)} project pages.')
