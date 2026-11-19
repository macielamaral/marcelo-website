#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent

ALLOWED_SECTIONS = {"notes", "publications/articles", "blog/posts"}
ALLOWED_STATUS = {
    "peer-reviewed",
    "accepted-manuscript",
    "preprint",
    "technical-report",
    "research-note",
    "preliminary-investigation",
}


def validate_manifest(manifest: dict) -> list[str]:
    errors = []
    required = [
        "slug",
        "title",
        "authors",
        "date",
        "target_section",
        "epistemic_status",
        "approved_for_public_release",
        "summary",
        "source_repository",
        "markdown_body_path",
    ]
    for field in required:
        if field not in manifest:
            errors.append(f"Missing required field: {field}")
    if errors:
        return errors

    if manifest["approved_for_public_release"] is not True:
        errors.append("approved_for_public_release must be explicitly true.")
    repo = manifest["source_repository"]
    if not isinstance(repo, dict) or repo.get("is_public") is not True:
        errors.append("source_repository.is_public must be explicitly true.")
    if not re.match(r"^[0-9a-f]{7,40}$", str(repo.get("commit_sha", ""))):
        errors.append("source_repository.commit_sha must be a valid Git SHA.")
    if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", manifest["slug"]):
        errors.append("slug must be lowercase kebab-case.")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", manifest["date"]):
        errors.append("date must be YYYY-MM-DD.")
    if manifest["target_section"] not in ALLOWED_SECTIONS:
        errors.append(f"target_section must be one of {sorted(ALLOWED_SECTIONS)}.")
    if manifest["epistemic_status"] not in ALLOWED_STATUS:
        errors.append(f"epistemic_status must be one of {sorted(ALLOWED_STATUS)}.")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate and import an approved agent research submission.")
    parser.add_argument("manifest", help="Path to JSON or YAML submission manifest")
    parser.add_argument("--dry-run", action="store_true", help="Validate manifest without writing files")
    args = parser.parse_args()

    mpath = Path(args.manifest).resolve()
    raw = mpath.read_text(encoding="utf-8")
    manifest = json.loads(raw) if mpath.suffix == ".json" else yaml.safe_load(raw)
    errors = validate_manifest(manifest)
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        sys.exit(1)

    body_path = (mpath.parent / manifest["markdown_body_path"]).resolve()
    if not body_path.exists():
        sys.exit(f"ERROR: markdown_body_path not found: {body_path}")

    if manifest["target_section"] == "blog/posts":
        yyyy, mm, dd = manifest["date"].split("-")
        dest_dir = ROOT / yyyy / mm / dd / manifest["slug"]
    else:
        dest_dir = ROOT / manifest["target_section"] / manifest["slug"]
    dest_qmd = dest_dir / "index.qmd"

    if args.dry_run:
        print(f"Manifest valid. Would stage to: {dest_qmd}")
        return

    dest_dir.mkdir(parents=True, exist_ok=True)
    ids = manifest.get("identifiers") or {}
    repo = manifest["source_repository"]
    frontmatter = {
        "title": manifest["title"],
        "author": manifest["authors"],
        "date": manifest["date"],
        "description": manifest["summary"],
        "categories": manifest.get("categories", ["Science"]),
    }
    header_yaml = yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True).strip()
    provenance_box = [
        "::: {.project-meta}",
        f"**Epistemic Status:** `{manifest['epistemic_status']}`  ",
        f"**Source Repository:** [{repo['url']}]({repo['url']}) (`{repo['commit_sha'][:10]}`)",
    ]
    if ids.get("doi"):
        provenance_box.append(f"  \n**DOI:** [https://doi.org/{ids['doi']}](https://doi.org/{ids['doi']})")
    if ids.get("arxiv"):
        provenance_box.append(f"  \n**arXiv:** [arXiv:{ids['arxiv']}](https://arxiv.org/abs/{ids['arxiv']})")
    if manifest.get("reproducibility_statement"):
        provenance_box.append(f"\n\n**Reproducibility:** {manifest['reproducibility_statement']}")
    provenance_box.append(":::\n")

    content = f"---\n{header_yaml}\n---\n\n" + "\n".join(provenance_box) + "\n" + body_path.read_text(encoding="utf-8")
    dest_qmd.write_text(content, encoding="utf-8")
    print(f"Staged approved update at: {dest_qmd}")


if __name__ == "__main__":
    main()
