# Web Generator Roadmap

CLI v0.1을 핵심 엔진으로 두고 웹 UI는 얇은 입력/미리보기 계층으로 확장한다.

## 목표 UX

```text
주제 한 줄 입력
  ↓
자동 Project Blueprint
  ↓
Name / slug / type / country / site / GCP level 확인
  ↓
생성될 Vault Tree 미리보기
  ↓
ZIP 생성 또는 GitHub repository 생성
```

## 권장 구조

```text
Web UI
  ↓
Generator API
  ↓
kb_generator core
  ↓
Vault / GitHub / GCP manifests
```

CLI와 Web이 서로 다른 생성 로직을 갖지 않도록 `kb_generator` core를 공통으로 사용한다.

## v0.2
- Flask/FastAPI 없이도 시작 가능한 정적 form prototype 또는 Cloud Run API 설계
- Project Blueprint preview
- Generated tree preview
- ZIP export

## v0.3
- GitHub App/Token 연동
- repository create / initial commit
- Quartz/MkDocs 선택 배포
- GCP project 연결

## v1
- Source Hunter
- Evidence Auditor
- scheduled update workflow
- RAG configuration wizard
