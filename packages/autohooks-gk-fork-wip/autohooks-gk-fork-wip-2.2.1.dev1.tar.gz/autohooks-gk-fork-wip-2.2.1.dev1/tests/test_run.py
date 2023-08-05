from contextlib import redirect_stdout
import io
from pathlib import Path
import tempfile
from unittest import TestCase

from autohooks.precommit import run
from autohooks.settings import Mode
from autohooks.template import PreCommitTemplate


class Test(TestCase):
    def test_run(self):
        template = PreCommitTemplate()
        with tempfile.TemporaryDirectory() as tempdir:
            tmp_hook_path = Path(tempdir) / 'pre-commit-test'

            # Test run using all shebang modes
            for mode in [m for m in Mode if m.value > 0]:
                with open(str(tmp_hook_path), 'w') as tmpfile:
                    tmpfile.write(template.render(mode=mode))

                buf = io.StringIO()
                with redirect_stdout(buf):
                    self.assertEqual(0, run(['pre-conf-test'], tmp_hook_path))

                expected_stdout = (
                    'ℹ autohooks => pre-conf-test\n'
                    'ℹ     Running autohooks.plugins.black\n'
                    'ℹ     Running autohooks.plugins.pylint\n'
                )

                self.assertEqual(expected_stdout, buf.getvalue())
