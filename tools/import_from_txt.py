#!/usr/bin/env python3
"""
Import domains from a plaintext .txt file (one domain per line) into data/domains.csv

Usage:
  python tools/import_from_txt.py input/new_domains.txt     --category spam --source community --evidence "Community report"     [--risk 70] [--first-seen 2025-09-13] [--last-seen YYYY-MM-DD] [--geo VN] [--notes "batch-1"]     [--output data/domains.csv] [--dry-run]

Notes:
- Lines starting with '#' are ignored.
- Accepts lines like 'domain: example.com' or 'https://example.com/path' (it will extract the domain).
- Skips duplicates already present in the target CSV.
"""
import argparse, csv, re, sys
from pathlib import Path
from urllib.parse import urlparse
from datetime import date

DEFAULT_OUTPUT = Path("data/domains.csv")
HEADER = ["domain","category","evidence","source","risk_score","first_seen","last_seen","geo","notes"]
DOMAIN_RE = re.compile(r"^[a-z0-9.-]+\.[a-z]{2,}$", re.I)

def extract_domain(line: str):
    s = line.strip()
    if not s or s.startswith("#"):
        return None
    if s.lower().startswith("domain:"):
        s = s.split(":",1)[1].strip()
    if s.startswith("http://") or s.startswith("https://"):
        try:
            d = urlparse(s).hostname or ""
        except Exception:
            d = ""
    else:
        d = s
    d = d.lower().rstrip(".")
    if d.startswith("www."):
        d = d[4:]
    return d if d else None

def valid_domain(d: str) -> bool:
    return bool(DOMAIN_RE.match(d))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("txt", help="Path to plaintext list (one domain per line)")
    ap.add_argument("--category","--cat", default="spam")
    ap.add_argument("--source", default="community")
    ap.add_argument("--evidence", default="Imported from TXT")
    ap.add_argument("--risk", type=int, default=None)
    ap.add_argument("--first-seen", dest="first_seen", default=str(date.today()))
    ap.add_argument("--last-seen", dest="last_seen", default="")
    ap.add_argument("--geo", default="")
    ap.add_argument("--notes", default="")
    ap.add_argument("--output", default=str(DEFAULT_OUTPUT))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    src = Path(args.txt)
    out = Path(args.output)
    if not src.exists():
        print(f"❌ Input not found: {src}", file=sys.stderr)
        sys.exit(1)

    # Load existing domains (for deduplication)
    existing = set()
    if out.exists():
        with out.open(encoding="utf-8") as f:
            r = csv.DictReader(f)
            for row in r:
                d = (row.get("domain") or "").strip().lower()
                if d.startswith("www."):
                    d = d[4:]
                if d:
                    existing.add(d)

    # Prepare rows
    new_rows = []
    seen_batch = set()
    with src.open(encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            d = extract_domain(line)
            if not d:
                continue
            if not valid_domain(d):
                print(f"⚠️  Skip invalid domain at line {i}: {line.strip()}")
                continue
            if d in existing or d in seen_batch:
                print(f"ℹ️  Skip duplicate: {d}")
                continue
            row = [
                d,
                args.category.strip().lower(),
                args.evidence,
                args.source.strip().lower(),
                ("" if args.risk is None else str(args.risk)),
                args.first_seen,
                args.last_seen,
                args.geo,
                args.notes,
            ]
            new_rows.append(row)
            seen_batch.add(d)

    if not new_rows:
        print("No new domains to import.")
        return

    print(f"Will import {len(new_rows)} domains into {out}")
    if args.dry_run:
        for d, *_ in new_rows[:20]:
            print(" -", d)
        if len(new_rows) > 20:
            print(f" ... and {len(new_rows)-20} more")
        return

    out.parent.mkdir(parents=True, exist_ok=True)
    # Ensure header exists
    write_header = not out.exists() or out.stat().st_size == 0
    with out.open("a", newline="", encoding="utf-8") as o:
        w = csv.writer(o)
        if write_header:
            w.writerow(HEADER)
        w.writerows(new_rows)

    print(f"✅ Imported {len(new_rows)} domains.")
    print("Next steps:")
    print("  python tools/validate.py")
    print("  python tools/merge_and_build.py")

if __name__ == "__main__":
    main()
