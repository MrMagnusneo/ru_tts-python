# ru_tts_python

Python integration of ru_tts based on the newer `ru_tts-for-nvda` backend.

## What is included
- Python API/CLI in `ru_tts_port/`
- NVDA backend sources vendored in `ru_tts_port/vendor_nvda/` (`ru_tts` + `sonic` + bridge)
- Build scripts:
  - `ru_tts_port/build_nvda_backend.py` -> `bin/libru_tts_nvda.so`
  - `ru_tts_port/build_local.py` -> `bin/ru_tts_compat`

## Quick start
```bash
cd /home/x13/VScodeProjects/tts/ru_tts_python
python -m ru_tts_port --backend nvda --text "Привет, мир" --out out.wav --format wav
```

The NVDA backend is built automatically on first run. To force rebuild:
```bash
python -m ru_tts_port --backend nvda --build-nvda --text "Тест" --out out.wav
```

## Legacy options
You can still pass legacy `ru_tts` style arguments after `--`:
```bash
python -m ru_tts_port --backend nvda --text "Тест" --out out.wav -- -r 0.9 -p 1.1 -e 0.7
```

## Backends
- `--backend nvda` (default): newer backend (`ru_tts` + `sonic`), outputs 16-bit PCM.
- `--backend compat`: older compatibility mode using `ru_tts` executable, outputs 8-bit PCM.
