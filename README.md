# ru-tts-python

## Contents
- [Русский](#русский)
- [English](#english)

## Русский

### О проекте
`ru-tts-python` - Python CLI и API для `ru_tts`. Python-часть управляет синтезом, а аудио генерируется одним нативным backend.

Оригинальные проекты:
- `ru_tts`: https://github.com/poretsky/ru_tts

### Структура
- `ru_tts/` - Python-пакет, CLI и API.
- `ru_tts/vendor/` - C-исходники backend.
- `ru_tts/native/` - Python-интеграция с нативным backend.
- `ru_tts/build_backend.py` - сборка нативной backend-библиотеки.
- `bin/` - собранные локальные backend-артефакты.
- `ru-tts-python.spec` - spec-файл PyInstaller.

### Возможности
- Синтез русской речи в WAV или raw PCM.
- Ввод текста через `--text` или stdin.
- Единый backend: `ru_tts` + `sonic`, 16-bit PCM.
- Legacy-аргументы `ru_tts` после `--`: `-r`, `-p`, `-e`, `-g`, `-a`, `-d.`, `-d,`, `-d-`.
- Post-processing: `--sonic-speed` и `--volume`.
- Сборка одного исполняемого файла для текущей ОС.

### Запуск из исходников
Требования:
- Python 3.9+
- `gcc` для сборки нативного backend.
- На Windows нужен MinGW-w64 `gcc` в `PATH`, например из MSYS2 MinGW.

```bash
cd /home/x13/VScodeProjects/tts/ru-tts-python
python -m ru_tts --text "Привет, мир" --out out.wav --format wav
```

Backend собирается автоматически при первом запуске, если библиотека еще не создана. Принудительная сборка:

```bash
python -m ru_tts --build-backend --text "Тест" --out out.wav
```

Пример legacy-аргументов:

```bash
python -m ru_tts --text "Тест" --out out.wav -- -r 0.9 -p 1.1 -e 0.7
```

CLI после установки пакета:

```bash
ru-tts-python --text "Привет" --out out.wav
```

### Сборка исполняемого файла
PyInstaller собирает бинарник под текущую ОС:
- Linux: `dist/ru-tts-python`
- Windows: `dist\ru-tts-python.exe`

```bash
python -m pip install pyinstaller
python -c "from ru_tts.build_backend import build_backend; build_backend()"
python -m PyInstaller --clean ru-tts-python.spec
```

Нативная библиотека называется `bin/libru_tts_backend.so` на Linux, `bin\ru_tts_backend.dll` на Windows и `bin/libru_tts_backend.dylib` на macOS.

### Быстрая проверка
```bash
python -m ru_tts --help
```

## English

### About
`ru-tts-python` is a Python CLI and API for `ru_tts`. The Python layer controls synthesis, while audio generation is provided by a single native backend.

Original projects:
- `ru_tts`: https://github.com/poretsky/ru_tts

### Layout
- `ru_tts/` - Python package, CLI, and API.
- `ru_tts/vendor/` - C backend sources.
- `ru_tts/native/` - Python integration with the native backend.
- `ru_tts/build_backend.py` - native backend library builder.
- `bin/` - locally built backend artifacts.
- `ru-tts-python.spec` - PyInstaller spec file.

### Features
- Russian speech synthesis to WAV or raw PCM.
- Text input through `--text` or stdin.
- Single backend: `ru_tts` + `sonic`, 16-bit PCM.
- Legacy `ru_tts` arguments after `--`: `-r`, `-p`, `-e`, `-g`, `-a`, `-d.`, `-d,`, `-d-`.
- Post-processing controls: `--sonic-speed` and `--volume`.
- Single-file executable builds for the current OS.

### Run From Source
Requirements:
- Python 3.9+
- `gcc` to build the native backend.
- On Windows, MinGW-w64 `gcc` must be available in `PATH`, for example from MSYS2 MinGW.

```bash
cd /home/x13/VScodeProjects/tts/ru-tts-python
python -m ru_tts --text "Привет, мир" --out out.wav --format wav
```

The backend is built automatically on first run if the native library does not exist. To force a rebuild:

```bash
python -m ru_tts --build-backend --text "Тест" --out out.wav
```

Legacy argument example:

```bash
python -m ru_tts --text "Тест" --out out.wav -- -r 0.9 -p 1.1 -e 0.7
```

Installed CLI:

```bash
ru-tts-python --text "Привет" --out out.wav
```

### Build Executable
PyInstaller builds for the current OS:
- Linux: `dist/ru-tts-python`
- Windows: `dist\ru-tts-python.exe`

```bash
python -m pip install pyinstaller
python -c "from ru_tts.build_backend import build_backend; build_backend()"
python -m PyInstaller --clean ru-tts-python.spec
```

The native library is named `bin/libru_tts_backend.so` on Linux, `bin\ru_tts_backend.dll` on Windows, and `bin/libru_tts_backend.dylib` on macOS.

### Smoke Test
```bash
python -m ru_tts --help
```
