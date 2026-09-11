# PROJECT KNOWLEDGE BASE

**Generated:** 2026-07-30
**Commit:** bb25df8
**Branch:** main

## OVERVIEW

- Markdown/Obsidian second-brain template using an evidence-first LLM wiki model.
- The repository root is the wiki root; no database, service, or build system exists.
- `SCHEMA.md` is the operational contract. `README.md` covers optional tool setup
  but describes a generic PARA layout that is not the current repository structure.
- Current curated state: 50 raw Markdown records and 18 canonical pages.

## START HERE

1. Read `SCHEMA.md` completely.
2. Read `index.md` to find existing canonical subjects and avoid duplicates.
3. Read the newest entries in append-only `log.md` before changing the wiki.
4. Resolve every path relative to this repository root.

## STRUCTURE

```text
./
├── .agents/
│   └── skills/llm-wiki/ # Shared, audited project skill; other agent state stays ignored
├── inbox/                 # Temporary intake; neither evidence nor canonical
├── raw/
│   ├── articles/          # Immutable captured article Markdown
│   ├── notebooklm/        # Immutable NotebookLM-imported source records
│   ├── papers/            # Immutable extracted paper and standards records
│   ├── transcripts/       # Immutable captured transcript Markdown
│   ├── web/               # Importer-preserved web captures
│   ├── youtube/           # Importer-preserved video transcript captures
│   └── assets/            # Local assets referenced by raw records
├── entities/              # Canonical type: entity
├── concepts/              # Canonical type: concept
├── comparisons/           # Canonical type: comparison
├── queries/               # Canonical type: query
├── docs/
│   ├── architecture/      # Narrative architecture plus rendered exports
│   ├── tech-stack/        # Editable and rendered technology-stack diagram
│   └── workflow/          # Editable and rendered workflow diagram
├── .understand-anything/
│   ├── knowledge-graph.json # Versioned shared graph snapshot
│   └── meta.json            # Input fingerprint and generation provenance
├── SCHEMA.md              # Authoritative content and integrity contract
├── index.md               # Complete active canonical catalog
└── log.md                 # Append-only wiki operation history
```

`raw/papers/files/`, `templates/`, and `_archive/` are schema-defined, on-demand
paths. Ignored `.obsidian/` is local editor configuration and ignored `.ua/` is a
legacy graph path. Only the two allowlisted `.understand-anything/` snapshot files
are versioned; they remain derived state and never canonical evidence.

## WHERE TO LOOK

| Task | Location | Notes |
| --- | --- | --- |
| Learn the rules | `SCHEMA.md` | Wins over README examples |
| Install optional tools | `README.md` | Obsidian, Zotero, MCP, CLI, and agent skills |
| Use or maintain the shared skill | `.agents/skills/llm-wiki/` | Versioned project skill; keep unrelated local agent links ignored |
| Find existing knowledge | `index.md` | Count must equal active canonical files |
| Understand recent work | `log.md` | Read the tail; never rewrite history |
| Stage unclassified input | `inbox/` | Capture properly before canonical use |
| Preserve source evidence | Registered source directories under `raw/` | Body integrity boundary; preserve importer paths |
| Curate reusable knowledge | `entities/`, `concepts/`, `comparisons/`, `queries/` | Folder and frontmatter `type` must agree |
| Inspect architecture and diagrams | `docs/` | Deliverables only; not raw or canonical evidence |
| Inspect the shared enriched graph | `.understand-anything/knowledge-graph.json` | Versioned derived snapshot; validate with Gate C |
| Inspect local editor behavior | `.obsidian/` | Git-ignored; wikilinks enabled and attachments use `raw/assets` |

## CONTENT CONTRACT

- Canonical filenames are lowercase kebab-case and end in `.md`.
- Canonical frontmatter starts at byte zero and contains `title`, `created`,
  `updated`, `type`, `tags`, `sources`, `confidence`, `contested`, and `contradictions`.
- Preserve `created`; bump `updated` whenever content or metadata changes.
- Register tags in the `SCHEMA.md` taxonomy before use; 21 tags currently exist.
- Use `confidence: high` only when multiple sources support the content.
- When `contested` is true, record dated, sourced unresolved positions in the body;
  `contradictions` lists conflicting canonical slugs or is empty.
- Replace or remove every `<angle-bracket>` token before promoting a template copy
  to a raw record or canonical page.
- Create a page only for a source's central subject or a subject repeated across
  at least two sources. Update an existing subject instead of creating a synonym.
- Split pages near 200 lines while preserving provenance and useful links.
- Every canonical page needs two distinct, resolvable, non-self `[[wikilinks]]`
  to active canonical pages; one- and two-page canonical sets are invalid.

## RAW INTEGRITY AND PROVENANCE

- Treat captured raw bodies as immutable.
- Keep the GitHub repository private while licensed standards source records are
  present; never make it public or redistribute those records without explicit
  owner authorization and an access-rights review.
