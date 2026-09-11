# KB-02 — Existing Knowledge Base Expansion

기존 KB를 파괴하지 않고 새로운 자료·기능·문서군을 확장한다.

## 입력
`KB_REPOSITORY`, `PROJECT_REPOSITORY`, `PUBLIC_SITE`, `TARGET_TOPIC`, `KNOWN_CURRENT_COMMIT`, `REQUESTED_SCOPE`.

## 실행
1. README, roadmap, backlog, architecture, taxonomy, schema, templates, source registry, 관련 문서를 먼저 읽는다.
2. repository 역할과 현재 taxonomy/metadata/link 구조를 파악한다.
3. 동일·유사 문서 중복을 검사한다.
4. `Missing Knowledge / Source / Metadata / Evidence / Cross-link / Timeline / Comparison / Automation / UI`로 gap을 분류한다.
5. 필요한 공식 원문을 추가 조사하고 version, status, publication/effective date, 후속 개정을 검증한다.
6. 기존 문서를 우선 수정하고 필요할 때만 신규 문서를 만든다.
7. Topic↔Regulation↔Organization↔Country↔Standard↔Project 관계를 연결한다.
8. 비교표·timeline·source registry를 함께 업데이트한다.
9. unresolved 항목은 `evidence-gaps.md`에 남긴다.
10. roadmap/backlog/research-log/changelog를 갱신한다.
11. schema, broken link, duplicate, site build를 검증한다.

## 완료조건
분석 보고서만 남기지 말고 검토 가능한 Markdown/데이터/코드 변경과 검증 결과를 만든다.

## 필수 저장소·원문 정책

- 공개 `<name>`과 비공개 개발 `<name>-dev` 저장소 두 개를 반드시 운영한다. 개발 저장소명은 공개 저장소의 전체 이름에 `-dev`를 붙인다.
- 원문은 Source ID·공식 URL·버전·발행일·확인일·페이지/절로 추적한다. 수집 원문 파일과 추출 전문은 비공개 개발 저장소 `sources/`에 저장하고 Git으로 관리한다.
- 개발 저장소 `data/source-archive.yaml`에 Source ID·URL·보관 경로·수집 시각·SHA-256·버전을 기록한다. 미확보 원문은 사유와 후속 작업을 기록한다.
- 공개 지식·요약에는 출처를 연결하되 원문 제공은 공식 URL 링크로만 한다. 원문 파일·전문·embed·개발 저장소 경로는 공개 저장소·사이트·검색 인덱스에 포함하지 않는다.
- 연구·운영 기록은 개발 저장소에 두고 검증된 지식만 공개 저장소 PR로 반영한다. 사이트는 공개 저장소만 빌드하며 배포 산출물의 원문 미포함을 검사한다.
- 상세 규칙은 [원문 및 저장소 정책](../docs/source-policy.md)을 따른다.
