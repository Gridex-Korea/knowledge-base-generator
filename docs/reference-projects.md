# Reference Projects and Design Lessons

이 문서는 Knowledge Base Generator 설계를 보강하기 위해 참고한 공개 프로젝트의 핵심 패턴을 정리합니다. 특정 저장소의 내용을 복제하지 않고, 재사용 가능한 운영·구조 원칙만 추출합니다.

## 1. International Data Spaces Association — Knowledge Base

Repository: `International-Data-Spaces-Association/knowledge-base`

관찰 포인트:
- MkDocs Material 기반 정적 문서 사이트
- GitHub Pages/Actions 중심 배포
- 여러 저장소의 콘텐츠를 빌드 시점에 조립
- 문서 품질을 CI gate로 관리
- 표준 문서와 기술 문서를 하나의 탐색 구조로 통합

Generator에 반영한 점:
- 배포 전 `strict build` 개념
- 링크·Markdown·메타데이터·schema 검증을 병합 게이트로 사용
- 여러 source repository를 하나의 public KB로 조립할 수 있는 확장 모델
- public content와 project management를 분리하되 navigation 관점에서는 일관된 정보구조 유지

## 2. Quartz

Repository: `jackyzha0/quartz`

관찰 포인트:
- Markdown-first digital garden
- Obsidian 친화적인 wikilink
- backlinks와 graph navigation
- 단일 저장소 콘텐츠를 정적 사이트로 변환

Generator에 반영한 점:
- atomic document + wikilink
- orphan 문서 탐지
- backlink/graph를 부가 탐색 계층으로 활용
- authoring format과 publishing format을 분리하지 않는 Markdown-first 정책

## 3. Foam

Repository: `foambubble/foam`

관찰 포인트:
- GitHub 기반 개인/팀 지식관리
- wikilink와 graph 중심 연결
- Markdown 파일 자체가 장기 보존 가능한 지식 원본

Generator에 반영한 점:
- GitHub를 canonical knowledge store로 사용
- 링크가 없는 문서를 품질 문제로 취급
- ID/metadata와 링크 그래프를 함께 관리

## 4. Docusaurus

Repository: `facebook/docusaurus`

관찰 포인트:
- documentation portal 중심 구조
- 문서 버전 관리
- localization 지원
- 제품/개발 문서 규모가 커져도 확장하기 쉬운 정보구조

Generator에 반영한 점:
- 규정/표준처럼 version이 중요한 도메인은 문서 현재본만 덮어쓰지 않고 history를 보존
- 한국어를 primary로 하되 source language와 영어 표준용어를 별도 메타데이터로 유지
- 국제 확장 시 locale과 canonical concept를 분리

## 5. Google Cloud Generative AI / Vertex AI sample ecosystem

관찰 포인트:
- managed embeddings/vector search
- RAG Engine과 retrieval 구성
- chunk metadata 보존
- 평가 데이터셋과 검색 품질 평가
- 검색과 생성 단계를 분리

Generator에 반영한 점:
- RAG는 GitHub canonical knowledge의 파생 인덱스로 취급
- chunk마다 `document_id`, `section`, `source_url`, `version`, `last_verified` 보존
- retrieval evaluation을 별도 품질 축으로 운영
- LLM 답변 품질보다 retrieval evidence quality를 먼저 측정

## 6. 보강된 공통 설계 원칙

### 6.1 CI-gated knowledge
Knowledge Base의 콘텐츠 변경도 코드처럼 검증합니다.

최소 gate:
1. YAML/schema validation
2. duplicate ID detection
3. broken internal link detection
4. orphan document detection
5. invalid status/evidence detection
6. Markdown/site build
7. source URL validation
8. stale verification warning

### 6.2 Provenance ledger
중요한 claim은 필요 시 다음 정보를 연결합니다.

```yaml
claim_id: CLAIM-0001
statement: "..."
source_id: SRC-0001
source_locator: "section/page/paragraph"
evidence_level: Confirmed
verified_at: 2026-09-11
verified_by: human-or-agent-id
```

모든 문장을 claim 단위로 관리할 필요는 없지만, 규제·표준·수치·시행일처럼 오류 비용이 큰 항목은 claim provenance를 사용할 수 있습니다.

### 6.3 Temporal knowledge
정책과 표준은 '무엇이 맞는가'뿐 아니라 '언제 맞았는가'가 중요합니다.

권장 필드:
- `published`
- `effective`
- `valid_from`
- `valid_to`
- `supersedes`
- `superseded_by`
- `status`

### 6.4 Content lifecycle

```text
candidate
  ↓
researched
  ↓
verified
  ↓
published
  ↓
monitored
  ↓
updated / superseded / archived
```

문서의 `draft/final` 상태와 지식 자체의 `verification status`를 혼동하지 않습니다.

### 6.5 Retrieval layers

```text
Layer 1: exact / keyword / metadata
Layer 2: semantic vector retrieval
Layer 3: link/entity graph expansion
Layer 4: reranking
Layer 5: grounded generation
```

초기 MVP는 Layer 1만으로도 충분해야 하며, 벡터 검색이 없어도 KB 자체의 탐색성이 무너지지 않아야 합니다.

### 6.6 Evaluation set

```yaml
- id: QA-001
  question: "현재 적용 중인 규정은 무엇인가?"
  expected_sources:
    - REG-001
  answer_type: factual
  freshness_sensitive: true
```

이 세트는 retrieval recall, citation correctness, temporal correctness 평가에 사용합니다.

## 7. 프로젝트별 적용 원칙

- 작은 KB: Quartz + GitHub Pages + 최소 CI
- 규정/표준 중심 KB: MkDocs Material + strict schema + version history
- 제품/개발 문서형 KB: Docusaurus 검토
- 그래프 탐색이 중요한 연구 KB: Quartz/Foam 스타일 link graph 강화
- 대규모 자동화/RAG: GCP Level 2~3 추가

사이트 엔진은 정체성이 아니라 구현 선택입니다. Markdown과 metadata가 canonical하기 때문에 향후 Quartz ↔ MkDocs ↔ Docusaurus 전환이 가능해야 합니다.
