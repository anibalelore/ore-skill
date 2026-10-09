#!/usr/bin/env python3
"""Validate, typecheck and launch native status commands for each local mod."""
import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--claude', default='claude')
    parser.add_argument('--tsc', default='tsc')
    args = parser.parse_args()
    failures = []
    for folder in sorted((ROOT / 'mods').glob('ore-*')):
        if not folder.is_dir():
            continue
        calls = [('manifest', [args.claude, 'plugin', 'validate', str(folder)]),
                 ('types', [args.tsc, '-p', str(folder), '--noEmit']),
                 ('launch', [args.claude, '--plugin-dir', str(folder), '--no-session-persistence', '-p', f'/{folder.name}-status'])]
        for kind, argv in calls:
            try:
                result = subprocess.run(argv, capture_output=True, text=True, encoding='utf-8', timeout=30, cwd=ROOT)
                if result.returncode:
                    failures.append(f'{folder.name}/{kind}: {(result.stderr or result.stdout)[-1500:]}')
            except (OSError, subprocess.TimeoutExpired) as error:
                failures.append(f'{folder.name}/{kind}: {type(error).__name__}')
        print(f'{folder.name}: checked', flush=True)
    for failure in failures:
        print(failure, file=sys.stderr)
    print(f'Native validation finished: {len(failures)} failures')
    return int(bool(failures))


if __name__ == '__main__':
    raise SystemExit(main())
