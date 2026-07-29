# Zotero Ingest

Use this workflow whenever a source comes from Zotero or the user asks to repair Zotero metadata.
Apply the repository's `SCHEMA.md` first when its field names or path rules differ.

## Contents

- [Required order](#required-order)
- [Matching rules](#matching-rules)
- [Raw frontmatter](#raw-frontmatter)
- [Readable metadata block](#readable-metadata-block)
- [Metadata completion and fallback](#metadata-completion-and-fallback)
- [Backfill existing Zotero papers](#backfill-existing-zotero-papers)
- [Lint checks](#lint-checks)

## Required order

1. Identify the bibliographic **parent item key** by exact title, DOI, citation key, or a
   user-supplied key. Exclude note and attachment results.
2. Fetch the parent metadata before full text:
   - complete item metadata;
   - BibTeX or another structured bibliographic export;
   - child attachments and notes;
   - full text from the appropriate child attachment.
3. Use connected Zotero MCP tools when available. If an installed `zotero-cli` exposes the same
   operations, the equivalent sequence is:

   ```bash
   zotero-cli get metadata ITEM_KEY
   zotero-cli get bibtex ITEM_KEY
   zotero-cli get children ITEM_KEY
   zotero-cli get fulltext ITEM_KEY
   ```

4. Use the parent item's metadata as authoritative for Zotero identity. Use children only to
   capture attachment keys and filenames. Never substitute a PDF attachment key for the parent key.
5. Store a new raw record at the schema-registered paper path using the repository's lowercase
   kebab-case convention and the most precise publication date available.
6. Strip any transport-only duplicated title or metadata preamble from returned full text. Preserve
   the extracted-text bytes and normalize the assembled file to exactly one final LF during initial
   capture.
7. Compute `sha256` over everything after the closing frontmatter delimiter, including the readable
   metadata block and extracted text after final-newline normalization.

If the connector cannot return parent metadata, stop and report the blocker instead of silently
creating a metadata-free paper. A semantic-search database is optional for exact-key ingestion; an
empty ChromaDB index is not permission to bypass parent lookup.

## Matching rules

Prefer identifiers in this order:

1. Exact Zotero parent item key
2. Exact DOI
3. Exact citation key
4. Exact normalized title plus publication year

When title search returns multiple candidates, compare DOI, year, and first author. Do not select a
candidate on title similarity alone. A note titled “Untitled” or a PDF attachment is never the
bibliographic parent.

## Raw frontmatter

Use YAML lists for authors, tags, collections, and attachment keys. Quote values containing YAML
punctuation. Keep unavailable optional fields absent rather than filling them with `unknown`.

```yaml
---
source_type: zotero
zotero_item_key: ZXT9CKFK
zotero_attachment_keys: [TRUJTFYP]
item_type: journalArticle
title: "CTI-Thinker: an LLM-driven system for CTI knowledge graph construction and attack reasoning"
authors:
  - Yang, Xiuzhang
  - Zhong, Ruijie
published: 2026-01-16
publication: Cybersecurity
volume: "9"
issue: "1"
pages: "106"
doi: 10.1186/s42400-025-00505-y
issn: 2523-3246
url: https://doi.org/10.1186/s42400-025-00505-y
language: en
citation_key: Yang2026
zotero_tags: [Attack reasoning, Cyber threat intelligence]
zotero_collections: [NK7LTLD6]
ingested: 2026-07-14
metadata_status: complete
sha256: <body-only-sha256>
---
```

Require these fields for every Zotero paper unless `SCHEMA.md` is stricter:

- `source_type: zotero`
- `zotero_item_key`
- `item_type`
- `title`
- non-empty `authors`
- `published`, using the most precise Zotero date available
- at least one stable locator such as DOI, URL, ISBN, or arXiv URL
- `ingested`, `metadata_status`, and `sha256`

Capture all available optional fields: publication or container title, publisher, volume, issue,
pages, DOI, ISBN or ISSN, URL, language, citation key, Zotero tags, collection keys, attachment
keys, edition, place, conference, and series. Preserve Zotero values; do not invent missing
metadata from the PDF.

Set `metadata_status: incomplete` when a required field is missing, list the missing names in
`metadata_missing`, and tell the user. Retain an incomplete record only for explicit repair; do not
report it as a completed ingest.

## Readable metadata block

Place this immediately after frontmatter and before extracted text:

```markdown
# Paper Title

## Zotero Metadata

- Zotero Item Key: ZXT9CKFK
- Item Type: journalArticle
- Citation Key: Yang2026
- Authors: Yang, Xiuzhang; Zhong, Ruijie
- Published: 2026-01-16
- Publication: Cybersecurity 9(1):106
- DOI: 10.1186/s42400-025-00505-y
- URL: https://doi.org/10.1186/s42400-025-00505-y
- Attachment Keys: TRUJTFYP
- Tags: Attack reasoning; Cyber threat intelligence

## Abstract

<Zotero abstract, when present>

## Extracted Text

<Zotero full text>
```

Keep the abstract outside YAML to avoid large, fragile frontmatter. Repeat every available citation
field from frontmatter in the readable block so a person can audit the record without parsing YAML.
Do not include private Zotero notes unless the user explicitly asks to ingest them as distinct
sources.

## Metadata completion and fallback

Treat Zotero as authoritative for item identity and user curation. When an optional publication
field is missing, fill it from DOI, Crossref, publisher, or arXiv metadata only after matching a
stable identifier. Record the fallback source in `metadata_enriched_from`.

Never overwrite a conflicting Zotero value silently. Retain both values or ask the user when the
conflict changes citation identity.

## Backfill existing Zotero papers

Perform this only when the user explicitly asks for metadata repair:

1. Inventory candidate files by existing Zotero key, DOI, URL, title, and year.
2. Resolve each file to exactly one parent item using the matching rules.
3. Preserve the original extracted-text suffix for a byte comparison.
4. Add or repair frontmatter and the `## Zotero Metadata` block only.
5. Verify that the extracted-text suffix is byte-identical before and after the migration.
6. Recompute `sha256`, set `metadata_status`, and append one repair entry to `log.md` listing every
   updated file and unresolved item.

Keep an existing raw file at its current path during metadata backfill. Do not create a duplicate
record or move immutable source content unless the user explicitly requests a path migration; when
moving, update every canonical `sources` path in the same operation.

Ask before a backfill that would modify 10 or more raw files. Do not create canonical pages as a
side effect of metadata-only repair.

## Lint checks

For every `source_type: zotero` record, report:

- missing required fields or an empty author list;
- `metadata_status: complete` despite missing requirements;
- duplicate `zotero_item_key` values;
- an attachment key used as `zotero_item_key`;
- frontmatter values conflicting with the readable metadata block;
- a body hash mismatch;
- a missing `## Zotero Metadata` or `## Extracted Text` section;
- any raw-body change outside the explicitly authorized metadata-repair boundary.
