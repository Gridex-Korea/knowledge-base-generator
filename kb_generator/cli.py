from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import unicodedata
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

from .repositories import ARCHIVE_REGISTRY, PUBLIC_ATTACHMENTS, PUBLIC_IGNORE, SOURCE_POLICY, development_root

VERSION = "0.1.0"

DOMAIN_ALIASES = {
    "gfm": ("gfm", "Technology / Regulation / Standards"),
    "grid-forming": ("gfm", "Technology / Regulation / Standards"),
    "hvdc": ("hvdc", "Technology / Research / Projects"),
    "해상풍력": ("offshore-wind", "Technology / Policy / Industry"),
    "offshore wind": ("offshore-wind", "Technology / Policy / Industry"),
    "수소": ("hydrogen", "Industry / Technology / Policy"),
    "수소산업": ("hydrogen-industry", "Industry / Technology / Policy"),
    "hydrogen": ("hydrogen", "Industry / Technology / Policy"),
    "배터리": ("battery", "Industry / Technology / Research"),
    "battery": ("battery", "Industry / Technology / Research"),
    "ess": ("ess", "Technology / Market / Projects"),
    "전력정책": ("power-policy", "Policy / Regulation / Market"),
    "power policy": ("power-policy", "Policy / Regulation / Market"),
    "스마트그리드": ("smart-grid", "Technology / Policy / Research"),
    "smart grid": ("smart-grid", "Technology / Policy / Research"),
    "ai": ("ai", "Technology / Research / Industry"),
    "인공지능": ("ai", "Technology / Research / Industry"),
    "전력입찰": ("power-procurement", "Procurement / Business Intelligence"),
    "공공조달": ("public-procurement", "Procurement / Business Intelligence"),
}

TYPE_KEYWORDS = {
    "Procurement / Business Intelligence": ["입찰", "조달", "procurement", "bid", "tender"],
    "Policy / Regulation": ["정책", "규정", "규제", "법", "policy", "regulation", "rule"],
    "Research": ["논문", "연구", "paper", "research"],
    "Industry / Market": ["산업", "시장", "industry", "market", "supply chain"],
    "Technology": ["기술", "technology", "converter", "inverter", "hvdc", "gfm", "ess"],
}


@dataclass
class ProjectSpec:
    topic: str
    name: str
    slug: str
    kb_type: str
    language: str
    countries: list[str]
    site: str
    gcp_level: int
    public: bool
    created: str


def _normalize_key(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def infer_type(topic: str) -> str:
    key = _normalize_key(topic)
    if key in DOMAIN_ALIASES:
        return DOMAIN_ALIASES[key][1]
    scores: list[tuple[int, str]] = []
    for kind, words in TYPE_KEYWORDS.items():
        score = sum(1 for word in words if word in key)
        if score:
            scores.append((score, kind))
    if not scores:
        return "Mixed"
    scores.sort(reverse=True)
    if len(scores) > 1 and scores[0][0] == scores[1][0]:
        return "Mixed"
    return scores[0][1]


def slugify(topic: str) -> str:
    key = _normalize_key(topic)
    if key in DOMAIN_ALIASES:
        return DOMAIN_ALIASES[key][0]
    ascii_text = unicodedata.normalize("NFKD", topic).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_text.lower()).strip("-")
    if slug:
        return slug[:64]
    digest = hashlib.sha1(topic.encode("utf-8")).hexdigest()[:8]
    return f"knowledge-base-{digest}"


def project_name(topic: str) -> str:
    clean = topic.strip()
    return clean if clean.lower().endswith("knowledge base") else f"{clean} Knowledge Base"


