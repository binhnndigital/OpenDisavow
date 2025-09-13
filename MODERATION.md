# Moderation Policy

OpenDisavow curates *indicative* domains for disavow. We avoid absolute labels like "bad" or "malicious".

## Evidence Requirements
Every new domain MUST include:
- `category` (spam | pbn | ghost-referrer | adult | casino | malware | other)
- `evidence` (short description + at least one verifiable link/screenshot URL)
- `source` (tool or origin, e.g., "GSC export", "crawler", "community")
- Optional but recommended: `risk_score` (0-100), `first_seen`, `last_seen` (YYYY-MM-DD)

Submissions without evidence are rejected by CI.

## Review Workflow
1. **Issue → PR**: Propose a domain via Issue template, then submit a PR referencing the Issue.
2. **Automated checks**: CI validates CSV schema/format and basic heuristics.
3. **Human review**: A maintainer checks evidence, category, and risk rationale.
4. **Merge**: Squash merge after at least **1 maintainer approval**.
5. **Appeals/Removal**: Domain owners may file an appeal (see template) with remediation proof.

## Anti-Abuse
- Limit scope to root domains (`domain: example.com`).
- Maintain `data/allowlist.csv` to exempt well-known safe domains.
- Neutral language: “indicative of low-quality per criteria”.
- Rate-limit: large bulk additions may be split into batches for proper review.
- No doxxing, no personal data, no targeted harassment.

## Transparency
- Keep change log via PRs.
- Provide rationale in commit messages and Issues.
