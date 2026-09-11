# Knowledge Base Generator Architecture

## 1. 목표

이 프레임워크는 특정 도메인의 자료를 단순 수집하는 것이 아니라 다음 생명주기를 표준화한다.

```text
Source Discovery
  → Acquisition
  → Archival
  → Parsing
  → Normalization
  → Verification
  → Knowledge Modeling
  → Obsidian Authoring/Linking
  → Review
  → Publication
  → Search/RAG
  → Monitoring
  → Update/Supersession
```

## 2. Canonical layer

GitHub를 canonical knowledge layer로 사용한다.

Canonical artifacts:
- Obsidian-compatible Markdown knowledge documents
- YAML/JSON metadata
- source registry
- entity registry
- timeline/comparison datasets
- schemas/templates
- validation scripts
- change history

GCP의 DB/vector index는 모두 파생 계층이다. 삭제되어도 GitHub canonical data로 재생성할 수 있어야 한다.

## 3. Repository model

### Public KB
사람과 AI 모두가 읽는 공개 지식, schema, site, 공개 가능한 automation을 둔다. 저장소는 그대로 Obsidian Vault로 열 수 있어야 한다.

### Project management
roadmap, backlog, research log, evidence gaps, QA/deployment record를 둔다.

이 분리는 공개 지식과 운영 메모가 뒤섞이는 것을 막는다.

## 4. Obsidian authoring layer

Obsidian은 별도의 원본 저장소가 아니라 **GitHub canonical Markdown을 편집·연결·탐색하는 authoring interface**로 취급한다.

기본 요구사항:

- `.md` + YAML Front Matter
- `[[Wikilink]]`, aliases, section links
- backlink/graph 탐색
- Hub/MOC(Map of Content)
- `attachments/` 규칙
- Dataview-compatible metadata
- 선택적 callout/embed
- GitHub와 정적 사이트에서 핵심 내용이 계속 읽혀야 함

권장 역할 분담:

```text
Obsidian  → authoring / backlinks / graph / research navigation
GitHub    → canonical history / review / collaboration / CI
Quartz    → Obsidian-native public publishing
MkDocs    → structured technical documentation publishing
GCP       → collection / indexing / automation / RAG
```

`.obsidian/` 폴더는 팀 공용 설정만 선택적으로 버전 관리하고 개인 workspace/캐시 상태는 저장하지 않는다. 세부 규칙은 `obsidian-conventions.md`를 따른다.

## 5. Content model

문서의 최소 필드:

```yaml
id:
title:
type:
status:
evidence_level:
source_ids: []
published:
effective:
valid_from:
valid_to:
last_verified:
supersedes: []
superseded_by: []
tags: []
aliases: []
related: []
```

정책/표준 도메인은 `published`, `effective`, `valid_from`, `valid_to`를 분리한다.

## 6. Evidence model

- Confirmed: 공식 1차 원문 직접 확인
- Supported: 복수의 신뢰 가능한 근거
- Reported: 신뢰할 수 있는 2차 발표/보도
- Inferred: 확인된 사실에 기반한 분석
- Unverified: 확인 필요

고위험 주장에는 claim provenance를 선택적으로 적용한다.

```yaml
claim_id: CLAIM-0001
statement: "..."
source_id: SRC-0001
source_locator: "Section 4.2 / p.17"
evidence_level: Confirmed
verified_at: 2026-09-11
```

## 7. Source lifecycle

```text
candidate → registered → fetched → verified → monitored → revised/superseded/archived
```

각 source는 `Manual`, `Watch`, `Automated` 중 하나로 수집 방식을 지정한다.

## 8. GCP architecture

### Level 1

```text
Cloud Scheduler
  ↓
Cloud Run Job
  ↓
Fetch / Parse
  ↓
Cloud Storage archive
  ↓
GitHub branch / PR
```

### Level 2

```text
Scheduler/Event
  ↓
Pub/Sub
  ↓
Collector jobs
  ↓
Cloud Storage raw snapshot
  ↓
Parser/Normalizer
  ↓
BigQuery/Firestore metadata
  ↓
Diff engine
  ↓
Candidate Obsidian-compatible Markdown
  ↓
GitHub PR
```

### Level 3

```text
GitHub canonical content
  ↓
Index pipeline
  ↓
Chunk + metadata + link graph
  ↓
Embeddings
  ↓
Vector Search / RAG Engine
  ↓
Hybrid retrieval
  ↓
Reranking
  ↓
Vertex AI generation
  ↓
Answer + citations
```

## 9. Retrieval architecture

검색은 단계적으로 확장한다.

1. exact/keyword
2. metadata filtering
3. semantic vector retrieval
4. wikilink/entity graph expansion
5. reranking
6. grounded generation

초기 KB는 1~2단계만으로도 충분히 유용해야 한다.

## 10. CI/CD

PR마다 다음을 검증한다.

- schema
- duplicate IDs
- wikilinks/internal links
- orphan notes
- enum/status consistency
- source references
- Markdown/site build
- external link health
- stale verification warnings
- attachment paths
- Obsidian/GitHub compatibility

Merge 후 public site와 검색 인덱스를 갱신한다.

## 11. Evaluation

### Knowledge quality
- official-source coverage
- verified ratio
- unresolved evidence gaps
- stale verification count
- broken link rate
- orphan-note ratio

### Retrieval quality
- recall@k
- source hit rate
- citation correctness
- temporal correctness
- graph-assisted retrieval gain

### Generation quality
- groundedness
- answer-source consistency
- unsupported-claim rate

## 12. Security

- Secret Manager 사용
- service account 최소권한
- 공개/비공개 source 분리
- public repo에 credential 금지
- 자동 에이전트의 main 직접 변경 금지
- audit log 보존

## 13. 핵심 설계 판단

AI/RAG는 최종 목적이 아니라 **검증된 지식을 더 쉽게 찾는 인터페이스**다. Obsidian은 그 지식을 사람이 편집하고 연결하는 인터페이스다. 따라서 Obsidian, public site, retrieval index와 model은 교체 가능해야 하며 Markdown/YAML canonical layer는 장기 보존 가능해야 한다.
