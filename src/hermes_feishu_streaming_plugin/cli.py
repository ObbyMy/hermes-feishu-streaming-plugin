from __future__ import annotations

import argparse
import json
from pathlib import Path

from .bundle import bundle_manifest, export_bundle
from .installer import apply_bundle


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hermes-feishu-plugin")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("manifest", help="Print bundled file manifest as JSON")

    export_p = sub.add_parser("export", help="Export the bundled migration kit")
    export_p.add_argument("--output-dir", required=True)

    apply_p = sub.add_parser("apply", help="Copy bundled files into a Hermes repo")
    apply_p.add_argument("--target", required=True)
    apply_p.add_argument("--dry-run", action="store_true")
    return parser


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
    if args.command == 'apply':
        result = apply_bundle(Path(args.target), dry_run=args.dry_run)
        print(json.dumps({
            'target': str(result.target),
            'files_copied': result.files_copied,
            'copied_paths': result.copied_paths,
            'dry_run': args.dry_run,
        }, ensure_ascii=False, indent=2))
        return 0

    parser.error(f'Unknown command: {args.command}')
    return 2
