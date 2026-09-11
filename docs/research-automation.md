# Research Automation

Knowledge Base Generator의 자동 연구 계층은 **검색 결과를 곧바로 확정 지식으로 취급하지 않습니다.**

## Workflow

```text
Topic / Country Scope
        ↓
Research Plan
        ↓
Grounded Web Discovery
        ↓
Candidate Sources
        ↓
Source Hunter verification
        ↓
Source Registry
        ↓
Knowledge Notes
        ↓
Evidence Audit
```

## Vertex AI provider

`kbgen research --provider vertex`는 Vertex AI Gemini의 Google Search grounding을 사용해 현재 웹의 관련 자료와 출처 후보를 찾습니다.

필요 조건:

- Google Cloud project
- Vertex AI API 사용 가능
- `gcloud auth print-access-token`이 동작하거나 `GOOGLE_OAUTH_ACCESS_TOKEN` 환경변수 설정

검색으로 발견한 URL은 비공개 개발 폴더의 `data/source-candidates.json`에 저장합니다. 이 단계의 출처는 아직 `Confirmed`가 아닙니다. 공식 기관 여부, 문서 버전, 시행 상태, 후속 개정 여부를 확인한 뒤 Source Registry로 승격해야 합니다.

## Commands

```bash
# 연구계획만 생성
kbgen research ./my-kb

# Google Search grounding으로 실제 source discovery
kbgen research ./my-kb \
  --provider vertex \
  --gcp-project MY_PROJECT \
  --location us-central1 \
  --model gemini-2.5-flash
```

## Safety and evidence rule

- 검색 결과 URL은 Candidate Source다.
- AI가 작성한 요약은 원문 자체가 아니다.
- 규정·표준·시행일·수치 등 고위험 사실은 공식 원문을 직접 확인하기 전 `Confirmed`로 표시하지 않는다.
- 발견 결과는 GitHub branch/PR을 거쳐 검토하는 것을 권장한다.

## 공개/개발 저장소와 원문

모든 프로젝트는 공개 `<name>`과 비공개 `<name>-dev` 두 저장소를 사용합니다.
CLI는 출력 폴더 옆에 `-dev` 폴더를 함께 생성하며 Web ZIP도 두 폴더를 포함합니다.
`project/`의 연구계획·결과·감사·roadmap·evidence gaps와 `gcp/`는 개발 폴더에 생성됩니다.
`data/source-candidates.json`도 개발 폴더에 저장하고 검증된 출처만 공개 `data/source-registry.yaml`에 등록합니다.
원문 파일·추출 전문은 개발 저장소 `sources/`에 저장하고 `data/source-archive.yaml`로 보관 이력을 추적합니다.
공개 사이트의 원문 제공은 공식 URL 링크만 허용합니다. 원문이나 개발 폴더 전체를 사이트에 배포하지 않습니다.
`kbgen github <공개 폴더> --execute`는 두 저장소를 Public/Private로 각각 생성·push합니다.
