# WordPress to Quarto Migration Report

**Source Site:** `https://www.marcelomacielamaral.com/` (WordPress on DreamHost)  
**Target Site:** Quarto static website in `marcelo-website`  
**Audit Date:** 2026-11-11  
**Machine-Readable Inventory:** `data/migration-inventory.yml`

## 1. Discovery Summary

Inspection of the live WordPress site via `/wp-json/wp/v2/` (`pages`, `posts`, `categories`, `tags`, `media`, `types`), XML sitemaps (`sitemap.xml`, `post-sitemap.xml`, `page-sitemap.xml`, `category-sitemap.xml`), HTML/JSON-LD inspection, Crossref/arXiv bibliography verification, and desktop/mobile headless Chrome screenshots identified:

- **11 WordPress Pages** (10 public content pages + 1 default WordPress `sample-page` placeholder).
- **14 Published Blog Posts** spanning `2023-09-23` through `2026-09-21`.
- **5 Categories**: `Science`, `Code`, `Culture`, `Open-Sourcing`, plus unused `Uncategorized` (0 posts).
- **0 Tags**.
- **39 Media Attachments**: 25 active images, audio, and video assets (`8.59 MB` total) were downloaded into `assets/images/` and `assets/media/`; bitmap equation screenshots were upgraded to native MathJax; 2 unlinked attachments were intentionally excluded (detailed below).

## 2. Direct URL Path Preservation & Redirect Strategy

**26 of 28** public WordPress routes (8 of 10 pages, all **14 of 14** blog posts at `/YYYY/MM/DD/<slug>/`, and all **4 of 4** category archive pages at `/category/{science,code,culture,open-sourcing}/`) retain their **exact WordPress URL paths directly** as first-class HTML pages in Quarto without client-side redirects.

For the remaining **2** renamed section hubs (`/about/` -> `/research/` and `/gpts/` -> `/creator/`), Quarto `aliases:` upgraded by `scripts/upgrade_redirects.py` (`project.post-render`) emit `<link rel="canonical">`, `<meta http-equiv="refresh" content="0; url=...">`, hash-preserving JavaScript replacement, and semantic HTML fallback links.

| Original WordPress URL | Quarto Canonical Path | Legacy Redirect | Status |
|:---|:---|:---|:---|
| `/` | `/` | — | Retained directly & upgraded |
| `/about/` | `/research/` | `/about/` | Canonical + meta-refresh + JS redirect |
| `/bio/` | `/bio/` | — | Retained directly (verbatim) |
| `/venture/` | `/venture/` | — | Retained directly (verbatim + links) |
| `/gpts/` | `/creator/` | `/gpts/` | Canonical + meta-refresh + JS redirect |
| `/books/` | `/books/` | — | Retained directly (verbatim) |
| `/consulting-services/` | `/consulting-services/` | — | Retained directly (static contact CTA) |
| `/contact/` | `/contact/` | — | Retained directly & enriched |
| `/blog/` | `/blog/` | — | Retained directly + RSS (`/blog/index.xml`) |
| `/category/{science,code,culture,open-sourcing}/` | `/category/{science,code,culture,open-sourcing}/` | — | Retained directly as filtered archive pages |
| `/privacy-policy/` | `/privacy-policy/` | — | Retained directly (verbatim) |
| `/sample-page/` | *(Excluded)* | — | Intentionally excluded (WP install boilerplate) |

## 3. Blog Post URL Mapping (All 14 Posts Retained at Native WordPress Permalinks)

Every historical WordPress post is rendered directly at its exact `/YYYY/MM/DD/<slug>/` path with 100% verbatim prose, headings, lists, equations, local media, and original figure attributions:

