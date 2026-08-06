# Wiki Schema

## Repository orientation

This repository root is the wiki root. Every wiki operation resolves paths from the
current project root; no database, hosted service, or separate vault is required.
Before curating, read this file, `index.md`, and the most recent entries in `log.md`.

## Three layers

1. **Layer 1 — raw immutable source evidence:** Markdown source records live under
   `raw/`. Their captured body is immutable except for the two narrow metadata
   operations defined below.
2. **Layer 2 — canonical pages:** Curated pages live only in `entities/`,
   `concepts/`, `comparisons/`, and `queries/`. These pages synthesize and connect
   raw evidence; they never replace it.
3. **Layer 3 — schema, navigation, and log metadata:** `SCHEMA.md` defines the
   contract, `index.md` is the complete canonical catalog, and `log.md` is the
   append-only action history.

Zero canonical pages is a valid wiki state. The initial repository deliberately
contains no raw source record and no canonical page.

## Directory roles

| Path | Role |
| --- | --- |
| `inbox/` | Temporary intake awaiting classification and capture; not canonical evidence. |
| `raw/articles/` | Immutable captured article or clipping Markdown. |
| `raw/notebooklm/` | Immutable importer-preserved NotebookLM source records and source identifiers. |
| `raw/papers/` | Immutable text captures of local or imported papers and standards, with source-file and extraction metadata. |
| `raw/papers/files/` | Optional copied paper attachments; initially only the empty `.gitkeep` placeholder is allowed. |
| `raw/transcripts/` | Immutable captured transcript Markdown. |
| `raw/web/` | Immutable importer-preserved web captures whose existing provenance paths must remain stable. |
| `raw/youtube/` | Immutable importer-preserved video metadata and transcript captures. |
| `entities/` | Canonical pages whose exact `type` is `entity`. |
| `concepts/` | Canonical pages whose exact `type` is `concept`. |
| `comparisons/` | Canonical pages whose exact `type` is `comparison`. |
| `queries/` | Canonical filed syntheses whose exact `type` is `query`. |
| `_archive/` | Fully superseded canonical pages removed from active navigation. |
| `.understand-anything/knowledge-graph.json` | Versioned, reproducible graph snapshot for shared exploration; derived state, never evidence. |
| `.understand-anything/meta.json` | Versioned graph provenance and deterministic input fingerprint. |
| `.factlog/sources` | Symlink to `raw/`; the factlog knowledge base reads evidence in place and never writes here. |
| `.factlog/facts/` | Extracted claim review queue (`candidates.csv`) and accepted engine input (`accepted.dl`); derived state, never evidence. |
| `.factlog/policy/` | Hand-edited factlog review questions, logic policy, and relation declarations. |
| `.factlog/decisions/` | Recorded factlog review decisions and open questions. |

A factlog claim is never a citable source. Cite the `raw/` record the claim was
extracted from, which `factlog provenance` reports. A `needs_review` candidate has
not cleared the human trust boundary and must not enter a canonical page at all.

## File and frontmatter rules

- Markdown is UTF-8, uses LF line endings, and has no byte-order mark.
- Canonical file names use lowercase words separated by hyphens and end in `.md`;
  imported raw file names and relative paths are preserved exactly.
- Frontmatter, when required, starts at byte zero with `---` followed by LF.
- Every canonical page has these fields: `title`, `created`, `updated`, `type`,
  `tags`, `sources`, `confidence`, `contested`, and `contradictions`.
- Canonical `type` is exactly one of `entity`, `concept`, `comparison`, or `query`,
  and it must match the containing directory.
- `created` and `updated` are calendar dates. Preserve `created`; change `updated`
  whenever the page content or metadata changes.
- `confidence` is exactly `high`, `medium`, or `low`. Use `high` only for evidence
  supported across multiple sources.
