"""Render the files that need a browser: the CV PDF, the social preview image
and the apple-touch-icon.

    pip install playwright && playwright install chromium
    python3 build.py && python3 make_assets.py

Optional — only needed after changing site-content.json. build.py alone is
enough for everything else.
"""
from pathlib import Path
import asyncio
import json

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent
C = json.loads((ROOT / 'site-content.json').read_text(encoding='utf-8'))
LAYERS = C['layers']

OG = f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="styles.css">
<style>
body{{margin:0;width:1200px;height:630px;background:var(--paper);overflow:hidden}}
.og{{display:grid;grid-template-columns:1.05fr 1fr;gap:48px;height:100%;padding:64px 64px 56px;box-sizing:border-box}}
.og h1{{font-weight:780;font-stretch:125%;font-size:96px;line-height:.9;letter-spacing:-.035em;margin:28px 0 28px}}
.og .role{{font-size:28px;font-weight:650;font-stretch:110%}}
.og .url{{position:absolute;left:64px;bottom:52px;font-size:24px;color:var(--ink-2)}}
.og ol{{display:grid;gap:12px;align-content:center;padding-left:30px;position:relative}}
.og ol::before{{content:'';position:absolute;left:9px;top:40px;bottom:40px;width:4px;border-radius:4px;background:var(--signal)}}
.og li{{position:relative;border-radius:16px;padding:22px 24px}}
.og li::before{{content:'';position:absolute;left:-29px;top:50%;width:14px;height:14px;margin-top:-7px;border-radius:50%;background:var(--paper);border:4px solid var(--signal)}}
.og li b{{display:block;font-size:26px;font-stretch:112%}}
.og li span{{font-size:19px;color:var(--deep)}}
</style></head><body><div class="og"><div><span class="brand-mark" style="width:64px;height:64px;font-size:24px;border-radius:16px">{C['initials']}</span>
<h1>{C['name'].replace(' ', '<br>')}</h1><p class="role">{C['role']}</p><p class="url">{C['site_url'].replace('https://', '')}</p></div>
<ol>{''.join(f'<li class="tint-{l["color"]}"><b>{l["name"]}</b><span>{l["note"]}</span></li>' for l in LAYERS)}</ol></div></body></html>'''


async def main():
    tmp = ROOT / '.og-render.html'
    tmp.write_text(OG, encoding='utf-8')
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page(viewport={'width': 1200, 'height': 630})
            await page.goto(tmp.as_uri())
            await page.wait_for_timeout(500)
            await page.screenshot(path=str(ROOT / 'assets' / 'og-image.png'))

            icon = await browser.new_page(viewport={'width': 180, 'height': 180})
            await icon.goto((ROOT / 'index.html').as_uri())
            await icon.set_content(f'<html><head><link rel="stylesheet" href="{(ROOT / "styles.css").as_uri()}"></head><body style="margin:0;background:#F2541B;display:grid;place-items:center;width:180px;height:180px"><span style="font:800 64px/1 Archivo, Arial;font-stretch:125%;color:#18202E;letter-spacing:.02em">{C["initials"]}</span></body></html>')
            await icon.wait_for_timeout(300)
            await icon.screenshot(path=str(ROOT / 'assets' / 'apple-touch-icon.png'))

            cv = await browser.new_page()
            await cv.goto((ROOT / 'resume.html').as_uri())
            await cv.wait_for_timeout(500)
            await cv.pdf(path=str(ROOT / C['cv_pdf']), format='A4', print_background=True, prefer_css_page_size=True)
            await browser.close()
    finally:
        tmp.unlink(missing_ok=True)
    print('Wrote assets/og-image.png, assets/apple-touch-icon.png and', C['cv_pdf'])


if __name__ == '__main__':
    asyncio.run(main())
