# ru-tts-python

## Contents
- [Русский](#русский)
- [English](#english)

## Русский

### О проекте
`ru-tts-python` - Python CLI и API для `ru_tts` на базе обновленного backend из `ru_tts-for-nvda`. Это не полный перенос C-кода в Python: Python-часть управляет синтезом, а аудио backend собирается в нативную библиотеку.

Оригинальные проекты:
- `ru_tts`: https://github.com/poretsky/ru_tts
- `ru_tts-for-nvda`: https://gitverse.ru/kvark128/ru_tts-for-nvda

### Структура
- `ru_tts_python/` - Python-пакет, CLI и API.
- `ru_tts_python/vendor_nvda/` - C-исходники backend из NVDA-порта.
- `ru_tts_python/native/` - Python-интеграция с нативным backend.
- `bin/` - собранные локальные backend-артефакты.
- `build_executable.py` - сборка backend и одного исполняемого файла через PyInstaller.
- `pyinstaller_entry.py` - точка входа для PyInstaller.
- `ru-tts-python.spec` - spec-файл PyInstaller.

### Возможности
- Синтез русской речи в WAV или raw PCM.
- Ввод текста через `--text` или stdin.
- Backend `nvda` по умолчанию: `ru_tts` + `sonic`, 16-bit PCM.
- Backend `compat`: совместимый режим через бинарник `ru_tts_compat`, 8-bit PCM.
- Legacy-аргументы `ru_tts` после `--`: `-r`, `-p`, `-e`, `-g`, `-a`, `-d.`, `-d,`, `-d-`.
- Post-processing для `nvda`: `--sonic-speed` и `--volume`.
- Сборка одного исполняемого файла для текущей ОС.

### Запуск из исходников
Требования:
- Python 3.9+
- `gcc` для сборки нативного `nvda` backend.
- На Windows нужен MinGW-w64 `gcc` в `PATH`, например из MSYS2 MinGW.

```bash
cd /home/x13/VScodeProjects/tts/ru-tts-python
python -m ru_tts_python --backend nvda --text "Привет, мир" --out out.wav --format wav
```

Backend `nvda` собирается автоматически при первом запуске, если библиотека еще не создана. Принудительная сборка:

```bash
python -m ru_tts_python --backend nvda --build-nvda --text "Тест" --out out.wav
```

Сборка совместимого backend:

```bash
python -m ru_tts_python --backend compat --build-compat --text "Тест" --out out.wav
```

Пример legacy-аргументов:

```bash
python -m ru_tts_python --backend nvda --text "Тест" --out out.wav -- -r 0.9 -p 1.1 -e 0.7
```

CLI после установки пакета:

```bash
ru-tts-python --backend nvda --text "Привет" --out out.wav
```

### Сборка исполняемого файла
PyInstaller собирает бинарник под текущую ОС:
- Linux: `dist/ru-tts-python`
- Windows: `dist\ru-tts-python.exe`

```bash
python -m pip install pyinstaller
python build_executable.py
```

Скрипт всегда собирает и упаковывает `nvda` backend. `compat` backend также собирается и добавляется, если это возможно в текущем окружении.

То же через spec-файл после сборки backend:

```bash
python -m PyInstaller --clean ru-tts-python.spec
```

Нативная библиотека называется `bin/libru_tts_nvda.so` на Linux, `bin\ru_tts_nvda.dll` на Windows и `bin/libru_tts_nvda.dylib` на macOS.

### Быстрая проверка
```bash
python -m ru_tts_python --help
```

## English

### About
`ru-tts-python` is a Python CLI and API for `ru_tts` using the updated backend from `ru_tts-for-nvda`. This is not a full C-to-Python rewrite: the Python layer controls synthesis, while audio generation is provided by a compiled native backend.

Original projects:
- `ru_tts`: https://github.com/poretsky/ru_tts
- `ru_tts-for-nvda`: https://gitverse.ru/kvark128/ru_tts-for-nvda

### Layout
- `ru_tts_python/` - Python package, CLI, and API.
- `ru_tts_python/vendor_nvda/` - C backend sources from the NVDA port.
- `ru_tts_python/native/` - Python integration with the native backend.
- `bin/` - locally built backend artifacts.
- `build_executable.py` - backend and executable build helper.
- `pyinstaller_entry.py` - PyInstaller entry point.
- `ru-tts-python.spec` - PyInstaller spec file.

### Features
- Russian speech synthesis to WAV or raw PCM.
- Text input through `--text` or stdin.
- Default `nvda` backend: `ru_tts` + `sonic`, 16-bit PCM.
- `compat` backend: compatibility mode through the `ru_tts_compat` binary, 8-bit PCM.
- Legacy `ru_tts` arguments after `--`: `-r`, `-p`, `-e`, `-g`, `-a`, `-d.`, `-d,`, `-d-`.
- `nvda` post-processing controls: `--sonic-speed` and `--volume`.
- Single-file executable builds for the current OS.

### Run From Source
Requirements:
- Python 3.9+
- `gcc` to build the native `nvda` backend.
- On Windows, MinGW-w64 `gcc` must be available in `PATH`, for example from MSYS2 MinGW.

```bash
cd /home/x13/VScodeProjects/tts/ru-tts-python
python -m ru_tts_python --backend nvda --text "Привет, мир" --out out.wav --format wav
```

The `nvda` backend is built automatically on first run if the native library does not exist. To force a rebuild:

```bash
python -m ru_tts_python --backend nvda --build-nvda --text "Тест" --out out.wav
```

Build the compatibility backend:

```bash
python -m ru_tts_python --backend compat --build-compat --text "Тест" --out out.wav
```

Legacy argument example:

```bash
python -m ru_tts_python --backend nvda --text "Тест" --out out.wav -- -r 0.9 -p 1.1 -e 0.7
```

Installed CLI:

```bash
ru-tts-python --backend nvda --text "Привет" --out out.wav
```

### Build Executable
PyInstaller builds for the current OS:
- Linux: `dist/ru-tts-python`
- Windows: `dist\ru-tts-python.exe`

```bash
python -m pip install pyinstaller
python build_executable.py
```

The script always builds and bundles the `nvda` backend. It also builds and bundles the `compat` backend when the current environment can build it.

The spec file can also be used directly after the backend exists:

```bash
python -m PyInstaller --clean ru-tts-python.spec
```

The native library is named `bin/libru_tts_nvda.so` on Linux, `bin\ru_tts_nvda.dll` on Windows, and `bin/libru_tts_nvda.dylib` on macOS.

### Smoke Test
```bash
python -m ru_tts_python --help
```
