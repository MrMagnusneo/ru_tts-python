from __future__ import annotations

import subprocess
import sys
import unittest


class CliHelpTests(unittest.TestCase):
    def test_help_lists_legacy_rate_flag(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "ru_tts", "--help"],
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertIn("-a -l -d.", result.stdout)
