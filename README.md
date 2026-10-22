# titovmykhailo.me

Personal portfolio and resume of **Mykhailo Titov** — software engineer and ICT student in Bratislava.
Live at [titovmykhailo.me](https://titovmykhailo.me), served by GitHub Pages from the `main` branch.

It is a static site with no framework and no npm build: one content file, one Python generator.

## Structure

| Path | What it is |
| --- | --- |
| `site-content.json` | **All content**: profile, stack layers, projects, metrics, toolbox, education |
| `build.py` | Generates every HTML page from the JSON (Python standard library only) |
| `styles.css`, `script.js` | Design and small progressive enhancements (sticky header, active section, copy email) |
| `make_assets.py` | Renders the CV PDF, the social preview image and the app icon (needs Playwright) |
| `assets/fonts/` | Self-hosted Archivo (variable width + weight) and JetBrains Mono |
| `assets/projects/<id>/` | Project screenshots (WebP) |
| `index.html`, `resume.html`, `projects/*.html`, `sitemap.xml`, `robots.txt` | Generated — don't edit by hand |
| `TODO_CONTENT.md` | Generated list of content that is still missing |

## Editing content

1. Edit `site-content.json`.
2. Run `python3 build.py`.
3. If you changed your name, role, layers or anything shown in the CV, also run `python3 make_assets.py`
   (`pip install playwright && playwright install chromium` the first time).
4. Commit and push. GitHub Pages publishes `main` automatically.

### Adding a project

Add an object to `projects` with the same fields as the existing ones, then reference its `id` in one of the
`layers` (that puts it on the hero diagram). To feature it in "Selected work", add the `id` to `featured_order`.

- `outcome` is the headline: what the project does or achieved, in one sentence.
- `metrics` are 1–3 real numbers (`value` + `label`). Leave the list empty rather than inventing one.
- `media` is either `{"kind": "image", "src": …, "width": …, "height": …, "alt": …}` or a diagram from `build.py`.
- `role`, `team` and `demo` are optional; they appear in the case study summary when filled in.

### Screenshots

Save them as WebP around 1600 px wide in `assets/projects/<id>/`, and always write an `alt` text that describes what is on screen.

## Local preview

```bash
python3 -m http.server 8000
# open http://localhost:8000
```
