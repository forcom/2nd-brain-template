# Wiki Log

> Chronological record of wiki actions. This file is append-only: add entries at
> the end and never rewrite or remove an earlier entry.
>
> Entry heading format: `## [YYYY-MM-DD] <action> | <subject>`
>
> Allowed actions: `ingest`, `create`, `update`, `query`, `lint`, `archive`,
> `delete`, `map`, and `repair`.
>
> Each entry lists every affected repository-relative path. After 500 entries,
> rotate the completed file to `log-YYYY.md` and begin a new `log.md`; preserve the
> completed file unchanged.

## [2026-07-21] ingest | 2nd-Brain 개인지식 관리 원본 배치

- Selection: `understand-chat` identified the 2nd-Brain PKM core subgraph and its one-hop canonical neighbors; their leading frontmatter referenced 13 unique raw sources.
- Created:
  - `raw/notebooklm/2026-07-16-all-notes.md`
  - `raw/notebooklm/codegraph-github.md`
  - `raw/notebooklm/graphify-github.md`
  - `raw/notebooklm/llm-wiki-skill-github.md`
  - `raw/notebooklm/llm-wiki-zotero-notebooklm-youtube.md`
  - `raw/notebooklm/notebooklm-py-github.md`
  - `raw/notebooklm/understand-anything-github.md`
  - `raw/notebooklm/zotero-mcp-github.md`
  - `raw/web/NomaDamasslides-grab Best harness + editor + linter for generating slides in Claude Code  Codex - Claude Design Open Source Alternative.md`
  - `raw/web/stablyaiorca Orca is the ADE for working with a fleet of parallel agents. Run any coding agent with your own subscription. Available on desktop and mobile..md`
  - `raw/youtube/📺 How To Build LLM Wiki In Obsidian 🧠 A Memory Layer For Any Agentic AI.md`
  - `raw/youtube/📺 LLM Wiki를 업그레이드하는 외부 지식 시스템! 연구자를 위한 최강의 조합 Zotero × Notebook × Obsidian x Claude Code.md`
  - `raw/youtube/📺 Orca Is the Free Cursor Killer Nobody's Talking About!.md`
- Updated: `SCHEMA.md`, `AGENTS.md` to register importer-preserved raw directories and legacy hash-coverage handling.
- Integrity: all 13 target files are byte-identical to the source vault; all 8 recorded post-frontmatter body hashes match; 5 legacy web/video captures have no recorded `sha256` and retain their original missing final LF as explicit coverage and format gaps.
- Canonical state: unchanged at 0 pages; `index.md` was not modified.

## [2026-07-21] lint | 0 issues found

- Raw files in the imported source set: 13.
- Source/target byte-identical files: 13.
- Recorded post-frontmatter body hashes checked and matched: 8.
- Documented legacy hash-coverage and final-LF format gaps: 5.
- Invalid UTF-8, BOM, CRLF, body-hash drift, missing ingest-log paths, and unregistered importer directories: 0.
- Canonical pages and index entries: 0; no canonical navigation update was required.

## [2026-07-21] create | 2nd-Brain canonical 지식 코어

- Evidence: the existing 13-file raw source set was mapped to eight central, reusable PKM subjects; no raw record was duplicated or mutated.
- Created:
  - `concepts/ai-knowledge-workflow.md`
  - `concepts/ai-personal-knowledge-management.md`
  - `concepts/llm-wiki.md`
  - `concepts/research-feedback-loop.md`
  - `concepts/second-brain-research-workflow.md`
  - `comparisons/knowledge-tool-roles.md`
  - `queries/notebooklm-query-compounding.md`
  - `queries/ua-knowledge-graph-workflow.md`
- Updated:
  - `SCHEMA.md`
  - `index.md`
  - `log.md`

- Navigation: the eight-page graph uses only resolvable canonical wikilinks, with at least two distinct non-self links per page.
- Provenance: every source and claim marker resolves to an existing repository-relative raw Markdown path.

## [2026-07-21] lint | 0 issues found

- Canonical pages: 8 total (5 concepts, 1 comparison, and 2 queries); all required frontmatter fields, types, dates, confidence values, contestation fields, and contradiction lists are valid.
- Taxonomy and navigation: 9 registered tags, 8 exact alphabetical index entries, 33 canonical links, minimum 3 outbound links per page, and minimum 2 inbound links per page.
- Provenance: 27 source references and 17 claim-level markers resolve to existing raw Markdown records; no marker is absent from its page source list.
- Raw integrity: 13 Markdown records checked, 8 recorded body hashes matched, and 5 importer-preserved legacy hash/final-LF coverage gaps remain documented.
- Formatting, duplicate slugs, broken links, self-links, orphan pages, source drift, and lint warnings: 0.

