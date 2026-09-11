# KB-01 — Initial Knowledge Base Build

신규 Knowledge Base를 실제 구축한다. 계획만 제시하지 말고 가능한 파일·구조·설정까지 만든다.

## 입력
`PROJECT_NAME`, `TOPIC`, `DOMAIN`, `TARGET_USERS`, `GITHUB_KB_REPOSITORY`(Public), `GITHUB_DEV_REPOSITORY`(Private, 공개 저장소명 + `-dev`), `PUBLIC_SITE`, `GCP_PROJECT`, `UPDATE_POLICY`.

## 실행 순서
1. Domain discovery: 핵심 개념·기술·정책·규정·표준·기관·기업·프로젝트·연구·데이터·timeline을 도출한다.
2. Source discovery: Tier 1 공식 원문부터 조사한다.
3. Repository architecture를 설계한다.
4. **저장소를 Obsidian Vault로 바로 열 수 있도록 Obsidian-compatible Markdown 구조를 만든다.**
5. Metadata schema와 evidence model을 정의한다.
6. Seed knowledge를 만든다: overview, glossary, 기관, 기술, 정책/규정, 표준, 프로젝트, timeline, source registry, 비교표.
7. 문서 간 `[[Wikilink]]`, aliases, backlink, 관계 메타데이터를 연결하고 Hub/MOC를 만든다.
8. `attachments/`, `templates/`, `.obsidian/` 팀 공용 설정 정책을 정의한다.
9. GCP Level 1 아키텍처를 만든다.
10. Quartz/MkDocs/Docusaurus 중 사이트 엔진을 선택한다. Obsidian 문법과 공개 사이트 호환성을 검증한다.
11. 검색·RAG는 retrieval-ready metadata와 link graph를 준비하되 MVP를 지연시키지 않는다.
12. schema/wikilink/orphan-note/attachment/build validation을 실행한다.

## Obsidian 문서 표준

- `.md` + YAML Front Matter
- `[[Wikilink]]` 기본
- `aliases`, `tags`, `related`, `source_ids` 지원
- Hub/MOC 제공
- 한 문서 한 주제 원칙
- 첨부는 `attachments/`에서 관리
- Dataview-compatible metadata 허용
- callout/embed는 선택적으로 사용
- 플러그인 전용 문법이 핵심 지식의 유일한 표현이 되어서는 안 됨
- GitHub에서도 핵심 내용이 읽혀야 함

## Evidence level
`Confirmed`, `Supported`, `Reported`, `Inferred`, `Unverified`.

## 완료조건
README, HOME, architecture, roadmap, taxonomy, schema, templates, source registry, seed documents, hubs/MOC, timeline, evidence gaps, attachments 정책, Obsidian conventions, public-site 기본 구성, GCP architecture가 존재해야 한다. 저장소를 Obsidian Vault로 열었을 때 wikilink와 탐색 구조가 작동하고, GitHub/정적 사이트의 빌드·링크 검증도 통과해야 한다.

## 필수 저장소·원문 정책

- 공개 `<name>`과 비공개 개발 `<name>-dev` 저장소 두 개를 반드시 운영한다. 개발 저장소명은 공개 저장소의 전체 이름에 `-dev`를 붙인다.
- 원문은 Source ID·공식 URL·버전·발행일·확인일·페이지/절로 추적한다. 수집 원문 파일과 추출 전문은 비공개 개발 저장소 `sources/`에 저장하고 Git으로 관리한다.
- 개발 저장소 `data/source-archive.yaml`에 Source ID·URL·보관 경로·수집 시각·SHA-256·버전을 기록한다. 미확보 원문은 사유와 후속 작업을 기록한다.
- 공개 지식·요약에는 출처를 연결하되 원문 제공은 공식 URL 링크로만 한다. 원문 파일·전문·embed·개발 저장소 경로는 공개 저장소·사이트·검색 인덱스에 포함하지 않는다.
- 연구·운영 기록은 개발 저장소에 두고 검증된 지식만 공개 저장소 PR로 반영한다. 사이트는 공개 저장소만 빌드하며 배포 산출물의 원문 미포함을 검사한다.
- 상세 규칙은 [원문 및 저장소 정책](../docs/source-policy.md)을 따른다.
