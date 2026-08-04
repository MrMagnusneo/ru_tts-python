# Upstream ru_tts and Sonic Update Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update the vendored synthesis core to `ru_tts` v6.3.3, verify the selected Sonic snapshot, and expose the new core's legacy rate-algorithm flag without changing the existing Python API or audio format.

**Architecture:** Keep the current ctypes engine and local C bridge. Mechanically synchronize `ru_tts/vendor/ru_tts/` with the pinned upstream `src/` tree while preserving the standalone `config.h`; retain only Sonic's `sonic.c` and `sonic.h`. Add offline source-baseline tests, an isolated backend build option for integration tests, and smoke tests for both speech-rate algorithms.

**Tech Stack:** Python 3.9+, `unittest`, `ctypes`, GCC C11 shared-library build, `ru_tts` C sources, Sonic C API.

## Global Constraints

- `ru_tts` baseline is v6.3.3 commit `2848d2892097320ed37fc963b439b15803f47f0c`.
- Sonic baseline is commit `b93885dcb70aae50c6f76b0fe4e0868f029a077e` from the `ru_tts-for-nvda` submodule.
- Do not add NVDA preprocessing, RuLex, LMDB, PCRE2, Speedy, Sonic utilities, samples, or unrelated build files.
- Preserve `ru_tts/vendor/ru_tts/config.h` for builds that do not run Autoconf.
- Preserve all existing Python API signatures, CLI options, 16-bit mono PCM output, and the 10 kHz WAV format.
- The adaptive upstream speech-rate algorithm is the default; `-l` after `--` enables the legacy algorithm.

## File Map

- Create `tests/__init__.py`: marks the standard-library test package.
- Create `tests/test_vendor_sources.py`: verifies the pinned core features and exact Sonic file hashes offline.
- Create `tests/test_engine.py`: verifies flag parsing, isolated compilation, PCM synthesis, and WAV metadata.
- Create `ru_tts/vendor/UPSTREAM.md`: records dependency origins, commits, selected files, and the local `config.h` exception.
- Modify `ru_tts/vendor/ru_tts/*`: synchronize the upstream v6.3.3 source snapshot and add `phonemes.h`.
- Modify `ru_tts/engine.py`: bind `USE_LEGACY_RATE_ALGO` and recognize legacy argument `-l`.
- Modify `ru_tts/build_backend.py`: support an optional build output directory for isolated tests.
- Modify `README.md`: document pinned versions and `-l` in Russian and English.
- Modify `PORTING_STATUS.md`: record the completed v6.3.3/Sonic synchronization.
- Modify `bin/libru_tts_backend.so`: rebuild the checked-in Linux backend so default execution does not use stale native code.

---

### Task 1: Pin and Synchronize Native Sources

**Files:**
- Create: `tests/__init__.py`
- Create: `tests/test_vendor_sources.py`
- Create: `ru_tts/vendor/UPSTREAM.md`
- Create: `ru_tts/vendor/ru_tts/phonemes.h`
- Modify: `ru_tts/vendor/ru_tts/Makefile.am`
- Modify: `ru_tts/vendor/ru_tts/intonator.c`
- Modify: `ru_tts/vendor/ru_tts/numerics.c`
- Modify: `ru_tts/vendor/ru_tts/ru_tts.c`
- Modify: `ru_tts/vendor/ru_tts/ru_tts.h`
- Modify: `ru_tts/vendor/ru_tts/sink.c`
- Modify: `ru_tts/vendor/ru_tts/sink.h`
- Modify: `ru_tts/vendor/ru_tts/soundproducer.c`
- Modify: `ru_tts/vendor/ru_tts/soundscript.h`
- Modify: `ru_tts/vendor/ru_tts/synth.c`
- Modify: `ru_tts/vendor/ru_tts/text2speech.c`
- Modify: `ru_tts/vendor/ru_tts/time_planner.c`
- Modify: `ru_tts/vendor/ru_tts/transcription.c`
- Modify: `ru_tts/vendor/ru_tts/utterance.c`
- Test: `tests/test_vendor_sources.py`