## [2026-07-21] repair | lint source-reference count correction

- Correction: the immediately preceding lint entry reports 27 source references, but the measured canonical frontmatter total is 30.
- Unchanged measurements: 17 claim-level markers, 33 canonical links, 8 canonical pages, and 0 lint errors or warnings.
- Updated: `log.md` only; no raw or canonical page was changed.

## [2026-07-29] ingest | ISO·IEC·KS 표준 PDF 37개 배치

- Capture: 37 local PDFs, 2,386 pages, and 722,868,839 source bytes were converted into immutable Markdown source records; absolute user paths and PDF attachments were not copied into the repository.
- Extraction: 35 PDFs used reviewed embedded-text extraction; image-based `ISOIEC 27701 2025.pdf` and `ISOIEC 42001 2023(en).pdf` used reviewed 250 dpi Tesseract OCR.
- Integrity: all 37 source-PDF SHA-256 values and all 37 exact post-frontmatter raw body SHA-256 values matched after capture.
- Curation: related editions and language versions were consolidated into nine standards-family concepts plus one 37-source portfolio comparison; ISO/IEC 27001:2022 and KS X ISO/IEC 27001:2014 remain explicitly distinguished.
- Created raw records:
  - `raw/papers/iso-iec-27001-2022-en.md`
  - `raw/papers/iso-iec-27701-2019-en.md`
  - `raw/papers/iso-iec-27701-2025-en.md`
  - `raw/papers/iso-iec-42001-2023-en.md`
  - `raw/papers/ks-a-iso-37001-20260420-ko.md`
  - `raw/papers/ks-c-iec-61508-1-20251118-ko.md`
  - `raw/papers/ks-i-iso-14001-20210928-ko.md`
  - `raw/papers/ks-i-iso-14002-1-20211027-ko.md`
  - `raw/papers/ks-m-iso-22716-20250703-ko.md`
  - `raw/papers/ks-p-iso-13485-20231228-ko.md`
  - `raw/papers/ks-q-iso-9000-20210330-ko.md`
  - `raw/papers/ks-q-iso-9001-20241213-ko.md`
  - `raw/papers/ks-q-iso-9004-20220630-ko.md`
  - `raw/papers/ks-q-iso-10006-20241213-ko.md`
  - `raw/papers/ks-q-iso-22000-20210804-ko.md`
  - `raw/papers/ks-q-iso-31000-20210804-ko.md`
  - `raw/papers/ks-q-iso-45001-20241004-ko.md`
  - `raw/papers/ks-q-iso-45002-20241231-ko.md`
  - `raw/papers/ks-q-iso-ts-9002-20231017-ko.md`
  - `raw/papers/ks-r-iso-26262-1-20240524-ko.md`
  - `raw/papers/ks-x-iso-27799-20230605-ko.md`
  - `raw/papers/ks-x-iso-iec-22989-20231214-ko.md`
  - `raw/papers/ks-x-iso-iec-25000-20230421-ko.md`
  - `raw/papers/ks-x-iso-iec-25010-20210819-ko.md`
  - `raw/papers/ks-x-iso-iec-27001-20241030-ko.md`
  - `raw/papers/ks-x-iso-iec-27002-20251223-ko.md`
  - `raw/papers/ks-x-iso-iec-27017-20241030-ko.md`
  - `raw/papers/ks-x-iso-iec-27018-20241030-ko.md`
  - `raw/papers/ks-x-iso-iec-27032-20241030-ko.md`
  - `raw/papers/ks-x-iso-iec-27701-20220225-ko.md`
  - `raw/papers/ks-x-iso-iec-42001-20251030-ko.md`
  - `raw/papers/ks-x-iso-iec-ieee-29119-1-20231208-ko.md`
  - `raw/papers/ks-x-iso-iec-ieee-29119-2-20231208-ko.md`
  - `raw/papers/ks-x-iso-iec-ieee-29119-3-20231208-ko.md`
  - `raw/papers/ks-x-iso-iec-ieee-29119-4-20231208-ko.md`
  - `raw/papers/ks-x-iso-iec-tr-24028-20231214-ko.md`
  - `raw/papers/ks-x-iso-iec-tr-24029-1-20231214-ko.md`
