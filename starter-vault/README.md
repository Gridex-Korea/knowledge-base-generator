# Starter Vault

새 Knowledge Base를 시작할 때 이 디렉터리의 내용을 프로젝트 저장소 루트로 복사해 사용합니다.

## 포함 구조

```text
HOME.md
content/
hubs/
templates/
schemas/
taxonomy/
data/
attachments/
```

Obsidian에서는 복사한 프로젝트 저장소 루트를 Vault로 엽니다. Obsidian이 생성하는 `.obsidian/` 중 개인 workspace·cache·개인 상태는 Git에 커밋하지 않는 것을 권장합니다.

## 시작 순서

1. `HOME.md`의 프로젝트 이름과 탐색 링크를 조정합니다.
2. `content/Overview.md`에 범위와 핵심 질문을 작성합니다.
3. `taxonomy/taxonomy.yaml`을 도메인에 맞게 조정합니다.
4. `data/source-registry.yaml`에 공식 Source-of-Truth를 등록합니다.
5. `templates/knowledge-document.md`로 Note를 생성합니다.
6. 각 Note를 Hub/MOC와 `[[Wikilink]]`로 연결합니다.
7. Evidence Level과 `last_verified`를 유지합니다.

전체 규칙은 상위 저장소의 `docs/obsidian-conventions.md`를 참고합니다.

## 공개/개발 저장소와 원문

모든 프로젝트는 공개 `<name>`과 비공개 `<name>-dev` 두 저장소를 사용합니다.
CLI는 출력 폴더 옆에 `-dev` 폴더를 함께 생성하며 Web ZIP도 두 폴더를 포함합니다.
`project/`의 연구계획·결과·감사·roadmap·evidence gaps와 `gcp/`는 개발 폴더에 생성됩니다.
`data/source-candidates.json`도 개발 폴더에 저장하고 검증된 출처만 공개 `data/source-registry.yaml`에 등록합니다.
원문 파일·추출 전문은 개발 저장소 `sources/`에 저장하고 `data/source-archive.yaml`로 보관 이력을 추적합니다.
공개 사이트의 원문 제공은 공식 URL 링크만 허용합니다. 원문이나 개발 폴더 전체를 사이트에 배포하지 않습니다.
`kbgen github <공개 폴더> --execute`는 두 저장소를 Public/Private로 각각 생성·push합니다.
