# Web Generator

웹 Generator는 CLI와 동일한 `kb_generator` core를 사용합니다. 브라우저에서 주제·국가·사이트 엔진·GCP Level을 입력하면 완성된 Knowledge Base를 ZIP으로 생성합니다.

## Local run

```bash
pip install -e .
kbgen-web --host 127.0.0.1 --port 8080
```

브라우저에서 `http://127.0.0.1:8080`을 엽니다.

`/healthz`는 단순 health check를 제공합니다.

## Generated ZIP

ZIP 내부에는 CLI와 동일하게 다음이 포함됩니다.

- Obsidian `HOME.md`, Overview, Hub/MOC, Glossary
- document schema
- taxonomy
- source registry
- roadmap / evidence gaps
- GCP config manifest
- generated Knowledge Base validator
- GitHub Actions validation workflow

## Docker

```bash
docker build -t knowledge-base-generator .
docker run --rm -p 8080:8080 knowledge-base-generator
```

## Google Cloud Run

예시:

```bash
gcloud run deploy knowledge-base-generator \
  --source . \
  --region asia-northeast3 \
  --allow-unauthenticated
```

현재 Web Generator는 서버에 생성 파일을 영구 저장하지 않습니다. 요청마다 임시 디렉터리에서 Vault를 생성하고 ZIP bytes를 응답한 뒤 임시 파일을 제거합니다.

## Security notes

- 입력 payload는 64 KiB로 제한합니다.
- 서버가 GitHub token이나 GCP credential을 사용자 입력으로 받지 않습니다.
- v0.2는 repository 생성 대신 ZIP export만 제공합니다.
- 향후 GitHub 연동은 OAuth/GitHub App 방식으로 별도 권한 경계를 둡니다.

## Next

- Project Blueprint 미리보기
- 생성될 파일 tree 미리보기
- GitHub repository 자동 생성
- Quartz/MkDocs 배포
- Source Hunter / Evidence Auditor UI

## 공개/개발 저장소와 원문

모든 프로젝트는 공개 `<name>`과 비공개 `<name>-dev` 두 저장소를 사용합니다.
CLI는 출력 폴더 옆에 `-dev` 폴더를 함께 생성하며 Web ZIP도 두 폴더를 포함합니다.
`project/`의 연구계획·결과·감사·roadmap·evidence gaps와 `gcp/`는 개발 폴더에 생성됩니다.
`data/source-candidates.json`도 개발 폴더에 저장하고 검증된 출처만 공개 `data/source-registry.yaml`에 등록합니다.
원문 파일·추출 전문은 개발 저장소 `sources/`에 저장하고 `data/source-archive.yaml`로 보관 이력을 추적합니다.
공개 사이트의 원문 제공은 공식 URL 링크만 허용합니다. 원문이나 개발 폴더 전체를 사이트에 배포하지 않습니다.
`kbgen github <공개 폴더> --execute`는 두 저장소를 Public/Private로 각각 생성·push합니다.
