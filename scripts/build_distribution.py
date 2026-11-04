"""Package the checked-out Firmory plugin for one release environment."""

import argparse
import json
import re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_PATH = 'plugins/firmory'
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


def build(env, release_version, destination, review_cases=None, demo_recording_url=None, public_only=False):
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
        if config['mcpServers'] != {'firmory_cloud': {'type': transport, 'url': ENDPOINTS['production']}}:
            raise ValueError(f'Unexpected production server in {path}')
        config['mcpServers']['firmory_cloud']['url'] = ENDPOINTS[env]
        configs[path] = config

    common = {name: (PLUGIN / name).read_bytes() for name in (
        'assets/icon.svg', 'assets/logo-blue.png', 'assets/composer-blue.png', 'README.md',
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
    distributions = {}
    for client, catalog in [('codex', CATALOGS[0]), ('claude-code', CATALOGS[1])]:
        files = {k: v for k, v in marketplace.items() if k not in CATALOGS or k == catalog}
        files['README.md'] = (ROOT / f'docs/install-{client}.md').read_bytes()
        distributions[client] = {f'firmory-{client}/{k}': v for k, v in files.items()}
    # The upload accepts OAuth metadata that the Codex marketplace loader rejects.
    configs['mcp.json']['mcpServers']['firmory_cloud']['extensions'] = {
        'com.openai': {'auth': {'type': 'oauth', 'client': {'mode': 'cimd'}}}
    }
    upload = {**common, 'mcp.json': json_bytes(configs['mcp.json'])}
    if env == 'production' and not public_only:
        openai = portable['extensions']['com.openai']
        if not review_cases:
            raise ValueError('Production requires --review-cases pointing to the cases for the actual reviewer workspace')
        cases = json.loads(review_cases.read_text(encoding='utf-8'))
        if not isinstance(cases, dict) or set(cases) != {'positive', 'negative'}:
            raise ValueError('Review cases must contain positive and negative lists')
        for kind, count in [('positive', 5), ('negative', 3)]:
            required = ('description', 'prompt') if kind == 'negative' else ('description', 'prompt', 'expected_behavior', 'tools_triggered')
            if (not isinstance(cases[kind], list) or len(cases[kind]) != count or
                    not all(isinstance(case, dict) and all(isinstance(case.get(k), str) and case[k].strip()
                                for k in required) for case in cases[kind])):
                raise ValueError(f'Expected {count} complete {kind} review cases')
        openai['review'] = {'test_cases': cases}
        if demo_recording_url:
            if not demo_recording_url.startswith('https://'):
                raise ValueError('The review recording must use a public HTTPS URL')
            openai['review']['demo_recording_url'] = demo_recording_url
        openai['publication']['release_notes'] = f'Firmory {release_version} connects to your team workspace to compare file versions, trace references, summarize project briefings, and save or revise a checklist with its source versions.'
        upload['plugin.json'] = json_bytes(portable)
    if env == 'production':
        all_files = {**marketplace, **upload}
        for files in distributions.values():
            all_files.update(files)
        for name, data in all_files.items():
            if not name.endswith('.png') and any(x in data.lower() for x in (b'preview.firmory.ai', b'clerk.accounts.dev')):
                raise ValueError(f'Development host found in {name}')
    destination.mkdir(parents=True, exist_ok=True)
    prefix = f"firmory-{portable['version']}-{env}"
    if not public_only:
        archive(destination / f'{prefix}-openai.zip', upload)
    archive(destination / f'{prefix}-marketplace.zip', marketplace)
    for client, files in distributions.items():
        archive(destination / f"firmory-{portable['version']}-{client}.zip", files)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--env', choices=ENDPOINTS, default='preview')
    parser.add_argument('--release-version')
    parser.add_argument('--review-cases', type=Path, help='JSON containing the production reviewer workspace test cases')
    parser.add_argument('--demo-recording-url', help='Public HTTPS video link for OpenAI reviewers')
    parser.add_argument('--public-only', action='store_true', help='Build public installers without OpenAI review materials')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'dist')
    args = parser.parse_args()
    try:
        build(args.env, args.release_version, args.output_dir, args.review_cases, args.demo_recording_url, args.public_only)
    except (ValueError, OSError) as error:
        parser.error(str(error))
