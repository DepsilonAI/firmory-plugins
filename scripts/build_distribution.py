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
PREVIEW_NAME = 'firmory-preview'
PREVIEW_LABEL = 'Firmory Preview'
PREVIEW_SERVER = 'firmory_preview'
PREVIEW_SKILLS = {'firmory': PREVIEW_NAME, 'sync': 'firmory-preview-sync'}


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()


def read_json(path):
    return json.loads((PLUGIN / path).read_text(encoding='utf-8'))


def preview_skill_path(path):
    for name, preview_name in PREVIEW_SKILLS.items():
        path = path.replace(f'skills/{name}/', f'skills/{preview_name}/')
    return path


def package_file(path, env):
    data = path.read_bytes()
    if env != 'preview':
        return data
    if path == PLUGIN / 'hooks/sync_reminder.py':
        return data.replace(
            b'Firmory: after actual local deliverable changes, follow the Firmory sync skill',
            b'Firmory Preview: after local edits, follow the firmory-preview-sync skill',
        )
    if path.suffix != '.md':
        return data
    text = data.decode('utf-8')
    text = text.replace(ENDPOINTS['production'], ENDPOINTS['preview'])
    text = text.replace('firmory_cloud', PREVIEW_SERVER)
    text = text.replace(f'plugin:firmory:{PREVIEW_SERVER}', f'plugin:{PREVIEW_NAME}:{PREVIEW_SERVER}')
    text = preview_skill_path(text)
    for name, preview_name in PREVIEW_SKILLS.items():
        text = text.replace(f'../{name}/', f'../{preview_name}/')
    text = text.replace('@Firmory', f'@{PREVIEW_LABEL}')
    if path.name == 'SKILL.md':
        name = path.parent.name
        text = text.replace(f'name: {name}\n', f'name: {PREVIEW_SKILLS[name]}\n', 1)
        frontmatter, title, body = text.split('\n\n', 2)
        preview_connection = (
            '## Verify the preview connection\n\n'
            f'Use only this installed {PREVIEW_LABEL} plugin\'s `{PREVIEW_SERVER}` MCP connection for '
            'every Firmory call. The host may prefix tool names. Before creating projects, writing '
            'or uploading files, saving Skills, changing sharing, or performing any other Firmory '
            'write, call `workspace({})` on that connection and require the returned `resourceUrl` '
            f'to equal `{ENDPOINTS["preview"]}` exactly. Use the same verified tool namespace for '
            'all subsequent operations and use only IDs obtained from that workspace. If the '
            'connection or matching URL is missing, finish any local work and report that preview '
            'could not be verified. Make no Firmory writes. Never substitute the production '
            'plugin, globally configured connections such as `firmory_remote`, or another tool namespace.'
        )
        text = '\n\n'.join((frontmatter, title, preview_connection, body))
    if path.name in ('install-codex.md', 'install-claude-code.md'):
        text = text.replace('# Firmory for ', f'# {PREVIEW_LABEL} for ', 1)
        if path.name == 'install-claude-code.md':
            text = text.replace('firmory-claude-code folder', f'{PREVIEW_NAME}-claude-code folder')
            text = text.replace('firmory@firmory-plugins', f'{PREVIEW_NAME}@{PREVIEW_NAME}-plugins', 1)
        else:
            text = text.replace('`firmory-', f'`{PREVIEW_NAME}-', 1)
        start = text.index('## Install the production plugin from GitHub instead')
        end = text.index('This ZIP connects to ', start)
        text = text[:start] + text[end:]
        text = text.replace(
            'This ZIP connects to ',
            f'In a new chat, choose **{PREVIEW_LABEL}**. Verify the preview connection before '
            'uploading files or saving a Skill. This ZIP connects to ',
            1,
        )
    return text.encode('utf-8')


