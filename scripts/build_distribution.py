"""Package the checked-out Firmory plugin for one release environment."""

import argparse
import json
import re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_PATH = 'plugins/ask-firmory'
PLUGIN = ROOT / PLUGIN_PATH
ENDPOINTS = {
    'preview': 'https://preview.firmory.ai/mcp',
    'production': 'https://firmory.ai/mcp',
}
CATALOGS = ('.agents/plugins/marketplace.json', '.claude-plugin/marketplace.json')


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


def read_json(path):
    return json.loads((PLUGIN / path).read_text(encoding='utf-8'))


def archive(path, files):
    with ZipFile(path, 'w') as output:
        for name, data in sorted(files.items()):
            entry = ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            output.writestr(entry, data, compress_type=ZIP_DEFLATED)
    print(path)


def build(env, release_version, destination):
    portable = read_json('plugin.json')
    claude = read_json('.claude-plugin/plugin.json')
    if (portable['name'], portable['version']) != (claude['name'], claude['version']):
        raise ValueError('Plugin IDs and versions must match across clients')
    if env == 'production':
        if not re.fullmatch(r'(?:0|[1-9][0-9]*)(?:\.(?:0|[1-9][0-9]*)){2}', release_version or ''):
            raise ValueError('Production requires --release-version MAJOR.MINOR.PATCH')
        portable['version'] = claude['version'] = release_version
    elif release_version is not None:
        raise ValueError('Preview uses the version in plugin.json')

    configs = {}
    for path, transport in [('mcp.json', 'streamable-http'), ('.mcp.json', 'http')]:
        config = read_json(path)
        # The marketplace on main must always install the preview server directly.
        if config['mcpServers'] != {'firmory_cloud': {'type': transport, 'url': ENDPOINTS['preview']}}:
            raise ValueError(f'Unexpected development server in {path}')
        config['mcpServers']['firmory_cloud']['url'] = ENDPOINTS[env]
        configs[path] = config

    common = {name: (PLUGIN / name).read_bytes() for name in (
        'assets/logo-blue.png', 'assets/composer-blue.png', 'README.md',
        'skills/firmory/SKILL.md', 'skills/setup/SKILL.md',
    )}
    if (PLUGIN / 'LICENSE').is_file():
        common['LICENSE'] = (PLUGIN / 'LICENSE').read_bytes()
    common['plugin.json'] = json_bytes(portable)
    runtime = {**common, 'mcp.json': json_bytes(configs['mcp.json']),
               '.mcp.json': json_bytes(configs['.mcp.json']),
               '.claude-plugin/plugin.json': json_bytes(claude),
               '.claude-plugin/icon.png': (PLUGIN / '.claude-plugin/icon.png').read_bytes()}
    marketplace = {f'{PLUGIN_PATH}/{k}': v for k, v in runtime.items()}
    marketplace.update({k: (ROOT / k).read_bytes() for k in CATALOGS})
    marketplace['README.md'] = common['README.md']
    # The upload accepts OAuth metadata that the Codex marketplace loader rejects.
    configs['mcp.json']['mcpServers']['firmory_cloud']['extensions'] = {'com.openai': {'auth': {'type': 'oauth'}}}
    upload = {**common, 'mcp.json': json_bytes(configs['mcp.json'])}
    if env == 'production':
        for name, data in {**marketplace, **upload}.items():
            if not name.endswith('.png') and any(x in data.lower() for x in (b'preview.firmory.ai', b'clerk.accounts.dev')):
                raise ValueError(f'Development host found in {name}')
    destination.mkdir(parents=True, exist_ok=True)
    prefix = f"firmory-{portable['version']}-{env}"
    archive(destination / f'{prefix}-openai.zip', upload)
    archive(destination / f'{prefix}-marketplace.zip', marketplace)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--env', choices=ENDPOINTS, default='preview')
    parser.add_argument('--release-version')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'dist')
    args = parser.parse_args()
    try:
        build(args.env, args.release_version, args.output_dir)
    except ValueError as error:
        parser.error(str(error))