**Interfaces:**
- Consumes: the pinned upstream `src/` tree and Sonic `sonic.c`/`sonic.h` files.
- Produces: a v6.3.3 `ru_tts` source tree containing `USE_LEGACY_RATE_ALGO` and `phonemes.h`, plus audited Sonic provenance.

- [ ] **Step 1: Write the failing offline source-baseline tests**

Create `tests/__init__.py` as an empty file and create `tests/test_vendor_sources.py`:

```python
from __future__ import annotations

import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RU_TTS = ROOT / "ru_tts" / "vendor" / "ru_tts"
SONIC = ROOT / "ru_tts" / "vendor" / "sonic"


class VendorSourceTests(unittest.TestCase):
    def test_ru_tts_v633_features_are_present(self) -> None:
        self.assertTrue((RU_TTS / "phonemes.h").is_file())
        self.assertIn(
            "#define USE_LEGACY_RATE_ALGO 8",
            (RU_TTS / "ru_tts.h").read_text(encoding="utf-8"),
        )
        self.assertIn(
            "powf(p, adaptive_power)",
            (RU_TTS / "soundproducer.c").read_text(encoding="utf-8"),
        )
        self.assertIn(
            "ttscb_t ttscb = {0};",
            (RU_TTS / "text2speech.c").read_text(encoding="utf-8"),
        )

    def test_sonic_matches_pinned_snapshot(self) -> None:
        expected = {
            "sonic.c": "4a21d8086f844e3e68cb4f85961623a69d35da8ca93cf6ea704ccd125e64eaf5",
            "sonic.h": "a2fc087b68c25141e2fb7ab56e71b111bee79cf311fcc850d492eb574c0eeffe",
        }
        for name, digest in expected.items():
            with self.subTest(name=name):
                actual = hashlib.sha256((SONIC / name).read_bytes()).hexdigest()
                self.assertEqual(digest, actual)
```

- [ ] **Step 2: Run the source-baseline tests and confirm the expected failure**

Run:

```bash
python -m unittest tests.test_vendor_sources -v
```

Expected: `test_ru_tts_v633_features_are_present` fails because `phonemes.h` is absent; the Sonic hash test passes.

- [ ] **Step 3: Synchronize the exact v6.3.3 source snapshot**

Verify the already downloaded upstream clone, or clone it if absent:

```bash
git -C /tmp/ru_tts-upstream-github-full rev-parse HEAD
```

Expected: `2848d2892097320ed37fc963b439b15803f47f0c`.

Mechanically copy every regular file from `/tmp/ru_tts-upstream-github-full/src/` into `ru_tts/vendor/ru_tts/`. Do not delete the existing local `config.h`. Confirm that no files other than `config.h` differ from upstream:

```bash
diff -ru --exclude=config.h ru_tts/vendor/ru_tts /tmp/ru_tts-upstream-github-full/src
```

Expected: exit status 0 and no output.

- [ ] **Step 4: Record dependency provenance**

Create `ru_tts/vendor/UPSTREAM.md` with this content:

```markdown
# Vendored Native Dependencies

## ru_tts

- Repository: https://github.com/poretsky/ru_tts
- Version: v6.3.3
- Commit: `2848d2892097320ed37fc963b439b15803f47f0c`
- Vendored path: upstream `src/` copied to `ru_tts/`

`ru_tts/config.h` is maintained locally because this project compiles the shared
library directly and does not run the upstream Autoconf configuration step.

## Sonic

- Repository used by ru_tts-for-nvda: https://gitverse.ru/kvark128/sonic
- Commit: `b93885dcb70aae50c6f76b0fe4e0868f029a077e`
- Vendored files: `sonic/sonic.c` and `sonic/sonic.h`

Only the classic Sonic C implementation used by the local bridge is included.
```

