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

## 필수 저장소·원문 정책

- 공개 `<name>`과 비공개 개발 `<name>-dev` 저장소 두 개를 반드시 운영한다. 개발 저장소명은 공개 저장소의 전체 이름에 `-dev`를 붙인다.
- 원문은 Source ID·공식 URL·버전·발행일·확인일·페이지/절로 추적한다. 수집 원문 파일과 추출 전문은 비공개 개발 저장소 `sources/`에 저장하고 Git으로 관리한다.
- 개발 저장소 `data/source-archive.yaml`에 Source ID·URL·보관 경로·수집 시각·SHA-256·버전을 기록한다. 미확보 원문은 사유와 후속 작업을 기록한다.
- 공개 지식·요약에는 출처를 연결하되 원문 제공은 공식 URL 링크로만 한다. 원문 파일·전문·embed·개발 저장소 경로는 공개 저장소·사이트·검색 인덱스에 포함하지 않는다.
- 연구·운영 기록은 개발 저장소에 두고 검증된 지식만 공개 저장소 PR로 반영한다. 사이트는 공개 저장소만 빌드하며 배포 산출물의 원문 미포함을 검사한다.
- 상세 규칙은 [원문 및 저장소 정책](../docs/source-policy.md)을 따른다.
