"""Verify the archive shape required by single-plugin ZIP importers."""
import contextlib
import io
import json
import re
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from scripts.build_distribution import build


class DistributionTests(unittest.TestCase):
    def test_preview_instructions_match_the_packaged_server(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            with contextlib.redirect_stdout(io.StringIO()):
                build('preview', None, output)
            archives = list(output.glob('*.zip'))
            self.assertEqual(len(archives), 4)
            for path in archives:
                with self.subTest(archive=path.name), ZipFile(path) as archive:
                    self.assertIsNone(archive.testzip())
                    for name in archive.namelist():
                        if name.endswith(('mcp.json', '.md')):
                            self.assertNotIn(b'https://firmory.ai/mcp', archive.read(name), name)
                        if name.endswith('mcp.json'):
                            servers = json.loads(archive.read(name))['mcpServers']
                            self.assertEqual(set(servers), {'firmory_preview'})
                            self.assertEqual(servers['firmory_preview']['url'], 'https://preview.firmory.ai/mcp')
                        if name.endswith('plugin.json'):
                            manifest = json.loads(archive.read(name))
                            self.assertEqual(manifest['name'], 'firmory-preview')
                            if '.claude-plugin/' not in name:
                                self.assertEqual(manifest['extensions']['com.openai']['interface']['displayName'],
                                                 'Firmory Preview')
                        if name.endswith('marketplace.json'):
                            catalog = json.loads(archive.read(name))
                            self.assertEqual(catalog['name'], 'firmory-preview-plugins')
                            entry, = catalog['plugins']
                            self.assertEqual(entry['name'], 'firmory-preview')
                            source = entry['source']
                            source_path = source['path'] if isinstance(source, dict) else source
                            self.assertEqual(source_path, './plugins/firmory-preview')
                        if name.endswith('/SKILL.md'):
                            skill = archive.read(name)
                            self.assertIn(f'name: {Path(name).parent.name}\n'.encode(), skill)
                            for requirement in (b'`firmory_preview`', b'`workspace({})`', b'`resourceUrl`',
                                                b'https://preview.firmory.ai/mcp', b'Make no Firmory writes'):
                                self.assertIn(requirement, skill, name)
                    skills = {name.split('/skills/', 1)[-1] if '/skills/' in name else name.removeprefix('skills/')
                              for name in archive.namelist() if name.endswith('/SKILL.md')}
                    self.assertEqual(skills, {'firmory-preview/SKILL.md', 'firmory-preview-sync/SKILL.md'})
                    self.assertFalse(any('skills/setup/' in name for name in archive.namelist()))
                    connection = next(name for name in archive.namelist() if name.endswith('skills/firmory-preview/references/connection.md'))
                    self.assertIn(b'https://preview.firmory.ai/mcp', archive.read(connection))
                    self.assertIn(b'`verify_connection`', archive.read(connection))
                    connection_guide = archive.read(connection)
                    self.assertIn(b'`scripts/codex_oauth.py`', connection_guide)
                    self.assertIn(b'`switch_team({teamId})`', connection_guide)
                    self.assertIn(b'Switching Teams on an account grant does not start OAuth', connection_guide)
                    launcher = next(name for name in archive.namelist() if name.endswith('skills/firmory-preview/scripts/codex_oauth.py'))
                    self.assertIn(b'SERVER = "firmory_preview"', archive.read(launcher))
                    self.assertIn(b'RESOURCE = "https://preview.firmory.ai/mcp"', archive.read(launcher))
                    self.assertIn(b'"--scopes", "openid"', archive.read(launcher))
                    reference_path = 'skills/firmory-preview/references/production-library.md'
                    reference = next(name for name in archive.namelist() if name.endswith(reference_path))
                    skill = reference.removesuffix('references/production-library.md') + 'SKILL.md'
                    activation = archive.read(skill)
                    self.assertIn(b'(references/production-library.md)', activation)
                    self.assertIn(b'../firmory-preview-sync/SKILL.md', activation)
                    guide = archive.read(reference)
                    self.assertIn(b'Never upload a Skill ZIP as a fallback', guide)
                    for tool in (
                        b'`library_submit`', b'`get_resource_link`',
                        b'`set_skill_sharing({itemId, visibility: "public"})`', b'`read_shared_resource`',
                    ):
                        self.assertIn(tool, guide)
                    for kind in (b'skills', b'projects', b'files'):
                        self.assertIn(b'/shared/' + kind + b'/{resourceId}/{key}', guide)
                    self.assertIn(b'#turn-a-task-into-a-skill', activation)
                    self.assertIn(b'#use-a-shared-skill-for-new-work', activation)
                    if path.name.endswith('-codex.zip'):
                        self.assertEqual(path.name, 'firmory-preview-1.1.5-codex.zip')
                        readme = archive.read('README.md')
                        self.assertIn(b'https://preview.firmory.ai/mcp', readme)
                        self.assertIn(b'choose **Firmory Preview**', readme)
                        self.assertNotIn(b'codex plugin marketplace add DepsilonAI/firmory-plugins', readme)
                    for name in archive.namelist():
                        if name.endswith('hooks/sync_reminder.py'):
                            self.assertIn(b'follow the firmory-preview-sync skill', archive.read(name))

    def test_codex_zip_is_one_uploadable_plugin(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            with contextlib.redirect_stdout(io.StringIO()):
                build('production', '1.0.1', output, public_only=True)
            with ZipFile(output / 'firmory-1.0.1-codex.zip') as archive:
                self.assertIsNone(archive.testzip())
                names = set(archive.namelist())
                self.assertIn('plugin.json', names)
                self.assertEqual([name for name in names if name.endswith('plugin.json')], ['plugin.json'])
                self.assertFalse(any('marketplace.json' in name for name in names))
                manifest = json.loads(archive.read('plugin.json'))
                self.assertEqual((manifest['name'], manifest['version']), ('firmory', '1.0.1'))
                metadata = manifest['extensions']['com.openai']
                self.assertEqual(metadata['interface']['displayName'], 'Firmory')
                self.assertNotIn('review', metadata)
                self.assertNotIn('onboardingSkill', metadata)
                for path in [metadata['interface']['logo'], metadata['interface']['composerIcon']]:
                    self.assertIn(path.removeprefix('./'), names)
                mcp = json.loads(archive.read('mcp.json'))
                self.assertEqual(mcp['mcpServers'], {'firmory_cloud': {
                    'type': 'streamable-http', 'url': 'https://firmory.ai/mcp',
                }})
                self.assertIn('skills/firmory/SKILL.md', names)
                self.assertNotIn(b'`resourceUrl`', archive.read('skills/firmory/SKILL.md'))
                self.assertNotIn('skills/setup/SKILL.md', names)
                self.assertIn('skills/firmory/references/connection.md', names)
                self.assertIn('skills/firmory/references/production-library.md', names)
                self.assertIn('skills/firmory/scripts/codex_oauth.py', names)
                self.assertIn('skills/sync/SKILL.md', names)
                self.assertIn('hooks/hooks.json', names)
                self.assertIn('hooks/sync_reminder.py', names)
                for name in names:
                    if name.endswith(('.md', '.json')):
                        self.assertIsNone(re.search(r'[\u3400-\u4dbf\u4e00-\u9fff]', archive.read(name).decode()), name)
            with ZipFile(output / 'firmory-1.0.1-claude-code.zip') as archive:
                catalog = json.loads(archive.read('firmory-claude-code/.claude-plugin/marketplace.json'))
                self.assertEqual(catalog['name'], 'firmory-plugins')
                self.assertIn('firmory-claude-code/plugins/firmory/.claude-plugin/plugin.json', archive.namelist())
                for name in archive.namelist():
                    if name.endswith(('.md', '.json')):
                        self.assertIsNone(re.search(r'[\u3400-\u4dbf\u4e00-\u9fff]', archive.read(name).decode()), name)


    def test_desktop_uses_discovery_and_portal_has_explicit_oauth(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            cases = output / 'cases.json'
            cases.write_text(json.dumps({
                'positive': [{'description': 'Read a fixture', 'prompt': 'Show files',
                              'expected_behavior': 'List fixture files', 'tools_triggered': 'workspace'}] * 5,
                'negative': [{'description': 'Unsupported action', 'prompt': 'Transfer money'}] * 3,
            }))
            with contextlib.redirect_stdout(io.StringIO()):
                build('production', '1.0.1', output, review_cases=cases)
            with ZipFile(output / 'firmory-1.0.1-codex.zip') as public, \
                    ZipFile(output / 'firmory-1.0.1-production-openai.zip') as review, \
                    ZipFile(output / 'firmory-1.0.1-production-marketplace.zip') as marketplace:
                self.assertEqual(public.read('mcp.json'), marketplace.read('plugins/firmory/mcp.json'))
                review_server = json.loads(review.read('mcp.json'))['mcpServers']['firmory_cloud']
                self.assertEqual(review_server['extensions']['com.openai']['auth'], {
                    'type': 'oauth', 'client': {'mode': 'cimd'}, 'baseScopes': ['openid'],
                })
                self.assertEqual(review_server['url'], 'https://firmory.ai/mcp')
                self.assertNotIn('review', json.loads(public.read('plugin.json'))['extensions']['com.openai'])
                self.assertIn('review', json.loads(review.read('plugin.json'))['extensions']['com.openai'])
                self.assertNotIn('onboardingSkill', json.loads(review.read('plugin.json'))['extensions']['com.openai'])
                self.assertFalse(any(name.startswith('hooks/') for name in review.namelist()))
                self.assertIn('skills/sync/SKILL.md', review.namelist())
                for archive in (public, review, marketplace):
                    self.assertFalse(any('skills/setup/' in name for name in archive.namelist()))
                    for name in archive.namelist():
                        if name.endswith('.md'):
                            self.assertNotIn(b'../setup/SKILL.md', archive.read(name))
                runtime = json.loads(marketplace.read('plugins/firmory/mcp.json'))
                self.assertNotIn('extensions', runtime['mcpServers']['firmory_cloud'])


if __name__ == '__main__':
    unittest.main()
