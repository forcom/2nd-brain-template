# Typed (comparable-literal) relations
#
# Declare relations whose literal object should be COMPARED, not just matched —
# so the deterministic engine can order them, threshold them, or range over them
# (e.g. "launched after 2030", "rank <= 3"). A relation listed here should ALSO
# be declared in attribute-relations.md (its object is a literal, not an entity).
#
# One declaration per line:
#   - `relation name` : <type> as <ascii_alias>
# where <type> is one of: date | number | ordinal | amount, and <ascii_alias>
# names the engine side-relation that holds the comparable value. The alias must
# be an ASCII identifier ([A-Za-z_][A-Za-z0-9_]*); it is author-chosen so it
# stays a legal engine name even when the relation name is non-ASCII. Quote a
# relation name containing spaces in `backticks`.
#
# Type meanings:
#   date     2030.1 / 2030-01-15  -> sortable yyyymmdd
#   number   1,000 / 3.5          -> fixed-point int64, scaled ×1000 (3 decimals,
#                                    positive only); thresholds in scaled units
#                                    (e.g. `V >= 2.0` -> `V >= 2000`)
#   ordinal  rank 3 / 3rd         -> int rank
#   amount   100억 / 1,000원       -> integer base unit (needs a unit table)
#
# An `amount` line MAY carry an inline unit table; values must be positive ints:
#   - `relation name` : amount as <ascii_alias> (억=1e8, 만=1e4, 원=1)
# Omit the clause to use the built-in default unit table.
#
# The corpus holds several editions of the same standard (ISO/IEC 27701:2019 and
# 2025, for example), so edition year must be comparable — "which edition is
# current" and "what changed after 2022" are range queries, not string matches.
- `edition_year` : date as edition_year_value

# 같은 표준의 판 순서(제2판 → 제5판)는 문자열이 아니라 순위 비교 대상이다.
- `iso_edition_ordinal` : ordinal as iso_edition_ordinal_value
