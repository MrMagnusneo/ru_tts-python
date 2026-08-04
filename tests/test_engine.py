from __future__ import annotations

import unittest

from ru_tts.engine import RU_TTS_CONF_T, RuTTSPythonEngine


class LegacyArgumentTests(unittest.TestCase):
    def test_l_enables_legacy_rate_algorithm(self) -> None:
        engine = object.__new__(RuTTSPythonEngine)
        config = RU_TTS_CONF_T()

        engine._apply_legacy_args(config, ["-l"])

        self.assertEqual(config.flags, 8)