- Compute raw `sha256` over the exact post-frontmatter body bytes.
- Preserve byte-identical legacy imports with missing `sha256` or final LF;
  report coverage/format gaps instead of normalizing paths, frontmatter, or EOF.
- Only the Zotero metadata-repair and NotebookLM frontmatter-mapping operations
  defined in `SCHEMA.md` may mutate a raw record; follow their byte-preservation
  requirements exactly.
- Capture a PDF from its **rendered page images**, transcribed by reading them
  (`extraction_method: llm-vision-transcription`). Never capture a PDF body with an
  OCR tool or from its embedded text layer: Korean OCR is unreliable, and the KS
  text layers are reflowed and drop table columns. Rendering and text-layer probing
  are allowed as diagnosis; only the body that lands in `raw/` is constrained.
- Re-extracting a PDF with a better method is not a permitted mutation. Add a new
  versioned record beside the old one and say in `log.md` which one to cite.
- Put corrections and interpretation in canonical pages, never in captured text.
- Canonical `sources` entries must be exact, existing repository-relative raw
  Markdown paths under a source directory registered in `SCHEMA.md`. Assets and
  attachments do not qualify as sources.
- A claim-level `^[raw/...md]` marker must resolve and already appear in that
  page's `sources` list.

## TRANSACTIONAL WIKI UPDATES

For every canonical create, update, filed query, archive, or delete:

1. Keep `index.md` alphabetic, type-correct, unique, and count-accurate.
2. Append one `log.md` entry using an allowed action and list every affected path.
3. Archive only fully superseded pages; repair active links and remove them from
   the index.

Never index raw records, docs, templates, archived pages, or generated outputs as
active canonical pages.
Log headings use `## [YYYY-MM-DD] <action> | <subject>`; actions are `ingest`,
`create`, `update`, `query`, `lint`, `archive`, `delete`, `map`, and `repair`.
Rotate after 500 entries without changing the completed log. Split an index section
after 50 entries and add thematic navigation after 200 total entries.

## COMMANDS AND VALIDATION

Run the shared deterministic gate checker before graph generation and again after
the graph is built. Generate the graph from a copy holding only the files Git sees —
the Understand-Anything parser ignores `.gitignore` while Gate C does not, so parsing
the repository in place inflates the article count roughly tenfold and fails the gate.
See "Generate the graph from a git-visible copy" in the llm-wiki skill:

```bash
python3 .agents/skills/llm-wiki/scripts/validate-wiki.py --gate a --gate b
python3 .agents/skills/llm-wiki/scripts/validate-wiki.py --write-graph-input-metadata
python3 .agents/skills/llm-wiki/scripts/validate-wiki.py \
  --gate c --require-clean-main --allow-graph-output-changes
```

No build, CI, or release pipeline is configured. The checker covers the deterministic
contract below; still inspect semantic contradictions and batch-analysis outcomes
directly:

- UTF-8, LF, no BOM, final newline, and correct leading frontmatter; documented
  byte-identical legacy raw imports may retain their original missing final LF.
- Required fields, date/enumeration values, registered tags, and type-directory fit.
- Existing source paths and valid claim-level provenance markers.
- Two valid outbound canonical links per page and no broken canonical links.
- Filesystem canonical count equals `index.md`; each active page appears once.
- Raw hashes still match exact post-frontmatter bytes.
- Obsidian JSON remains parseable after shared setting changes.
- Before graph generation, lint canonical state; afterward verify `kind: knowledge`,
  complete batches, full article/source coverage, content-hash freshness, required
  node fields, and no dangling edges.

## ANTI-PATTERNS

- Do not use README's PARA tree, optional metadata/free tags, or Markdown-link
  guidance for canonical work; the active `SCHEMA.md` contract wins.
- Do not edit raw bodies, invent provenance paths, or treat attachments as evidence.
- Do not create passing-mention, isolated, free-form-tag, or duplicate canonical pages.
- Do not rewrite prior `log.md` entries or silently omit index/log synchronization.
- Do not treat `docs/`, `.ua/`, or the versioned `.understand-anything/` snapshot
  as evidence, auto-promote graph output, or overwrite canonical Markdown from
  graph hypotheses; verify against raw sources.
- Do not commit credentials, personal data, Obsidian workspace state, local plugin
  symlinks, automation tokens/log URLs, copied assets, graph intermediate/cache
  files, `output/`, or QA artifacts. Only `knowledge-graph.json` and `meta.json`
  are allowlisted graph outputs. The audited `.agents/skills/llm-wiki/` directory
  is the sole allowlisted project skill; keep other `.agents/` contents ignored.

## NOTES

- Markdown is the durable asset; Obsidian is an optional editing and graph UI.
- `templates/` and `_archive/` should be created only when their workflows require
  them, not merely to fill the tree.
- No code-symbol map exists. Even explicit project-path Codegraph queries return
  ancestor/global cache data, and no Markdown LSP is active; reject both as evidence.
