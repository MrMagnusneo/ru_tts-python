# ru-tts-python Status

The project now exposes one native `ru_tts` backend. The older executable backend and legacy backend-specific public naming were removed.

The vendored core is synchronized with `ru_tts` v6.3.3
(`2848d2892097320ed37fc963b439b15803f47f0c`). The selected Sonic sources match
commit `b93885dcb70aae50c6f76b0fe4e0868f029a077e` from `ru_tts-for-nvda`.

## Implemented
1. Vendored backend sources in `ru_tts/vendor/`:
   - `ru_tts` core
   - `sonic` post-processor
   - `ru_tts_backend` bridge
2. Added shared backend library builder:
   - `ru_tts/build_backend.py`
   - Linux output: `bin/libru_tts_backend.so`
   - Windows output: `bin/ru_tts_backend.dll`
   - macOS output: `bin/libru_tts_backend.dylib`
3. Python engine (`ru_tts/engine.py`) uses `ctypes` with the native backend.
4. CLI (`ru_tts/cli.py`) has a single backend and supports legacy `ru_tts` arguments after `--`.
5. The adaptive v6.3.3 speech-rate algorithm is used by default; `-l` enables the legacy algorithm.

## Optional Next Improvements
1. Port text preprocessing rules from the original driver (`abbr/latin/braille normalization`) into a standalone module.
2. Add rulex dictionary support in the native backend build.
3. Extend audio regression coverage with stable output metrics for representative phrases.
