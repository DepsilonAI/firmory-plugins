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
                            server = json.loads(archive.read(name))['mcpServers']['firmory_cloud']
                            self.assertEqual(server['url'], 'https://preview.firmory.ai/mcp')
                    skills = {name.split('/skills/', 1)[-1] if '/skills/' in name else name.removeprefix('skills/')
                              for name in archive.namelist() if name.endswith('/SKILL.md')}
                    self.assertEqual(skills, {'firmory/SKILL.md', 'sync/SKILL.md'})
                    self.assertFalse(any('skills/setup/' in name for name in archive.namelist()))
                    connection = next(name for name in archive.namelist() if name.endswith('skills/firmory/references/connection.md'))
                    self.assertIn(b'https://preview.firmory.ai/mcp', archive.read(connection))
                    self.assertIn(b'`verify_connection`', archive.read(connection))
                    reference_path = 'skills/firmory/references/production-library.md'
                    reference = next(name for name in archive.namelist() if name.endswith(reference_path))
                    skill = reference.removesuffix('references/production-library.md') + 'SKILL.md'
                    self.assertIn(b'(references/production-library.md)', archive.read(skill))
                    self.assertIn(b'`library_submit`', archive.read(reference))
                    if path.name.endswith('-codex.zip'):
                        self.assertIn(b'https://preview.firmory.ai/mcp', archive.read('README.md'))

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
                self.assertNotIn('review', metadata)
                self.assertNotIn('onboardingSkill', metadata)
                for path in [metadata['interface']['logo'], metadata['interface']['composerIcon']]:
                    self.assertIn(path.removeprefix('./'), names)
                mcp = json.loads(archive.read('mcp.json'))
                self.assertEqual(mcp['mcpServers'], {'firmory_cloud': {
                    'type': 'streamable-http', 'url': 'https://firmory.ai/mcp',
                }})
                self.assertIn('skills/firmory/SKILL.md', names)
                self.assertNotIn('skills/setup/SKILL.md', names)
                self.assertIn('skills/firmory/references/connection.md', names)
                self.assertIn('skills/firmory/references/production-library.md', names)
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
                    'type': 'oauth', 'client': {'mode': 'cimd'}, 'baseScopes': ['user:org:read'],
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
