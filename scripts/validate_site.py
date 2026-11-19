#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import sys
import urllib.parse
import yaml

ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = ROOT / "_site"


class PageInspector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.media: list[str] = []
        self.imgs_missing_alt: list[str] = []
        self.in_main = False
        self.main_depth = 0
        self.h2_texts: list[str] = []
        self._in_h2 = False
        self._h2_buf: list[str] = []
        self.has_title = False
        self.has_meta_desc = False
        self.has_canonical = False
        self.is_redirect = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        ad = dict(attrs)
        if tag == "main":
            self.in_main = True
            self.main_depth = 1
        elif self.in_main:
            self.main_depth += 1

        if tag == "title":
            self.has_title = True
        if tag == "meta":
            if (ad.get("name") or "").lower() == "description" and (ad.get("content") or "").strip():
                self.has_meta_desc = True
            if (ad.get("http-equiv") or "").lower() == "refresh":
                self.is_redirect = True
        if tag == "link":
            rel_tokens = (ad.get("rel") or "").lower().split()
            if "canonical" in rel_tokens and (ad.get("href") or "").strip():
                self.has_canonical = True
            if ad.get("href") and any(r in rel_tokens for r in ("stylesheet", "icon")):
                self.media.append(ad["href"])
        if tag == "script" and ad.get("src"):
            self.media.append(ad["src"])
        if tag == "a" and ad.get("href"):
            self.links.append(ad["href"])
        if tag in ("img", "video", "audio", "source") and ad.get("src"):
            self.media.append(ad["src"])
            if tag == "img" and self.in_main and "alt" not in ad:
                self.imgs_missing_alt.append(ad["src"])
        if tag == "h2":
            self._in_h2 = True
            self._h2_buf = []

    def handle_endtag(self, tag: str) -> None:
        if self.in_main:
            self.main_depth -= 1
            if self.main_depth == 0:
                self.in_main = False
        if tag == "h2" and self._in_h2:
            self._in_h2 = False
            self.h2_texts.append(" ".join("".join(self._h2_buf).split()))

    def handle_data(self, data: str) -> None:
        if self._in_h2:
            self._h2_buf.append(data)


def resolve_local_target(source_html: Path, ref: str, subpath_prefix: str) -> tuple[Path | None, bool]:
    parsed = urllib.parse.urlparse(ref)
    if parsed.scheme in ("http", "https", "mailto", "tel", "javascript", "data"):
        return None, False
    path_part = urllib.parse.unquote(parsed.path)
    if not path_part:
        return None, False
    escaped_subpath = False
    if subpath_prefix != "/" and path_part.startswith("/"):
        if path_part.startswith(subpath_prefix):
            rel = path_part[len(subpath_prefix):]
            target = SITE_DIR / rel
        else:
            escaped_subpath = True
            target = SITE_DIR / path_part.lstrip("/")
    elif path_part.startswith("/"):
        target = SITE_DIR / path_part.lstrip("/")
    else:
        target = (source_html.parent / path_part).resolve()
    if target.is_dir():
        target = target / "index.html"
    return target, escaped_subpath


