# ru-tts-python Status

Current direction changed from full C->Python transliteration to integration of the newer `ru_tts-for-nvda` backend.

## Implemented
1. Vendored updated sources in `ru_tts_port/vendor_nvda/`:
   - `ru_tts` core
   - `sonic` post-processor
   - `ru_tts_nvda` bridge
2. Added Linux build pipeline for shared backend library:
   - `ru_tts_port/build_nvda_backend.py`
   - Linux output: `bin/libru_tts_nvda.so`
   - Windows output: `bin/ru_tts_nvda.dll`
3. Reworked Python engine (`ru_tts_port/engine.py`) to use `ctypes` with the new backend.
4. Reworked CLI (`ru_tts_port/cli.py`) with backend selection:
   - `nvda` (default)
   - `compat`

## Optional next improvements
1. Port text preprocessing rules from NVDA driver (`abbr/latin/braille normalization`) into standalone module.
2. Add rulex dictionary support in Linux build.
3. Add regression tests comparing `compat` and `nvda` output metrics.
