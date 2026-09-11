# KB-07 — GitHub / GCP Deployment

GitHub 중심 Knowledge Base를 실제 운영 가능한 자동화·검색·RAG 플랫폼으로 배포한다.

## 목표
Canonical knowledge는 GitHub에 유지하고, GCP는 수집·처리·인덱싱·검색·RAG·모니터링 계층으로 사용한다.

## 단계
### Level 1 — Minimal
- GitHub repository + branch/PR workflow
- GitHub Actions
- static site deploy
- Cloud Storage
- Cloud Scheduler
- Cloud Run / Cloud Run Jobs
- Secret Manager

### Level 2 — Automated Research
- source watcher
- fetch/archive pipeline
- parser/normalizer
- structured change detection
- Pub/Sub
- BigQuery 또는 Firestore
- candidate markdown 생성
- GitHub PR 자동 생성

### Level 3 — AI Knowledge Platform
- Vertex AI embeddings
- Vector Search 또는 RAG Engine
- metadata-aware chunking
- hybrid retrieval
- reranking
- grounded generation
- citation rendering
- retrieval/generation evaluation

## CI quality gates
병합 전 다음을 검사한다.
1. YAML/frontmatter schema
2. required fields
3. duplicate IDs
4. broken internal links
5. orphan documents
6. invalid enum/status
7. site build
8. external source link health
9. stale `last_verified`
10. official source version change requiring review

## RAG metadata
각 chunk는 최소 다음을 유지한다.
`document_id`, `section`, `source_id`, `source_url`, `issuer`, `country`, `version`, `status`, `published`, `effective`, `last_verified`, `evidence_level`.

## 검색
MVP는 lexical/metadata 검색만으로도 유용해야 한다. 이후 semantic vector retrieval과 entity/link graph expansion을 추가한다.

## 평가
대표 질문 세트를 별도 관리하고 retrieval recall, source correctness, citation correctness, temporal correctness, groundedness를 측정한다.

## 보안
- credential/API key를 repo에 저장하지 않는다.
- GCP Secret Manager를 사용한다.
- public/private source 경계를 분리한다.
- 자동 에이전트는 기본적으로 main에 직접 쓰지 않고 PR을 생성한다.

## 완료조건
배포 아키텍처, CI, site build, source watcher 또는 그 최소 골격, secret handling, monitoring, rollback 절차, 검색/RAG evaluation 계획이 문서화되고 검증 가능해야 한다.

## 필수 저장소·원문 정책

- 공개 `<name>`과 비공개 개발 `<name>-dev` 저장소 두 개를 반드시 운영한다. 개발 저장소명은 공개 저장소의 전체 이름에 `-dev`를 붙인다.
- 원문은 Source ID·공식 URL·버전·발행일·확인일·페이지/절로 추적한다. 수집 원문 파일과 추출 전문은 비공개 개발 저장소 `sources/`에 저장하고 Git으로 관리한다.
- 개발 저장소 `data/source-archive.yaml`에 Source ID·URL·보관 경로·수집 시각·SHA-256·버전을 기록한다. 미확보 원문은 사유와 후속 작업을 기록한다.
- 공개 지식·요약에는 출처를 연결하되 원문 제공은 공식 URL 링크로만 한다. 원문 파일·전문·embed·개발 저장소 경로는 공개 저장소·사이트·검색 인덱스에 포함하지 않는다.
- 연구·운영 기록은 개발 저장소에 두고 검증된 지식만 공개 저장소 PR로 반영한다. 사이트는 공개 저장소만 빌드하며 배포 산출물의 원문 미포함을 검사한다.
- 상세 규칙은 [원문 및 저장소 정책](../docs/source-policy.md)을 따른다.
