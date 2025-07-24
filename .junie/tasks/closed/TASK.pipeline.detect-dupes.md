# TASK.pipeline.detect-dupes.md

## 🧩 Task: Deduplicate GPU Listings via Embedding Similarity

Junie, your task is to implement a `dedup` subcommand for the `glyphsieve` CLI that identifies likely duplicate listings using semantic similarity on the `title` column. This is especially useful for marketplaces like eBay, where vendors may repost the same item multiple times with slight phrasing differences.

---

## 🎯 Objectives

- Add a `glyphsieve dedup` CLI command
- Accept input CSV with at least a `title` column
- Compute semantic embeddings for each title
- Cluster or compare listings using cosine similarity
- Flag likely duplicates and emit a new column: `dedup_status`

---

## 🧠 Deduplication Logic

1. Use the `sentence-transformers` library with the `all-MiniLM-L6-v2` model (or similar)
2. For each listing:
   - Compute its embedding vector
   - Group listings by cosine similarity ≥ 0.95 (configurable) as candidate duplicates
   - For listings within a group, only mark as duplicates if:
     - URLs are identical
     - OR prices are identical (or near-identical within epsilon threshold)
     - OR metadata (e.g. seller, listing_age) strongly suggests redundancy

  - Before comparing URLs, sanitize known vendor links (e.g., eBay) by removing tracking or query params:
    - `https://www.ebay.com/itm/123456?campid=abc123` → `https://www.ebay.com/itm/123456`
    - Listings that resolve to the same base URL should be considered the *same listing*
    - In these cases, prefer the newest record (if timestamped) or retain the last loaded entry and normalize its title downstream

   - Listings with same title but distinct URLs and pricing are **not** duplicates — they represent real market signal and should be preserved.

3. Annotate listings as:
   - `UNIQUE`
   - `DUPLICATE_PRIMARY` (the first occurrence in a redundant group)
   - `DUPLICATE_SECONDARY` (subsequent listings that meet redundancy criteria)

Optional: emit a `dedup_group_id` for matched groups.

---

## 📦 Dependencies

Install with:
```bash
uv add sentence-transformers scikit-learn
```

---

## 📁 Structure

- Core logic: `glyphsieve/core/deduplication.py`
- CLI subcommand: `glyphsieve/cli/dedup.py`

---

## 🧪 Output

- Appends a `dedup_status` column to the output CSV
- Optionally: `dedup_group_id` column for grouped matches
- Retains original title and price fields for audit
- Normalize URLs before reporting duplicates
- Preserve only the winning/latest record per base URL match

---

## 🧪 Tests

- Use small synthetic CSV with similar/variant titles
- Ensure matches are stable and accurate
- Validate that fuzzy duplicates are flagged while distinct listings are preserved

---

## ✅ Completion Criteria

- `uv run glyphsieve dedup --input foo.csv --output bar.csv` works
- Semantic matches are detected and flagged
- Results are deterministic (e.g. first item is primary)
- Code is testable and performant for ≤ 1000 listings
- Tests run via `uv run pytest`

---

## ✍️ Notes

This task improves dataset quality and helps prevent skew in scoring or rack planning. Later extensions may include seller awareness or time window constraints.