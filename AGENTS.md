# AGENTS.md — Autonomous Maintenance & Scientific Publishing Protocol

## 1. Mission

This repository (`macielamaral/marcelo-website`) powers the personal scientific website and open-science research hub of **Marcelo Maciel Amaral** (Theoretical Physicist, Research Scientist, Founder).

Core scientific mission: **Open-sourcing the code of reality** — connecting research across quantum gravity, gauge theory, quasicrystalline spin foams, aperiodic topological quantum computing, information geometry, energy-efficient artificial intelligence, and the foundations of physics.

## 2. Public / Private Data Policy (MANDATORY)

> **Public by default for website content; private by default for unpublished or unapproved research.**

1. **Public Repository Assumption:** This Git repository is intended to be **PUBLIC**. Every committed file, commit message, metadata record, and rendered artifact must be safe for unrestricted public distribution.
2. **Strict `private/` Boundary:** The `private/` directory holds local working material and prompts. It is excluded via `.gitignore` and excluded from Quarto rendering in `_quarto.yml`.
   - Never run `git add -f` on anything in `private/`.
   - Never copy files, text, or figures from `private/` into published pages unless explicitly instructed by Marcelo.
   - Never reference `private/` inside scripts or GitHub Actions workflows.
3. **No Implied Publication Permission:** Having filesystem or Git access to another local or remote research repository **never** grants permission to publish its contents, benchmarks, manuscripts, collaborator names, or preliminary results. Only import material from **publicly released sources** or material **explicitly approved by Marcelo** for website publication.
4. **Forbidden Content:** Never commit API keys, `.env` files, tokens, passwords, private correspondence, collaborator contact details, restricted manuscripts, or proprietary venture documents. If sensitive data is ever found in Git history, stop immediately and report remediation steps before continuing.
5. **Confidential Collaborations:** Genuine confidential research belongs in dedicated private repositories, never solely in a Git-ignored subdirectory of this public site.

## 3. Shared Memory Protocol

Before executing any non-trivial task, read `README.md`, `STATUS.md`, and `NEXT.md` alongside this `AGENTS.md`. Before concluding a task, update `STATUS.md` and `NEXT.md` cleanly—pruning completed items and stale notes so collective context stays compact.

## 4. Technology Stack & Repository Structure

- **Framework:** Quarto (`>= 1.6`, verified on `1.11.x`) static website generator, Markdown/Qarto (`.qmd`), SCSS (`assets/styles.scss`), YAML data (`data/`), BibTeX (`publications/references.bib`), and Python 3 (`>= 3.10`, standard library + PyYAML) for data generation and validation.
- **Zero-Framework Bloat:** Do not introduce React, Next.js, or heavy client-side JS frameworks. Use native Quarto listings, Pandoc fenced divs, semantic HTML, CSS Grid/Flexbox, and MathJax.
- **Subpath Compatibility:** Use Quarto-native `.qmd` targets or relative paths for internal links and media (`[Publications](publications/index.qmd)` or relative `../assets/...`), never hardcoded domain-root raw HTML `<a href="/...">`, so builds work identically under local preview, the GitHub Pages project subpath (`/marcelo-website/`), and the production custom domain (`www.marcelomacielamaral.com`).

```text
marcelo-website/
├── AGENTS.md                  # Mandatory agent instructions and policies
├── README.md                  # Architecture, quickstart, and maintainer guide
├── STATUS.md                  # Current repository state and pending approvals
├── NEXT.md                    # Short-term roadmap
├── _quarto.yml                # Quarto site configuration
├── index.qmd                  # Homepage (must preserve "Quantum Gravity Research" H2)
├── bio/index.qmd              # Full academic and professional biography (/bio/)
├── contact/index.qmd          # Verified public profiles and contact (/contact/)
├── consulting-services/       # Scientific consulting overview (/consulting-services/)
├── venture/index.qmd          # Gauge Freedom, Inc. & AperiodiQ (/venture/)
├── creator/index.qmd          # Music and books (/creator/, noindex redirect from /gpts/)
├── books/index.qmd            # Book series landing page (/books/)
├── privacy-policy/index.qmd   # Personal website privacy policy (/privacy-policy/)
├── research/                  # Research overview (/research/, alias /about/) + 6 domain pages
├── projects/                  # Living scientific project pages
├── publications/              # Structured bibliography, BibTeX, and full articles
├── notes/                     # Technical notes and reusable article template (_template.qmd)
├── blog/                      # Historical and new blog posts (preserving WP URL aliases)
├── data/                      # Single-source YAML (publications, projects, migration, schemas)
├── scripts/                   # Publication builder, Zenodo linker, agent importer, validator
├── docs/                      # Design system, migration report, Zenodo & DNS cutover guides
├── assets/                    # styles.scss, images/, and media/
└── private/                   # Git-ignored local working directory (NEVER PUBLISH)
```

