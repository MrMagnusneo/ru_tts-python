# Upstream ru_tts and Sonic Update Design

## Goal

Update the native dependencies used by `ru-tts-python` while preserving its
lightweight Python CLI/API architecture. The update is limited to `ru_tts` and
Sonic; NVDA text preprocessing, RuLex, and other NVDA add-on dependencies are
out of scope.

## Upstream Baselines

- `ru_tts`: `poretsky/ru_tts` v6.3.3 at commit
  `2848d2892097320ed37fc963b439b15803f47f0c`.
- Sonic: the `ru_tts-for-nvda` Sonic submodule at commit
  `b93885dcb70aae50c6f76b0fe4e0868f029a077e`.

The GitVerse `ru_tts-for-nvda` repository references the same `ru_tts` v6.3.3
commit. The existing vendored `sonic.c` and `sonic.h` already match the selected
Sonic baseline, so they do not require content changes.

## Architecture and Components

The existing dependency boundaries remain unchanged:

- `ru_tts/vendor/ru_tts/` contains the upstream synthesis core.
- `ru_tts/vendor/sonic/` contains the two Sonic files used by the bridge.
- `ru_tts/vendor/bridge/` remains the local adapter from 8-bit `ru_tts` output
  through Sonic to 16-bit PCM callbacks.
- `ru_tts/engine.py` remains the public Python API implementation.
- `ru_tts/cli.py` remains the command-line entry point.

The `ru_tts` directory will be synchronized with the selected upstream `src/`
snapshot. The upstream `phonemes.h` file will be added. The local generated
compatibility header `config.h` will be retained because the standalone Python
build does not run the upstream Autoconf pipeline.

Only `sonic.c` and `sonic.h` will remain vendored. Files unrelated to the bridge,
such as Sonic utilities, samples, build metadata, and its optional Speedy
submodule, will not be added.

## Runtime Behavior

The updated `ru_tts` adaptive speech-rate algorithm becomes the default, matching
the library's upstream configuration initialization. The upstream
`USE_LEGACY_RATE_ALGO` flag will be represented in the Python binding, and the
existing legacy argument parser will accept `-l` after `--` to enable the old
linear-interpolation rate algorithm.

All existing public Python methods, CLI options, audio format, sample rate, voice
selection, and decimal-separator behavior remain compatible.

## Build and Packaging

`ru_tts/build_backend.py` will continue compiling a single shared library. Its
source list will be adjusted only if required by the v6.3.3 source layout. Header
discovery continues through the existing include directory, and setuptools'
existing `vendor/ru_tts/*` package-data pattern includes `phonemes.h`.

The repository will record the selected upstream commits so a future update can
be audited without reverse-engineering vendored file contents.

## Error Handling

Existing build failures continue to surface as `RuntimeError` with compiler
stdout and stderr. Invalid or incomplete legacy options retain the current parser
behavior. The new `-l` flag requires no value and only sets the corresponding
configuration bit.

## Verification

Automated tests will verify:

1. configuration flag constants and `-l` legacy argument handling;
2. successful native backend compilation against the synchronized sources;
3. non-empty raw PCM synthesis for representative Russian text;
4. valid mono, 16-bit, 10 kHz WAV output;
5. successful synthesis with both the adaptive default and legacy rate algorithm.

The final verification will also compare vendored source hashes against the
selected upstream files, run the complete test suite, and run CLI smoke tests.

## Non-Goals

- NVDA-specific text normalization, abbreviation, Latin-letter, or Braille rules;
- RuLex database or library support;
- LMDB, PCRE2, or other `ru_tts-for-nvda` dependencies;
- changing the C bridge design or public Python API;
- vendoring the complete Sonic repository.