def package_catalog(path, env, plugin_path):
    original = (ROOT / path).read_bytes()
    if env != 'preview':
        return original
    catalog = json.loads(original)
    catalog['name'] = f'{PREVIEW_NAME}-plugins'
    if 'interface' in catalog:
        catalog['interface']['displayName'] = PREVIEW_LABEL
    entry, = catalog['plugins']
    entry['name'] = PREVIEW_NAME
    if isinstance(entry['source'], dict):
        entry['source']['path'] = f'./{plugin_path}'
    else:
        entry['source'] = f'./{plugin_path}'
    return json_bytes(catalog)


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

    server_name = 'firmory_cloud'
    plugin_path = PLUGIN_PATH
    if env == 'preview':
        portable['name'] = claude['name'] = PREVIEW_NAME
        portable['description'] = claude['description'] = 'Test workflows in the Firmory preview workspace'
        interface = portable['extensions']['com.openai']['interface']
        interface['displayName'] = PREVIEW_LABEL
        interface['shortDescription'] = 'Connect to Firmory preview'
        interface['longDescription'] = 'Connect to the Firmory preview workspace to test project files and reusable Skills with separate preview authorization.'
        server_name = PREVIEW_SERVER
        plugin_path = f'plugins/{PREVIEW_NAME}'

    configs = {}
    for path, transport in [('mcp.json', 'streamable-http'), ('.mcp.json', 'http')]:
        config = read_json(path)
        if config['mcpServers'] != {'firmory_cloud': {'type': transport, 'url': ENDPOINTS['production']}}:
            raise ValueError(f'Unexpected production server in {path}')
        config['mcpServers'] = {server_name: {'type': transport, 'url': ENDPOINTS[env]}}
        configs[path] = config

    common = {(preview_skill_path(name) if env == 'preview' else name): package_file(PLUGIN / name, env) for name in (
        'assets/icon.svg', 'assets/logo-blue.png', 'assets/composer-blue.png', 'README.md',
        'skills/firmory/SKILL.md', 'skills/firmory/references/connection.md',
        'skills/firmory/references/production-library.md', 'skills/sync/SKILL.md',
    )}
    if (PLUGIN / 'LICENSE').is_file():
        common['LICENSE'] = (PLUGIN / 'LICENSE').read_bytes()
    common['plugin.json'] = json_bytes(portable)
    local_hooks = {name: package_file(PLUGIN / name, env) for name in ('hooks/hooks.json', 'hooks/sync_reminder.py')}
    runtime = {**common, **local_hooks, 'mcp.json': json_bytes(configs['mcp.json']),
               '.mcp.json': json_bytes(configs['.mcp.json']),
               '.claude-plugin/plugin.json': json_bytes(claude),
               '.claude-plugin/icon.png': (PLUGIN / '.claude-plugin/icon.png').read_bytes()}
    marketplace = {f'{plugin_path}/{k}': v for k, v in runtime.items()}
    marketplace.update({k: package_catalog(k, env, plugin_path) for k in CATALOGS})
    marketplace['README.md'] = common['README.md']
    # ZIP uploaders accept one plugin root, not a nested marketplace catalog.
    distributions = {'codex': {**common, **local_hooks, 'mcp.json': runtime['mcp.json'],
                               'README.md': package_file(ROOT / 'docs/install-codex.md', env)}}
    for client, catalog in [('claude-code', CATALOGS[1])]:
        files = {k: v for k, v in marketplace.items() if k not in CATALOGS or k == catalog}
        files['README.md'] = package_file(ROOT / f'docs/install-{client}.md', env)
        distributions[client] = {f'{portable["name"]}-{client}/{k}': v for k, v in files.items()}
    # The submission portal accepts explicit OAuth metadata. Desktop's current
    # MCP loader rejects server extensions, so install ZIPs use OAuth discovery.
    configs['mcp.json']['mcpServers'][server_name]['extensions'] = {
        'com.openai': {'auth': {'type': 'oauth', 'client': {'mode': 'cimd'},
                                'baseScopes': ['user:org:read']}}
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
        openai['publication']['release_notes'] = f'Firmory {release_version} connects to your authorized team to compare file versions, trace references, summarize project briefings, and save or revise a checklist with its source versions.'
        upload['plugin.json'] = json_bytes(portable)
    if env == 'production':
        all_files = {**marketplace, **upload}
        for files in distributions.values():
            all_files.update(files)
        for name, data in all_files.items():
            if not name.endswith('.png') and any(x in data.lower() for x in (b'preview.firmory.ai', b'clerk.accounts.dev')):
                raise ValueError(f'Development host found in {name}')
    destination.mkdir(parents=True, exist_ok=True)
    plugin_version = f"{portable['name']}-{portable['version']}"
    prefix = f'{plugin_version}-{env}' if env == 'production' else plugin_version
    if not public_only:
        archive(destination / f'{prefix}-openai.zip', upload)
    archive(destination / f'{prefix}-marketplace.zip', marketplace)
    for client, files in distributions.items():
        archive(destination / f'{plugin_version}-{client}.zip', files)


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
