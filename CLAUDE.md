# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Start here

**Read `AGENTS.md` first** — it is the generated project knowledge base and takes precedence over the summary below. It documents the full directory contract, workflow, and gates. `SCHEMA.md` is the authoritative data contract referenced throughout AGENTS.md; consult it whenever a rule needs the exact wording. `README.md` covers optional tool setup (Obsidian, Zotero, MCP) and may describe a generic layout that does not match the current repo structure — AGENTS.md and SCHEMA.md win over README examples.

Before making any change:
1. Read `SCHEMA.md` in full.
2. Read `index.md` to see what canonical subjects already exist (avoid duplicates).
3. Read the tail of `log.md` for recent activity.

## What this repository is

A Markdown/Obsidian second-brain wiki, not a software project — there is no build, lint, or test tooling, and no application code to run. All work is editing Markdown files under a three-layer model defined in `SCHEMA.md`:

1. **Raw evidence** (`raw/*`) — immutable captured source records.
2. **Canonical pages** (`entities/`, `concepts/`, `comparisons/`, `queries/`) — curated synthesis that cites raw evidence and links to other canonical pages.
3. **Contract/navigation/log** (`SCHEMA.md`, `index.md`, `log.md`) — the rules, the catalog, and the append-only history.

## Non-negotiable rules

- Never edit a `raw/*` body after capture (the only exceptions are the two narrow metadata-repair operations defined in `SCHEMA.md`).
- Capture a PDF by reading its rendered page images, never with an OCR tool and never from the embedded text layer — Korean OCR is unreliable and the KS text layers drop table columns. See "PDF page images are the evidence" in `SCHEMA.md`.
- Every canonical page edit is only complete once `index.md` and `log.md` are updated in the same change — never rewrite or remove existing `log.md` entries.
- Canonical `sources` must point to real files under registered `raw/` subdirectories; a PDF/image attachment alone is not a valid source.
- Every tag used on a canonical page must already be registered in the SCHEMA.md tag taxonomy.
- `.understand-anything/knowledge-graph.json` and `meta.json` are derived/versioned exploration snapshots, not evidence — never cite graph output as a source or auto-promote it into canonical knowledge.

## Common commands

There is no build/test suite. The only routine commands are Git:

```bash
git add .
git commit -m "docs: ..."
git push
```

## Shared skill

`.agents/skills/llm-wiki/` is the versioned, audited project skill for wiki operations (capture, compile, validate). Prefer it over ad hoc edits when performing capture/compile/archive workflows; keep other local agent state out of version control.
