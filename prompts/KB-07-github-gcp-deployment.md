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