def yaml_scalar(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def render_project_yaml(spec: ProjectSpec) -> str:
    countries = "\n".join(f"  - {yaml_scalar(c)}" for c in spec.countries) or "  []"
    return (
        "version: 1\n"
        f"topic: {yaml_scalar(spec.topic)}\n"
        f"name: {yaml_scalar(spec.name)}\n"
        f"slug: {yaml_scalar(spec.slug)}\n"
        f"kb_type: {yaml_scalar(spec.kb_type)}\n"
        f"language: {yaml_scalar(spec.language)}\n"
        "countries:\n"
        f"{countries}\n"
        f"site: {yaml_scalar(spec.site)}\n"
        f"gcp_level: {spec.gcp_level}\n"
        f"public: {'true' if spec.public else 'false'}\n"
        f"created: {spec.created}\n"
    )


def render_readme(spec: ProjectSpec) -> str:
    country_text = ", ".join(spec.countries) if spec.countries else "TBD"
    return f"""# {spec.name}

{spec.topic}에 대한 **검증 가능하고 Obsidian-compatible한 Living Knowledge Base**입니다.

## Project profile

- Topic: **{spec.topic}**
- Type: **{spec.kb_type}**
- Primary language: **{spec.language}**
- Country scope: **{country_text}**
- Public site engine: **{spec.site}**
- GCP maturity level: **{spec.gcp_level}**

## Start

Obsidian에서 이 저장소를 Vault로 열고 [`HOME.md`](HOME.md)에서 시작합니다.

## Knowledge rules

1. 공식 원문을 우선합니다.
2. 핵심 주장에는 `source_ids`와 Evidence Level을 연결합니다.
3. 한 문서 한 주제를 기본으로 합니다.
4. 내부 연결은 wikilink를 사용합니다.
5. 변경이 큰 자동 수집 결과는 Pull Request에서 검토합니다.
6. `published`, `effective`, `valid_from`, `valid_to`를 혼동하지 않습니다.
7. 공개 저장소와 비공개 `<공개 저장소명>-dev` 두 저장소를 반드시 운영합니다.
8. 원문 파일·추출 전문은 개발 저장소 `sources/`에 저장하고, 공개 사이트에는 원문 공식 URL 링크만 제공합니다.
9. 자세한 보관·추적 규칙은 `source-policy.md`를 따릅니다.

## Project files

- `project.yaml` — 생성기 입력과 프로젝트 설정
- `HOME.md` — Obsidian 시작 페이지
- `content/` — 지식 문서
- `hubs/` — MOC/Hub
- `data/source-registry.yaml` — 원문 출처 레지스트리
- `taxonomy/taxonomy.yaml` — 분류 체계
- `schemas/document.schema.yaml` — 문서 메타데이터 스키마
- 개발 저장소 `project/roadmap.md` — 구축 로드맵
- 개발 저장소 `project/evidence-gaps.md` — 확인되지 않은 근거 공백
- 개발 저장소 `gcp/` — GCP 자동화/RAG 확장 구성

Generated by Knowledge Base Generator v{VERSION}.
"""


def render_home(spec: ProjectSpec) -> str:
    return f"""---
title: {yaml_scalar(spec.name + ' Home')}
type: hub
status: active
evidence_level: Confirmed
tags:
  - hub
  - knowledge-base
aliases:
  - Home
---

# {spec.name}

**Topic:** {spec.topic}

## Start here

- [[Overview]]
- [[Topic Hub]]
- [[Organization Hub]]
- [[Country Hub]]
- [[Timeline Hub]]
- [[Glossary]]

## Research workflow

1. `data/source-registry.yaml`에 Source를 등록합니다.
2. 공식 원문을 확인하고 비공개 개발 저장소 `sources/`에 보관합니다. 공개 사이트에는 공식 원문 URL 링크만 제공합니다.
3. `templates/knowledge-document.md`로 Note를 작성합니다.
4. 관련 Note를 wikilink로 연결합니다.
5. Evidence Level과 `last_verified`를 기록합니다.
6. 변경은 GitHub branch/PR을 거쳐 병합합니다.
"""


def render_overview(spec: ProjectSpec) -> str:
    return f"""---
id: OVERVIEW-001
title: Overview
type: overview
status: active
evidence_level: Unverified
source_ids: []
last_verified:
aliases: []
tags:
  - overview
related: []
---

# Overview

## 주제

**{spec.topic}**

## 목적

이 Knowledge Base는 {spec.topic}의 공식 원문, 핵심 개념, 기관, 정책·규정·표준, 프로젝트 및 연구를 검증 가능한 형태로 연결합니다.

## 다음 작업

- [[Topic Hub]]에서 핵심 하위 주제를 정의합니다.
- `data/source-registry.yaml`에 Tier 1 Source를 등록합니다.
- 비공개 개발 저장소의 `project/evidence-gaps.md`에서 미확인 근거를 관리합니다.
"""


def render_glossary() -> str:
    return """---
id: GLOSSARY-001
title: Glossary
type: glossary
status: active
evidence_level: Confirmed
source_ids: []
last_verified:
aliases: []
tags:
  - glossary
related: []
---

# Glossary

| Term | Korean | Definition | Source |
|---|---|---|---|
|  |  |  |  |
"""


def render_hub(title: str, description: str, hub_id: str) -> str:
    return f"""---
id: {hub_id}
title: {yaml_scalar(title)}
type: hub
status: active
evidence_level: Confirmed
source_ids: []
last_verified:
aliases: []
tags:
  - hub
related: []
---

# {title}

{description}

## Notes

- [[Overview]]
"""


def render_note_template() -> str:
    return """---
id:
title: "{{title}}"
type: concept
status: active
evidence_level: Unverified
source_ids: []
published:
effective:
valid_from:
valid_to:
last_verified:
supersedes: []
superseded_by: []
aliases: []
tags: []
related: []
---

# {{title}}

## 한눈에 보기

핵심 내용을 3~7문장으로 요약합니다.

## 배경

## 핵심 내용

## Evidence

- Evidence Level: `Unverified`
- 확인된 사항:
- 미확인 사항:
- 추가 조사:

## 관련 문서

- [[Topic Hub]]

## 출처

- Source ID:
- Official URL:
- Version:
- Last verified:
"""


def render_schema() -> str:
    return """$schema: https://json-schema.org/draft/2020-12/schema
$title: Knowledge Base Document Metadata
type: object
required: [title, type, status, evidence_level]
properties:
  id: {type: [string, 'null']}
  title: {type: string}
  type: {type: string}
  status:
    type: string
    enum: [draft, active, superseded, archived]
  evidence_level:
    type: string
    enum: [Confirmed, Supported, Reported, Inferred, Unverified]
  source_ids:
    type: array
    items: {type: string}
  published: {type: [string, 'null']}
  effective: {type: [string, 'null']}
  valid_from: {type: [string, 'null']}
  valid_to: {type: [string, 'null']}
  last_verified: {type: [string, 'null']}
  aliases:
    type: array
    items: {type: string}
  tags:
    type: array
    items: {type: string}
  related:
    type: array
    items: {type: string}
additionalProperties: true
"""


def render_taxonomy(spec: ProjectSpec) -> str:
    return f"""version: 1
domain:
  - {yaml_scalar(spec.topic)}
subdomains: []
types:
  - overview
  - concept
  - technology
  - policy
  - regulation
  - standard
  - organization
  - company
  - project
  - country
  - research
  - dataset
  - hub
  - glossary
status: [draft, active, superseded, archived]
evidence_level: [Confirmed, Supported, Reported, Inferred, Unverified]
source_type:
  - law
  - regulation
  - standard
  - official-report
  - official-web
  - dataset
  - paper
  - technical-report
  - company-document
  - news
relationships:
  - related_to
  - issued_by
  - applies_to
  - implements
  - references
  - amends
  - supersedes
  - superseded_by
  - derived_from
"""


def render_source_registry() -> str:
    return """version: 1
sources: []

# Example
# - id: SRC-0001
#   title: Example Official Document
#   organization: Example Organization
#   country: KR
#   source_type: official-report
#   url: https://example.org/document
#   publication_date: 2026-01-01
#   version: '1.0'
#   status: final
#   official: true
#   evidence_level: Confirmed
#   collection_mode: Watch
#   last_verified: 2026-09-11
#   source_locator: Section 4.2 / p.17
# 보관 경로·수집 시각·SHA-256은 비공개 개발 저장소 data/source-archive.yaml에서 같은 Source ID로 관리합니다.
"""


def render_roadmap(spec: ProjectSpec) -> str:
    return f"""# {spec.name} Roadmap

## P0 — Initialization
- [x] Vault skeleton
- [x] Project metadata
- [x] Schema / taxonomy / source registry

## P1 — Source map
- [ ] Source-of-Truth 기관 지도
- [ ] 핵심 공식 Source 10건 이상 등록
- [ ] 저작권/재배포 정책 확인

## P2 — Seed knowledge
- [ ] Overview 보강
- [ ] 핵심 개념 5~10개
- [ ] 핵심 기관 3~10개
- [ ] Timeline
- [ ] 비교표

## P3 — Public site
- [ ] {spec.site} 구성
- [ ] 검색과 navigation 검증

## P4 — Quality gates
- [ ] Frontmatter 검사
- [ ] Broken wikilink 검사
- [ ] Duplicate ID 검사
- [ ] Orphan note 검사

## P5 — GCP automation
- [ ] Level {spec.gcp_level} 구성 검토
- [ ] Source watch / change detection

## P6 — AI/RAG
- [ ] Retrieval evaluation set
- [ ] Citation correctness
- [ ] Temporal correctness
"""


def render_evidence_gaps() -> str:
    return """# Evidence Gaps

| ID | Topic | Confirmed | Missing evidence | Needed source | Priority | Status |
|---|---|---|---|---|---|---|
| GAP-001 | 초기 핵심 근거 |  | 공식 원문 확인 필요 | Tier 1 source | P0 | OPEN |
"""


def render_gcp_readme(spec: ProjectSpec) -> str:
    levels = {
        0: "GCP 미사용. GitHub/Obsidian 중심으로 시작합니다.",
        1: "Cloud Storage + Cloud Scheduler + Cloud Run + Secret Manager를 기본으로 사용합니다.",
        2: "Level 1 + Pub/Sub + BigQuery/Firestore + change detection을 사용합니다.",
        3: "Level 2 + Vertex AI + embeddings + Vector Search/RAG Engine + evaluation을 사용합니다.",
    }
    services = {
        0: [],
        1: ["storage.googleapis.com", "run.googleapis.com", "cloudscheduler.googleapis.com", "secretmanager.googleapis.com"],
        2: ["storage.googleapis.com", "run.googleapis.com", "cloudscheduler.googleapis.com", "secretmanager.googleapis.com", "pubsub.googleapis.com", "bigquery.googleapis.com"],
        3: ["storage.googleapis.com", "run.googleapis.com", "cloudscheduler.googleapis.com", "secretmanager.googleapis.com", "pubsub.googleapis.com", "bigquery.googleapis.com", "aiplatform.googleapis.com"],
    }
    enable = " \\\n  ".join(services[spec.gcp_level]) if services[spec.gcp_level] else "# none"
    return f"""# GCP deployment notes

Selected level: **{spec.gcp_level}**

{levels[spec.gcp_level]}

## Canonical rule

GitHub Markdown/YAML이 canonical knowledge입니다. GCP의 DB, object archive, vector index는 재생성 가능한 파생 계층으로 취급합니다.

## Suggested APIs

```bash
gcloud services enable \\
  {enable}
```

## Recommended flow

```text
Cloud Scheduler / Event
        ↓
Cloud Run Job
        ↓
Fetch / Archive / Parse
        ↓
Candidate Markdown
        ↓
GitHub branch / PR
        ↓
Human review
```

Level 3에서는 merge된 canonical content를 별도 index pipeline으로 Vertex AI 검색 계층에 반영합니다.
"""


def render_gcp_config(spec: ProjectSpec, repository_name: str | None = None) -> str:
    repository_name = repository_name or f"{spec.slug}-knowledge-base"
    return f"""version: 1
level: {spec.gcp_level}
region: asia-northeast3
archive_bucket: "{spec.slug}-source-archive"
collector_job: "{spec.slug}-collector"
update_schedule: "0 6 * * 1"
canonical_repository: "REPLACE_WITH_OWNER/{repository_name}"
source_archive_repository: "REPLACE_WITH_OWNER/{repository_name}-dev"
archive_visibility: private
vertex_ai:
  enabled: {'true' if spec.gcp_level >= 3 else 'false'}
  location: asia-northeast3
  index_name: "{spec.slug}-index"
"""


def render_validation_script() -> str:
    return r'''#!/usr/bin/env python3
from __future__ import annotations
import re
import sys
from pathlib import Path

REQUIRED = {"title", "type", "status", "evidence_level"}
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")


def frontmatter(text: str):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end < 0:
        return None
    keys = set()
    for line in text[4:end].splitlines():
        if line and not line.startswith(" ") and ":" in line:
            keys.add(line.split(":", 1)[0].strip())
    return keys


def knowledge_notes(root: Path):
    notes = []
    home = root / "HOME.md"
    if home.exists():
        notes.append(home)
    for folder in ("content", "hubs"):
        path = root / folder
        if path.exists():
            notes.extend(path.rglob("*.md"))
    return notes


def main(root: Path) -> int:
    notes = knowledge_notes(root)
    stems = {p.stem for p in notes}
    errors = []
    for private_path in ("sources", "project", "gcp", "data/source-archive.yaml", "data/source-candidates.json"):
        if (root / private_path).exists():
            errors.append(f"{private_path}: belongs in the private <name>-dev repository")
    seen_ids = {}
    id_re = re.compile(r"^id:\s*[\"']?([^\"'\n]+)", re.M)
    for p in notes:
        text = p.read_text(encoding="utf-8")
        fm = frontmatter(text)
        if fm is None:
            errors.append(f"{p}: missing YAML frontmatter")
        else:
            missing = REQUIRED - fm
            if missing:
                errors.append(f"{p}: missing frontmatter fields {sorted(missing)}")
        match = id_re.search(text[:1500])
        if match:
            doc_id = match.group(1).strip()
            if doc_id in seen_ids:
                errors.append(f"duplicate id {doc_id}: {seen_ids[doc_id]} and {p}")
            seen_ids[doc_id] = p
        for target in WIKILINK.findall(text):
            target = target.strip()
            if target and target not in stems:
                errors.append(f"{p}: broken wikilink [[{target}]]")
    if errors:
        print("Knowledge Base validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Knowledge Base validation OK: {len(notes)} knowledge notes")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()))
'''


def render_workflow() -> str:
    return """name: validate-knowledge-base

on:
  pull_request:
  push:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: python scripts/validate_kb.py .
"""


def write_builtin_starter(output: Path, spec: ProjectSpec) -> None:
    files = {
        output / "HOME.md": render_home(spec),
        output / "content" / "Overview.md": render_overview(spec),
        output / "content" / "Glossary.md": render_glossary(),
        output / "hubs" / "Topic Hub.md": render_hub("Topic Hub", "핵심 주제와 개념을 연결합니다.", "HUB-TOPIC"),
        output / "hubs" / "Organization Hub.md": render_hub("Organization Hub", "정부·규제기관·연구기관·기업을 연결합니다.", "HUB-ORG"),
        output / "hubs" / "Country Hub.md": render_hub("Country Hub", "국가·관할권별 지식을 연결합니다.", "HUB-COUNTRY"),
        output / "hubs" / "Timeline Hub.md": render_hub("Timeline Hub", "정책·표준·프로젝트의 시간 변화를 연결합니다.", "HUB-TIMELINE"),
        output / "templates" / "knowledge-document.md": render_note_template(),
        output / "schemas" / "document.schema.yaml": render_schema(),
        output / "taxonomy" / "taxonomy.yaml": render_taxonomy(spec),
        output / "data" / "source-registry.yaml": render_source_registry(),
        output / "attachments" / "README.md": PUBLIC_ATTACHMENTS,
    }
    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def copy_starter(template_root: Path, output: Path) -> None:
    if not template_root.exists():
        raise FileNotFoundError(f"starter vault not found: {template_root}")
    for item in template_root.iterdir():
        dest = output / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest)


