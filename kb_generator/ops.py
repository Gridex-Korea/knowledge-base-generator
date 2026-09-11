from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from typing import Any

from .repositories import development_root


HIGH_VALUE_SOURCE_CATEGORIES = [
    ("Government", "정부·부처의 법령, 정책, 기본계획, 공식 보도자료"),
    ("Regulator", "규제기관의 규정, 결정문, 공청회, 시행 문서"),
    ("System/Market Operator", "운영기관의 시장규칙, 계통규정, 모델·시험 요구사항"),
    ("Standards Body", "국가·국제 표준기관의 표준, 개정안, 기술보고서"),
    ("Public Research Institute", "공공 연구기관의 기술보고서와 실증 결과"),
    ("Official Dataset", "공공 통계·공식 데이터셋"),
]


def parse_project_yaml(path: Path) -> dict[str, Any]:
    """Parse the small project.yaml emitted by kbgen without a YAML dependency."""
    data: dict[str, Any] = {}
    current_list: str | None = None
    if not path.exists():
        raise FileNotFoundError(f"project.yaml not found: {path}")
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - ") and current_list:
            value = line[4:].strip().strip('"').strip("'")
            data.setdefault(current_list, []).append(value)
            continue
        if line.startswith(" ") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        current_list = None
        if not value:
            current_list = key
            data[key] = []
            continue
        value = value.strip('"').strip("'")
        if value in {"true", "false"}:
            data[key] = value == "true"
        elif re.fullmatch(r"-?\d+", value):
            data[key] = int(value)
        else:
            data[key] = value
    return data


def load_project(root: Path) -> dict[str, Any]:
    root = root.resolve()
    project = parse_project_yaml(root / "project.yaml")
    project["root"] = str(root)
    return project


def research_queries(project: dict[str, Any]) -> list[str]:
    topic = project.get("topic", "")
    countries = project.get("countries", []) or []
    kb_type = project.get("kb_type", "Mixed")
    scope = " ".join(countries)
    queries = [
        f"{topic} official government regulator standard primary source {scope}".strip(),
        f"{topic} official regulation standard technical requirements {scope}".strip(),
        f"{topic} official report dataset research institute {scope}".strip(),
    ]
    lower = kb_type.lower()
    if "policy" in lower or "regulation" in lower:
        queries.append(f"{topic} law regulation consultation effective date official {scope}".strip())
    if "technology" in lower:
        queries.append(f"{topic} grid code testing model requirements standard official {scope}".strip())
    if "market" in lower or "procurement" in lower:
        queries.append(f"{topic} market rules procurement specification official {scope}".strip())
    if "research" in lower:
        queries.append(f"{topic} public research institute technical report official {scope}".strip())
    return queries


def render_research_plan(project: dict[str, Any]) -> str:
    topic = project.get("topic", "")
    countries = project.get("countries", []) or []
    queries = research_queries(project)
    category_rows = "\n".join(f"| {name} | {purpose} | P0/P1 |" for name, purpose in HIGH_VALUE_SOURCE_CATEGORIES)
    query_lines = "\n".join(f"- `{q}`" for q in queries)
    countries_text = ", ".join(countries) if countries else "Global / TBD"
    return f"""# Research Plan — {topic}

## Scope

- Topic: **{topic}**
- Type: **{project.get('kb_type', 'Mixed')}**
- Countries: **{countries_text}**
- Primary language: **{project.get('language', 'ko')}**

## Source-of-Truth map

| Category | What to find | Priority |
|---|---|---|
{category_rows}

## Discovery queries

{query_lines}

## Acceptance criteria

1. 핵심 사실은 가능한 한 Tier 1 공식 원문으로 확인합니다.
2. Draft / Consultation / Final / Effective / Superseded 상태를 구분합니다.
3. 문서 제목, 발행기관, 발행일, 버전, 시행일, 관할범위, 원문 URL을 기록합니다.
4. Google Search grounding으로 발견된 URL은 **Candidate Source**이며 자동으로 `Confirmed`가 되지 않습니다.
5. 공식 원문 확인 후에만 공개 저장소 `data/source-registry.yaml`로 승격합니다.
6. 원문은 비공개 `<공개 저장소명>-dev/sources/`에 보관하고 `data/source-archive.yaml`에 Source ID·버전·수집 시각·SHA-256을 기록합니다. 공개 사이트에는 원문 공식 URL 링크만 제공합니다.

## Seed target

- 공식 핵심 Source: 10~20건
- 핵심 기관: 5~10개
- 초기 Knowledge Note: 10~20개
- 비교/Timeline 문서: 최소 1개씩
"""


