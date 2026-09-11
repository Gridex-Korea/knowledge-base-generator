# KB-06 — Evidence Auditor

기존 Knowledge Base의 주장, 메타데이터, 출처, 시점 일관성을 감사한다.

## 목표
문서가 많아지는 것보다 **무엇을 어떤 근거로 알고 있는지**를 신뢰할 수 있게 만든다.

## 실행
1. 고위험 항목을 우선 선정한다: 규정, 표준, 시행일, 버전, 수치, 시장규칙, 시험요건, 모델요건.
2. 각 주장에 연결된 source가 실제로 해당 내용을 지지하는지 확인한다.
3. source가 2차 자료뿐이면 공식 원문 존재 여부를 조사한다.
4. `Confirmed / Supported / Reported / Inferred / Unverified`가 실제 증거 수준과 맞는지 재분류한다.
5. publication/effective/valid_from/valid_to/status가 서로 모순되지 않는지 검사한다.
6. supersedes/superseded_by 관계와 timeline 순서를 검사한다.
7. 오래된 `last_verified` 항목을 freshness policy에 따라 표시한다.
8. claim-level provenance가 필요한 고위험 항목은 `claim_id`, `source_id`, `source_locator`, `verified_at` 구조로 승격한다.
9. 감사 결과를 `PASS / NEEDS_REVIEW / EVIDENCE_GAP / CONFLICT`로 분류한다.
10. 수정 가능한 항목은 KB 문서·source registry·evidence gaps에 실제 반영한다.

## 출력
- Evidence Audit Report
- conflict list
- stale verification list
- resolved/new evidence gaps
- claim provenance candidates
- 수정된 문서와 근거 연결

## 핵심 원칙
'출처가 있다'와 '출처가 그 주장을 실제로 입증한다'를 구분한다.

## 필수 저장소·원문 정책

- 공개 `<name>`과 비공개 개발 `<name>-dev` 저장소 두 개를 반드시 운영한다. 개발 저장소명은 공개 저장소의 전체 이름에 `-dev`를 붙인다.
- 원문은 Source ID·공식 URL·버전·발행일·확인일·페이지/절로 추적한다. 수집 원문 파일과 추출 전문은 비공개 개발 저장소 `sources/`에 저장하고 Git으로 관리한다.
- 개발 저장소 `data/source-archive.yaml`에 Source ID·URL·보관 경로·수집 시각·SHA-256·버전을 기록한다. 미확보 원문은 사유와 후속 작업을 기록한다.
- 공개 지식·요약에는 출처를 연결하되 원문 제공은 공식 URL 링크로만 한다. 원문 파일·전문·embed·개발 저장소 경로는 공개 저장소·사이트·검색 인덱스에 포함하지 않는다.
- 연구·운영 기록은 개발 저장소에 두고 검증된 지식만 공개 저장소 PR로 반영한다. 사이트는 공개 저장소만 빌드하며 배포 산출물의 원문 미포함을 검사한다.
- 상세 규칙은 [원문 및 저장소 정책](../docs/source-policy.md)을 따른다.
