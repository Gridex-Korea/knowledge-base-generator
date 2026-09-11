# Knowledge Base Generator

**Build verified, Obsidian-compatible knowledge bases with GitHub, Google Cloud, and AI.**

Knowledge Base Generator는 특정 분야의 자료를 단순히 모으는 도구가 아니라, **공식 원문 → 검증 → 구조화 → Obsidian 지식화 → GitHub 버전관리 → 공개 사이트 → 자동 업데이트 → 검색/RAG**까지 이어지는 범용 Knowledge Base 생성 프레임워크입니다.

전력정책, GFM, HVDC, 해상풍력, 수소, 배터리, AI, 공공조달 등 주제만 바꿔 동일한 구조를 재사용하는 것을 목표로 합니다.

## CLI — 한 줄로 시작하기

```bash
python -m kb_generator "해상풍력"
```

또는 editable install 후:

```bash
pip install -e .
kbgen "해상풍력" --countries KR AU --site quartz --gcp-level 2
```

예를 들어 `해상풍력`을 입력하면 `offshore-wind` slug와 기술·정책·산업 혼합형 구조를 자동 추론하고 다음을 생성합니다.

```text
offshore-wind-knowledge-base/
├─ README.md
├─ HOME.md
├─ project.yaml
├─ content/
├─ hubs/
├─ templates/
├─ schemas/
├─ taxonomy/
├─ data/source-registry.yaml
├─ project/
│  ├─ roadmap.md
│  └─ evidence-gaps.md
├─ gcp/
│  ├─ README.md
│  └─ config.yaml
├─ scripts/validate_kb.py
├─ .github/workflows/validate.yml
└─ generator-manifest.json
```

생성 직후에는 다음 검증을 실행할 수 있습니다.

```bash
python offshore-wind-knowledge-base/scripts/validate_kb.py offshore-wind-knowledge-base
```

자세한 사용법은 [CLI guide](docs/cli.md)를 참고하세요.

## Web Generator

같은 생성 엔진을 웹 UI에서도 사용할 수 있습니다.

```bash
pip install -e .
kbgen-web --host 127.0.0.1 --port 8080
```

브라우저에서 `http://127.0.0.1:8080`을 열고 주제·국가·사이트 엔진·GCP Level을 선택하면 완성된 Knowledge Base ZIP을 생성합니다.

Docker/Cloud Run 배포도 지원합니다.

```bash
docker build -t knowledge-base-generator .
docker run --rm -p 8080:8080 knowledge-base-generator
```

자세한 내용은 [Web Generator guide](docs/web.md)를 참고하세요.

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
├─ kb_generator/        # CLI + Web generator core
├─ tests/               # generator smoke/unit tests
├─ prompts/             # KB-00 ~ KB-07
├─ docs/
│  ├─ architecture.md
│  ├─ obsidian-conventions.md
│  ├─ reference-projects.md
│  ├─ cli.md
│  └─ web.md
├─ Dockerfile           # Cloud Run-ready web container
└─ starter-vault/       # reusable reference Vault
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

### Level 0 — Local / GitHub only
Obsidian + GitHub 중심으로 시작합니다.

### Level 1 — Minimal
Cloud Storage + Cloud Scheduler + Cloud Run + Secret Manager

### Level 2 — Automated Research
Level 1 + Pub/Sub + BigQuery/Firestore + change detection

### Level 3 — AI Knowledge Platform
Level 2 + Vertex AI + embeddings + Vector Search/RAG Engine + evaluation

GCP의 데이터베이스와 인덱스는 **파생 계층**입니다. 삭제되어도 GitHub canonical knowledge로 재생성할 수 있어야 합니다.

## Current generator features

- 한 줄 주제 입력
- 자주 쓰는 한국어/영문 도메인 slug 자동 추론
- Knowledge Base 유형 자동 추론
- Obsidian Hub/MOC와 초기 Note 생성
- Schema / Taxonomy / Source Registry 생성
- Roadmap / Evidence Gap 생성
- GCP level별 설정 초안 생성
- GitHub Actions validation workflow 생성
- Frontmatter / duplicate ID / broken wikilink 검사
- 사용자 정의 Starter Vault 지원
- 웹 폼 기반 ZIP export
- Docker / Cloud Run-ready 웹 실행

## Roadmap

다음 단계에서는 다음을 확장할 예정입니다.

- GitHub repository 생성 및 초기 push 자동화
- Quartz/MkDocs 실제 사이트 scaffold
- GCP Terraform 생성
- `kbgen research` — Source Hunter 실행 구조
- `kbgen audit` — Evidence Auditor 자동화
- Project Blueprint / file tree 웹 미리보기

## Reference implementation

GRIDEX Power Policy Knowledge Base와 HVDC Knowledge Base 같은 실제 KB 프로젝트에서 얻은 운영 경험을 일반화한 프레임워크입니다. 특정 도메인에 종속되지 않도록 설계 원칙과 템플릿만 분리합니다.

## Status

**v0.2 preview** — one-line CLI + web ZIP generator + Obsidian scaffold + GitHub validation + GCP configuration manifest.
