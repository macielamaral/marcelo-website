# Production Custom-Domain Staged Files (Inactive During Preview)

These files are staged here for the future DNS cutover to `www.marcelomacielamaral.com` and are **intentionally inactive** while previewing at `https://macielamaral.github.io/marcelo-website/`.

When ready to cut over (see `docs/deployment-and-domain.md` Part 2):

1. Copy `config/custom-domain/CNAME.production` to `./CNAME` and add `"CNAME"` to `project.resources` in `_quarto.yml`.
2. Copy `config/custom-domain/robots.production.txt` to `./robots.txt`.
3. Update `website.site-url` in `_quarto.yml` from `"https://macielamaral.github.io/marcelo-website"` to `"https://www.marcelomacielamaral.com"`.
4. Run `quarto render && python3 scripts/validate_site.py` (updating `SUBPATH_PREFIX = "/"` in `scripts/validate_site.py` once no longer on the `/marcelo-website/` subpath).
