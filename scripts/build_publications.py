#!/usr/bin/env python3
from pathlib import Path
from datetime import date
import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "publications.yml"
PUB_DIR = ROOT / "publications"

TYPE_LABELS = {
    "peer-reviewed": ("Peer-Reviewed Journal Articles", "status-verified", "Peer-Reviewed"),
    "preprint": ("Preprints & Archived Manuscripts", "status-preprint", "Preprint"),
    "research-note": ("Preprints / Research Notes — Gauge Freedom Field Notes", "status-preprint", "Preprint / Research Note"),
    "report": ("Technical Essays & Philosophical Works", "status-preprint", "Essay / Report"),
    "software": ("Open-Source Research Software", "status-verified", "Software"),
}

CATEGORY_ORDER = [
    "Topological Quantum Computing",
    "Quantum Gravity and Cosmology",
    "Quantum Field Theory and the Standard Model",
    "Emergence Theory and Quasicrystalline Codes",
    "Genetic Code and Quantum Information",
    "Information Geometry",
    "Artificial Intelligence",
    "Riemann Hypothesis and Arithmetic Geometry",
    "Philosophy, Theology, and Foundations of Physics",
]


def to_bibtex(pub: dict) -> str:
    ptype = pub["type"]
    entry_type = "article" if ptype == "peer-reviewed" else ("software" if ptype == "software" else "misc")
    authors = " and ".join(pub["authors"])
    fields = [
        ("author", authors),
        ("title", "{" + pub["title"] + "}"),
        ("year", str(pub["year"])),
    ]
    if ptype == "peer-reviewed":
        fields.append(("journal", pub["venue"]))
    else:
        fields.append(("howpublished", pub["venue"]))
    if pub.get("date"):
        fields.append(("date", pub["date"]))
    if ptype == "research-note":
        fields.append(("note", "Preprint / Research Note"))
    for key in ("volume", "issue", "pages", "doi"):
        if pub.get(key):
            bib_key = "number" if key == "issue" else key
            fields.append((bib_key, str(pub[key])))
    if pub.get("arxiv"):
        fields.append(("eprint", str(pub["arxiv"])))
        fields.append(("archivePrefix", "arXiv"))
    if pub.get("url"):
        fields.append(("url", pub["url"]))
    body = ",\n".join(f"  {k} = {{{v}}}" for k, v in fields)
    return f"@{entry_type}{{{pub['id']},\n{body}\n}}"


def render_card(pub: dict) -> str:
    _, pill_class, badge_text = TYPE_LABELS[pub["type"]]
    authors = ", ".join(pub["authors"])
    venue_parts = [pub["venue"]]
    if pub.get("volume"):
        vol = f"{pub['volume']}"
        if pub.get("issue"):
            vol += f"({pub['issue']})"
        venue_parts.append(vol)
    if pub.get("pages"):
        venue_parts.append(str(pub["pages"]))
    date_label = str(pub["year"])
    if pub.get("date"):
        published = date.fromisoformat(pub["date"])
        date_label = f"{published.strftime('%B')} {published.day}, {published.year}"
    venue_str = ", ".join(venue_parts) + f" ({date_label})"

    links = [f'<span class="status-pill {pill_class}">{badge_text}</span>']
    if pub.get("article_page"):
        target_qmd = pub["article_page"].strip("/") + "/index.qmd"
        links.append(f"[Research Article](/{target_qmd})")
    if pub.get("doi"):
        links.append(f"[DOI: {pub['doi']}](https://doi.org/{pub['doi']})")
    elif pub.get("url"):
        links.append(f"[Link]({pub['url']})")
    if pub.get("arxiv"):
        links.append(f"[arXiv:{pub['arxiv']}](https://arxiv.org/abs/{pub['arxiv']})")
    if pub.get("pdf_url"):
        links.append(f"[PDF]({pub['pdf_url']})")
    if pub.get("repo_url"):
        links.append(f"[Code Repository]({pub['repo_url']})")
    if pub.get("zenodo_doi"):
        links.append(f"[Zenodo: {pub['zenodo_doi']}](https://doi.org/{pub['zenodo_doi']})")

    links_line = " ".join(links)
    title_link = f"[{pub['title']}]({pub['url']})" if pub.get("url") else pub["title"]

    lines = [
        "::: {.pub-item}",
        f"::: {{.pub-title}}\n{title_link}\n:::",
        f"::: {{.pub-authors}}\n{authors}\n:::",
        f"::: {{.pub-venue}}\n{venue_str}\n:::",
        f"::: {{.pub-links}}\n{links_line}\n:::",
        ":::",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    data = yaml.safe_load(DATA_FILE.read_text(encoding="utf-8"))
    pubs = sorted(data["publications"], key=lambda p: (p["year"], p["id"]), reverse=True)
    PUB_DIR.mkdir(parents=True, exist_ok=True)

    bib_entries = [to_bibtex(p) for p in pubs]
    (PUB_DIR / "references.bib").write_text("\n\n".join(bib_entries) + "\n", encoding="utf-8")

    by_type_sections = []
    for ptype in ("peer-reviewed", "preprint", "research-note", "report", "software"):
        heading, _, _ = TYPE_LABELS[ptype]
        subset = [p for p in pubs if p["type"] == ptype]
        if not subset:
            continue
        by_type_sections.append(f"## {heading} ({len(subset)})\n")
        for p in subset:
            by_type_sections.append(render_card(p))
    (PUB_DIR / "_by_type.md").write_text("\n".join(by_type_sections), encoding="utf-8")

    by_cat_sections = []
    for cat in CATEGORY_ORDER:
        subset = [
            p for p in pubs
            if p["category"] == cat or cat in (p.get("additional_categories") or [])
        ]
        if not subset:
            continue
        by_cat_sections.append(f"### {cat}\n")
        for p in subset:
            by_cat_sections.append(render_card(p))
    (PUB_DIR / "_by_category.md").write_text("\n".join(by_cat_sections), encoding="utf-8")

    featured = [p for p in pubs if p.get("featured")]
    feat_lines = [render_card(p) for p in featured[:6]]
    (PUB_DIR / "_featured.md").write_text("\n".join(feat_lines), encoding="utf-8")
    print(f"Generated references.bib and markdown includes for {len(pubs)} publications.")


if __name__ == "__main__":
    main()
