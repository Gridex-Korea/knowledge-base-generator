# KB-00 — Knowledge Base Project Generator

사용자가 한 문장으로 주제를 제시하면 실제 운영 가능한 Knowledge Base 프로젝트로 변환한다.

## 역할

Knowledge Architect + Research Lead + GitHub/GCP Architect + Technical PM 역할을 수행한다.

## 입력

- 주제: `[TOPIC]`
- 기존 저장소/사이트/국가 범위가 있으면 활용
- 정보가 부족해도 질문만 반복하지 말고 합리적 기본값으로 초안을 만든다.

## 기본값

- GitHub = canonical source of truth
- Public KB `<name>` + 비공개 개발 저장소 `<name>-dev` 두 개 필수
- 한국어 primary, 영어 공식 원문 병행
- Official source 우선
- **Obsidian-compatible Markdown** + YAML/JSON 중심
- 저장소를 그대로 Obsidian Vault로 열 수 있게 설계
- YAML Front Matter + `[[Wikilink]]` + Hub/MOC + backlink/graph 구조
- Quartz 또는 MkDocs Material
- GitHub Pages 우선
- GCP Level 1부터 시작
- RAG는 source/evidence 구조 이후

## 실행

1. 프로젝트 유형을 판별한다: Technology / Policy-Regulation / Industry-Market / Research / Procurement-BI / Mixed.
2. `PRIMARY_DOMAIN`, `SECONDARY_DOMAINS`, `COUNTRY_SCOPE`, `LANGUAGE_SCOPE`, `TARGET_USERS`, `CORE_QUESTIONS`를 정의한다.
3. 사람이 읽는 프로젝트명과 GitHub slug를 제안한다.
4. Public `<name>`과 Private `<name>-dev` 두 저장소를 만들고 역할을 분리한다.
5. 핵심 Entity, Taxonomy, Metadata schema 초안을 만든다.
6. **Obsidian Vault 구조, Hub/MOC, wikilink, aliases, attachments, `.obsidian/` 관리 정책을 설계한다.**
7. Source-of-Truth 기관 지도와 Source Priority Matrix를 만든다.
8. 초기 핵심 문서 10~30개와 Hub/Timeline/Comparison 후보를 선정한다.
9. 사이트 엔진을 Quartz / MkDocs Material / Docusaurus 중 선택하고 이유를 기록한다. Obsidian wikilink 호환을 고려한다.
10. GCP Level 1/2/3 중 초기 수준을 결정한다.
11. MVP 완료조건과 KPI를 정의한다.
12. 초기 roadmap을 P0~P6으로 생성한다.
13. 상태에 따라 KB-01/02/03/04 중 다음 프롬프트를 선택하고 가능한 경우 즉시 이어서 실행한다.

## 프로젝트 유형별 기본 구조

### Technology
Technology / Architecture / Control / Equipment / Standards / Testing / Projects / Companies / Research

### Policy-Regulation
Law / Policy / Regulation / Market Rules / Institutions / Timeline / Consultation / Implementation

### Industry-Market
Industry Structure / Companies / Supply Chain / Projects / Market / Policy / Statistics

### Research
Topics / Papers / Authors / Institutions / Methods / Datasets / Experiments / Trends

### Procurement-BI
Notices / Buyers / Products / Suppliers / Specifications / Certifications / Projects / Bids

## Obsidian 기본 구조

최소 다음을 포함한다.

```text
README.md
HOME.md
content/
hubs/
attachments/
templates/
data/
schemas/
.obsidian/   # 팀 공용 설정만 선택적으로 관리
```

문서 간 연결은 `[[Wikilink]]`를 기본으로 하고, GitHub/정적 사이트에서도 핵심 문서가 읽히도록 표준 Markdown 호환성을 유지한다.

## GCP 단계

- Level 1: GitHub Actions + Cloud Storage + Cloud Scheduler + Cloud Run
- Level 2: + Pub/Sub + BigQuery/Firestore + Secret Manager + structured change detection
- Level 3: + Vertex AI + embeddings + Vector Search/RAG Engine + evaluation

## 최소 생성 파일

`README.md`, `HOME.md`, `architecture.md`, `roadmap.md`, `backlog.md`, `evidence-gaps.md`, `taxonomy.yaml`, `document.schema.yaml`, `source-registry.yaml`, `document-template.md`, `topic-hub.md`, `obsidian-conventions.md`

## 최종 출력

Project Blueprint에 Name, Slug, Type, Scope, Target Users, Repositories, Website, Obsidian Vault Model, Knowledge Model, Source Strategy, Initial Content, GCP Architecture, Roadmap, MVP, Evidence Risks, Next Action을 포함한다.

## 핵심 원칙

`Source → Evidence → Structure → Knowledge → Connection → Search → Automation → AI` 순서를 유지한다. AI 기능보다 출처와 증거 구조를 먼저 완성하고, 지식 문서는 사람이 Obsidian에서 연결·탐색할 수 있는 형태로 유지한다.

## 필수 저장소·원문 정책

- 공개 `<name>`과 비공개 개발 `<name>-dev` 저장소 두 개를 반드시 운영한다. 개발 저장소명은 공개 저장소의 전체 이름에 `-dev`를 붙인다.
- 원문은 Source ID·공식 URL·버전·발행일·확인일·페이지/절로 추적한다. 수집 원문 파일과 추출 전문은 비공개 개발 저장소 `sources/`에 저장하고 Git으로 관리한다.
- 개발 저장소 `data/source-archive.yaml`에 Source ID·URL·보관 경로·수집 시각·SHA-256·버전을 기록한다. 미확보 원문은 사유와 후속 작업을 기록한다.
- 공개 지식·요약에는 출처를 연결하되 원문 제공은 공식 URL 링크로만 한다. 원문 파일·전문·embed·개발 저장소 경로는 공개 저장소·사이트·검색 인덱스에 포함하지 않는다.
- 연구·운영 기록은 개발 저장소에 두고 검증된 지식만 공개 저장소 PR로 반영한다. 사이트는 공개 저장소만 빌드하며 배포 산출물의 원문 미포함을 검사한다.
- 상세 규칙은 [원문 및 저장소 정책](../docs/source-policy.md)을 따른다.
