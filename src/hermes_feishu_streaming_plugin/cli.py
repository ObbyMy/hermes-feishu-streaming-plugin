from __future__ import annotations

import argparse
import json
from pathlib import Path

from .bundle import bundle_manifest, export_bundle
from .installer import DEFAULT_VERIFY_TESTS, apply_bundle, verify_target_repo
from .locator import locate_bundle_targets, locator_manifest_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hermes-feishu-plugin")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("manifest", help="Print bundled file manifest as JSON")

    export_p = sub.add_parser("export", help="Export the bundled migration kit")
    export_p.add_argument("--output-dir", required=True)

    sub.add_parser("locators", help="Print the file locator manifest as JSON")

    locate_p = sub.add_parser("locate", help="Locate migration touchpoints inside a Hermes repo")
    locate_p.add_argument("--target", required=True)

    verify_p = sub.add_parser("verify", help="Run the focused Feishu regression tests in a Hermes repo")
    verify_p.add_argument("--target", required=True)
    verify_p.add_argument("--python", dest="python_bin")
    verify_p.add_argument("--test", dest="tests", action="append")

    apply_p = sub.add_parser("apply", help="Copy bundled files into a Hermes repo")
    apply_p.add_argument("--target", required=True)
    apply_p.add_argument("--dry-run", action="store_true")
    apply_p.add_argument("--verify", action="store_true")
    apply_p.add_argument("--python", dest="python_bin")
    apply_p.add_argument("--test", dest="tests", action="append")

    sub.add_parser("agent-handoff", help="Print the exact workflow another Hermes agent should follow")
    return parser


def _apply_result_payload(result, *, dry_run: bool) -> dict:
    payload = {
        'target': str(result.target),
        'files_copied': result.files_copied,
        'copied_paths': result.copied_paths,
        'dry_run': dry_run,
    }
    if result.verify is not None:
        payload['verify'] = {
            'command': result.verify.command,
            'returncode': result.verify.returncode,
            'passed': result.verify.passed,
            'stdout': result.verify.stdout,
            'stderr': result.verify.stderr,
        }
    return payload


def _verify_result_payload(result) -> dict:
    return {
        'command': result.command,
        'returncode': result.returncode,
        'passed': result.passed,
        'stdout': result.stdout,
        'stderr': result.stderr,
    }


def _agent_handoff_text() -> str:
    tests = " ".join(DEFAULT_VERIFY_TESTS)
    return (
        "# Hermes agent handoff\n\n"
        "If the user only gives you this repository URL, clone it and follow these steps exactly:\n\n"
        "1. Read `README.md` and `docs/feishu-restore-runbook.md`.\n"
        "2. Install the plugin in editable mode: `pip install -e .[dev]`.\n"
        "3. Run `python -m hermes_feishu_streaming_plugin locate --target /path/to/hermes-agent` to inspect the target repo.\n"
        "4. Run `python -m hermes_feishu_streaming_plugin apply --target /path/to/hermes-agent --verify --python /path/to/hermes-agent/venv/bin/python`.\n"
        f"5. Verification defaults to: `{tests}`.\n"
        "6. Report: files copied, locate summary, exact pytest result, and remaining risks.\n\n"
        "If the task also requires restoring a specific machine's live Feishu credentials/service config, ask for that machine's private restore bundle; it is intentionally not stored in git.\n"
    )


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == 'manifest':
        print(bundle_manifest().to_json())
        return 0
    if args.command == 'export':
        exported = export_bundle(Path(args.output_dir))
        print(str(exported))
        return 0
    if args.command == 'locators':
        print(locator_manifest_json())
        return 0
    if args.command == 'locate':
        print(locate_bundle_targets(Path(args.target)).to_json())
        return 0
    if args.command == 'verify':
        result = verify_target_repo(Path(args.target), python_bin=args.python_bin, tests=args.tests)
        print(json.dumps(_verify_result_payload(result), ensure_ascii=False, indent=2))
        return 0 if result.passed else 1
    if args.command == 'apply':
        result = apply_bundle(
            Path(args.target),
            dry_run=args.dry_run,
            verify=args.verify,
            python_bin=args.python_bin,
            tests=args.tests,
        )
        exit_code = 0 if result.verify is None or result.verify.passed else 1
        print(json.dumps(_apply_result_payload(result, dry_run=args.dry_run), ensure_ascii=False, indent=2))
        return exit_code
    if args.command == 'agent-handoff':
        print(_agent_handoff_text())
        return 0

    parser.error(f'Unknown command: {args.command}')
    return 2
