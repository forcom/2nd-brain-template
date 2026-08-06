# Sync-ignore list
#
# STAGED ROLLOUT — PHASE 1 (HLS comparison set).
#
# The fact model in questions.md, single-valued.md, and logic-policy.md has
# never been run against a real standard. Extracting all 50 sources before it is
# validated would mean redoing all 50 when the model turns out wrong, so phase 1
# extracts only the four Annex SL management-system standards that share the HLS
# structure. They exercise the parts most likely to be wrong: clause
# namespacing, `clause_title` as a single-valued relation, and `maps_to_hls`
# across standards.
#
# Kept in scope (all Korean, so HLS clause titles stay comparable):
#   papers/ks-q-iso-9001-20241213-ko.md        ISO 9001 QMS
#   papers/ks-x-iso-iec-27001-20241030-ko.md   ISO/IEC 27001 ISMS
#   papers/ks-x-iso-iec-42001-20251030-ko.md   ISO/IEC 42001 AIMS
#   papers/ks-i-iso-14001-20210928-ko.md       ISO 14001 EMS
#
# Everything below is excluded from THIS PHASE ONLY, not judged irrelevant.
# Widen the scope by removing entries:  factlog ignore --remove <pattern>
# Already-merged facts of an ignored source are kept; ignoring only stops
# re-extraction.
#
# One pattern per line; '#' comments and '-' bullets allowed.

- notebooklm/2026-07-16-all-notes.md
- notebooklm/codegraph-github.md
- notebooklm/graphify-github.md
- notebooklm/llm-wiki-skill-github.md
- notebooklm/llm-wiki-zotero-notebooklm-youtube.md
- notebooklm/notebooklm-py-github.md
- notebooklm/understand-anything-github.md
- notebooklm/zotero-mcp-github.md
- papers/iso-iec-27001-2022-en.md
- papers/iso-iec-27701-2019-en.md
- papers/iso-iec-27701-2025-en.md
- papers/iso-iec-42001-2023-en.md
- papers/ks-a-iso-37001-20260420-ko.md
- papers/ks-c-iec-61508-1-20251118-ko.md
- papers/ks-i-iso-14002-1-20211027-ko.md
- papers/ks-m-iso-22716-20250703-ko.md
- papers/ks-p-iso-13485-20231228-ko.md
- papers/ks-q-iso-10006-20241213-ko.md
- papers/ks-q-iso-22000-20210804-ko.md
- papers/ks-q-iso-31000-20210804-ko.md
- papers/ks-q-iso-45001-20241004-ko.md
- papers/ks-q-iso-45002-20241231-ko.md
- papers/ks-q-iso-9000-20210330-ko.md
- papers/ks-q-iso-9004-20220630-ko.md
- papers/ks-q-iso-ts-9002-20231017-ko.md
- papers/ks-r-iso-26262-1-20240524-ko.md
- papers/ks-x-iso-27799-20230605-ko.md
- papers/ks-x-iso-iec-22989-20231214-ko.md
- papers/ks-x-iso-iec-25000-20230421-ko.md
- papers/ks-x-iso-iec-25010-20210819-ko.md
- papers/ks-x-iso-iec-27002-20251223-ko.md
- papers/ks-x-iso-iec-27017-20241030-ko.md
- papers/ks-x-iso-iec-27018-20241030-ko.md
- papers/ks-x-iso-iec-27032-20241030-ko.md
- papers/ks-x-iso-iec-27701-20220225-ko.md
- papers/ks-x-iso-iec-ieee-29119-1-20231208-ko.md
- papers/ks-x-iso-iec-ieee-29119-2-20231208-ko.md
- papers/ks-x-iso-iec-ieee-29119-3-20231208-ko.md
- papers/ks-x-iso-iec-ieee-29119-4-20231208-ko.md
- papers/ks-x-iso-iec-tr-24028-20231214-ko.md
- papers/ks-x-iso-iec-tr-24029-1-20231214-ko.md
- web/NomaDamasslides-grab Best harness + editor + linter for generating slides in Claude Code  Codex - Claude Design Open Source Alternative.md
- web/stablyaiorca Orca is the ADE for working with a fleet of parallel agents. Run any coding agent with your own subscription. Available on desktop and mobile..md
- youtube/📺 How To Build LLM Wiki In Obsidian 🧠 A Memory Layer For Any Agentic AI.md
- youtube/📺 LLM Wiki를 업그레이드하는 외부 지식 시스템! 연구자를 위한 최강의 조합 Zotero × Notebook × Obsidian x Claude Code.md
- youtube/📺 Orca Is the Free Cursor Killer Nobody's Talking About!.md