def main() -> None:
    errors: list[str] = []

    tracked = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
    for f in tracked:
        if f.startswith("private/") or f == "private" or f.startswith(".env"):
            errors.append(f"PRIVACY VIOLATION: Git tracks restricted path '{f}'")

    if not SITE_DIR.exists():
        sys.exit("ERROR: _site/ directory does not exist. Run 'quarto render' first.")

    cfg = yaml.safe_load((ROOT / "_quarto.yml").read_text(encoding="utf-8"))
    site_url = cfg["website"]["site-url"].rstrip("/")
    parsed_site = urllib.parse.urlparse(site_url)
    subpath_prefix = (parsed_site.path.rstrip("/") + "/") if parsed_site.path.strip("/") else "/"

    if subpath_prefix != "/" and (SITE_DIR / "CNAME").exists():
        errors.append("CONFIGURATION ERROR: _site/CNAME must not be active while site-url uses a subpath preview")

    for built in SITE_DIR.rglob("*"):
        rel_parts = built.relative_to(SITE_DIR).parts
        if "private" in rel_parts or "config" in rel_parts:
            errors.append(f"BOUNDARY VIOLATION: restricted artifact found in _site/: {built}")

    pubs = yaml.safe_load((ROOT / "data" / "publications.yml").read_text(encoding="utf-8"))["publications"]
    doi_re = re.compile(r"^10\.\d{4,9}/[-._;()/:A-Za-z0-9]+$")
    arxiv_re = re.compile(r"^\d{4}\.\d{4,5}$")
    for p in pubs:
        if p.get("doi") and not doi_re.match(p["doi"]):
            errors.append(f"Invalid DOI format in {p['id']}: {p['doi']}")
        if p.get("arxiv") and not arxiv_re.match(str(p["arxiv"])):
            errors.append(f"Invalid arXiv ID format in {p['id']}: {p['arxiv']}")
        if p.get("zenodo_doi") and not doi_re.match(p["zenodo_doi"]):
            errors.append(f"Invalid Zenodo DOI format in {p['id']}: {p['zenodo_doi']}")

    html_files = sorted(SITE_DIR.rglob("*.html"))
    for hf in html_files:
        inspector = PageInspector()
        raw_html = hf.read_text(encoding="utf-8", errors="replace")
        inspector.feed(raw_html)
        rel_hf = hf.relative_to(SITE_DIR)

        if not inspector.has_canonical:
            errors.append(f"SEO: Missing <link rel='canonical'> in {rel_hf}")
        if not inspector.is_redirect and not inspector.has_meta_desc:
            errors.append(f"SEO: Missing <meta name='description'> in {rel_hf}")

        for link in inspector.links:
            t, escaped = resolve_local_target(hf, link, subpath_prefix)
            if escaped:
                errors.append(f"Subpath prefix missing on root-relative link in {rel_hf}: '{link}'")
            if t is not None and not t.exists():
                errors.append(f"Broken internal link in {rel_hf}: '{link}' -> {t.relative_to(ROOT) if t.is_relative_to(ROOT) else t}")

        for src in inspector.media:
            t, escaped = resolve_local_target(hf, src, subpath_prefix)
            if escaped:
                errors.append(f"Subpath prefix missing on root-relative asset in {rel_hf}: '{src}'")
            if t is not None and not t.exists():
                errors.append(f"Missing media/asset in {rel_hf}: '{src}'")

        for missing_alt in inspector.imgs_missing_alt:
            errors.append(f"Accessibility: <img> missing alt attribute in {rel_hf}: {missing_alt}")

    home_html = SITE_DIR / "index.html"
    if not home_html.exists():
        errors.append("Missing _site/index.html")
    else:
        home_raw = home_html.read_text(encoding="utf-8")
        home_ins = PageInspector()
        home_ins.feed(home_raw)
        if not any("Quantum Gravity Research" in h for h in home_ins.h2_texts):
            errors.append("SEO REQUIREMENT FAILED: Homepage missing <h2> containing 'Quantum Gravity Research'")
        if "application/ld+json" not in home_raw or '"Person"' not in home_raw:
            errors.append("SEO REQUIREMENT FAILED: Homepage missing Schema.org Person JSON-LD")

    required_artifacts = (
        "sitemap.xml",
        "robots.txt",
        "blog/index.xml",
        "publications/references.bib",
        "publications/articles/fibonacci-quasicrystal-inflation-code/index.pdf",
    )
    for required_artifact in required_artifacts:
        art_path = SITE_DIR / required_artifact
        if not art_path.exists() or art_path.stat().st_size == 0:
            errors.append(f"Missing or empty required build artifact: _site/{required_artifact}")

    inv = yaml.safe_load((ROOT / "data" / "migration-inventory.yml").read_text(encoding="utf-8"))
    for entry in inv.get("pages", []) + inv.get("categories", []) + inv.get("posts", []):
        if entry.get("migration_status") == "intentionally-excluded":
            continue
        for url_field in [entry.get("proposed_quarto_url")] + (entry.get("alias_urls") or []):
            if not url_field:
                continue
            p = SITE_DIR / url_field.strip("/")
            if p.is_dir() or not p.suffix:
                p = p / "index.html"
            if not p.exists():
                errors.append(f"Missing migrated route or alias '{url_field}' (expected {p.relative_to(SITE_DIR)})")

    if errors:
        print(f"VALIDATION FAILED ({len(errors)} issue(s)):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print(
        f"VALIDATION PASSED: {len(html_files)} HTML pages, {len(pubs)} publications, "
        "all internal links, subpath assets, canonical tags, PDF output, aliases, SEO metadata, and privacy boundaries verified."
    )


if __name__ == "__main__":
    main()
