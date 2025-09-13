import csv, re, sys
from pathlib import Path

DOMAINS = Path("data/domains.csv")
ALLOW = Path("data/allowlist.csv")

domain_re = re.compile(r"^[a-z0-9.-]+\.[a-z]{2,}$")

def validate_csv(path: Path, required_cols):
    with path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = [c for c in required_cols if c not in reader.fieldnames]
        if missing:
            print(f"❌ Missing required columns in {path}: {missing}")
            sys.exit(1)
        for i, row in enumerate(reader, start=2):
            d = row["domain"].strip().lower().split('/')[0]
            if d.startswith("www."):
                d = d[4:]
            if not domain_re.match(d):
                print(f"❌ Invalid domain at {path}:{i} -> {row['domain']}")
                sys.exit(1)
    print(f"✅ {path} OK.")

def main():
    validate_csv(DOMAINS, ["domain"])
    validate_csv(ALLOW, ["domain"])

if __name__ == "__main__":
    main()
