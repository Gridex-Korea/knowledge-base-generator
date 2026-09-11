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
