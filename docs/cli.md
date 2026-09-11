# KB Generator CLI

`kbgen`은 한 줄의 주제를 받아 Obsidian-compatible Knowledge Base 골격을 생성합니다.

## Quick start

```bash
python -m kb_generator "해상풍력"
```

기본 출력은 `./offshore-wind-knowledge-base`입니다.

설치 후에는 다음처럼 사용할 수 있습니다.

```bash
pip install -e .
kbgen "해상풍력"
```

## Example

```bash
kbgen "해상풍력" \
  --countries KR AU \
  --site quartz \
  --gcp-level 2 \
  --output ./offshore-wind-kb
```

생성 결과에는 다음이 포함됩니다.

```text
HOME.md
README.md
project.yaml
content/
hubs/
templates/
schemas/
taxonomy/
data/source-registry.yaml
project/roadmap.md
project/evidence-gaps.md
gcp/config.yaml
gcp/README.md
scripts/validate_kb.py
.github/workflows/validate.yml
generator-manifest.json
```

## Automatic inference

v0.1은 일부 자주 쓰는 에너지·전력 주제를 자동 인식합니다.

| 입력 | 자동 slug | 기본 유형 |
|---|---|---|
| `해상풍력` | `offshore-wind` | Technology / Policy / Industry |
| `HVDC` | `hvdc` | Technology / Research / Projects |
| `GFM` | `gfm` | Technology / Regulation / Standards |
| `수소산업` | `hydrogen-industry` | Industry / Technology / Policy |
| `전력정책` | `power-policy` | Policy / Regulation / Market |
| `전력입찰` | `power-procurement` | Procurement / Business Intelligence |

알 수 없는 영문 주제는 일반 slugify를 사용합니다. 영문으로 변환하기 어려운 한글 주제는 안정적인 hash 기반 slug를 만들며, `--slug`로 원하는 이름을 직접 지정할 수 있습니다.

## Options

```text
--output, -o       출력 폴더
--name             표시 프로젝트명
--slug             프로젝트 slug
--type             KB 유형 강제 지정
--language         기본 언어 (기본 ko)
--countries        국가 코드 목록
--site             quartz / mkdocs / docusaurus / none
--gcp-level        0 / 1 / 2 / 3
--private          비공개 프로젝트 표시
--template-root    사용자 정의 Starter Vault 사용
--force            비어 있지 않은 폴더에 병합
--json             생성 결과를 JSON으로 출력
```

## GCP levels

- **0** — GitHub + Obsidian만 사용
- **1** — Cloud Storage + Cloud Scheduler + Cloud Run + Secret Manager
- **2** — Level 1 + Pub/Sub + BigQuery/Firestore + change detection
- **3** — Level 2 + Vertex AI + embeddings + Vector Search/RAG Engine + evaluation

GCP 인프라는 canonical knowledge가 아닙니다. Markdown/YAML을 GitHub에 유지하고 GCP의 저장소·검색 인덱스는 재생성 가능한 파생 계층으로 취급합니다.

## Validation

생성된 KB에는 독립 검증기가 포함됩니다.

```bash
python scripts/validate_kb.py .
```

현재 v0.1은 다음을 검사합니다.

- 핵심 Note의 YAML Front Matter
- 필수 metadata 필드
- 중복 document ID
- broken wikilink

생성되는 GitHub Actions workflow도 동일 검증기를 PR 및 main push에서 실행합니다.

## Custom starter vault

기본 내장 scaffold 대신 기존 Obsidian Vault 구조를 템플릿으로 사용할 수 있습니다.

```bash
kbgen "HVDC" --template-root ./my-starter-vault
```

Generator가 프로젝트 설정, roadmap, GCP 설정, validator 등 제어 파일을 추가합니다.

## v0.2 candidates

- `kbgen research` — KB-05 Source Hunter 실행용 research manifest 생성
- `kbgen audit` — KB-06 Evidence Auditor 로컬 검사
- GitHub repository 자동 생성 및 초기 push
- Quartz/MkDocs 실제 사이트 scaffold 생성
- GCP Terraform 생성
- Web UI
