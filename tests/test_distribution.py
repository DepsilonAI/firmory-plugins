"""Verify the archive shape required by single-plugin ZIP importers."""
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from scripts.build_distribution import build


class DistributionTests(unittest.TestCase):
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
                for path in [metadata['interface']['logo'], metadata['interface']['composerIcon'], metadata['onboardingSkill']]:
                    self.assertIn(path.removeprefix('./'), names)
                mcp = json.loads(archive.read('mcp.json'))
                self.assertEqual(mcp['mcpServers'], {'firmory_cloud': {
                    'type': 'streamable-http', 'url': 'https://firmory.ai/mcp',
                }})
                self.assertIn('skills/firmory/SKILL.md', names)
            with ZipFile(output / 'firmory-1.0.1-claude-code.zip') as archive:
                catalog = json.loads(archive.read('firmory-claude-code/.claude-plugin/marketplace.json'))
                self.assertEqual(catalog['name'], 'firmory-plugins')
                self.assertIn('firmory-claude-code/plugins/firmory/.claude-plugin/plugin.json', archive.namelist())


if __name__ == '__main__':
    unittest.main()