- Created canonical pages:
  - `concepts/iso-ai-standards.md`
  - `concepts/iso-environmental-management-standards.md`
  - `concepts/iso-health-product-and-food-standards.md`
  - `concepts/iso-information-security-and-privacy-standards.md`
  - `concepts/iso-management-system-standards.md`
  - `concepts/iso-occupational-and-functional-safety-standards.md`
  - `concepts/iso-quality-management-standards.md`
  - `concepts/iso-risk-and-compliance-standards.md`
  - `concepts/iso-software-quality-and-testing-standards.md`
  - `comparisons/iso-standards-portfolio-map.md`
- Updated:
  - `SCHEMA.md`
  - `index.md`
  - `log.md`

## [2026-07-29] lint | 0 issues found

- PDF batch: 37 local-PDF raw records and 2,386 page markers; all 37 source-PDF hashes, byte counts, and new post-frontmatter body hashes matched.
- Canonical state: 18 pages total (14 concepts, 2 comparisons, and 2 queries), 18 exact alphabetical index entries, 77 unique canonical links, and minimum 2 outbound and 2 inbound links per page.
- Provenance: 112 canonical source references and 100 claim-level markers resolve; every marker appears in its page source list.
- Taxonomy and formatting: 21 registered tags; required frontmatter, type-directory fit, dates, confidence, contestation fields, contradiction lists, UTF-8, LF, final newlines, filenames, and 200-line limits all pass.
- Raw integrity: 50 Markdown records checked and 45 recorded body hashes matched; the five importer-preserved legacy web/video records retain their previously documented missing-hash and missing-final-LF coverage gaps.
- Duplicate slugs, broken links, self-links, orphan pages, source drift, index mismatches, and lint errors or warnings: 0.
- Updated: `log.md` only.

## [2026-07-29] repair | lint log entry ordering

- Correction: the ISO PDF batch lint entry had been inserted inside the 2026-07-21 canonical-create entry instead of after the 2026-07-29 ingest entry.
- Restored the original create entry's navigation and provenance lines to the same contiguous entry and relocated the unchanged lint block to chronological order.
- Updated: `log.md` only; no raw or canonical page was changed.

## [2026-07-29] map | Understand Anything wiki knowledge graph

- Precondition: all 18 canonical pages and index entries passed frontmatter, provenance, and link validation with 77 unique canonical links, 112 source references, and 100 claim markers.
- Detection: the Karpathy-wiki scan found 73 Markdown articles, 50 raw sources, 4 index topics, and 100 wikilinks; all 23 unresolved detector links are examples in README, schema, manual, or raw records rather than canonical links.
- Analysis: five complete article-analyzer batches added 33 deduplicated entities, 50 claims, and implicit relationships; merge dropped 0 dangling edges.
- Graph: `kind: knowledge`, 210 nodes, 186 edges, 5 layers, and 4 tour steps; every node has `id`, `type`, `name`, `summary`, `tags`, and `complexity`.
- Created derived state:
  - `.understand-anything/knowledge-graph.json`
  - `.understand-anything/meta.json`
- Updated:
  - `.gitignore`
  - `log.md`
- Cleanup: `.understand-anything/intermediate/` was removed after validation.

## [2026-07-30] lint | 0 issues found

- Review branch: `review/compile-wiki-2026-07-30`; no merge or push was performed.
- Intake: all 50 raw Markdown records are already represented by prior ingest entries; no additional unlogged raw record was promoted or processed.
- Canonical state: 18 pages and 18 exact alphabetical index entries; 77 unique canonical links with minimum 2 outbound and 2 inbound links per page.
- Provenance: 112 canonical source references and 100 claim-level markers resolve; every marker appears in its page source list.
- Raw integrity: 45 recorded post-frontmatter body hashes match, including all 37 pending PDF records and 2,386 page markers; five previously documented legacy web/video records remain hash-coverage and final-LF format gaps rather than drift.
- Contract checks: frontmatter, registered tags, type-directory fit, dates, confidence and contestation fields, canonical filenames, UTF-8/LF/BOM rules, final newlines, page-size limits, source paths, links, orphans, index count, raw drift, and log rotation all pass with 0 errors and 0 warnings.
- Updated: `log.md` only.

## [2026-07-30] update | versioned shared knowledge graph snapshot

