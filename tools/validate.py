import csv, re, sys
from pathlib import Path
from datetime import datetime

DOMAINS = Path("data/domains.csv")
ALLOW = Path("data/allowlist.csv")

domain_re = re.compile(r"^[a-z0-9.-]+\.[a-z]{2,}$")
category_set = {"spam","pbn","ghost-referrer","adult","casino","malware","other"}

def check_date(val, field, rowno):
    if not val:
        return
    try:
        datetime.strptime(val, "%Y-%m-%d")
    except Exception:
        print(f"❌ Invalid date in {field} at line {rowno}: {val} (expected YYYY-MM-DD)")
        sys.exit(1)

def validate_csv(path: Path, required_cols):
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            print(f"❌ {path} has no header")
            sys.exit(1)
        missing = [c for c in required_cols if c not in reader.fieldnames]
        if missing:
            print(f"❌ Missing required columns in {path}: {missing}")
            sys.exit(1)
        seen = set()
        for i, row in enumerate(reader, start=2):
            raw = row["domain"].strip().lower().split('/')[0]
            if raw.startswith("www."):
                raw = raw[4:]
            if not domain_re.match(raw):
                print(f"❌ Invalid domain at {path}:{i} -> {row['domain']}")
                sys.exit(1)
            if raw in seen:
                print(f"❌ Duplicate domain at line {i}: {raw}")
                sys.exit(1)
            seen.add(raw)

            # Required metadata
            cat = (row.get("category") or "").strip().lower()
            if cat not in category_set:
                print(f"❌ Invalid category at line {i}: '{cat}' (allowed: {sorted(category_set)})")
                sys.exit(1)

            evidence = (row.get("evidence") or "").strip()
            source = (row.get("source") or "").strip().lower()
            if not evidence or not source:
                print(f"❌ Missing evidence/source at line {i}: evidence='{evidence}', source='{source}'")
                sys.exit(1)

            # Optional checks
            rs = (row.get("risk_score") or "").strip()
            if rs:
                try:
                    val = int(float(rs))
                    if val < 0 or val > 100:
                        raise ValueError
                except Exception:
                    print(f"❌ risk_score must be 0-100 at line {i}: {rs}")
                    sys.exit(1)

            check_date((row.get("first_seen") or "").strip(), "first_seen", i)
            check_date((row.get("last_seen") or "").strip(), "last_seen", i)

    print(f"✅ {path} OK.")

def main():
    validate_csv(DOMAINS, ["domain","category","evidence","source"])
    validate_csv(ALLOW, ["domain"])

if __name__ == "__main__":
    main()
