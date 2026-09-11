# Obsidian-compatible Knowledge Base Conventions

이 프레임워크의 기본 문서 형식은 **Obsidian-compatible Markdown**이다. 즉, 저장소를 그대로 Obsidian Vault로 열어도 지식 구조가 유지되어야 하며 동시에 GitHub와 정적 사이트에서도 읽을 수 있어야 한다.

## 1. 기본 원칙

- 모든 핵심 지식 문서는 `.md`로 작성한다.
- YAML Front Matter를 사용한다.
- 내부 지식 연결은 `[[Wikilink]]`를 기본으로 한다.
- GitHub/정적 사이트 호환이 필요한 경우 일반 Markdown 링크를 병행하거나 빌드 단계에서 변환한다.
- 한 문서는 가능한 한 한 주제를 다룬다.
- Hub/MOC(Map of Content) 문서를 사용해 탐색 구조를 만든다.
- 태그는 보조 분류로만 사용하고, 핵심 관계는 링크와 메타데이터로 표현한다.
- 첨부파일은 규칙화된 전용 폴더에서 관리한다.

## 2. 권장 Vault 구조

```text
/
├─ README.md
├─ HOME.md
├─ content/
│  ├─ concepts/
│  ├─ technology/
│  ├─ policy/
│  ├─ regulation/
│  ├─ standards/
│  ├─ countries/
│  ├─ organizations/
│  ├─ projects/
│  └─ research/
├─ hubs/
│  ├─ topic-hub.md
│  ├─ country-hub.md
│  ├─ organization-hub.md
│  └─ timeline-hub.md
├─ attachments/
├─ templates/
├─ data/
├─ schemas/
└─ .obsidian/
```

`.obsidian/`은 팀 공용 설정만 선택적으로 버전 관리한다. 개인 workspace 상태, 캐시, 개인 플러그인 상태는 기본적으로 커밋하지 않는다.

## 3. Front Matter

권장 최소 필드:

```yaml
---
id: TECH-GFM
title: Grid-Forming Inverter
title_en: Grid-Forming Inverter
type: technology
status: active
evidence_level: Confirmed
source_ids:
  - SRC-0001
published:
effective:
valid_from:
valid_to:
last_verified: 2026-09-11
tags:
  - power-system
  - inverter
aliases:
  - GFM
  - Grid Forming
related:
  - TECH-GFL
  - STD-IEEE-2800
---
```

`aliases`는 Obsidian 링크 해석과 검색성을 높이는 데 활용한다.

## 4. Wikilink 규칙

기본:

```markdown
[[Grid-Forming Inverter]]
[[IEEE 2800]]
[[Australia]]
```

표시명을 다르게 할 때:

```markdown
[[Grid-Forming Inverter|GFM 인버터]]
```

특정 섹션 연결:

```markdown
[[IEEE 2800#Model Requirements]]
```

가능하면 파일명은 사람이 읽기 좋은 canonical title을 사용하고, 기계 식별자는 frontmatter의 `id`로 분리한다.

## 5. Backlink와 연결성

새 문서를 만들 때 최소 다음 연결을 검토한다.

- 상위 Hub/MOC
- 관련 개념
- 관련 기관
- 관련 국가
- 관련 정책/규정/표준
- 관련 프로젝트/연구
- 원문 Source Registry

CI에서는 orphan note를 탐지하되, 의도적인 standalone 문서는 예외 목록으로 관리한다.

## 6. Hub / MOC

Hub는 단순 디렉터리 목록이 아니라 사람이 탐색하는 지식 지도다.

예:

```markdown
# Grid-Forming Hub

## Overview
- [[What is Grid-Forming]]

## Technology
- [[Droop Control]]
- [[Virtual Synchronous Machine]]

## Regulation
- [[Korea GFM Regulation]]
- [[Australia GFM Framework]]

## Standards
- [[IEEE 2800]]

## Evidence Gaps
- [[GFM Evidence Gaps]]
```

## 7. 문서 템플릿

