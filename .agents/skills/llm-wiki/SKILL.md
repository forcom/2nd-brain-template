---
name: llm-wiki
description: "Build, query, and lint the evidence-first Markdown wiki in the current project; ingest web, PDF, pasted, NotebookLM, and Zotero sources while preserving raw integrity and bibliographic metadata; maintain canonical pages, provenance, wikilinks, index.md, and log.md. Use for source ingestion, Zotero imports or metadata repairs, wiki questions, canonical updates, batch compilation, and wiki health checks."
---

# LLM Wiki

Maintain the current project as a durable, evidence-first Markdown knowledge base. Compile source
material once into interlinked canonical pages, preserve provenance, and keep every update
reviewable in Git.

## Establish the wiki root

Resolve every path from the current working directory:

```bash
WIKI="$(pwd -P)"
```

Require `$WIKI/SCHEMA.md`, `$WIKI/index.md`, and `$WIKI/log.md`. Stop and report the missing file
instead of silently choosing `~/wiki`, reading `WIKI_PATH`, or creating a second vault elsewhere.

## Orient before every operation

1. Read `SCHEMA.md` completely. Treat it as authoritative when this skill, a README example, an
   importer, or a tool convention differs.
2. Read `index.md` to discover active canonical subjects and avoid synonyms or duplicates.
3. Read the newest entries in append-only `log.md` to understand recent work and known gaps.
4. Search the current wiki before creating a page.

Use repository-relative paths in content and reports. Never record a user-specific absolute path in
source metadata.

## Respect the three layers

- Treat schema-registered Markdown under `raw/` as immutable evidence.
- Curate reusable knowledge only in `entities/`, `concepts/`, `comparisons/`, and `queries/`.
- Maintain `SCHEMA.md`, `index.md`, and `log.md` as the operational contract, catalog, and history.
- Treat `inbox/` as temporary intake, `docs/` as documentation, and graph/runtime directories as
  derived state rather than evidence. The repository may version the two schema-allowlisted graph
  snapshot files for sharing without making them canonical.

Do not cite attachments, generated graphs, documentation diagrams, or an inbox item as canonical
evidence.

## Ingest a source

1. Classify the source and choose a source directory registered by `SCHEMA.md`.
2. Capture a new raw Markdown record with the required metadata.
3. Compute `sha256` over the exact bytes after the closing frontmatter delimiter, including the
   final LF. Do not hash the frontmatter.
4. Preserve the captured raw body after initial ingest. Put corrections and interpretation in
   canonical pages.
5. Search `index.md` and canonical files for the source's central subjects.
6. Create a page only when the subject is central to one source or repeated across at least two
   sources. Update an existing page instead of creating a synonym.
7. Synchronize `index.md` and append one allowed `log.md` entry in the same transaction.
8. Run the complete contract checks before reporting success.

For web content, preserve the original URL and capture date. When the upstream page changes, create
a new versioned raw capture unless `SCHEMA.md` explicitly defines another operation; do not rewrite
the old captured body.

For importer-preserved legacy records, keep paths and bytes stable. Report missing hashes or final
newlines as documented coverage gaps instead of normalizing the files.

## Extract and verify facts with factlog

The `.factlog/` knowledge base reads `raw/` in place through the `.factlog/sources` symlink. It
never writes to `raw/`, so running it does not touch Layer 1 immutability.

factlog requires Python 3.11+ and runs on the ambient `python3`. This repository expects a pyenv
interpreter on the 3.14 line; install the CLI into it with
`python3 -m pip install -r .agents/plugins/factlog/requirements.txt -e .agents/plugins/factlog`.

The factlog plugin's gate hook resolves its interpreter from `FACTLOG_PYTHON` when that is set, and
blocks edits when the value does not point at a usable Python 3.11+. Leave it unset so the hook
falls through to `python3`.

After a raw record is captured and the contract checks pass, extract its claims and reconcile them
against the facts already accepted:

```bash
/factlog sync                 # extract candidate claims from raw/ into .factlog/facts/candidates.csv
/factlog query                # compile policy/questions.md into facts/query.dl
/factlog check                # compile accepted facts, run the logic check, print the report
```

Run `query` before `check`; the logic check evaluates the draft `query` produces. `sync`, `query`,
`check`, `repair`, and `ask` exist only as slash commands because each needs an in-session LLM step.
Everything else is Python CLI.

Review each candidate before it can influence a canonical page. Approval is a human step:

```bash
python3 -m factlog accept "<subject>" <relation> "<object>"
python3 -m factlog reject "<subject>" <relation> "<object>"
python3 -m factlog amend ...          # correct a value; never hand-edit candidates.csv
python3 -m factlog provenance "<subject>" <relation> "<object>"   # trace back to the raw/ record
```

Use the result as a research aid, not as evidence:

- Cite the `raw/` record that `factlog provenance` reports. Never cite `candidates.csv`,
  `accepted.dl`, `logic_report.txt`, or a `runs/` record as a canonical `sources` entry.
- Never promote a `needs_review` candidate into a canonical page. It has not cleared the trust
  boundary.
- Treat a reported conflict as a signal to read both cited raw records. When they genuinely
  disagree, record it on the canonical page with `contested: true` and populate `contradictions`.
- Extraction is not deterministic; verification is. Re-running `sync` may yield different
  candidates, so never treat its absence of a claim as evidence of absence.

Run `python3 -m factlog eject <path>` when a raw record is superseded, so its facts retire with it.