## 5. Scientific Integrity Requirements

Agents working on this website must uphold strict scientific standards:

- **Never fabricate** experimental data, numerical improvements, theorems, citations, arXiv IDs, DOIs, repositories, collaborators, or institutional affiliations.
- **Distinguish epistemic status clearly:** Every publication and project must accurately state whether it is a *Peer-Reviewed Journal Article*, *Conference Proceeding*, *Preprint*, *Technical Note*, *Open-Source Software*, or *Preliminary / Draft Investigation*.
- **Traceability:** Link scientific claims to public DOIs, arXiv preprints, figures, or pinned public GitHub commits.
- **Biographical fidelity:** Never silently rewrite Marcelo's biography or personal voice with generic AI marketing prose.
- **Mathematical rigor:** Check dimensional consistency, notation definitions, limiting cases, and clean LaTeX rendering (`$...$` and `$$...$$`).

## 6. Critical SEO & URL Continuity Rules

1. **"Quantum Gravity Research" Requirement:** The homepage (`index.qmd`) **must** retain a prominent, semantically meaningful `<h2>` heading containing the exact phrase `Quantum Gravity Research`, alongside natural context distinguishing the research field of quantum gravity from Marcelo's collaboration with the Los Angeles non-profit organization Quantum Gravity Research (`quantumgravityresearch.org`).
2. **Permalink Preservation:** Do not break existing WordPress URLs (`/bio/`, `/venture/`, `/contact/`, `/consulting-services/`, `/privacy-policy/`, `/books/`, `/about/` via alias, `/gpts/` via alias, and `/YYYY/MM/DD/<slug>/` blog permalinks via Quarto `aliases:`). Whenever moving or renaming a page, add the old path to `aliases:` and record it in `data/migration-inventory.yml`.
3. **Technical SEO:** Every `.qmd` page must define a clear `title`, `description`, heading hierarchy (single `h1` from Quarto title, `h2`/`h3` in body), and `fig-alt` / image `alt` text.

## 7. Publication, Article Import & Zenodo Workflows

### Adding or Updating a Publication
1. Edit `data/publications.yml` with verified metadata (never invent a DOI; leave `doi: null` or `zenodo_doi: null` when pending).
2. Run `python3 scripts/build_publications.py` to regenerate `publications/references.bib` and `publications/_listings.md`.
3. Render and validate the site.

### Importing an Approved Research Update from Another Repository
Follow the lifecycle: `Research repository → verified public/approved results → submission manifest → website import → validation → human approval`.
1. Prepare or receive a JSON/YAML manifest conforming to `data/schemas/agent-submission.schema.json` (or copy `notes/_template.qmd` into `notes/<slug>/index.qmd` or `publications/articles/<slug>/index.qmd`).
2. Run `python3 scripts/import_research_update.py <manifest.json>` to validate provenance fields (public repo URL, commit SHA, epistemic status, explicit approval flag) and scaffold/update the target page.
3. Verify equations, figures, and citations, then run full site validation.

### Zenodo DOI Handling
- **NEVER automatically deposit or publish records to Zenodo.** Depositing to Zenodo creates permanent DOIs and requires Marcelo's explicit authorization.
- Only after a record is publicly minted on Zenodo, link it via `python3 scripts/link_zenodo.py <record_id_or_doi> --pub-id <id>` (read-only query against `https://zenodo.org/api/records`) or edit `data/publications.yml`. See `docs/zenodo-workflow.md`.

## 8. Build, Validation & Deployment Commands

Run from the repository root (`~/lab/research/marcelo-website`):

```bash
# 1. Regenerate BibTeX & structured publication includes from data/publications.yml
python3 scripts/build_publications.py

# 2. Render the complete Quarto website into _site/
quarto render

# 3. Run automated validation (privacy boundary, internal links, images, DOIs, SEO checks)
python3 scripts/validate_site.py

# 4. Local live preview
quarto preview
```

### Deployment & Approval Gates
- **Do NOT** push to `origin` (`git push`), enable GitHub Pages in remote repo settings, modify DreamHost/WordPress, or alter DNS (`marcelomacielamaral.com`) without Marcelo's explicit approval.
- Keep diffs focused, clean, and free of explanatory code-comment cruft. Always run `quarto render && python3 scripts/validate_site.py` before concluding any edit session.