- `contested` is a YAML boolean. When it is `true`, describe unresolved positions
  with dates and provenance in the body. `contradictions` is a list of canonical
  page slugs whose claims conflict; use an empty list when there is no conflict.

Templates live outside canonical directories and are not pages. All angle-bracket
tokens in a copied template must be replaced or removed before the copy can become
a valid source record or canonical page.

## Tag taxonomy

- Every tag used by a canonical page must first be registered in this section.
- Register a tag before using it, and keep its spelling stable.
- Add only tags that fit the chosen wiki domain; do not seed domain tags here.

### Registered tags

- `artificial-intelligence`: AI concepts, systems, governance, and assurance.
- `automation`: deterministic or agent-driven workflow automation.
- `compliance`: organizational obligations, controls, and conformity practices.
- `comparison`: explicit side-by-side analysis of tools or methods.
- `environmental-management`: environmental aspects and management systems.
- `healthcare`: health, medical-device, and health-information contexts.
- `information-security`: information security and cybersecurity governance or controls.
- `knowledge-base`: durable, structured knowledge systems.
- `knowledge-graph`: graph-derived relationship analysis.
- `management-system`: organization-wide policy, objective, process, and review systems.
- `notebooklm`: source-scoped NotebookLM workflows.
- `pkm`: personal knowledge management.
- `privacy`: privacy information management and personally identifiable information protection.
- `provenance`: source traceability and claim lineage.
- `quality-management`: quality systems, models, practices, and improvement.
- `research`: research collection, synthesis, and verification.
- `risk-management`: risk principles, frameworks, and treatment.
- `safety`: occupational, functional, product, or food safety.
- `software-engineering`: software quality, lifecycle, and testing practices.
- `standards`: formal standards, technical specifications, and technical reports.
- `workflow`: ordered operational processes and feedback loops.

## Raw source integrity

Initial capture establishes an immutable raw record. The `sha256` field is the
SHA-256 digest of the exact post-frontmatter body bytes: every byte after the LF
that terminates the closing `---` delimiter through end of file. For a Zotero
record this includes the readable Zotero metadata block, extracted-text suffix,
and the normalized final LF.

Byte-identical records copied from a trusted legacy vault may lack a recorded
`sha256`. Preserve those files exactly, record the whole-file source/target hash
comparison in `log.md`, and report the missing field as a hash-coverage gap rather
than source drift. Do not add frontmatter merely to normalize a legacy capture.
A trusted legacy copy may also retain its original missing final LF. Treat that as
a documented format gap, not permission to alter the immutable raw bytes.

A local PDF capture under `raw/papers/` records `source_type`, the source basename
without a user-specific absolute path, document identifier, language, page and byte
counts, source-PDF SHA-256, extraction method and quality, extracted-text SHA-256,
`ingested`, and the post-frontmatter body `sha256`. Text-layer extraction and OCR
are both permitted when their method is explicit. Normalize only during initial
capture: use LF, replace PDF form feeds with numbered page markers, remove NUL and
backspace controls, and end with one LF. Do not copy the PDF into
`raw/papers/files/` unless attachment preservation is explicitly required.

Only these raw-record mutations are allowed:

1. **Zotero metadata repair:** replace raw frontmatter and the readable Zotero
   metadata block only, prove the extracted-text suffix remains byte-exact, and
   recompute `sha256` over the resulting complete post-frontmatter body.
2. **NotebookLM mapping:** change only byte-zero leading frontmatter, preserve
   every body byte, and preserve the existing `sha256` scalar byte-for-byte.

No other edit to a captured raw body is allowed. Corrections and interpretations
belong in canonical pages. A copied attachment does not substitute for its raw
Markdown record or for Zotero parent metadata.

## Provenance

- Every canonical `sources` item is an exact repository-relative path to an
  existing raw Markdown record under a source directory registered in the table
  above, including importer-preserved `raw/notebooklm/`, `raw/web/`, and
  `raw/youtube/` paths.
