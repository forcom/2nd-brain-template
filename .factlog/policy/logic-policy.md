# Logic policy

Rules the deterministic engine reasons with. Each bullet is `- [id] <rule>`;
backtick-quoted names are relations declared in the other policy files.

These encode the two things this wiki is for: implementing several management
systems as one, and deriving an organization's deliverables from the clauses
that actually bind it.

## Rules

- [certification_mandatory] A clause is mandatory for certification when its `obligation` is shall, or when it belongs to an annex whose `annex_status` is normative. A clause whose only obligation is should, may, or can is not mandatory for certification.

- [hls_integration_point] Two clauses from different standards that `maps_to_hls` the same HLS slot are one integration point: a single implemented control can satisfy both. List them together rather than as separate obligations.

- [hls_strictest_wins] When clauses sharing an HLS slot carry different `obligation` levels, the integrated system must satisfy the strictest one — shall over should over may over can. Never downgrade an obligation because a sibling standard states it more weakly.

- [deliverable_scope] The deliverables an organization must produce are the `requires_document` values of every clause that is mandatory for certification under the standards in its scope. A document required by one standard in scope is required by the integrated system.

- [edition_currency] When one standard `supersedes` another, requirements are read from the superseding edition. Report a clause cited only from a superseded edition as needing review rather than treating it as current.
