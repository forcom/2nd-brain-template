---
title: ISO·IEC 소프트웨어 품질·테스팅 표준군
created: 2026-07-29
updated: 2026-07-29
type: concept
tags:
  - quality-management
  - software-engineering
  - standards
  - workflow
sources:
  - raw/papers/ks-x-iso-iec-25000-20230421-ko.md
  - raw/papers/ks-x-iso-iec-25010-20210819-ko.md
  - raw/papers/ks-x-iso-iec-ieee-29119-1-20231208-ko.md
  - raw/papers/ks-x-iso-iec-ieee-29119-2-20231208-ko.md
  - raw/papers/ks-x-iso-iec-ieee-29119-3-20231208-ko.md
  - raw/papers/ks-x-iso-iec-ieee-29119-4-20231208-ko.md
confidence: high
contested: false
contradictions: []
---

# ISO·IEC 소프트웨어 품질·테스팅 표준군

이 배치의 소프트웨어 표준은 “무엇을 품질로 볼 것인가”를 다루는 SQuaRE 계열과 “어떻게 시험을 조직하고 기록할 것인가”를 다루는 ISO/IEC/IEEE 29119 계열로 나뉜다.

## SQuaRE 품질 모델

- **KS X ISO/IEC 25000:2014:** 시스템·소프트웨어 품질 요구사항과 평가(SQuaRE) 시리즈의 구조, 공통 모델과 용어를 안내한다. ^[raw/papers/ks-x-iso-iec-25000-20230421-ko.md]
- **KS X ISO/IEC 25010:2011:** 시스템·소프트웨어 제품 품질과 사용 품질을 특성 모델로 구조화한다. 평가 대상과 품질 요구를 정의할 때 기준 어휘가 된다. ^[raw/papers/ks-x-iso-iec-25010-20210819-ko.md]

품질 모델은 측정·시험의 목적과 범위를 정하지만, 프로젝트별 합격기준과 시험 절차를 자동으로 제공하지는 않는다.

## 29119 테스팅 체계

| 문서 | 역할 |
| --- | --- |
| KS X ISO/IEC/IEEE 29119-1:2013 | 소프트웨어 테스팅의 개념과 정의를 제공한다. ^[raw/papers/ks-x-iso-iec-ieee-29119-1-20231208-ko.md] |
| KS X ISO/IEC/IEEE 29119-2:2013 | 조직·관리·동적 시험 프로세스를 포함한 테스트 프로세스를 다룬다. ^[raw/papers/ks-x-iso-iec-ieee-29119-2-20231208-ko.md] |
| KS X ISO/IEC/IEEE 29119-3:2013 | 테스트 계획, 상태, 완료와 결과를 포함한 테스트 문서 체계를 다룬다. ^[raw/papers/ks-x-iso-iec-ieee-29119-3-20231208-ko.md] |
| KS X ISO/IEC/IEEE 29119-4:2015 | 명세 기반, 구조 기반 등 테스트 설계기법의 적용을 다룬다. ^[raw/papers/ks-x-iso-iec-ieee-29119-4-20231208-ko.md] |

## 연결 방법

1. ISO/IEC 25010의 품질특성으로 요구와 위험을 구조화한다.
2. 29119-2로 시험 프로세스와 책임을 설계한다.
3. 29119-3으로 계획과 결과의 증거 형식을 정한다.
4. 29119-4의 설계기법을 위험, 품질특성과 시험수준에 맞게 선택한다.
5. 시험 결과를 품질 요구와 추적해 개선과 출시 판단으로 환류한다.

조직 수준의 품질경영은 [[iso-quality-management-standards]], 안전 관련 소프트웨어의 수명주기 관점은 [[iso-occupational-and-functional-safety-standards]]에서 이어진다. 전체 수집 범위는 [[iso-standards-portfolio-map]]을 참고한다.
