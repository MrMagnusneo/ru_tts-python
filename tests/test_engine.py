from __future__ import annotations

import hashlib
import tempfile
import unittest
import wave
from io import BytesIO
from pathlib import Path

from ru_tts.build_backend import build_backend
from ru_tts.engine import RU_TTS_CONF_T, RuTTSPythonEngine


class LegacyArgumentTests(unittest.TestCase):
    def test_l_enables_legacy_rate_algorithm(self) -> None:
        engine = object.__new__(RuTTSPythonEngine)
        config = RU_TTS_CONF_T()

        engine._apply_legacy_args(config, ["-l"])

        self.assertEqual(config.flags, 8)


class NativeBackendTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._tmp = tempfile.TemporaryDirectory()
        cls.lib_path = build_backend(output_dir=Path(cls._tmp.name))

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmp.cleanup()

    def test_adaptive_and_legacy_algorithms_produce_distinct_audio(self) -> None:
        engine = RuTTSPythonEngine(lib_path=str(self.lib_path), auto_build=False)
        try:
            adaptive = engine.synthesize_raw(
                "Проверка скорости синтеза", args=["-r", "2.0"]
            )
            legacy = engine.synthesize_raw(
                "Проверка скорости синтеза", args=["-r", "2.0", "-l"]
            )
        finally:
            engine.close()

        self.assertGreater(len(adaptive), 0)
        self.assertGreater(len(legacy), 0)
        self.assertNotEqual(
            hashlib.sha256(adaptive).digest(), hashlib.sha256(legacy).digest()
        )

    def test_wav_output_is_mono_16_bit_10khz(self) -> None:
        engine = RuTTSPythonEngine(lib_path=str(self.lib_path), auto_build=False)
        try:
            data = engine.synthesize_wav("Проверка формата")
        finally:
            engine.close()

        with wave.open(BytesIO(data), "rb") as wav_file:
            self.assertEqual(wav_file.getnchannels(), 1)
            self.assertEqual(wav_file.getsampwidth(), 2)
            self.assertEqual(wav_file.getframerate(), 10000)
            self.assertGreater(wav_file.getnframes(), 0)