```markdown
---
id:
title:
type:
status:
evidence_level:
source_ids: []
last_verified:
tags: []
aliases: []
related: []
---

# 제목

## 한눈에 보기

## 핵심 내용

## 세부 내용

## 적용 범위

## 관련 문서
- [[관련 문서]]

## Evidence Status

## Sources
```

## 8. 첨부파일

권장:

```text
attachments/
  images/
  diagrams/
```

- 원문 PDF·HTML·추출 전문은 비공개 `<공개 저장소명>-dev/sources/`에 저장하고 보관 이력을 추적한다.
- 공개 저장소와 사이트는 Source Registry와 공식 원문 URL 링크만 제공한다. 원문 embed·다운로드는 제공하지 않는다.
- 상세 규칙은 [원문 및 저장소 정책](source-policy.md)을 따른다.
- 이미지 파일명은 의미 있는 slug를 사용한다.
- Obsidian embed는 `![[image-name.png]]`를 사용할 수 있다.
- 공개 사이트 빌드가 Obsidian embed를 지원하지 않으면 변환 규칙을 둔다.

## 9. Obsidian Callout

설명·주의·근거 수준 표시에 Obsidian callout을 선택적으로 사용한다.

```markdown
> [!note]
> 배경 설명

> [!warning]
> 공식 원문 미확인

> [!source]
> 근거 문서와 확인 위치
```

정적 사이트 엔진이 callout을 처리하지 못하는 경우 일반 blockquote로 graceful degradation되어야 한다.

## 10. 태그 규칙

태그는 지나치게 세분화하지 않는다.

권장 예:

```text
#technology/gfm
#country/korea
#document/standard
#status/draft
#evidence/confirmed
```

동일 정보를 frontmatter와 tag에 중복 저장해야 할 이유가 없다면 frontmatter를 우선한다.

## 11. Dataview 호환성

Obsidian Dataview를 사용할 수 있도록 frontmatter 타입을 일관되게 유지한다. 다만 Dataview 자체가 canonical data source가 되어서는 안 된다.

예:

```dataview
TABLE status, evidence_level, last_verified
FROM "content/regulation"
WHERE country = "KR"
SORT last_verified DESC
```

공개 사이트는 Dataview 없이도 동일 핵심 정보를 탐색할 수 있어야 한다.

## 12. GitHub 호환성

Obsidian 전용 기능 때문에 GitHub에서 문서가 읽히지 않게 만들지 않는다.

우선순위:

1. 표준 Markdown
2. YAML Front Matter
3. Wikilink
4. Callout/embed
5. Plugin-specific syntax

플러그인 전용 문법은 핵심 지식을 담는 유일한 표현 방식으로 사용하지 않는다.

## 13. 파일명 규칙

- 사람이 읽을 수 있는 이름 사용
- 불필요한 날짜 prefix 금지
- 동일 제목 충돌 시 국가/기관/버전으로 구분
- `/`, `:`, `?`, `#` 등 호환성 낮은 문자는 피한다

예:

```text
Grid-Forming Inverter.md
IEEE 2800.md
Australia - GFM Framework.md
KEPCO - GFM Requirements.md
```

## 14. Obsidian과 공개 사이트의 역할 분리

```text
Obsidian
→ 작성 / 탐색 / backlink / graph / 연구노트

GitHub
→ canonical history / review / collaboration / CI

Quartz or MkDocs
→ public publishing / search / navigation

GCP
→ collection / indexing / RAG / automation
```

따라서 같은 Markdown 지식 원본을 여러 인터페이스가 재사용하는 구조를 유지한다.

## 15. 완료 기준

신규 KB는 최소 다음을 만족해야 한다.

- 저장소 루트를 Obsidian Vault로 열 수 있음
- 핵심 문서에 YAML Front Matter 존재
- Hub/MOC 존재
- wikilink가 정상 연결됨
- orphan note 검증 가능
- 첨부파일 경로 규칙 존재
- GitHub에서도 Markdown이 읽힘
- 정적 사이트 빌드가 성공함
- `.obsidian/` 정책이 문서화됨