- Assets and attachments may support a raw record but are not canonical `sources`
  entries by themselves.
- Never invent, approximate, or retain a source path that does not resolve.
- Where a synthesized paragraph needs claim-level attribution, append a marker of
  the form `^[raw/<source-kind>/<source-file>.md]`. Use markers for multi-source
  synthesis, contested claims, or wherever the frontmatter list alone is
  ambiguous. Each marker must resolve to a path already listed in `sources`.

## Canonical link validity

Explicit Obsidian `[[wikilinks]]` connect canonical pages. When the canonical set
is nonempty, every canonical page must contain at least two distinct, resolvable,
non-self links to other canonical pages. Targets must resolve to active Markdown
pages in one of the four canonical directories.

Therefore a one-page or two-page canonical set is invalid. A three-page set can be
valid only when every page satisfies the same two-target rule. Links to templates,
raw records, archived pages, headings in the same page, or missing targets do not
count toward the minimum.

## Page thresholds and maintenance

- Create a canonical page when its subject appears in at least two raw sources or
  is central to one source.
- Add evidence to an existing page when the subject is already covered.
- Do not create pages for passing mentions, minor details, or out-of-domain items.
- Split a canonical page when it grows beyond roughly 200 lines, preserving links
  and provenance in both resulting pages.
- Archive a page only when it is fully superseded. Move it under `_archive/`,
  remove it from `index.md`, update active links, and append the archive to
  `log.md`.

## Index and log synchronization

For every canonical create, update, filed query, archive, or delete operation:

1. Update `index.md` in the same operation. List every active canonical page once
   under its matching type, sort entries alphabetically, keep a one-line summary,
   and make the total equal the filesystem canonical-page count.
2. Append one entry to `log.md` in the defined heading format. Record the action,
   subject, and every repository-relative file created, updated, archived, or
   deleted.
3. Never list raw records, templates, or archived pages as active canonical index
   entries. Never rewrite or remove prior log entries.

When an index section exceeds 50 entries, divide it into stable subsections. When
the full index exceeds 200 entries, add a thematic navigation map without changing
the canonical count. Rotate the log only under its policy in `log.md`.

## Versioned knowledge-graph snapshot

The repository versions only `.understand-anything/knowledge-graph.json` and
`.understand-anything/meta.json` so authorized clones can open the same enriched
graph without first regenerating it. These files remain derived output: they are
not raw evidence, canonical pages, active index entries, or valid `sources`.
Legacy `.ua/`, `.understand-anything/intermediate/`, analyzer batches, dashboard
tokens, caches, and other runtime files remain unversioned.

Gate C identifies freshness by a deterministic graph-input fingerprint rather
than requiring `meta.gitCommitHash` to equal the snapshot commit. The input set is:

1. Every Git-visible Markdown article that the Understand Anything parser scans,
   excluding root-level `index.md`, `log.md`, `CLAUDE.md`, `AGENTS.md`, and
   `SOUL.md`.
2. Root `index.md` and `log.md`, which affect categories and operation context.
3. Every non-hidden Git-visible file below `raw/`, including a future explicitly
   versioned attachment.

For `sha256-path-size-bytes-v1`, sort repository-relative paths by their UTF-8
bytes, initialize SHA-256 with the UTF-8 algorithm name followed by NUL, and then
append for each input: UTF-8 path, NUL, decimal byte length, NUL, exact file bytes,
and NUL. Store the result as `inputHash: sha256:<hex>`, plus the exact algorithm
name and input count in `meta.json`.

The graph project and metadata `gitCommitHash` values must match. They record the
generation base commit for provenance and must resolve to the current commit or one
of its ancestors. The value is not the freshness authority, because committing the
graph necessarily creates a newer commit. Before replacing a shared snapshot, Gate
A and Gate B must pass, every analyzer batch must finish, the input fingerprint
must be written, temporary files must be removed, and Gate C must pass. A failed
generation restores the previous versioned graph files.
