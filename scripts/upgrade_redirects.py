#!/usr/bin/env python3
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = ROOT / "_site"


def main() -> None:
    if not SITE_DIR.exists():
        return
    cfg = yaml.safe_load((ROOT / "_quarto.yml").read_text(encoding="utf-8"))
    site_url = cfg["website"]["site-url"].rstrip("/")

    for hf in sorted(SITE_DIR.rglob("*.html")):
        raw = hf.read_text(encoding="utf-8", errors="replace")
        if "<title>Redirect</title>" not in raw:
            continue
        m = re.search(r'var redirects = \{"":"([^"]+)"\};', raw)
        if not m:
            continue
        rel_target = m.group(1)
        resolved = (hf.parent / rel_target).resolve()
        rel_from_site = resolved.relative_to(SITE_DIR).as_posix()
        if rel_from_site.endswith("/index.html"):
            canonical_path = rel_from_site[: -len("index.html")]
        elif rel_from_site == "index.html":
            canonical_path = ""
        else:
            canonical_path = rel_from_site
        canonical_url = f"{site_url}/{canonical_path}"

        upgraded = f"""<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta charset="utf-8">
  <title>Redirecting…</title>
  <meta name="robots" content="noindex">
  <link rel="canonical" href="{canonical_url}">
  <meta http-equiv="refresh" content="0; url={rel_target}">
  <script type="text/javascript">
    var redirects = {{"":"{rel_target}"}};
    var hash = window.location.hash.startsWith('#') ? window.location.hash.slice(1) : window.location.hash;
    var redirect = redirects[hash] || redirects[""] || "/";
    redirect = redirect + window.location.search;
    if (!redirects[hash]) {{
      redirect = redirect + window.location.hash;
    }}
    window.location.replace(redirect);
  </script>
</head>
<body>
  <main>
    <p>Redirecting to <a href="{rel_target}">{canonical_url}</a>.</p>
  </main>
</body>
</html>
"""
        hf.write_text(upgraded, encoding="utf-8")


if __name__ == "__main__":
    main()
