from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable

from . import cli
from .ops import (
    audit_evidence,
    doctor,
    execute_github_bootstrap,
    github_bootstrap_plan,
    vertex_grounded_research,
    write_research_plan,
)

VERSION = "0.3.0"
COMMANDS = {"init", "research", "audit", "doctor", "github"}


def print_help() -> None:
    print(
        """Knowledge Base Generator

Usage:
  kbgen <topic> [init options]              Backward-compatible quick init
  kbgen init <topic> [init options]         Generate a new Knowledge Base
  kbgen research <root> [options]           Create research plan or grounded source discovery
  kbgen audit <root> [options]              Audit evidence metadata
  kbgen doctor <root>                       Validate generated Knowledge Base structure
  kbgen github <root> [options]             Plan or execute GitHub repository bootstrap

Examples:
  kbgen "해상풍력" --countries KR AU --gcp-level 2
  kbgen research ./offshore-wind-knowledge-base
  kbgen research ./offshore-wind-knowledge-base --provider vertex --gcp-project MY_PROJECT
  kbgen audit ./offshore-wind-knowledge-base
  kbgen doctor ./offshore-wind-knowledge-base
  kbgen github ./offshore-wind-knowledge-base --owner Uptec-khj
  kbgen github ./offshore-wind-knowledge-base --owner Uptec-khj --execute
"""
    )


def _research(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="kbgen research", description="Research planning and grounded source discovery")
    parser.add_argument("root", nargs="?", default=".", type=Path)
    parser.add_argument("--provider", choices=["plan", "vertex"], default="plan")
    parser.add_argument("--gcp-project")
    parser.add_argument("--location", default="us-central1")
    parser.add_argument("--model", default="gemini-2.5-flash")
    parser.add_argument("--max-sources", type=int, default=20)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.provider == "plan":
            path = write_research_plan(args.root)
            result = {"provider": "plan", "research_plan": str(path)}
        else:
            if not args.gcp_project:
                parser.error("--gcp-project is required with --provider vertex")
            result = vertex_grounded_research(
                args.root,
                gcp_project=args.gcp_project,
                location=args.location,
                model=args.model,
                max_sources=max(1, min(args.max_sources, 100)),
            )
            result["provider"] = "vertex"
    except (FileNotFoundError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Research provider: {result['provider']}")
        print(f"Research plan: {result.get('research_plan')}")
        if result.get("research_results"):
            print(f"Research results: {result['research_results']}")
            print(f"Candidate sources: {result.get('source_count', 0)}")
            print("Next: verify candidate sources before promoting them to source-registry.yaml")
    return 0


def _audit(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="kbgen audit", description="Audit Knowledge Base evidence metadata")
    parser.add_argument("root", nargs="?", default=".", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = audit_evidence(args.root, args.output)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Evidence audit: {result['report']}")
        print(
            "Notes: {notes} | Unverified: {unverified} | Missing sources: {missing_sources} | "
            "Missing last_verified: {missing_verified}".format(**result)
        )
    return 0


def _doctor(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="kbgen doctor", description="Check generated Knowledge Base health")
    parser.add_argument("root", nargs="?", default=".", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = doctor(args.root)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Status: {result['status']}")
        if result["missing"]:
            print("Missing:")
            for item in result["missing"]:
                print(f"- {item}")
        if result["validator_output"]:
            print(result["validator_output"])
    return 0 if result["status"] == "ok" else 1


def _github(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="kbgen github", description="Plan or execute GitHub repository bootstrap via gh CLI")
    parser.add_argument("root", nargs="?", default=".", type=Path)
    parser.add_argument("--owner")
    visibility = parser.add_mutually_exclusive_group()
    visibility.add_argument("--private", action="store_true")
    visibility.add_argument("--public", action="store_true")
    parser.add_argument("--execute", action="store_true", help="Actually run git/gh commands. Without this flag only print the plan.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    private: bool | None = True if args.private else False if args.public else None
    try:
        if args.execute:
            result = execute_github_bootstrap(args.root, owner=args.owner, private=private)
        else:
            result = github_bootstrap_plan(args.root, owner=args.owner, private=private)
    except (FileNotFoundError, RuntimeError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # subprocess CalledProcessError and platform-specific failures
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"GitHub target: {result['target']}")
        if args.execute:
            print(result.get("result", "GitHub bootstrap completed"))
        else:
            print("Dry run. Commands:")
            for command in result["commands"]:
                print(f"  {command}")
            print("Add --execute to run these operations.")
    return 0


def main(argv: Iterable[str] | None = None) -> int:
    args = list(argv) if argv is not None else sys.argv[1:]
    if not args or args[0] in {"-h", "--help"}:
        print_help()
        return 0
    if args[0] in {"-V", "--version"}:
        print(f"kbgen {VERSION}")
        return 0
    command = args[0]
    rest = args[1:]
    if command == "init":
        return cli.main(rest)
    if command == "research":
        return _research(rest)
    if command == "audit":
        return _audit(rest)
    if command == "doctor":
        return _doctor(rest)
    if command == "github":
        return _github(rest)
    # Backward compatibility: `kbgen "해상풍력" ...` behaves like init.
    return cli.main(args)


if __name__ == "__main__":
    raise SystemExit(main())
