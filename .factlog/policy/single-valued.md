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

# A standard applies exactly one harmonized clause structure. ISO moved from the
# Annex SL HLS (2012-2020) to the Harmonized Structure (2021-), and the two number
# clause 10 in opposite order, so a standard claiming both means the structure was
# inferred from the year instead of read from the body.
- structure_family

# One KS standard is based on exactly one ISO standard edition.
- based_on

# One ISO edition has one ordinal (제N판).
- iso_edition_ordinal

# NOT single-valued, deliberately:
#   obligation        — one clause normally carries several requirements at
#                       different modal levels (a shall sentence and a should
#                       sentence in the same clause is correct, not a conflict).
#   has_clause        — a standard has many clauses.
#   requires_documented_information — boolean; listed here only to say it is not
#                       single-valued-sensitive. One row per clause is the norm.
