from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ru_tts.build_backend import backend_library_name, build_backend


class BuildBackendTests(unittest.TestCase):
    def test_builds_library_in_requested_output_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)

            try:
                library = build_backend(output_dir=output_dir)
            except TypeError as exc:
                self.fail(f"build_backend must accept output_dir: {exc}")

            self.assertEqual(library, output_dir / backend_library_name())
            self.assertTrue(library.is_file())
