# Single-valued (functional) relations
#
# A relation listed here may hold at most ONE object per subject. When two
# accepted facts give the same subject two different values, `factlog check`
# reports a conflict. This is the corpus's contradiction detector, so a relation
# belongs here only when a second value is genuinely an error.
#
# One relation name per line; '#' comments and '-' bullets allowed.

# One clause number in one standard edition has exactly one title. A second
# title means a bad extraction, or a clause quoted from a different edition
# without namespacing it (see the identity rule in questions.md).
- clause_title

# Each clause occupies at most one HLS slot. Two slots means the HLS mapping
# was guessed rather than read.
- maps_to_hls

# An annex is normative or informative — never both. This one matters for
# certification scope: a wrong value silently changes what must be implemented.
- annex_status

# One edition is issued in one year.
- edition_year

# NOT single-valued, deliberately:
#   obligation        — one clause normally carries several requirements at
#                       different modal levels (a shall sentence and a should
#                       sentence in the same clause is correct, not a conflict).
#   has_clause        — a standard has many clauses.
#   requires_document — one clause can demand a policy and a record together.
