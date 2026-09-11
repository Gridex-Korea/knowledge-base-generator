# KB-01 — Initial Knowledge Base Build

신규 Knowledge Base를 실제 구축한다. 계획만 제시하지 말고 가능한 파일·구조·설정까지 만든다.

## 입력
`PROJECT_NAME`, `TOPIC`, `DOMAIN`, `TARGET_USERS`, `PUBLIC_OR_PRIVATE`, `GITHUB_KB_REPOSITORY`, `GITHUB_PROJECT_REPOSITORY`, `PUBLIC_SITE`, `GCP_PROJECT`, `UPDATE_POLICY`.

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