## Ingest or repair Zotero material

Read [references/zotero-ingest.md](references/zotero-ingest.md) before any Zotero ingest, batch,
or metadata repair.

Resolve the bibliographic parent item before reading full text. Fetch parent metadata, identifiers,
children, and attachment information first. Never use a PDF attachment key, note key, or attachment
title as the paper identity.

Treat Zotero metadata repair as the narrow raw mutation allowed by `SCHEMA.md`: replace only the
frontmatter and readable metadata block, prove the extracted-text suffix remains byte-identical,
and recompute the exact post-frontmatter hash.

## Curate canonical pages

Follow the active contract exactly:

- Start frontmatter at byte zero.
- Preserve `created` and bump `updated` for any content or metadata change.
- Make the directory agree with `type`.
- Use only tags registered in `SCHEMA.md`.
- Point every `sources` entry to an existing schema-registered raw Markdown record.
- Add claim-level `^[raw/...md]` markers for ambiguous, contested, or multi-source synthesis and
  ensure each marker already appears in the page's `sources` list.
- Maintain at least two distinct, resolvable, non-self canonical `[[wikilinks]]` per active page.
- Record unresolved sourced positions when `contested: true`; keep `contradictions` consistent.
- Split pages near the schema's line threshold while preserving useful links and provenance.

Never create a canonical page for a passing mention, an isolated free-form tag, or a generated
graph hypothesis that has not been verified against raw evidence.

## Answer and file queries

1. Locate relevant pages through `index.md`, filenames, tags, and content search.
2. Read the canonical pages and their cited raw records when accuracy depends on the source.
3. Answer from the compiled knowledge and identify the canonical pages used.
4. File only durable synthesis that would be costly to re-derive.
5. When filing, use `queries/` or `comparisons/` as appropriate and perform the full transactional
   update to the page, `index.md`, and `log.md`.

Do not file trivial lookups or unsupported speculation.

## Validate the wiki

Run the bundled deterministic gate validator:

```bash
python3 .agents/skills/llm-wiki/scripts/validate-wiki.py --gate a --gate b
```

Use `--require-clean-main` for scheduled graph generation. Run `--gate c` after graph generation
to verify deterministic input-hash freshness, complete article/source coverage, required node
fields, layers, tour steps, and dangling edges. Before Gate C, stamp the generated metadata:

```bash
python3 .agents/skills/llm-wiki/scripts/validate-wiki.py --write-graph-input-metadata
python3 .agents/skills/llm-wiki/scripts/validate-wiki.py \
  --gate c --require-clean-main --allow-graph-output-changes
```

The second command permits dirty state only for the versioned
`.understand-anything/knowledge-graph.json` and `.understand-anything/meta.json` outputs.

The validator checks:

1. Validate UTF-8, LF, no BOM, final-newline policy, canonical filenames, and byte-zero
   frontmatter.
2. Validate every required frontmatter field, enumeration, date, registered tag, and
   type-directory match.
3. Resolve every canonical `sources` path and every claim-level provenance marker.
4. Resolve canonical links, reject self-links, and enforce the minimum two distinct outbound
   targets.
5. Compare active canonical files with `index.md`; require a one-to-one, count-accurate catalog.
6. Recompute every recorded raw body hash without rewriting the file.
7. Validate every `log.md` heading and allowed action; use the Git diff to confirm prior entries
   remain unchanged and the new entry is append-only.
8. Report documented legacy coverage gaps separately from errors.
9. Keep graph data and other generated state out of canonical counts and evidence checks.

Group findings by integrity risk before style. Do not append a zero-issue lint entry unless every
applicable check actually ran.

## Run batch and scheduled work safely

For a batch, read all inputs first, build a source inventory, detect duplicates, then update
canonical pages in one pass. Update the index once and append one batch log entry listing every
affected path.

For Hermes or another scheduler:

- Set the repository with `--workdir`.
- Start each run in a fresh review branch.
- Process only validated new raw records.
- Return the diff and validation report.
- Do not merge or push unless the user explicitly authorizes that external change.
- Do not auto-promote graph output into canonical Markdown.
- Regenerate a graph only after deterministic Gate A and Gate B pass.
- Require every analysis batch to finish before replacing the last valid graph, then require
  deterministic Gate C to pass.
- Limit a successful graph run to the two allowlisted versioned snapshot files. Stamp their input
  fingerprint, return their diff for review, and do not commit, merge, or push unless the user
  explicitly authorizes it.

## Use Obsidian and graph tools

Open the repository root as the Obsidian vault. Use Graph View for explicit canonical
`[[wikilinks]]`; keep `.obsidian/` workspace and personal plugin state local unless the repository
contract explicitly allowlists a shared setting.

Treat Understand Anything or other graph output as reproducible derived state. The two versioned
snapshot files make the same enriched graph available to authorized clones but remain non-evidence.
Lint canonical Markdown before generation, verify the content fingerprint, complete coverage, and
dangling edges afterward, and validate any proposed relationship against raw evidence before
curating it.

## Protect sensitive and local state

Never commit credentials, cookies, authentication state, personal notes, private Zotero notes,
automation tokens, local databases, runtime logs, Obsidian workspace state, graph intermediates,
or generated caches. Commit graph output only when `SCHEMA.md` explicitly allowlists the snapshot
path and Gate C passes. Inspect staged files and ignore behavior before every commit that changes
integration, graph, or agent directories.
