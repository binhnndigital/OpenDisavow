# 🛡️ OpenDisavow

**OpenDisavow** is an open-source initiative that collects and maintains a list of **toxic / spam / referrer-farm domains** so the SEO community can easily generate a `disavow.txt` file for use with [Google Search Console](https://search.google.com/search-console).

**Goal:** Help SEO practitioners and webmasters **protect websites from unwanted backlinks** while **promoting transparency and knowledge-sharing** across the community.

---

## 🚀 Features

- Community-curated list of suspicious/toxic domains
- Auto-build `disavow.txt` from `data/domains.csv`
- `allowlist.csv` to prevent accidental removal of safe domains
- Scripts to normalize domains (punycode, strip `www.`, deduplicate)
- CI workflow to validate and build on every change
- Optional risk heuristics (`rules/heuristics.yaml`)

---

## 📂 Repository Structure

```
OpenDisavow/
├─ README.md
├─ data/
│  ├─ domains.csv
│  ├─ allowlist.csv
├─ rules/
│  ├─ heuristics.yaml
├─ tools/
│  ├─ merge_and_build.py
│  └─ validate.py
├─ build/
│  └─ disavow.txt
└─ .github/
   └─ workflows/
      └─ ci.yml
```

---

## ⚙️ Usage

Clone this repository:

```bash
git clone https://github.com/binhnndigital/OpenDisavow.git
cd OpenDisavow
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Build `disavow.txt`:

```bash
python tools/merge_and_build.py
```

> The generated file appears at `build/disavow.txt`. Review it manually before uploading to the
> [Google Disavow Tool](https://search.google.com/search-console/disavow-links).

---

## 📥 Import from TXT

If you keep a plain `.txt` list (one domain per line), use the helper:

```bash
python tools/import_from_txt.py input/new_domains.txt \  --category spam --source community --evidence "Community report" --first-seen 2025-09-13
python tools/validate.py
python tools/merge_and_build.py
```

See `HOWTO_TXT_IMPORT.md` and `input/new_domains.txt` (sample).

---

## 🤝 Contributing

We welcome community contributions!

- **Add new domains:** open an Issue with the template in `ISSUE_TEMPLATE/new_domain.md`
- **Fix / review:** submit a Pull Request with reasoning and evidence
- **Discussions:** use the Discussions tab
- See `CONTRIBUTING.md` for more details

---

## ⚠️ Important Notice

- Disavow is an extreme SEO action—misuse can remove valid backlinks and harm rankings.
- Always review the list and `allowlist.csv` before applying.
- This list is **for reference only**; **no legal warranty**. You are responsible for any submission to Google Search Console.

---

## 📜 License

**Temporary status (as of 2025-09-13)**: License **TBD** by the project owner. Until a license is added,
all rights are reserved by the author. External contributors should assume their contributions will be
relicensed once the project selects an official license. See `NOTICE` for details.

---

## ✍️ Author

**BinhNN Digital**  
🌐 https://binhnn.dev  
📧 contact@binhnn.dev  
💻 https://github.com/binhnndigital
