# Add domains from TXT

Put your plaintext list at `input/new_domains.txt` (one domain per line). Then run:

```bash
python tools/import_from_txt.py input/new_domains.txt \  --category spam \  --source community \  --evidence "Community report" \  --first-seen 2025-09-13
python tools/validate.py
python tools/merge_and_build.py
```

The importer will:
- Ignore comments (`# ...`)
- Accept `domain: example.com` and full URLs (extracts hostname)
- Skip duplicates and invalid domains
