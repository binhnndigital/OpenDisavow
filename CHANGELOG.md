## [v0.1.0] — Initial Community Seed (806 domains)

### Summary
- Seeded the project with **806 suspicious/toxic referrer domains** curated from community inputs and historical logs.
- Auto-generated `build/disavow.txt` using `tools/merge_and_build.py`.
- Enforced CSV schema & basic hygiene via `tools/validate.py`:
  - required fields: `domain, category, evidence, source`
  - normalized domains (lowercase, strip `www.`, IDN-safe)
  - duplicates prevented and format validated

### What’s inside
- `data/domains.csv`: 806 root domains with metadata (category, evidence, source, optional risk score & dates)
- `data/allowlist.csv`: reserved for safe/legit domains to avoid false positives
- `rules/heuristics.yaml`: example scoring heuristics (optional)
- `build/disavow.txt`: Google-friendly `domain: example.com` lines

### Notes & safeguards
- **Indicative, not absolute**: labeling is neutral (e.g., “indicative of low-quality per criteria”).
- **Appeals welcome** via Issues (`appeal_removal.md`) with remediation evidence.
- CI enforces validation and reproducible builds on every change.

### How to use
1. Review `data/domains.csv` and `allowlist.csv`.
2. Build: `python tools/merge_and_build.py`
3. Upload `build/disavow.txt` to Google Disavow Tool (Search Console) for your verified property.

### Credits
- Maintainer: **BinhNN Digital** (binhnn.dev · contact@binhnn.dev · github.com/binhnndigital)
