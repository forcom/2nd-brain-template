# Research questions
#
# These questions steer what `/factlog sync` extracts from raw/. The corpus is
# ISO/IEC and KS management-system and AI standards. The wiki's goal is to
# implement several management systems as one integrated system, and to generate
# deliverables (정책서 · 절차서 · 지침서 · 매뉴얼) for a given organization.
#
# IDENTITY RULE — always namespace a clause by its standard and edition:
#   "ISO/IEC 27001:2022 4.1", "ISO/IEC 42001:2023 A.6.2.2"
# A bare "4.1" collides across every standard in the corpus and makes the
# single-valued conflict check fire on nothing but its own ambiguity.
#
# Format: one `- [qN] <question>` per line.

- [q1] For each standard, which numbered clauses and annex items exist, and what is the exact title of each? Record as `has_clause` (standard → namespaced clause) and `clause_title`.
- [q2] Which High Level Structure (HLS/HS) slot does each clause of a management-system standard occupy? Record as `maps_to_hls`, e.g. `ISO/IEC 42001:2023 4.1` → `HS 4.1` and `ISO 9001:2015 4.1` → `HLS 4.1`. Slot ids carry the number only — the title belongs in `clause_title` on the slot, so a wrong title cannot corrupt the entity. This is what lets several standards be implemented as one system.
- [q3] For each requirement, which modal verb governs it — shall / should / may / can (and whichever Korean rendering that standard uses)? Record as `obligation`. Never collapse shall and should into one level.
- [q4] Is each annex normative (mandatory for certification) or informative/optional? Record as `annex_status`. State which clause of the main body makes a normative annex binding.
- [q5] Does the clause's own body require documented information at all? Record as `requires_documented_information` with the literal `true`, quoting the sentence that demands it. Do not record document names (정책서, 절차서, …) — the clause-level name is not what practitioners use, so the boolean is the whole fact.
- [q6] Which standard edition supersedes which, and in what year was each edition issued? Record as `supersedes` and `edition_year`.
- [q7] Between two standards built on different structure families (HLS 2020 vs HS 2026), which clauses have no counterpart at all — i.e. sit on a structure slot with no `slot_equivalent_to` partner? This is the non-overlap between two certification scopes at the main-body level; Annex A controls are a separate, unmapped question.
