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

## 필수 저장소·원문 정책

- 공개 `<name>`과 비공개 개발 `<name>-dev` 저장소 두 개를 반드시 운영한다. 개발 저장소명은 공개 저장소의 전체 이름에 `-dev`를 붙인다.
- 원문은 Source ID·공식 URL·버전·발행일·확인일·페이지/절로 추적한다. 수집 원문 파일과 추출 전문은 비공개 개발 저장소 `sources/`에 저장하고 Git으로 관리한다.
- 개발 저장소 `data/source-archive.yaml`에 Source ID·URL·보관 경로·수집 시각·SHA-256·버전을 기록한다. 미확보 원문은 사유와 후속 작업을 기록한다.
- 공개 지식·요약에는 출처를 연결하되 원문 제공은 공식 URL 링크로만 한다. 원문 파일·전문·embed·개발 저장소 경로는 공개 저장소·사이트·검색 인덱스에 포함하지 않는다.
- 연구·운영 기록은 개발 저장소에 두고 검증된 지식만 공개 저장소 PR로 반영한다. 사이트는 공개 저장소만 빌드하며 배포 산출물의 원문 미포함을 검사한다.
- 상세 규칙은 [원문 및 저장소 정책](../docs/source-policy.md)을 따른다.