def generate(spec: ProjectSpec, output: Path, template_root: Path | None = None, force: bool = False) -> list[Path]:
    output = output.resolve()
    dev = development_root(output)
    if not spec.public:
        raise ValueError("Every KB requires a public repository and a private <name>-dev repository; --private is no longer supported")
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]*", spec.slug):
        raise ValueError("slug must contain only ASCII letters, numbers, hyphens or underscores")
    for target in (output, dev):
        if target.exists() and any(target.iterdir()) and not force:
            raise FileExistsError(f"output directory is not empty: {target}; use --force to merge")
    if template_root is not None:
        for private_path in (".git", "sources", "project", "gcp", "data/source-archive.yaml", "data/source-candidates.json"):
            if (template_root / private_path).exists():
                raise ValueError(f"custom starter must contain only public files; remove {private_path} from the template")
    output.mkdir(parents=True, exist_ok=True)
    if template_root is not None:
        copy_starter(template_root, output)
    else:
        write_builtin_starter(output, spec)

    files = {
        output / "README.md": render_readme(spec),
        output / "source-policy.md": SOURCE_POLICY,
        output / "attachments" / "README.md": PUBLIC_ATTACHMENTS,
        dev / "source-policy.md": SOURCE_POLICY,
        dev / "README.md": f"# {output.name}-dev\n\n비공개 개발 저장소입니다. 공개 저장소는 `{output.name}`입니다.\n원문은 `sources/`, 보관 이력은 `data/source-archive.yaml`, 운영 기록은 `project/`에 저장합니다.\n이 저장소를 공개 사이트 빌드 대상으로 사용하지 않습니다.\n",
        dev / "sources" / "README.md": "# 원문 보관\n\nSource ID/수집일/파일명 구조로 원문을 저장하고 data/source-archive.yaml에 등록합니다.\n이 디렉터리의 실제 원문 파일도 비공개 Git 저장소에 커밋합니다.\n",
        dev / "data" / "source-archive.yaml": ARCHIVE_REGISTRY,
        dev / "repository.json": json.dumps({"name": dev.name, "visibility": "private", "public_repository": output.name}, indent=2) + "\n",
        output / "project.yaml": render_project_yaml(spec) + f"public_repository: {yaml_scalar(output.name)}\ndevelopment_repository: {yaml_scalar(dev.name)}\ndevelopment_visibility: private\nsource_policy: link-only\n",
        dev / "project" / "roadmap.md": render_roadmap(spec),
        dev / "project" / "evidence-gaps.md": render_evidence_gaps(),
        dev / "gcp" / "README.md": render_gcp_readme(spec),
        dev / "gcp" / "config.yaml": render_gcp_config(spec, output.name),
        output / "scripts" / "validate_kb.py": render_validation_script(),
        output / ".github" / "workflows" / "validate.yml": render_workflow(),
        output / "generator-manifest.json": json.dumps(asdict(spec), ensure_ascii=False, indent=2) + "\n",
    }
    for path, content in files.items():
        if path == dev / "data" / "source-archive.yaml" and path.exists():
            continue  # Preserve source provenance when regenerating with --force.
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    ignore = output / ".gitignore"
    existing_ignore = ignore.read_text(encoding="utf-8") if ignore.exists() else ""
    if PUBLIC_IGNORE not in existing_ignore:
        ignore.write_text(existing_ignore + "\n" + PUBLIC_IGNORE, encoding="utf-8")
    dev_ignore = dev / ".gitignore"
    if not dev_ignore.exists():
        dev_ignore.write_text(".env\n.env.*\n__pycache__/\n", encoding="utf-8")
    return sorted(files)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="kbgen", description="Generate an Obsidian-compatible, GitHub/GCP-ready Knowledge Base")
    parser.add_argument("topic", help="Knowledge Base topic, e.g. '해상풍력' or 'HVDC'")
    parser.add_argument("--output", "-o", type=Path, help="Output directory; defaults to ./<slug>-knowledge-base")
    parser.add_argument("--name", help="Project display name")
    parser.add_argument("--slug", help="ASCII project slug")
    parser.add_argument("--type", dest="kb_type", help="Knowledge Base type; auto-detected by default")
    parser.add_argument("--language", default="ko", help="Primary language (default: ko)")
    parser.add_argument("--countries", nargs="*", default=["KR"], help="Country codes, e.g. KR AU US")
    parser.add_argument("--site", choices=["quartz", "mkdocs", "docusaurus", "none"], default="quartz")
    parser.add_argument("--gcp-level", type=int, choices=[0, 1, 2, 3], default=1)
    parser.add_argument("--private", action="store_true", help="Unsupported: every KB now requires a public and a private -dev repository")
    parser.add_argument("--force", action="store_true", help="Merge into a non-empty output directory")
    parser.add_argument("--json", action="store_true", help="Print generated project metadata as JSON")
    parser.add_argument("--template-root", type=Path, help="Use a custom starter vault instead of the built-in scaffold")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(list(argv) if argv is not None else None)
    slug = args.slug or slugify(args.topic)
    spec = ProjectSpec(
        topic=args.topic.strip(),
        name=args.name or project_name(args.topic),
        slug=slug,
        kb_type=args.kb_type or infer_type(args.topic),
        language=args.language,
        countries=args.countries,
        site=args.site,
        gcp_level=args.gcp_level,
        public=not args.private,
        created=date.today().isoformat(),
    )
    output = (args.output or Path(f"{slug}-knowledge-base")).resolve()
    template_root = args.template_root.resolve() if args.template_root else None
    try:
        generated = generate(spec, output, template_root, force=args.force)
    except (FileNotFoundError, FileExistsError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({"output": str(output), "development_output": str(development_root(output)), "project": asdict(spec)}, ensure_ascii=False, indent=2))
    else:
        print(f"Created {spec.name}")
        print(f"Public output: {output}")
        print(f"Private development output: {development_root(output)}")
        print(f"Type: {spec.kb_type} | Site: {spec.site} | GCP Level: {spec.gcp_level}")
        print(f"Generated control files: {len(generated)}")
        print("Next: open the output directory as an Obsidian Vault and start at HOME.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