- [ ] **Step 5: Run tests and source comparisons**

Run:

```bash
python -m unittest tests.test_vendor_sources -v
diff -ru --exclude=config.h ru_tts/vendor/ru_tts /tmp/ru_tts-upstream-github-full/src
sha256sum ru_tts/vendor/sonic/sonic.c ru_tts/vendor/sonic/sonic.h
```

Expected: two tests pass, the directory diff is empty, and hashes match the values in `test_vendor_sources.py`.

- [ ] **Step 6: Commit the source synchronization**

```bash
git add tests/__init__.py tests/test_vendor_sources.py ru_tts/vendor
git commit -m "build: update ru_tts core to v6.3.3"
```

---

### Task 2: Expose the Legacy Speech-Rate Algorithm

**Files:**
- Create: `tests/test_engine.py`
- Modify: `ru_tts/engine.py`
- Modify: `README.md`
- Test: `tests/test_engine.py`

**Interfaces:**
- Consumes: `RU_TTS_CONF_T.flags` and upstream constant value `8`.
- Produces: module constant `USE_LEGACY_RATE_ALGO = 8` and `_apply_legacy_args(conf, ["-l"])` behavior that sets that bit.

- [ ] **Step 1: Write the failing legacy-flag test**

Create `tests/test_engine.py`:

```python
from __future__ import annotations

import unittest

from ru_tts.engine import RU_TTS_CONF_T, RuTTSPythonEngine, USE_LEGACY_RATE_ALGO


class LegacyArgumentTests(unittest.TestCase):
    def test_l_enables_legacy_rate_algorithm(self) -> None:
        engine = object.__new__(RuTTSPythonEngine)
        config = RU_TTS_CONF_T()

        engine._apply_legacy_args(config, ["-l"])

        self.assertEqual(USE_LEGACY_RATE_ALGO, 8)
        self.assertEqual(config.flags & USE_LEGACY_RATE_ALGO, USE_LEGACY_RATE_ALGO)
```

- [ ] **Step 2: Run the test and confirm it fails**

Run:

```bash
python -m unittest tests.test_engine.LegacyArgumentTests -v
```

Expected: import failure because `USE_LEGACY_RATE_ALGO` is not defined.

- [ ] **Step 3: Implement the minimal binding and parser change**

In `ru_tts/engine.py`, add the constant next to the existing flags:

```python
USE_LEGACY_RATE_ALGO = 8
```

In `_apply_legacy_args`, add the flag branch immediately after `-a`:

```python
elif a == "-l":
    conf.flags |= USE_LEGACY_RATE_ALGO
```

- [ ] **Step 4: Document the behavior in both README languages**

Add `-l` to both legacy-argument lists. Explain that v6.3.3 uses the adaptive algorithm by default and `-- -l` selects the legacy linear-interpolation algorithm. Add the pinned upstream versions and link `ru_tts/vendor/UPSTREAM.md` from the layout section.

- [ ] **Step 5: Run focused and regression tests**

Run:

```bash
python -m unittest tests.test_engine.LegacyArgumentTests -v
python -m unittest discover -s tests -v
```

Expected: all tests pass.

- [ ] **Step 6: Commit the Python binding**

```bash
git add ru_tts/engine.py README.md tests/test_engine.py
git commit -m "feat: expose legacy ru_tts rate algorithm"
```

---

### Task 3: Add Isolated Native Integration Tests and Rebuild the Backend

**Files:**
- Modify: `ru_tts/build_backend.py`
- Modify: `tests/test_engine.py`
- Modify: `PORTING_STATUS.md`
- Modify: `bin/libru_tts_backend.so`
- Test: `tests/test_engine.py`

**Interfaces:**
- Consumes: `build_backend()` and `RuTTSPythonEngine(lib_path=..., auto_build=False)`.
- Produces: `build_backend(output_dir: Optional[Path] = None) -> Path`; calls without arguments keep writing to `bin/`.

