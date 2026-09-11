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
