# Long COVID (ME/CFS Subtype) — Knowledge Base

A curated, peer-reviewed research corpus on the ME/CFS subtype of long COVID, covering
pathophysiology/mechanisms, treatments & clinical trials, and the long COVID ↔ ME/CFS overlap.

## Files
- `longcovid_mecfs_knowledge_base.md` — human-readable document: 25 sources grouped by theme,
  each with citation, study type, impact tier, verified DOI link, and a 2–3 sentence summary.
- `longcovid_mecfs.db` — SQLite database (same corpus, structured).
  Schema: `sources(id, theme, title, authors, journal, year, doi, pmid, url, impact_tier, study_type, summary)`
- `metadata.json` — Datasette configuration (facets, column descriptions).

## Browse the database
```bash
pip install datasette
datasette longcovid_mecfs.db -m metadata.json
# open http://localhost:8001 — faceted by theme, impact_tier, study_type, year
```

## Rigor notes
- DOIs verified against Europe PMC; no preprints.
- Observational work limited in favor of reviews, RCTs, and landmark mechanistic studies
  from high-impact journals.
- Two negative RCTs (rituximab; metformin/UDCA) are included deliberately — high-quality
  null results are core to an honest evidence base.
- `impact_tier`: **flagship** = Nature/Science/Nature Medicine/PNAS/Nature Reviews/Nature
  Immunology/JAMA-tier or the IOM consensus report; **high**/**solid** = strong specialist journals.