- [ ] **Step 1: Add failing isolated build and synthesis tests**

Append to `tests/test_engine.py`:

```python
import tempfile
import wave
from io import BytesIO
from pathlib import Path

from ru_tts.build_backend import build_backend


class NativeBackendTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._tmp = tempfile.TemporaryDirectory()
        cls.lib_path = build_backend(output_dir=Path(cls._tmp.name))

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmp.cleanup()

    def test_adaptive_and_legacy_algorithms_synthesize_audio(self) -> None:
        engine = RuTTSPythonEngine(lib_path=str(self.lib_path), auto_build=False)
        try:
            adaptive = engine.synthesize_raw("Проверка скорости синтеза", args=["-r", "2.0"])
            legacy = engine.synthesize_raw("Проверка скорости синтеза", args=["-r", "2.0", "-l"])
        finally:
            engine.close()

        self.assertGreater(len(adaptive), 0)
        self.assertGreater(len(legacy), 0)
        self.assertNotEqual(adaptive, legacy)

    def test_wav_format_is_mono_16_bit_10khz(self) -> None:
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
```

- [ ] **Step 2: Run the integration test and confirm it fails at the new interface**

Run:

```bash
python -m unittest tests.test_engine.NativeBackendTests -v
```

Expected: `TypeError: build_backend() got an unexpected keyword argument 'output_dir'`.

- [ ] **Step 3: Implement isolated output-directory support**

In `ru_tts/build_backend.py`, import `Optional` and change the function to:

```python
from typing import Optional


def build_backend(output_dir: Optional[Path] = None) -> Path:
    base = Path(__file__).resolve().parents[1]
    vendor = base / "ru_tts" / "vendor"
    # Keep the existing bridge, Sonic, ru_tts, source list, and command setup.
    out_dir = Path(output_dir) if output_dir is not None else base / "bin"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_lib = out_dir / backend_library_name()
```

Remove the old fixed `out_dir = base / "bin"` assignment; leave all compiler flags and error reporting unchanged.

- [ ] **Step 4: Run the integration and complete test suites**

Run:

```bash
python -m unittest tests.test_engine.NativeBackendTests -v
python -m unittest discover -s tests -v
```

Expected: all tests pass, including non-empty and different adaptive/legacy PCM outputs.

- [ ] **Step 5: Rebuild and smoke-test the checked-in Linux backend**

Run:

```bash
python -c "from ru_tts.build_backend import build_backend; print(build_backend())"
python -m ru_tts --text "Проверка обновлённого движка" --out /tmp/ru-tts-v633.wav
python -m ru_tts --text "Проверка старого алгоритма" --out /tmp/ru-tts-v633-legacy.wav -- -l
```

Expected: the shared library rebuild succeeds and both WAV files are non-empty.

- [ ] **Step 6: Update project status**

In `PORTING_STATUS.md`, state that the core is synchronized to `ru_tts` v6.3.3, Sonic matches commit `b93885d`, the adaptive algorithm is the default, and `-l` enables the legacy algorithm. Keep NVDA preprocessing and RuLex listed as optional, out-of-scope improvements.

- [ ] **Step 7: Run final verification**

Run:

```bash
git diff --check
diff -ru --exclude=config.h ru_tts/vendor/ru_tts /tmp/ru_tts-upstream-github-full/src
python -m unittest discover -s tests -v
python -m ru_tts --help
file bin/libru_tts_backend.so /tmp/ru-tts-v633.wav /tmp/ru-tts-v633-legacy.wav
git status --short
```

Expected: no whitespace errors, no upstream source differences other than excluded `config.h`, all tests pass, CLI help includes current legacy argument help, the native library and WAV files have valid formats, and status contains only intended changes.

- [ ] **Step 8: Commit integration coverage and rebuilt backend**

```bash
git add ru_tts/build_backend.py tests/test_engine.py PORTING_STATUS.md bin/libru_tts_backend.so
git commit -m "test: verify updated native backend"
```
