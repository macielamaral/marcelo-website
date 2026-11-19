# Marcelo Maciel Amaral — Scientific Research Website

Git-native **Quarto + GitHub Pages** research website for **Marcelo Maciel Amaral** (`www.marcelomacielamaral.com`), theoretical physicist, research scientist, and founder of Gauge Freedom, Inc.

> *Love and Reason — Open-sourcing the code of reality.*

---

## 1. Architecture Overview

| Path | Purpose |
|:---|:---|
| `_quarto.yml` | Global Quarto configuration, navigation, SEO/OpenGraph metadata, and render exclusions (`!private/**`) |
| `assets/styles.scss` | Scientific journal + open research lab theme (`Source Serif 4`, `Inter`, `JetBrains Mono`) |
| `index.qmd` | Homepage featuring **Quantum Gravity Research**, three broad research directions, current academic work, projects, and latest writing |
| `research/` | Research overview (`/about/` alias) + 6 domain pages (Quantum Gravity, TQC, Gauge Theory, Energy-Efficient AI, Information Geometry, Foundations) |
| `publications/` | Structured bibliography (`references.bib`), auto-generated views, and full HTML + Typst PDF articles (`publications/articles/`) |
| `projects/` | Living research & open-source software records backed by `data/projects.yml` |
| `notes/` | Technical notes, computational essays, and reusable agent template (`notes/_template.qmd`) |
| `blog/`, `2023/`–`2026/`, `category/` | Blog index (`/blog/` + RSS `/blog/index.xml`), all 14 historical essays retained at their exact WordPress `/YYYY/MM/DD/<slug>/` permalinks, and `/category/{science,code,culture,open-sourcing}/` archive pages |
| `venture/`, `bio/`, `creator/`, `books/`, `consulting-services/`, `contact/`, `privacy-policy/` | Venture, biography, music and books (`/gpts/` noindex redirect to `/creator/`), consulting, contact, and static-site privacy policy |
| `data/` | `publications.yml`, `projects.yml`, `migration-inventory.yml`, and `schemas/agent-submission.schema.json` |
| `scripts/` | `build_publications.py`, `upgrade_redirects.py`, `validate_site.py`, `import_research_update.py`, and `link_zenodo.py` |
| `config/custom-domain/` | Staged (inactive) `CNAME` and `robots.txt` templates for future `www.marcelomacielamaral.com` DNS cutover |
| `docs/` | `design-system.md`, `migration-report.md`, `zenodo-workflow.md`, and `deployment-and-domain.md` |
| `AGENTS.md`, `STATUS.md`, `NEXT.md` | Agent governance policy and Shared Memory Protocol state |

> **Privacy Boundary:** `private/` is strictly local, `.gitignore`-excluded, and blocked from Quarto rendering and CI validation.

---

## 2. Local Build, Preview & Validation

Requires **Python 3.10+** (`pyyaml`) and **Quarto CLI 1.6+** (tested on Quarto `1.11.9`).

```bash
# 1. Regenerate BibTeX and structured publication includes from data/publications.yml
python3 scripts/build_publications.py

# 2. Render full website (HTML + Typst PDFs) into _site/
quarto render

# 3. Validate internal links, media, alt text, aliases, SEO metadata, and privacy boundaries
python3 scripts/validate_site.py

# 4. Launch live local preview server
quarto preview
```

---

## 3. Maintainer Workflows

### Add a Paper or Preprint
1. Add an entry to `data/publications.yml` with verified `title`, `authors`, `year`, `type`, `category`, and `doi` / `arxiv` / `repo_url`. Use `date: "YYYY-MM-DD"` when the full publication date is verified. Gauge Freedom Field Notes use `type: research-note`, `status: preprint`, and their original venue name.
2. Run `python3 scripts/build_publications.py && quarto render && python3 scripts/validate_site.py`.

Keep publication IDs stable when a preprint gains a journal version: update the existing record and retain its arXiv access link. Manuscripts in preparation belong on project pages, not in the bibliography.

### Add a Full HTML + PDF Research Article
1. Copy `notes/_template.qmd` to `publications/articles/<slug>/index.qmd` (or `notes/<slug>/index.qmd`).
2. Add `article_url` (and `pdf_url` if dual-rendered with `format: typst`) to its entry in `data/publications.yml`, then rebuild and validate.

### Add or Update a Living Project
1. Add or update metadata in `data/projects.yml` and create/edit `projects/<slug>.qmd`.
2. Render and run `python3 scripts/validate_site.py`.

### Publish a New Blog Post
1. Create `YYYY/MM/DD/your-slug/index.qmd` with `title`, `author`, `date`, `categories`, `description`, and optional `image` + `image-alt`.
2. Run `quarto render && python3 scripts/validate_site.py`. Quarto automatically updates `/blog/`, `/category/.../`, homepage highlights, and `/blog/index.xml` (RSS).

### Link an Existing Zenodo DOI
See `docs/zenodo-workflow.md`:
```bash
python3 scripts/link_zenodo.py 10.5281/zenodo.<RECORD_ID> --pub-id <PUB_ID> --write
python3 scripts/build_publications.py && quarto render && python3 scripts/validate_site.py
```

### Stage an Approved Agent Research Update
See `AGENTS.md` and `data/schemas/agent-submission.schema.json`:
```bash
python3 scripts/import_research_update.py --dry-run path/to/manifest.json
python3 scripts/import_research_update.py path/to/manifest.json
```

### Deploy to GitHub Pages & Custom Domain Cutover
- Automatic build, validation, and GitHub Pages deployment are configured in `.github/workflows/publish.yml`.
- Follow `docs/deployment-and-domain.md` for initial preview activation at `https://macielamaral.github.io/marcelo-website/` and future DNS cutover of `www.marcelomacielamaral.com` without disrupting DreamHost email.
