# Scientific Design System

The visual identity of `marcelo-website` combines the typographic rigor of a peer-reviewed physics journal with the clarity and modularity of an open-source research laboratory. All custom styling is defined in `assets/styles.scss` atop Quarto's Bootstrap 5 `cosmo` base.

## 1. Typography

| Role | Font Family | CSS Variable | Purpose |
|:---|:---|:---|:---|
| Editorial & Scientific Body | `Source Serif 4` | `--mma-serif` | Headings (`h1`–`h3`), article prose, blockquotes, publication titles, and venue citations |
| Interface & Metadata | `Inter` | `--mma-sans` | Navigation bar, action buttons, metadata boxes (`.project-meta`), author lists, and responsive controls |
| Code, Identifiers & Tags | `JetBrains Mono` | `--mma-mono` | Code blocks, inline code, DOIs, arXiv badges, domain eyebrows, and epistemic status pills |
| Mathematical Notation | MathJax 3 | — | Accessible display and inline LaTeX equations across HTML pages; native Typst math in downloadable PDFs |

## 2. Color Tokens

| Token | Hex | Semantic Usage |
|:---|:---|:---|
| `--mma-paper` | `#FAF9F5` | Warm archival off-white background reducing eye strain during long mathematical reading |
| `--mma-surface` | `#FFFFFF` | Elevated card, spotlight, and bibliography item surface |
| `--mma-surface-alt` | `#F3F0E8` | Secondary metadata panels, blockquotes, and badge backgrounds |
| `--mma-ink` | `#18202C` | High-contrast primary body text |
| `--mma-muted` | `#526071` | Secondary metadata and author bylines |
| `--mma-indigo` | `#1A3A5F` | Primary scientific accent, spotlight borders, and interactive link accents |
| `--mma-teal` | `#0F6E6E` | Secondary geometric/topological accent, category eyebrows, and blockquote rules |
| `--mma-amber` | `#9E5A0A` | Exploratory / preliminary status emphasis |
| `--mma-border` | `#DFDCD2` | Crisp 1px structural dividers and card outlines |

## 3. Core Component Classes

- **`.hero-lab` / `.hero-grid`**: Deep slate-indigo-teal hero panel with a subtle 26px radial lattice motif, researcher portrait (`.hero-portrait`), eyebrow, mission statement, and primary/secondary call-to-action buttons (`.btn-lab-primary`, `.btn-lab-secondary`).
- **`.qgr-spotlight`**: Prominent left-bordered research spotlight container highlighting **Quantum Gravity Research** on the homepage.
- **`.card-grid` & `.lab-card`**: Responsive CSS Grid (`repeat(auto-fit, minmax(285px, 1fr))`) for research domains, living projects, ventures, and featured outputs.
- **`.status-pill`**: Epistemic provenance badges distinguishing `.status-verified` (peer-reviewed or verified open-source software), `.status-preprint` (arXiv preprint / manuscript), and `.status-preliminary` (active / preliminary investigation).
- **`.pub-item`**: Structured bibliography card generated automatically by `scripts/build_publications.py` with `.pub-title`, `.pub-authors`, `.pub-venue`, and `.pub-links` badges (`DOI`, `arXiv`, `Zenodo`, `Code`, `Article`, `PDF`).
- **`.project-meta`**: Compact sans-serif provenance header on project and article pages listing epistemic status, source repository, license, and persistent identifiers.
- **`.video-container`**: Responsive 16:9 container for embedded research interviews and demonstrations.
- **`.bio-logos` & `.profile-links-bar`**: Structured institutional affiliation strip and external scholarly profile links.

## 4. Responsive & Accessibility Rules

- At viewports `<= 820px`, `.hero-grid` collapses cleanly into a single column with an appropriately scaled portrait (`148px x 148px`).
- Every `<img>` inside `<main>` is validated by `scripts/validate_site.py` to carry descriptive `alt` text (`fig-alt` in Quarto).
- Equations previously embedded as low-resolution bitmaps in historical WordPress posts are rendered via MathJax for screen-reader compatibility and crisp zoom scaling.
