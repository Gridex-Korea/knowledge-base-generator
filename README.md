# Knowledge Base Generator

**Build verified, Obsidian-compatible knowledge bases with GitHub, Google Cloud, and AI.**

Knowledge Base Generator는 특정 분야의 자료를 단순히 모으는 도구가 아니라, **공식 원문 → 검증 → 구조화 → Obsidian 지식화 → GitHub 버전관리 → 공개 사이트 → 자동 업데이트 → 검색/RAG**까지 이어지는 범용 Knowledge Base 생성 프레임워크입니다.

전력정책, GFM, HVDC, 해상풍력, 수소, 배터리, AI, 공공조달 등 주제만 바꿔 동일한 구조를 재사용하는 것을 목표로 합니다.

## Design principles

1. **GitHub is canonical** — Markdown/YAML/JSON과 변경 이력의 최종 원본은 GitHub에 둡니다.
2. **Obsidian-compatible by default** — 저장소 또는 Starter Vault를 Obsidian에서 바로 열 수 있게 설계합니다.
3. **Evidence before AI** — RAG보다 출처, 버전, 시행상태, 증거 수준을 먼저 설계합니다.
4. **Human review gate** — 자동 수집 결과는 branch/PR 검토 후 병합합니다.
5. **Living Knowledge Base** — Build → Expand → Verify → Expand → Verify 사이클로 운영합니다.
6. **Atomic + linked notes** — 한 문서 한 주제를 기본으로 하고 `[[Wikilink]]`, backlinks, Hub/MOC로 연결합니다.
7. **Quality gates** — schema, frontmatter, wikilink, 중복 ID, build 오류를 CI에서 검사합니다.
8. **Hybrid retrieval ready** — keyword + metadata + semantic + graph + reranking 구조로 확장할 수 있게 합니다.
9. **Provenance preserved** — 핵심 주장은 source/version/locator/verified date까지 역추적할 수 있게 합니다.

## Prompt Orchestrator

| ID | 목적 | 사용 시점 |
|---|---|---|
| [KB-00](prompts/KB-00-project-generator.md) | Project Generator | 한 문장으로 새 지식창고를 시작할 때 |
| [KB-01](prompts/KB-01-initial-build.md) | Initial Build | 신규 KB를 실제 구축할 때 |
| [KB-02](prompts/KB-02-expand.md) | Expansion | 기존 KB에 자료·기능을 확장할 때 |
| [KB-03](prompts/KB-03-update-and-verify.md) | Update & Verify | 정기 최신화·검증할 때 |
| [KB-04](prompts/KB-04-country-domain-expansion.md) | Country/Domain Expansion | 국가·분야를 확장할 때 |
| [KB-05](prompts/KB-05-source-hunter.md) | Source Hunter | 공식 원문과 Source Map을 찾을 때 |
| [KB-06](prompts/KB-06-evidence-auditor.md) | Evidence Auditor | 주장-근거 연결과 Evidence Gap을 감사할 때 |
| [KB-07](prompts/KB-07-github-gcp-deployment.md) | GitHub/GCP Deployment | 자동화·검색·RAG를 배포할 때 |

## Architecture

```text
Official web / PDF / papers / APIs / datasets
                      ↓
            DISCOVER / FETCH / ARCHIVE
                      ↓
            PARSE / NORMALIZE / VERIFY
                      ↓
        Obsidian-compatible Markdown/YAML
                      ↓
                    GitHub
                Canonical Layer
                      ↓
        ┌─────────────┼──────────────┐
        ↓             ↓              ↓
     Obsidian      Public Site       GCP
 author/connect   Quartz/MkDocs   automation/RAG
        ↓             ↓              ↓
        └─────────────┴──────────────┘
                      ↓
            Grounded Search & Answers
```

## Repository layout

```text
knowledge-base-generator/
├─ README.md
├─ prompts/
│  ├─ KB-00-project-generator.md
│  ├─ KB-01-initial-build.md
│  ├─ KB-02-expand.md
│  ├─ KB-03-update-and-verify.md
│  ├─ KB-04-country-domain-expansion.md
│  ├─ KB-05-source-hunter.md
│  ├─ KB-06-evidence-auditor.md
│  └─ KB-07-github-gcp-deployment.md
├─ docs/
│  ├─ architecture.md
│  ├─ obsidian-conventions.md
│  └─ reference-projects.md
└─ starter-vault/
   ├─ HOME.md
   ├─ content/
   ├─ hubs/
   ├─ attachments/
   ├─ templates/
   ├─ schemas/
   ├─ taxonomy/
   └─ data/
```

## Obsidian-first, not Obsidian-only

문서의 canonical 형식은 표준 Markdown + YAML Front Matter를 기본으로 하고, `[[Wikilink]]`, aliases, backlinks, Hub/MOC 등 Obsidian의 강점을 활용합니다. 동시에 GitHub와 Quartz/MkDocs에서도 읽고 빌드할 수 있도록 전용 플러그인 의존성은 최소화합니다.

자세한 규칙은 [Obsidian conventions](docs/obsidian-conventions.md)를 참고합니다.

## Evidence Model

- `Confirmed` — 공식 1차 원문 직접 확인
- `Supported` — 복수의 신뢰도 높은 근거
- `Reported` — 신뢰 가능한 2차 발표/보도
- `Inferred` — 확인 사실에 기반한 분석
- `Unverified` — 추가 확인 필요

정책·규정·표준·시장규칙처럼 시간에 따라 변하는 지식은 `published`, `effective`, `valid_from`, `valid_to`, `supersedes`, `superseded_by`를 구분합니다.

## GCP maturity levels

### Level 1 — Minimal
GitHub Actions + Cloud Storage + Cloud Scheduler + Cloud Run

### Level 2 — Automated Research
Level 1 + Pub/Sub + BigQuery/Firestore + Secret Manager + change detection

### Level 3 — AI Knowledge Platform
Level 2 + Vertex AI + embeddings + Vector Search/RAG Engine + evaluation

GCP의 데이터베이스와 인덱스는 **파생 계층**입니다. 삭제되어도 GitHub canonical knowledge로 재생성할 수 있어야 합니다.

## Quick start

1. `starter-vault/`를 새 Knowledge Base의 초기 구조로 사용합니다.
2. 프로젝트 아이디어가 한 문장뿐이면 `prompts/KB-00-project-generator.md`부터 실행합니다.
3. 새 프로젝트라면 KB-01, 기존 프로젝트라면 KB-02/03/04를 선택합니다.
4. Source가 부족하면 KB-05, 근거 품질을 감사하려면 KB-06을 사용합니다.
5. 자동화·GCP·RAG 단계에서 KB-07을 사용합니다.

## Reference implementation

GRIDEX Power Policy Knowledge Base와 HVDC Knowledge Base 같은 실제 KB 프로젝트에서 얻은 운영 경험을 일반화한 프레임워크입니다. 특정 도메인에 종속되지 않도록 설계 원칙과 템플릿만 분리합니다.

## Status

v1 — Prompt framework + evidence architecture + Obsidian conventions + GitHub/GCP reference architecture + starter vault.
