# Logic policy

Rules the deterministic engine reasons with. Each bullet is `- [id] <rule>`;
backtick-quoted names are relations declared in the other policy files.

These encode the two things this wiki is for: implementing several management
systems as one, and deriving an organization's deliverables from the clauses
that actually bind it.

## Rules

- [certification_mandatory] A clause is mandatory for certification when its `obligation` is shall, or when its `annex_status` is normative. A clause whose only obligation is should, may, or can is not mandatory for certification.

- [normative_annex_item] Every individual item of a normative annex is itself in the certification scope, not just the annex as a whole. An annex item `belongs_to_annex` an annex whose `annex_status` is normative must be assessed one by one, and the main-body clause named by `made_binding_by` is what makes it binding.

- [hls_integration_point] Two clauses from different standards that `maps_to_hls` the same structure slot are one integration point: a single implemented control can satisfy both. List them together rather than as separate obligations.

- [cross_structure_integration_point] A slot of the Harmonized Structure and the Annex SL HLS slot it `slot_equivalent_to` are the same integration point even when their numbers differ. Clause 10 is the case that matters: HLS numbers 부적합 및 시정조치 as 10.1 and 지속적 개선 as 10.2, and HS reverses them, so never join clauses of an HLS standard and an HS standard by clause number alone.

- [structure_family_read_not_inferred] A standard's `structure_family` must come from its own body — the Annex SL / 상위 수준의 구조 wording for HLS, the 조화된 구조(harmonized structure) wording for HS. A standard whose body states neither is reported as needing review rather than assigned a family from its publication year.

- [hls_strictest_wins] When clauses sharing a structure slot carry different `obligation` levels, the integrated system must satisfy the strictest one — shall over should over may over can. Never downgrade an obligation because a sibling standard states it more weakly.

- [deliverable_scope] A clause that carries an `obligation` and whose body `requires_documented_information` is where a deliverable comes from. Collect these across every standard in scope: documentation demanded by one standard in scope is demanded of the integrated system.

- [edition_currency] When one standard `supersedes` another, requirements are read from the superseding edition. Report a clause cited only from a superseded edition as needing review rather than treating it as current.
