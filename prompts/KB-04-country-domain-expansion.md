# KB-04 — Country / Domain Expansion

기존 schema와 knowledge model을 유지하면서 새 국가 또는 새 분야를 확장한다.

## 입력
`KB_REPOSITORY`, `PROJECT_REPOSITORY`, `CURRENT_SCOPE`, `EXPANSION_TARGET`, `EXPANSION_TYPE`.

## 실행
1. 기존 taxonomy, schema, templates, source registry, comparison, country/topic hub를 먼저 읽는다.
2. 기존 구조와 확장 대상을 매핑하되 기능이 다른 기관·규정을 억지로 1:1 대응하지 않는다.
3. Government / Regulator / System Operator / Market Operator / Standards Body / Network Operator / Research / Industry Association의 공식 source map을 만든다.
4. 핵심 문서를 `법 → 시장규칙 → 계통규정 → 기술표준 → 시험규정 → 모델요건 → 정책 → 산업/연구` 우선순위로 조사한다.
5. 현지 용어를 보존하면서 canonical concept에 매핑한다.
6. 기존 공통 comparison schema로 비교하고 비교 불가능한 항목은 명시한다.
7. Country/Domain Hub, timeline, source registry, seed documents를 생성한다.
8. `Official Requirement / Industry Practice / Pilot / Proposal / Draft / Consultation / Final / Effective`를 구분한다.
9. G1~G8 식 단계별 expansion roadmap을 정의하고 완료조건을 기록한다.
10. 빌드·링크·schema 검증 후 roadmap에 반영한다.

## 원칙
다른 국가의 Pilot을 의무 규정처럼 비교하지 않으며, 현지 제도 구조와 적용 범위를 보존한다.
