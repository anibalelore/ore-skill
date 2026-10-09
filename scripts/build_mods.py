#!/usr/bin/env python3
"""Build self-contained optional runtime plugins from auditable local sources."""
from pathlib import Path
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/ore/scripts'))
from ore_runtime import MODULES
NATIVE_MODS = {'ore-cost-controller', 'ore-context-sentinel', 'ore-project-router'}


def template(name):
    return 'native.ts' if name in NATIVE_MODS else 'worktree.ts' if name == 'ore-worktree-manager' else 'register.ts'


def main():
    version = json.loads((ROOT / 'plugin.json').read_text(encoding='utf-8'))['version']
    for name in sorted(MODULES):
        folder = ROOT / 'mods' / name
        for part in ('.claude-plugin', 'hooks', 'scripts'):
            (folder / part).mkdir(parents=True, exist_ok=True)
        manifest = {'name': name, 'version': version, 'description': f'Optional ORE runtime adapter: {name}; see capability matrix for limits', 'author': {'name': 'anibalelore'}}
        (folder / '.claude-plugin/plugin.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
        (folder / 'hooks/hooks.json').write_text('{"modules": ["./register.ts"]}\n', encoding='utf-8')
        shutil.copyfile(ROOT / 'mods/sdk' / template(name), folder / 'hooks/register.ts')
        shutil.copyfile(ROOT / 'mods/ore-progress/hooks/state.ts', folder / 'hooks/state.ts')
        (folder / 'hooks/identity.ts').write_text(f"export const NAME: string = '{name}';\n", encoding='utf-8')
        shutil.copyfile(ROOT / 'mods/ore-progress/tsconfig.json', folder / 'tsconfig.json')
        for script in ('ore_state.py', 'ore_runtime.py', 'ore_first_contact.py', 'ore_flow.py', 'ore_regulatory.py'):
            target = folder / 'scripts' / script
            if name in NATIVE_MODS or name == 'ore-worktree-manager':
                if target.exists():
                    target.unlink()
            else:
                shutil.copyfile(ROOT / 'skills/ore/scripts' / script, target)
        if name not in NATIVE_MODS and name != 'ore-worktree-manager':
            shutil.copyfile(ROOT / 'skills/ore/requirements.txt', folder / 'requirements.txt')
    marketplace = ROOT / 'mods/.claude-plugin/marketplace.json'
    data = json.loads(marketplace.read_text(encoding='utf-8'))
    data['plugins'] = [{'name': folder.name, 'source': f'./{folder.name}', 'version': version,
                        'description': json.loads((folder / '.claude-plugin/plugin.json').read_text(encoding='utf-8'))['description']}
                       for folder in sorted((ROOT / 'mods').glob('ore-*')) if folder.is_dir()]
    marketplace.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    print(f'Built {len(MODULES)} runtime adapters')


if __name__ == '__main__':
    main()