def write_research_plan(root: Path) -> Path:
    root = root.resolve()
    project = load_project(root)
    path = development_root(root) / "project" / "research-plan.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_research_plan(project), encoding="utf-8")
    return path


def _access_token() -> str:
    token = os.environ.get("GOOGLE_OAUTH_ACCESS_TOKEN", "").strip()
    if token:
        return token
    if not shutil.which("gcloud"):
        raise RuntimeError("gcloud not found and GOOGLE_OAUTH_ACCESS_TOKEN is not set")
    proc = subprocess.run(
        ["gcloud", "auth", "print-access-token"],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        raise RuntimeError(proc.stderr.strip() or "unable to obtain Google Cloud access token")
    return proc.stdout.strip()


def extract_grounding(response: dict[str, Any], max_sources: int = 20) -> tuple[str, list[str], list[dict[str, str]]]:
    candidates = response.get("candidates") or []
    if not candidates:
        return "", [], []
    candidate = candidates[0]
    parts = ((candidate.get("content") or {}).get("parts") or [])
    text = "\n".join(str(part.get("text", "")) for part in parts if part.get("text"))
    metadata = candidate.get("groundingMetadata") or {}
    queries = [str(q) for q in metadata.get("webSearchQueries", [])]
    sources: list[dict[str, str]] = []
    seen: set[str] = set()
    for chunk in metadata.get("groundingChunks", []):
        web = (chunk or {}).get("web") or {}
        uri = str(web.get("uri", "")).strip()
        if not uri or uri in seen:
            continue
        seen.add(uri)
        sources.append({
            "uri": uri,
            "title": str(web.get("title", "")).strip(),
            "domain": str(web.get("domain", "")).strip(),
        })
        if len(sources) >= max_sources:
            break
    return text, queries, sources


def vertex_grounded_research(
    root: Path,
    gcp_project: str,
    location: str = "us-central1",
    model: str = "gemini-2.5-flash",
    max_sources: int = 20,
) -> dict[str, Any]:
    root = root.resolve()
    project = load_project(root)
    write_research_plan(root)
    topic = project.get("topic", "")
    countries = project.get("countries", []) or []
    kb_type = project.get("kb_type", "Mixed")
    prompt = f"""You are doing source discovery for a professional Knowledge Base.
Topic: {topic}
Knowledge-base type: {kb_type}
Countries/jurisdictions: {', '.join(countries) if countries else 'global'}

Use Google Search and prioritize PRIMARY OFFICIAL SOURCES: government, regulators, system/market operators, standards bodies, public research institutes and official datasets. Identify the most important current source documents or official pages needed to build this knowledge base. Prefer current/final documents, but explicitly identify draft/consultation status where relevant. Focus on document title, issuing organization, jurisdiction, publication/effective/version information if visible, and why it matters. Do not invent missing details. Avoid general blogs and SEO summaries when an official source exists.
"""
    token = _access_token()
    if location == "global":
        host = "aiplatform.googleapis.com"
    else:
        host = f"{location}-aiplatform.googleapis.com"
    url = (
        f"https://{host}/v1/projects/{gcp_project}/locations/{location}/"
        f"publishers/google/models/{model}:generateContent"
    )
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "tools": [{"googleSearch": {}}],
        "generationConfig": {"temperature": 0.1},
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            response = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Vertex AI request failed ({exc.code}): {detail[:1200]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Vertex AI request failed: {exc}") from exc

    answer, queries, sources = extract_grounding(response, max_sources=max_sources)
    today = date.today().isoformat()
    candidate_payload = {
        "version": 1,
        "topic": topic,
        "provider": "vertex-google-search-grounding",
        "model": model,
        "location": location,
        "discovered_at": today,
        "queries": queries,
        "sources": [
            {
                "id": f"CAND-{idx:03d}",
                "title": item["title"],
                "url": item["uri"],
                "domain": item["domain"],
                "status": "candidate",
                "evidence_level": "Unverified",
            }
            for idx, item in enumerate(sources, start=1)
        ],
    }
    candidate_file = development_root(root) / "data" / "source-candidates.json"
    candidate_file.parent.mkdir(parents=True, exist_ok=True)
    candidate_file.write_text(json.dumps(candidate_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    rows = "\n".join(
        f"| CAND-{idx:03d} | {item['title'].replace('|', '/')} | {item['domain']} | {item['uri']} | Unverified |"
        for idx, item in enumerate(sources, start=1)
    ) or "| - | No grounded web source returned | - | - | - |"
    result_file = development_root(root) / "project" / "research-results.md"
    result_file.parent.mkdir(parents=True, exist_ok=True)
    result_file.write_text(
        f"""# Grounded Research Results — {topic}

> [!warning]
> 아래 항목은 Google Search grounding으로 발견한 **Candidate Source**입니다. 공식성·문서 버전·시행상태를 직접 확인하기 전에는 Confirmed 근거로 사용하지 마십시오.

## Model synthesis

{answer or 'No model synthesis returned.'}

## Search queries used

{chr(10).join(f'- `{q}`' for q in queries) if queries else '- Not returned'}

## Candidate sources

| ID | Title | Domain | URL | Evidence |
|---|---|---|---|---|
{rows}

## Next action

1. 공식 기관/원문 여부 확인
2. 버전·발행일·시행일·Draft/Final 상태 확인
3. 확인 완료된 항목만 `data/source-registry.yaml`로 승격
4. Knowledge Note에 `source_ids` 연결
5. `kbgen audit`로 근거 품질 재검사
""",
        encoding="utf-8",
    )
    return {
        "research_plan": str(development_root(root) / "project" / "research-plan.md"),
        "research_results": str(result_file),
        "source_candidates": str(candidate_file),
        "source_count": len(sources),
        "queries": queries,
    }


def _frontmatter_block(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---", 4)
    return text[4:end] if end >= 0 else ""


def _frontmatter_value(block: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.*)$", block, re.M)
    return match.group(1).strip().strip('"').strip("'") if match else ""


def audit_evidence(root: Path, output: Path | None = None) -> dict[str, Any]:
    root = root.resolve()
    notes: list[Path] = []
    for folder in (root / "content", root / "hubs"):
        if folder.exists():
            notes.extend(folder.rglob("*.md"))
    home = root / "HOME.md"
    if home.exists():
        notes.append(home)

    evidence = Counter()
    missing_frontmatter: list[str] = []
    unverified: list[str] = []
    missing_sources: list[str] = []
    missing_verified: list[str] = []
    for path in sorted(set(notes)):
        text = path.read_text(encoding="utf-8")
        block = _frontmatter_block(text)
        rel = str(path.relative_to(root))
        if not block:
            missing_frontmatter.append(rel)
            continue
        level = _frontmatter_value(block, "evidence_level") or "MISSING"
        note_type = _frontmatter_value(block, "type")
        evidence[level] += 1
        if level == "Unverified":
            unverified.append(rel)
        source_match = re.search(r"^source_ids:\s*(.*)$", block, re.M)
        source_inline = source_match.group(1).strip() if source_match else ""
        has_source = bool(source_inline and source_inline not in {"[]", "null"}) or bool(
            re.search(r"^source_ids:\s*\n\s+-\s+\S+", block, re.M)
        )
        if note_type not in {"hub", "glossary"} and not has_source:
            missing_sources.append(rel)
        if note_type not in {"hub", "glossary"} and not _frontmatter_value(block, "last_verified"):
            missing_verified.append(rel)

    report_path = (output or development_root(root) / "project" / "evidence-audit.md").resolve()
    report_path.parent.mkdir(parents=True, exist_ok=True)
    evidence_rows = "\n".join(f"| {key} | {value} |" for key, value in sorted(evidence.items())) or "| - | 0 |"
    def bullets(items: list[str]) -> str:
        return "\n".join(f"- `{item}`" for item in items) if items else "- None"
    report_path.write_text(
        f"""# Evidence Audit

Generated: {date.today().isoformat()}

## Summary

- Knowledge notes scanned: **{len(notes)}**
- Missing frontmatter: **{len(missing_frontmatter)}**
- Unverified notes: **{len(unverified)}**
- Notes without source IDs: **{len(missing_sources)}**
- Notes without last_verified: **{len(missing_verified)}**

## Evidence levels

| Level | Count |
|---|---:|
{evidence_rows}

## Missing frontmatter

{bullets(missing_frontmatter)}

## Unverified

{bullets(unverified)}

## Missing source IDs

{bullets(missing_sources)}

## Missing last_verified

{bullets(missing_verified)}

## Interpretation

이 보고서는 metadata 품질 감사입니다. 실제 출처가 해당 주장을 입증하는지 여부는 Source Hunter/Evidence Auditor의 원문 검토가 추가로 필요합니다.
""",
        encoding="utf-8",
    )
    return {
        "report": str(report_path),
        "notes": len(notes),
        "missing_frontmatter": len(missing_frontmatter),
        "unverified": len(unverified),
        "missing_sources": len(missing_sources),
        "missing_verified": len(missing_verified),
    }


def doctor(root: Path) -> dict[str, Any]:
    root = root.resolve()
    required = [
        "README.md", "HOME.md", "project.yaml", "content", "hubs", "templates",
        "schemas", "taxonomy", "data/source-registry.yaml", "source-policy.md", "scripts/validate_kb.py",
    ]
    missing = [item for item in required if not (root / item).exists()]
    dev = development_root(root)
    missing.extend(f"{dev.name}/{item}" for item in (
        "repository.json", "sources", "data/source-archive.yaml", "project/roadmap.md", "project/evidence-gaps.md"
    ) if not (dev / item).exists())
    validator = root / "scripts" / "validate_kb.py"
    validation_code: int | None = None
    validation_output = ""
    if validator.exists():
        proc = subprocess.run(
            [sys.executable, str(validator), str(root)],
            check=False,
            capture_output=True,
            text=True,
        )
        validation_code = proc.returncode
        validation_output = (proc.stdout + proc.stderr).strip()
    status = "ok" if not missing and validation_code in {0, None} else "needs-attention"
    return {
        "status": status,
        "root": str(root),
        "missing": missing,
        "validator_exit_code": validation_code,
        "validator_output": validation_output,
    }


def github_bootstrap_plan(root: Path, owner: str | None = None, private: bool | None = None) -> dict[str, Any]:
    root = root.resolve()
    project = load_project(root)
    if private is True or project.get("public") is False:
        raise RuntimeError("Every KB requires public <name> and private <name>-dev repositories; remove --private and migrate legacy project.yaml")
    dev = development_root(root)
    if not (dev / "repository.json").exists():
        raise RuntimeError(f"required development scaffold missing: {dev}; generate the repository pair first")
    repositories = []
    commands = []
    for directory, is_private in ((dev, True), (root, False)):
        target = f"{owner or '<OWNER>'}/{directory.name}"
        visibility = "--private" if is_private else "--public"
        repo_commands = [
            f"git -C \"{directory}\" init -b main  # only for a new checkout",
            f"git -C \"{directory}\" add .",
            f'git -C "{directory}" commit -m "chore: initialize generated knowledge base"',
            f'gh repo create {target} {visibility} --source="{directory}" --remote=origin --push',
        ]
        repositories.append({"target": target, "private": is_private, "root": str(directory), "commands": repo_commands})
        commands.extend(repo_commands)
    return {"target": f"{owner or '<OWNER>'}/{root.name}", "private": False, "repositories": repositories, "commands": commands}


def _existing_origin(directory: Path, target: str, private: bool) -> bool:
    if not (directory / ".git").exists():
        return False
    remote = subprocess.run(["git", "remote", "get-url", "origin"], cwd=directory, capture_output=True, text=True)
    if remote.returncode != 0 or not remote.stdout.strip():
        return False
    allowed = {f"https://github.com/{target}", f"https://github.com/{target}.git", f"git@github.com:{target}.git", f"ssh://git@github.com/{target}.git"}
    push_remote = subprocess.run(["git", "remote", "get-url", "--push", "--all", "origin"], cwd=directory, capture_output=True, text=True, check=True)
    if remote.stdout.strip() not in allowed or any(url not in allowed for url in push_remote.stdout.splitlines()):
        raise RuntimeError(f"origin must point only to {target}: {directory}")
    metadata = subprocess.run(["gh", "repo", "view", target, "--json", "nameWithOwner,isPrivate"], capture_output=True, text=True, check=True)
    actual = json.loads(metadata.stdout)
    if actual["nameWithOwner"].lower() != target.lower() or actual["isPrivate"] != private:
        raise RuntimeError(f"repository name/visibility mismatch for {target}; expected {'private' if private else 'public'}")
    return True


def execute_github_bootstrap(root: Path, owner: str | None = None, private: bool | None = None) -> dict[str, Any]:
    root = root.resolve()
    if not shutil.which("git") or not shutil.which("gh"):
        raise RuntimeError("git and GitHub CLI (gh) are required")
    if owner is None:
        proc = subprocess.run(["gh", "api", "user", "--jq", ".login"], cwd=root, capture_output=True, text=True)
        if proc.returncode != 0 or not proc.stdout.strip():
            raise RuntimeError("unable to infer GitHub owner; pass --owner")
        owner = proc.stdout.strip()
    plan = github_bootstrap_plan(root, owner=owner, private=private)
    # Validate both destinations before staging or pushing either repository.
    origins = [_existing_origin(Path(repo["root"]), repo["target"], repo["private"]) for repo in plan["repositories"]]
    forbidden = ["sources", "project", "gcp", "data/source-archive.yaml", "data/source-candidates.json"]
    if any((root / path).exists() for path in forbidden):
        raise RuntimeError("move original sources and development records to the private -dev repository before publishing")
    if (root / ".git").exists():
        history = subprocess.run(["git", "log", "--all", "--format=%H", "--", *forbidden], cwd=root, capture_output=True, text=True, check=True)
        if history.stdout.strip():
            raise RuntimeError("development files exist in public Git history; use a clean public checkout before publishing")
    for repo, has_origin in zip(plan["repositories"], origins):
        directory = Path(repo["root"])
        if not (directory / ".git").exists():
            subprocess.run(["git", "init", "-b", "main"], cwd=directory, check=True)
        subprocess.run(["git", "add", "."], cwd=directory, check=True)
        has_head = subprocess.run(["git", "rev-parse", "--verify", "HEAD"], cwd=directory, capture_output=True).returncode == 0
        staged = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=directory).returncode != 0
        if staged:
            subprocess.run(["git", "-c", "user.name=Knowledge Base Generator", "-c", "user.email=kbgen@users.noreply.github.com", "commit", "-m", "chore: initialize generated knowledge base"], cwd=directory, check=True)
        elif not has_head:
            raise RuntimeError(f"no files available to create initial commit: {directory}")
        if has_origin:
            subprocess.run(["git", "push", "-u", "origin", "main"], cwd=directory, check=True)
        else:
            subprocess.run(["gh", "repo", "create", repo["target"], "--private" if repo["private"] else "--public", "--source=.", "--remote=origin", "--push"], cwd=directory, check=True)
    plan["result"] = "Created/pushed public and private development repositories"
    return plan
