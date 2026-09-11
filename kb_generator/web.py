from __future__ import annotations

import argparse
import html
import io
import os
import re
import tempfile
import zipfile
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs

from .cli import ProjectSpec, generate, infer_type, project_name, slugify

FORM = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Knowledge Base Generator</title>
<style>
body{font-family:system-ui,-apple-system,sans-serif;max-width:760px;margin:40px auto;padding:0 20px;line-height:1.5}
form{display:grid;gap:14px;padding:24px;border:1px solid #8885;border-radius:14px}
label{display:grid;gap:6px;font-weight:600} input,select{font:inherit;padding:10px;border:1px solid #8888;border-radius:8px}
button{font:inherit;padding:12px;border:0;border-radius:9px;font-weight:700;cursor:pointer} small{opacity:.75}
code{background:#8882;padding:2px 5px;border-radius:4px}
</style>
</head>
<body>
<h1>Knowledge Base Generator</h1>
<p>주제 한 줄로 공개 Knowledge Base와 비공개 개발 저장소(-dev) 두 폴더를 생성합니다.</p>
<form method="post" action="/generate">
<label>주제 <input name="topic" required placeholder="예: 해상풍력, HVDC, 수소산업"></label>
<label>프로젝트명 <input name="name" placeholder="비우면 자동 생성"></label>
<label>Slug <input name="slug" placeholder="비우면 자동 추론"></label>
<label>국가 범위 <input name="countries" value="KR" placeholder="KR AU US"></label>
<label>사이트 엔진 <select name="site"><option>quartz</option><option>mkdocs</option><option>docusaurus</option><option>none</option></select></label>
<label>GCP Level <select name="gcp_level"><option value="0">0 — GitHub/Obsidian only</option><option value="1" selected>1 — Minimal</option><option value="2">2 — Automated Research</option><option value="3">3 — AI/RAG</option></select></label>
<label>언어 <input name="language" value="ko"></label>
<button type="submit">Knowledge Base ZIP 생성</button>
</form>
<p><small>공개 사이트는 원문 링크만 제공하며 원문 파일은 비공개 개발 저장소에 보관합니다. ZIP에는 두 저장소 폴더와 Obsidian Hub/MOC, schema, taxonomy, source registry, roadmap, evidence gaps, GCP manifest, GitHub Actions validator가 포함됩니다.</small></p>
</body></html>"""


def split_countries(raw: str) -> list[str]:
    return [x.upper() for x in re.split(r"[,\s]+", raw.strip()) if x]


def spec_from_form(form: dict[str, list[str]]) -> ProjectSpec:
    def value(key: str, default: str = "") -> str:
        return form.get(key, [default])[0].strip()

    topic = value("topic")
    if not topic:
        raise ValueError("topic is required")
    slug = value("slug") or slugify(topic)
    level = int(value("gcp_level", "1"))
    if level not in {0, 1, 2, 3}:
        raise ValueError("gcp_level must be 0..3")
    site = value("site", "quartz")
    if site not in {"quartz", "mkdocs", "docusaurus", "none"}:
        raise ValueError("invalid site")
    countries = split_countries(value("countries", "KR")) or ["KR"]
    return ProjectSpec(
        topic=topic,
        name=value("name") or project_name(topic),
        slug=slug,
        kb_type=infer_type(topic),
        language=value("language", "ko") or "ko",
        countries=countries,
        site=site,
        gcp_level=level,
        public=True,
        created=date.today().isoformat(),
    )


def zip_project(spec: ProjectSpec) -> bytes:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / f"{spec.slug}-knowledge-base"
        generate(spec, root)
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for path in sorted(Path(td).rglob("*")):
                if path.is_file():
                    zf.write(path, path.relative_to(root.parent))
        return buffer.getvalue()


class Handler(BaseHTTPRequestHandler):
    server_version = "KBGenerator/0.2"

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/healthz":
            self._send(200, b"ok\n", "text/plain; charset=utf-8")
            return
        if self.path != "/":
            self._send(404, b"not found\n", "text/plain; charset=utf-8")
            return
        self._send(200, FORM.encode("utf-8"), "text/html; charset=utf-8")

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/generate":
            self._send(404, b"not found\n", "text/plain; charset=utf-8")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 64 * 1024:
                raise ValueError("request too large")
            form = parse_qs(self.rfile.read(length).decode("utf-8"), keep_blank_values=True)
            spec = spec_from_form(form)
            payload = zip_project(spec)
        except Exception as exc:
            message = f"<h1>Generation failed</h1><p>{html.escape(str(exc))}</p><p><a href='/'>Back</a></p>"
            self._send(400, message.encode("utf-8"), "text/html; charset=utf-8")
            return
        self.send_response(200)
        self.send_header("Content-Type", "application/zip")
        self.send_header("Content-Disposition", f'attachment; filename="{spec.slug}-knowledge-base.zip"')
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, fmt: str, *args: object) -> None:
        print(f"{self.address_string()} - {fmt % args}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Knowledge Base Generator web UI")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "8080")))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Knowledge Base Generator: http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
