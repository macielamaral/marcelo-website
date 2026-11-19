# Short-Term Roadmap (`NEXT.md`)

## 1. Release Follow-Up & Editorial Review
- [ ] With Marcelo's authorization, enable GitHub Pages using **GitHub Actions** in repository settings, then rerun and verify deployment at `https://macielamaral.github.io/marcelo-website/`. The release review found Pages disabled; no hosting or DNS settings were changed.
- [ ] Optional editorial review of historical GPT references, preserved unchanged: [Universal Family Benefit (2023-09-29)](2023/09/29/universal-love-based-child-care-universal-family-benefit-ufb-foundations-of-our-future/index.qmd) credits/discusses GPT-4; [Paul Dirac (2023-10-07)](2023/10/07/the-quantum-legacy-of-paul-dirac-spin-antimatter-and-the-evolution-of-the-scientific-method/index.qmd) credits ChatGPT editorial assistance; [Meta-Coding Theory (2023-10-24)](2023/10/24/meta-coding-theory-on-the-unification-of-information-systems/index.qmd) discusses GPT collaboration and translation.

## 2. Scientific Content & Persistent Identifiers
- [ ] Add ORCID identifier to `index.qmd` JSON-LD and `bio/index.qmd` once confirmed.
- [ ] Check Zenodo organization/account settings; when ready, enable GitHub–Zenodo archiving on `quasicrystal-inflation-code`, `tiling-space-cosmology`, `E8-Cycle-Clock-Analysis`, and `gaugebench`, then attach minted DOIs via `scripts/link_zenodo.py`.
- [ ] Publish structured HTML + Typst PDF companion articles for `tiling-space-cosmology` (`arXiv:2407.14520`), the 2026 *Nuclear Physics B* paper (`10.1016/j.nuclphysb.2026.117681`), and *Planck Scale Pioneers* Part 3+.

## 3. Production Cutover (`www.marcelomacielamaral.com`)
- [ ] Back up DreamHost WordPress database and `wp-content/uploads` archive.
- [ ] Execute `docs/deployment-and-domain.md` Part 2 using staged files in `config/custom-domain/` (`CNAME`, `robots.txt`, `_quarto.yml` `site-url` update, DreamHost web-only `A`/`CNAME` records preserving `MX`/`SPF`/`DKIM` email DNS, and GitHub Pages HTTPS enforcement).
