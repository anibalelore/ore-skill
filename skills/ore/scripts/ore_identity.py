#!/usr/bin/env python3
"""ORE Developer Identity: local profiles and conservative read-only identity audit."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys
import tempfile

FIRST_USE = 'Antes de comenzar, ¿cómo te llamas? Usaré tu nombre como desarrollador responsable de los proyectos en los que trabajemos.'
FIELDS = {'name', 'professional_name', 'email', 'website', 'team'}
MARK = re.compile(r'(?:generated (?:by|with)|created by|powered by|built with|developed by|co-authored-by:)\s*(?:Claude(?: AI)?|ChatGPT|Codex|Anthropic|OpenAI|Gemini)\b|made (?:with|by)\s*(?:AI|ChatGPT)\b|AI generated code\b', re.I)
SKIP = {'.git', '.ore', 'node_modules', 'vendor', '.venv', 'venv', '__pycache__', 'dist', 'build'}
EXTENSIONS = {'.md', '.txt', '.json', '.yaml', '.yml', '.toml', '.html', '.css', '.js', '.jsx', '.ts', '.tsx', '.py', '.sh', '.ps1', '.vue', '.svelte', '.xml', '.kt', '.swift', '.dart', '.java', '.go', '.rs', '.c', '.cpp', '.h'}


def global_path():
    """Independent of assistant installation; override supports portable hosts/tests."""
    if os.environ.get('ORE_IDENTITY_HOME'):
        return Path(os.environ['ORE_IDENTITY_HOME']) / 'identity.json'
    base = Path(os.environ.get('LOCALAPPDATA') or os.environ.get('XDG_CONFIG_HOME') or Path.home() / '.config')
    return base / 'ore' / 'identity.json'


def validate(data):
    if not isinstance(data, dict) or data.get('schema_version') != 1:
        raise ValueError('Unsupported identity schema')
    profiles = data.get('developers')
    if not isinstance(profiles, list) or not profiles:
        raise ValueError('At least one developer is required')
    for profile in profiles:
        if not isinstance(profile, dict) or set(profile) - FIELDS:
            raise ValueError('Unknown identity field')
        if not isinstance(profile.get('name'), str) or not profile['name'].strip():
            raise ValueError('Developer name is required')
        if any(not isinstance(v, str) or not v.strip() or any(ord(c) < 32 for c in v) for v in profile.values()):
            raise ValueError('Identity fields must contain nonempty single-line text')
    return data


def read(path):
    if path.is_symlink():
        raise ValueError('Identity configuration must not be a symlink')
    return validate(json.loads(path.read_text(encoding='utf-8'))) if path.exists() else None


def effective(repo, global_file=None):
    project = repo / '.ore' / 'identity.json'
    if project.resolve().is_relative_to(repo.resolve()) is False:
        raise ValueError('Project identity resolves outside repository')
    local = read(project)
    if local:
        return {'source': 'project', 'identity': local}
    shared = read(global_file or global_path())
    return {'source': 'global' if shared else None, 'identity': shared,
            **({'prompt': FIRST_USE} if shared is None else {})}


def write(path, data):
    validate(data)
    if path.is_symlink():
        raise ValueError('Identity configuration must not be a symlink')
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.identity-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            json.dump(data, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def classify(path, line):
    lower = line.lower()
    parts = {p.lower() for p in path.parts}
    if any(re.search(r'license|notice|copyright|attribution', p, re.I) for p in path.parts) or re.search(r'copyright|license|legally|required attribution|contractual', lower):
        return 'protected-attribution'
    if parts & {'audit', 'audits', 'history', 'logs', 'changelog', 'provenance'} or path.name.lower().startswith('changelog') or 'co-authored-by:' in lower:
        return 'historical-or-audit'
    if re.search(r'\b(sdk|endpoint|api|provider|dependency|dependencies|import|require|model)\b', lower):
        return 'technical-reference'
    # Only a standalone banner is a removable candidate; code/JSON/prose require context.
    bare = re.sub(r'^(?:\s|#|/|\*|<!--)+|(?:\s|\*|-->|/)+$', '', line)
    if MARK.fullmatch(bare):
        return 'removable-promotion'
    return 'human-review'


def audit(repo, paths=None, global_file=None):
    repo = repo.resolve()
    findings, skipped = [], []
    def repository_files():
        for directory, subdirs, names in os.walk(repo, followlinks=False):
            subdirs[:] = [d for d in subdirs if d not in SKIP and not (Path(directory) / d).is_symlink()]
            for name in names:
                yield Path(directory) / name
    files = [repo / p for p in paths] if paths is not None else repository_files()
    for path in files:
        resolved = path.resolve()
        if not resolved.is_relative_to(repo):
            raise ValueError('Audit path resolves outside repository')
        relative = path.relative_to(repo)
        if path.is_symlink() or set(relative.parts) & SKIP:
            continue
        if not path.is_file():
            if paths is not None:
                skipped.append({'path': str(relative), 'reason': 'not a regular file'})
            continue
        if path.suffix.lower() not in EXTENSIONS and not re.search(r'license|notice|readme', path.name, re.I):
            continue
        if path.stat().st_size > 2_000_000:
            skipped.append({'path': str(relative), 'reason': 'size limit'})
            continue
        try:
            content = path.read_text(encoding='utf-8')
        except (UnicodeError, OSError):
            skipped.append({'path': str(relative), 'reason': 'unreadable UTF-8'})
            continue
        for number, line in enumerate(content.splitlines(), 1):
            if MARK.search(line):
                findings.append({'path': relative.as_posix(), 'line': number, 'category': classify(relative, line),
                                 'automatic_change': False})
    identity = effective(repo, global_file)
    return {'control': 'ORE Identity Audit', 'scope': 'incremental' if paths is not None else 'repository',
            'identity_configured': identity['identity'] is not None, 'identity_source': identity['source'],
            'findings': findings, 'skipped': skipped, 'read_only': True,
            'manual_checks': ['appropriate new metadata', 'UI attribution context', 'third-party credits preserved',
                              'technical documentation correct', 'authorship and audit records intact'],
            'status': 'review-required' if findings or skipped or identity['identity'] is None else 'context-review-required'}


def main():
    # Machine-readable output must be UTF-8 even under Windows legacy code pages.
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['show', 'change', 'project', 'remove', 'audit'])
    parser.add_argument('--repo', type=Path, default=Path.cwd())
    parser.add_argument('--scope', choices=['global', 'project'], default='global')
    parser.add_argument('--name')
    parser.add_argument('--professional-name')
    parser.add_argument('--email')
    parser.add_argument('--website')
    parser.add_argument('--team')
    parser.add_argument('--additional-developer', action='append', default=[], help='JSON developer object')
    parser.add_argument('--path', action='append', help='Repeat for incremental audit; relative file paths')
    args = parser.parse_args()
    try:
        repo = args.repo.resolve()
        if not repo.is_dir():
            raise ValueError('Repository directory does not exist')
        target = repo / '.ore' / 'identity.json' if args.command == 'project' or args.scope == 'project' else global_path()
        if args.command == 'show':
            result = effective(repo)
        elif args.command == 'audit':
            result = audit(repo, args.path)
        elif args.command == 'remove':
            if target.is_symlink() or args.scope == 'project' and not target.resolve().is_relative_to(repo):
                raise ValueError('Unsafe configuration path')
            target.unlink(missing_ok=True)
            result = {'removed_scope': args.scope}
        else:
            if (args.command == 'project' or args.scope == 'project') and not target.resolve().is_relative_to(repo):
                raise ValueError('Unsafe configuration path')
            profile = {key: getattr(args, key) for key in FIELDS if getattr(args, key) is not None}
            data = {'schema_version': 1, 'developers': [profile] + [json.loads(v) for v in args.additional_developer]}
            write(target, data)
            result = {'saved_scope': 'project' if args.command == 'project' or args.scope == 'project' else 'global'}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError) as exc:
        parser.exit(2, f'ORE identity error: {exc}\n')


if __name__ == '__main__':
    raise SystemExit(main())
