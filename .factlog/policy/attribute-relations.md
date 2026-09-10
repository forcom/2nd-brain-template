# Attribute (literal-valued) relations
#
# Relations whose OBJECT is a literal value, not a first-class entity. Keeping
# them here stops clause titles, modal verbs, and years from being counted as
# entities in path queries and entity counts.
#
# Objects of these relations stay valid, verifiable relation-query objects.

- clause_title
- obligation
- annex_status
- edition_year
- structure_family
- iso_edition_ordinal
- control_objective
# 구조 계열 값(HS/HLS)을 객체로 갖는다 — structure_family 와 같은 영역이다.
- introduced_in_structure
# 조항이 문서화된 정보를 요구하는지의 불리언. 2026-09-11 에 requires_document 를 대체했다 —
# 구 관계는 객체가 "유지되는 문서화된 정보" 같은 일반 버킷이라 사실상 불리언이었고,
# 실무에서 조항별 문서 이름을 쓰지 않으므로 이름을 뽑는 대신 불리언으로 정리했다.
- requires_documented_information