- Sharing policy: only `.understand-anything/knowledge-graph.json` and `.understand-anything/meta.json` are versioned for authorized clones; analyzer batches, intermediate files, caches, tokens, legacy `.ua/`, and other runtime state remain ignored.
- Freshness contract: Gate C now verifies a deterministic `sha256-path-size-bytes-v1` fingerprint over every graph input instead of comparing the snapshot commit to `HEAD`; the graph and metadata retain the matching generation-base commit as ancestor provenance.
- Coverage contract: Gate C requires the exact Git-visible article and raw-source node sets, complete required node fields, valid layers and tour steps, and no dangling edges.
- Graph: five complete analyzer batches produced `kind: knowledge`, 212 nodes (75 articles, 50 sources, 34 deduplicated entities, 49 claims, and 4 topics), 190 edges, 5 layers, 4 tour steps, and 0 dangling edges.
- Automation: the review-only Hermes graph job now validates Gate A and Gate B, regenerates and stamps the two allowlisted outputs, validates Gate C, and leaves their diff for human review without committing, merging, or pushing.
- Updated:
  - `.agents/skills/llm-wiki/SKILL.md`
  - `.agents/skills/llm-wiki/scripts/validate-wiki.py`
  - `.gitignore`
  - `AGENTS.md`
  - `README.md`
  - `README.ko.md`
  - `SCHEMA.md`
  - `docs/architecture/second-brain-pkm-architecture.md`
  - `index.md`
  - `log.md`
  - `manual.md`
  - `queries/ua-knowledge-graph-workflow.md`
  - `.understand-anything/knowledge-graph.json`
  - `.understand-anything/meta.json`

## [2026-08-06] update | factlog fact-extraction and verification integration

- Tooling: added `semantic-reasoning/factlog` @ `6c1d5b6` as the Git submodule `.agents/plugins/factlog`, versioned through a new `.gitignore` exception under the otherwise ignored `.agents/` tree.
- Runtime: factlog requires Python 3.11+ while the system interpreter is 3.10, so the CLI runs through the unversioned `.venv` (pyrewire 1.0.4, factlog 0.8.0). `FACTLOG_PYTHON` pins the plugin hook to that interpreter from the gitignored `.claude/settings.local.json`, because a settings `env` value is passed through literally and `${CLAUDE_PROJECT_DIR}` does not expand, so only an absolute machine-specific path works.
- Ingest wiring: `.factlog/sources` is a symlink to `raw/`, so factlog reads all 50 raw records in place; it writes only under `.factlog/` and never mutates Layer 1 evidence.
- Evidence policy: factlog output is derived state. `candidates.csv`, `accepted.dl`, `logic_report.txt`, and `runs/` records are never valid canonical `sources`; a `needs_review` candidate must not enter a canonical page, and provenance resolves back to the cited `raw/` record.
- Fact model: registered `clause_title`, `obligation`, `annex_status`, and `edition_year` as attribute relations; declared `clause_title`, `maps_to_hls`, `annex_status`, and `edition_year` single-valued for conflict detection. `obligation` is deliberately multi-valued because one clause legitimately carries several modal levels.
- Domain policy: research questions require clauses namespaced by standard and edition, and logic rules cover certification-mandatory scope, HLS integration points, strictest-obligation resolution across standards, deliverable scope, and edition currency.
- Versioning split: `.factlog/facts/`, `policy/`, `decisions/`, and `templates/` are versioned as the reviewable trust boundary; `.factlog/runs/`, `pages/`, and `logic_report.txt` are ignored as regenerable engine state.
- Validator fix: `--write-graph-input-metadata` now writes `meta.json` bytes directly, since `write_text` with `newline="\n"` is not a valid combination for byte-exact output.
- Verification: Gate A and Gate B pass with 0 errors; `factlog status` resolves 50 sources, 4 attribute relations, and 4 single-valued relations. No `sync` has run yet, so the fact model is unvalidated against the corpus and 0 facts exist.
- Canonical state: unchanged at 18 pages and 18 index entries; no canonical page was created or edited, so `index.md` was not modified.
- Updated:
  - `.agents/plugins/factlog` (new submodule)
  - `.agents/skills/llm-wiki/SKILL.md`
  - `.agents/skills/llm-wiki/scripts/validate-wiki.py`
  - `.factlog/decisions/open-questions.md`
  - `.factlog/facts/candidates.csv`
  - `.factlog/policy/attribute-relations.md`
  - `.factlog/policy/logic-policy.md`
  - `.factlog/policy/questions.md`
  - `.factlog/policy/single-valued.md`
  - `.factlog/policy/prompts/natural_language_to_policy.md`
  - `.factlog/policy/prompts/self_correct.md`
  - `.factlog/policy/prompts/text_to_datalog.md`
  - `.factlog/policy/prompts/text_to_fact.md`
  - `.factlog/policy/sync-ignore.md`
  - `.factlog/policy/typed-relations.md`
  - `.factlog/sources` (symlink to `raw/`)
  - `.factlog/templates/pages.md`
  - `.gitignore`
  - `.gitmodules`
  - `CLAUDE.md`
  - `SCHEMA.md`
  - `log.md`
