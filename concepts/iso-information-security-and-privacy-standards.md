---
title: ISO·IEC 정보보호·개인정보 표준군
created: 2026-07-29
updated: 2026-07-29
type: concept
tags:
  - healthcare
  - information-security
  - management-system
  - privacy
  - standards
sources:
  - raw/papers/iso-iec-27001-2022-en.md
  - raw/papers/ks-x-iso-iec-27001-20241030-ko.md
  - raw/papers/ks-x-iso-iec-27002-20251223-ko.md
  - raw/papers/ks-x-iso-iec-27017-20241030-ko.md
  - raw/papers/ks-x-iso-iec-27018-20241030-ko.md
  - raw/papers/ks-x-iso-iec-27032-20241030-ko.md
  - raw/papers/iso-iec-27701-2019-en.md
  - raw/papers/iso-iec-27701-2025-en.md
  - raw/papers/ks-x-iso-iec-27701-20220225-ko.md
  - raw/papers/ks-x-iso-27799-20230605-ko.md
confidence: high
contested: false
contradictions: []
---

# ISO·IEC 정보보호·개인정보 표준군

이 표준군은 조직의 정보보호 경영시스템을 중심에 두고, 통제 지침, 클라우드, 개인정보, 사이버보안과 보건의료 맥락을 층별로 확장한다. 문서 번호가 가깝더라도 요구사항과 지침, 일반 표준과 분야별 적용문서를 구분해야 한다.

## 구조

| 문서 | 이 배치에서의 역할 |
| --- | --- |
| ISO/IEC 27001 | 정보보호경영시스템(ISMS)의 요구사항을 규정한다. 위험 평가·처리와 경영시스템 운영이 중심이다. ^[raw/papers/iso-iec-27001-2022-en.md] |
| KS X ISO/IEC 27002:2022 | 정보보호 통제와 구현 속성을 포함한 지침을 제공한다. 27001의 요구사항 문서와 역할이 다르다. ^[raw/papers/ks-x-iso-iec-27002-20251223-ko.md] |
| KS X ISO/IEC 27017:2015 | ISO/IEC 27002를 기초로 클라우드 서비스 제공자와 고객의 정보보호 통제 지침을 확장한다. ^[raw/papers/ks-x-iso-iec-27017-20241030-ko.md] |
| KS X ISO/IEC 27018:2014 | 공공 클라우드에서 개인정보 처리자 역할을 하는 사업자의 PII 보호 실무지침을 제공한다. ^[raw/papers/ks-x-iso-iec-27018-20241030-ko.md] |
| KS X ISO/IEC 27032:2014 | 사이버보안의 이해관계자, 자산, 위협과 협업에 관한 지침을 제공한다. ^[raw/papers/ks-x-iso-iec-27032-20241030-ko.md] |
| ISO/IEC 27701 | 개인정보보호 정보 경영시스템(PIMS)을 다룬다. 이 배치에는 구조가 다른 2019판과 2025판이 함께 있다. |
| KS X ISO 27799:2016 | ISO/IEC 27002의 통제를 보건의료 정보보호 맥락에 적용하는 지침이다. ^[raw/papers/ks-x-iso-27799-20230605-ko.md] |

## 판본 경계

### ISO/IEC 27001

영문 원본은 ISO/IEC 27001:2022 제3판이지만, 수집된 KS X ISO/IEC 27001은 2014판이다. 번호가 같아도 부속서 통제 구조와 조항 대응을 같은 판으로 간주하면 안 된다. 구현·심사 매핑에서는 각 문서의 판 연도를 함께 기록해야 한다. ^[raw/papers/iso-iec-27001-2022-en.md] ^[raw/papers/ks-x-iso-iec-27001-20241030-ko.md]

### ISO/IEC 27701

ISO/IEC 27701:2019는 ISO/IEC 27001과 ISO/IEC 27002를 개인정보보호 정보 관리로 확장하는 요구사항·지침 문서다. 수집된 KS X ISO/IEC 27701:2019도 이 판을 채택한다. ^[raw/papers/iso-iec-27701-2019-en.md] ^[raw/papers/ks-x-iso-iec-27701-20220225-ko.md]

ISO/IEC 27701:2025 제2판은 문서 자체의 개정 설명에 따라 독립형 개인정보보호 정보 경영시스템 표준으로 재작성되었다. 따라서 2019판의 확장 구조를 그대로 전제하지 말고 2025판의 본문, 부속서 매핑과 전환 관계를 별도로 검토해야 한다. ^[raw/papers/iso-iec-27701-2025-en.md]

## 적용 흐름

1. 보호할 정보, 사업 맥락, 법적·계약상 요구와 ISMS 범위를 정한다.
2. ISO/IEC 27001에 따라 위험 평가·처리와 경영시스템 프로세스를 운영한다.
3. ISO/IEC 27002에서 위험 처리에 적합한 통제와 구현 지침을 선택한다.
4. 클라우드에는 27017, 공공 클라우드 PII 처리에는 27018을 맥락별로 추가한다.
5. 개인정보 경영에는 적용 판을 명시한 27701 구조를 연결한다.
6. 보건의료 정보에는 27799의 분야별 지침을 적용한다.
7. 내부심사, 측정, 사건과 변경 결과를 경영검토와 개선으로 환류한다.

개인정보 법규 준수는 표준 채택만으로 자동 달성되는 것이 아니므로 관할 법령과 계약 요구를 별도로 매핑해야 한다. 이 페이지는 수집된 표준 문서의 관계를 설명하며 법적 판단을 대신하지 않는다.

공통 경영 구조는 [[iso-management-system-standards]], 일반 리스크 프레임은 [[iso-risk-and-compliance-standards]], 의료제품 품질과의 경계는 [[iso-health-product-and-food-standards]], 전체 판본 일람은 [[iso-standards-portfolio-map]]을 참고한다.
