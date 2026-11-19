#!/usr/bin/env python3
import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
PUB_FILE = ROOT / "data" / "publications.yml"


def resolve_record_id(identifier: str) -> str:
    m = re.search(r"zenodo\.(\d+)", identifier)
    if m:
        return m.group(1)
    if identifier.isdigit():
        return identifier
    raise ValueError(f"Cannot extract Zenodo numeric record ID from: {identifier}")


def fetch_zenodo_record(record_id: str) -> dict:
    url = f"https://zenodo.org/api/records/{record_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "marcelo-website-zenodo-linker/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Read-only linker associating an already-minted public Zenodo DOI with data/publications.yml."
    )
    parser.add_argument("zenodo_id", help="Existing public Zenodo record ID or 10.5281/zenodo.<id> DOI")
    parser.add_argument("--pub-id", help="Publication id in data/publications.yml to update")
    parser.add_argument("--write", action="store_true", help="Write verified zenodo_doi into data/publications.yml")
    args = parser.parse_args()

    rec_id = resolve_record_id(args.zenodo_id)
    record = fetch_zenodo_record(rec_id)
    doi = record.get("doi")
    md = record.get("metadata", {})
    print(f"Verified public Zenodo record {rec_id}:")
    print(f"  Title: {md.get('title')}")
    print(f"  DOI:   {doi}")
    print(f"  Date:  {md.get('publication_date')}")

    if not args.pub_id or not args.write:
        return

    data = yaml.safe_load(PUB_FILE.read_text(encoding="utf-8"))
    matched = False
    for pub in data["publications"]:
        if pub["id"] == args.pub_id:
            pub["zenodo_doi"] = doi
            matched = True
            break
    if not matched:
        sys.exit(f"Publication id '{args.pub_id}' not found in {PUB_FILE}")
    PUB_FILE.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"Updated {args.pub_id} with zenodo_doi={doi}")


if __name__ == "__main__":
    main()
