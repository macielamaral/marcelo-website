# Zenodo DOI Integration & Archiving Workflow

This repository supports linking persistent Zenodo DOIs to papers, technical reports, datasets, and open-source code releases while strictly enforcing **human-in-the-loop governance** over DOI minting.

## 1. Core Governance Rules

1. **No Automatic Deposits:** Neither GitHub Actions nor AI agents may automatically upload files or mint DOIs on Zenodo without explicit authorization from Marcelo Maciel Amaral.
2. **Never Fabricate DOIs:** Only verified, publicly resolvable `10.5281/zenodo.<id>` (or journal/arXiv `10.xxxx/...`) identifiers may be committed to `data/publications.yml` or article frontmatter.
3. **Concept DOI vs. Version DOI Discipline:**
   - Zenodo issues both a **Concept DOI** (resolving to the latest release of a work) and a **Version DOI** (resolving to a specific immutable tag, e.g., `v1.1.0`).
   - Record the **Version DOI** when citing a specific reproducible benchmark or tagged code release, and note the Concept DOI only when referencing the ongoing software package as a whole. Never mint duplicate standalone deposits for a repository already connected via the GitHub–Zenodo bridge.

## 2. Recommended GitHub–Zenodo Release Workflow (For Code & Reports)

For research repositories such as `quasicrystal-inflation-code`, `tiling-space-cosmology`, `E8-Cycle-Clock-Analysis`, or `gaugebench`:

1. Add a `CITATION.cff` or `.zenodo.json` metadata file in the target research repository specifying authors, ORCID, license, keywords, and title.
2. Log in to [zenodo.org](https://zenodo.org/) -> **GitHub** settings, and toggle the switch **ON** for that specific public repository.
3. When ready to mint an archival snapshot, create a semantic GitHub Release (e.g., `v1.1.0`) in that repository. Zenodo will automatically archive the release tarball and mint a persistent DOI.

## 3. Linking an Existing Zenodo DOI into This Website

Once a Zenodo record is live and public, run the read-only linker script in `marcelo-website` to verify the record via Zenodo's public REST API and attach its DOI to `data/publications.yml`:

```bash
# 1. Inspect and verify a public Zenodo record (read-only)
python3 scripts/link_zenodo.py 10.5281/zenodo.<RECORD_ID>

# 2. Write the verified zenodo_doi into data/publications.yml
python3 scripts/link_zenodo.py 10.5281/zenodo.<RECORD_ID> --pub-id amaral2025qic_software --write

# 3. Rebuild BibTeX + markdown includes and validate the site
python3 scripts/build_publications.py
quarto render
python3 scripts/validate_site.py
```

The `Zenodo` badge will automatically appear on the corresponding publication entry in `/publications/` and in `publications/references.bib`.
