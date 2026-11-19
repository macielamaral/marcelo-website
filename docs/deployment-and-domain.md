# GitHub Pages Deployment & Custom Domain Cutover Guide

The website is initially configured for safe previewing on **GitHub Pages** at a project subpath before any DNS cutover of `www.marcelomacielamaral.com`.

---

## Part 1: Activating the GitHub Pages Preview (`https://macielamaral.github.io/marcelo-website/`)

No changes to DreamHost or `www.marcelomacielamaral.com` occur during this phase.

1. **Review locally:**
   ```bash
   python3 scripts/build_publications.py
   quarto render
   python3 scripts/validate_site.py
   quarto preview
   ```
2. **Verify Git staging excludes private files:**
   ```bash
   git status
   # Confirm `private/` does NOT appear in untracked/staged files.
   ```
3. **Commit and push to `origin/main`** (only when ready to publish the preview):
   ```bash
   git add .
   git commit -m "Bootstrap Quarto scientific research website"
   git push origin main
   ```
4. **Configure GitHub Pages source:**
   - Open `https://github.com/macielamaral/marcelo-website/settings/pages`.
   - Under **Build and deployment -> Source**, select **GitHub Actions** (not "Deploy from a branch").
5. **Verify deployment:**
   - In the **Actions** tab, confirm `Build, Validate, and Deploy Quarto Site` succeeds (`build` -> `deploy`).
   - Browse `https://macielamaral.github.io/marcelo-website/` on desktop and mobile.

---

## Part 2: Future Custom Domain Cutover (`www.marcelomacielamaral.com`)

Perform these steps **only after** you have reviewed the GitHub Pages preview and backed up your DreamHost WordPress installation (database + `wp-content/uploads`).

### Step 1 — Preserve DreamHost Email & Non-Web DNS Records
Before editing any DNS record in the DreamHost Panel:
- Export or screenshot all existing DNS records for `marcelomacielamaral.com`.
- **Do NOT touch `MX`, `TXT` (`SPF`, `DKIM`, `DMARC`), or mail subdomain records** (`mail.`, `webmail.`, etc.) so domain email continues uninterrupted.

### Step 2 — Activate Staged Custom-Domain Files (`config/custom-domain/`)
Ready-to-copy production templates are already prepared in `config/custom-domain/` (and kept inactive during subpath preview):

1. Copy the staged `CNAME` and production `robots.txt` into the repository root:
   ```bash
   cp config/custom-domain/CNAME.production ./CNAME
   cp config/custom-domain/robots.production.txt ./robots.txt
   ```
2. In `_quarto.yml`:
   - Change `site-url: "https://macielamaral.github.io/marcelo-website"` to:
     ```yaml
     site-url: "https://www.marcelomacielamaral.com"
     ```
   - Add `"CNAME"` under `project.resources`:
     ```yaml
     resources:
       - "CNAME"
       - "robots.txt"
     ```
3. Render and validate locally (`quarto render && python3 scripts/validate_site.py`), then commit and push to `main`.

### Step 3 — Update DreamHost DNS Records for Web Traffic Only
In the DreamHost DNS control panel for `marcelomacielamaral.com`:
1. **`www` subdomain (`CNAME` record):**
   - Host: `www`
   - Type: `CNAME`
   - Value: `macielamaral.github.io.`
2. **Apex domain `@` (`A` and optional `AAAA` records to GitHub Pages):**
   - Remove the old DreamHost web-hosting `A`/`AAAA` records for `@` (root) **only**.
   - Add GitHub Pages `A` records for `@`:
     - `185.199.108.153`
     - `185.199.109.153`
     - `185.199.110.153`
     - `185.199.111.153`
   - Optional IPv6 `AAAA` records for `@`:
     - `2606:50c0:8000::153`
     - `2606:50c0:8001::153`
     - `2606:50c0:8002::153`
     - `2606:50c0:8003::153`

### Step 4 — Enable HTTPS & Verify Redirects
1. In GitHub **Settings -> Pages -> Custom domain**, enter `www.marcelomacielamaral.com` and click **Save**.
2. Wait for GitHub's DNS check and Let's Encrypt TLS certificate provisioning to complete, then check **Enforce HTTPS**.
3. Verify:
   - `https://marcelomacielamaral.com/` redirects cleanly to `https://www.marcelomacielamaral.com/`.
   - Legacy URLs (`/about/`, `/gpts/`, `/2024/12/25/moire-quasicrystals-topological-quantum-computing-a-new-frontier/`) redirect cleanly to their canonical Quarto destinations.
   - `https://www.marcelomacielamaral.com/sitemap.xml` and `/blog/index.xml` resolve over HTTPS.