| Published | Title | Preserved Canonical Path |
|:---|:---|:---|
| 2026-09-21 | Play with Science: A New Nik Seixas Album Made with Human + AI Creativity | `/2026/09/21/play-with-science-nik-seixas/` |
| 2025-01-05 | Planck Scale Pioneers 2: Poincaré and The Concept of Fundamental Time | `/2025/01/05/planck-scale-pioneers-2-poincare-and-the-concept-of-fundamental-time/` |
| 2025-01-03 | Planck Scale Pioneers 1: Max Planck, Planck Units, and the Quantum Revolution | `/2025/01/03/planck-scale-pioneers-1-max-planck-planck-units-and-the-quantum-revolution/` |
| 2024-12-25 | Moiré Quasicrystals & Topological Quantum Computing: A New Frontier | `/2024/12/25/moire-quasicrystals-topological-quantum-computing-a-new-frontier/` |
| 2024-08-22 | Planck Scale Pioneers: Article Series | `/2024/08/22/planck-scale-pioneers-article-series/` |
| 2024-03-31 | SU(2): A Fundamental Building Block of Reality | `/2024/03/31/su2-a-fundamental-building-block-of-reality/` |
| 2024-01-06 | Code and Open Source Beyond Computers: Planck Scale Pioneers | `/2024/01/06/code-and-open-source-beyond-computers-planck-scale-pioneers/` |
| 2023-11-30 | The Unification Vision of Abdus Salam: Bridging Forces and Cultures in Physics | `/2023/11/30/the-unification-vision-of-abdus-salam-bridging-forces-and-cultures-in-physics/` |
| 2023-11-25 | Beyond the Linear Politics: A Higher-Dimensional Political Perspective | `/2023/11/25/beyond-the-linear-dichotomy-of-left-and-right-a-higher-dimensional-political-perspective/` |
| 2023-10-24 | Meta-Coding Theory: On the Unification of Information Systems | `/2023/10/24/meta-coding-theory-on-the-unification-of-information-systems/` |
| 2023-10-13 | Open Source vs. Open Access: The Evolving Landscape of Scientific Research Licenses on arXiv | `/2023/10/13/open-source-vs-open-access-the-evolving-landscape-of-scientific-research-licenses-on-arxiv/` |
| 2023-10-07 | The Quantum Legacy of Paul Dirac: Spin, Antimatter, and the Evolution of the Scientific Method | `/2023/10/07/the-quantum-legacy-of-paul-dirac-spin-antimatter-and-the-evolution-of-the-scientific-method/` |
| 2023-09-29 | Universal Family Benefit (UFB): The Foundations of our Future | `/2023/09/29/universal-love-based-child-care-universal-family-benefit-ufb-foundations-of-our-future/` |
| 2023-09-23 | Code! | `/2023/09/23/open-source/` |

## 4. Documented Fixes, Replacements & Intentional Exclusions

1. **Corrected Planck Length Sign Typo (`Planck Scale Pioneers 1`):** In WordPress (`wp_id=249`), equation screenshot `image-2.png` displayed $4.13 \times 10^{33}\text{ cm}$ (missing the minus sign in the exponent). All four equation screenshots (`image-1.png` through `image-4.png`) across Parts 1 and 2, plus the 3 KaTeX `<pre>` blocks in `SU(2)` (`wp_id=193`), were rendered as crisp MathJax equations, correcting the 1899 Planck length value to $4.13 \times 10^{-33}\text{ cm}$.
2. **Fixed Broken Cross-Post Link (`Planck Scale Pioneers 2`):** The live WordPress post linked to `.../2025/01/31/planck-scale-pioneers-1-...` (404 date mismatch; Part 1 was published `2025/01/03`). Fixed to link directly to `/2025/01/03/planck-scale-pioneers-1-.../`.
3. **Minor Typo Touch-Ups:** Fixed `Integrationg` -> `Integration` (`wp_id=88`), `advancements]` -> `advancements` (`wp_id=193`), two stray standalone `.` paragraphs (`wp_id=178`), a mid-sentence paragraph break (`wp_id=258`), Portuguese false-cognate `graduate` -> `undergraduate` for 1996 UNESP Electrical Engineering (`wp_id=62`), and removed the trailing ChatGPT prompt line *"Let me know if you’d like any further refinements!"* on `/gpts/` (`wp_id=153`).
4. **Static Replacement for PHP WPForms (`Consulting Services`):** Because GitHub Pages is static and does not run PHP, the WordPress WPForms widget on `/consulting-services/` was replaced with a direct link to `/contact/`.
5. **PhilPapers Automated Fetch Note:** Automated HTTP requests to `https://philpapers.org/rec/AMADFA` returned `HTTP 403 Forbidden` (anti-bot protection); no bypass was attempted, and the exact citation metadata and public URL from WordPress `/about/` were preserved verbatim in `data/publications.yml` (`amaral2025deus`).
6. **Intentionally Excluded Unlinked Uploads:**
   - `Planck-Scale-Pioneers-1.mp4` (`wp_id=251`, `87.62 MB`): Not referenced in any published page or post; excluded to avoid bloating the Git repository.
   - `QGR-General-Review-updated-06.18.19.doc` (`wp_id=25`, `0.88 MB`): Unlinked legacy Word document in the WP media library; excluded per public/private data hygiene rules.
