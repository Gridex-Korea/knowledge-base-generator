# KB-03 — Periodic Update and Verification

기존 Knowledge Base를 최신 상태로 유지하고 변경·폐기·개정·시행 전환을 추적한다.

## 입력
`KB_REPOSITORY`, `PROJECT_REPOSITORY`, `PUBLIC_SITE`, `UPDATE_WINDOW`, `WATCH_SCOPE`, `PRIORITY_SOURCES`.

## 실행
1. 최근 commit 이후 roadmap, backlog, research-log, evidence-gaps, source registry를 읽는다.
2. 등록된 공식 source를 확인하고 변경을 `NEW / UPDATED / REVISED / SUPERSEDED / WITHDRAWN / URL_CHANGED / EFFECTIVE / DRAFT_RELEASED / CONSULTATION / FINAL_RELEASED`로 분류한다.
3. title, version, publication/effective date, status, URL, 요구사항, 수치, 적용대상, 시행일정을 이전 상태와 비교한다.
4. 중요도를 `Critical / Major / Minor / Informational`로 평가한다.
5. 기존 지식 문서를 업데이트하되 필요 시 version history를 보존한다.
6. timeline과 `supersedes/superseded_by` 관계를 갱신한다.
7. evidence gap을 `OPEN / PARTIALLY_RESOLVED / RESOLVED / BLOCKED`로 재평가한다.
8. source health: dead URL, redirect, 삭제 PDF, 공식 URL 이동, archive 필요성을 검사한다.
9. public site의 navigation/search/rendering/link를 QA한다.
10. 실행 결과를 update report로 기록한다.

## 자동화 기본형
`Cloud Scheduler → Cloud Run Job → Source Watch → Change Detection → Candidate Markdown → GitHub Branch/PR → CI → Human Review → Merge`.

중요 변경을 자동으로 main에 직접 병합하지 않는다.
