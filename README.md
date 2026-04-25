# ru-tts-python

## Содержание / Contents
- [Русский](#русский)
- [English](#english)

## Русский

### О проекте
`ru-tts-python` - Python CLI и API для `ru_tts` на базе обновленного backend из `ru_tts-for-nvda`. Это не полный перенос C-кода в Python: Python-часть управляет синтезом, а звуковой backend собирается в нативную библиотеку.

Оригинальные репозитории:
- `ru_tts`: https://github.com/poretsky/ru_tts
- `ru_tts-for-nvda`: https://gitverse.ru/kvark128/ru_tts-for-nvda

### Функционал
- Синтез русской речи в WAV или raw PCM.
- Ввод текста через `--text` или stdin.
- Backend `nvda` по умолчанию: `ru_tts` + `sonic`, вывод 16-bit PCM.
- Backend `compat`: совместимый режим через бинарник `ru_tts_compat`, вывод 8-bit PCM.
- Поддержка legacy-аргументов `ru_tts` после `--`: `-r`, `-p`, `-e`, `-g`, `-a`, `-d.`, `-d,`, `-d-`.
- Настройки post-processing для `nvda`: `--sonic-speed` и `--volume`.
- Сборка одного исполняемого файла для Linux или Windows.

### Запуск из исходников
Требования:
- Python 3.9+
- `gcc` для сборки нативного `nvda` backend.
- На Windows нужен MinGW-w64 `gcc` в `PATH`, например из MSYS2 MinGW.

```bash
cd /home/x13/VScodeProjects/tts/ru_tts-python
python -m ru_tts_port --backend nvda --text "Привет, мир" --out out.wav --format wav
```

Backend `nvda` собирается автоматически при первом запуске, если библиотека еще не создана. Принудительная сборка:
```bash
python -m ru_tts_port --backend nvda --build-nvda --text "Тест" --out out.wav
```

Сборка совместимого backend:
```bash
python -m ru_tts_port --backend compat --build-compat --text "Тест" --out out.wav
```

Пример legacy-аргументов:
```bash
python -m ru_tts_port --backend nvda --text "Тест" --out out.wav -- -r 0.9 -p 1.1 -e 0.7
```

### Сборка одного исполняемого файла
PyInstaller собирает исполняемый файл под ту ОС, на которой запущена сборка:
- Linux: `dist/ru-tts-python`
- Windows: `dist\ru-tts-python.exe`

Установите PyInstaller:
```bash
python -m pip install pyinstaller
```

Соберите нативный backend и один исполняемый файл:
```bash
python build_executable.py
```

Скрипт всегда собирает и упаковывает `nvda` backend. `compat` backend также собирается и добавляется в сборку, если это возможно в текущем окружении.

То же самое можно сделать через spec-файл после сборки нативного backend:
```bash
python -m PyInstaller --clean ru-tts-python.spec
```

Нативная библиотека называется `bin/libru_tts_nvda.so` на Linux и `bin\ru_tts_nvda.dll` на Windows.

## English

### About
`ru-tts-python` is a Python CLI and API for `ru_tts` using the updated backend from `ru_tts-for-nvda`. This is not a full C-to-Python rewrite: the Python layer controls synthesis, while audio generation is provided by a compiled native backend library.

Original repositories:
- `ru_tts`: https://github.com/poretsky/ru_tts
- `ru_tts-for-nvda`: https://gitverse.ru/kvark128/ru_tts-for-nvda

### Features
- Russian speech synthesis to WAV or raw PCM.
- Text input via `--text` or stdin.
- Default `nvda` backend: `ru_tts` + `sonic`, 16-bit PCM output.
- `compat` backend: compatibility mode through the `ru_tts_compat` binary, 8-bit PCM output.
- Legacy `ru_tts` arguments after `--`: `-r`, `-p`, `-e`, `-g`, `-a`, `-d.`, `-d,`, `-d-`.
- `nvda` post-processing controls: `--sonic-speed` and `--volume`.
- Single-file executable builds for Linux or Windows.

### Run From Source
Requirements:
- Python 3.9+
- `gcc` to build the native `nvda` backend.
- On Windows, MinGW-w64 `gcc` must be available in `PATH`, for example from MSYS2 MinGW.

```bash
cd /home/x13/VScodeProjects/tts/ru_tts-python
python -m ru_tts_port --backend nvda --text "Привет, мир" --out out.wav --format wav
```

The `nvda` backend is built automatically on first run if the native library does not exist yet. To force a rebuild:
```bash
python -m ru_tts_port --backend nvda --build-nvda --text "Тест" --out out.wav
```

Build the compatibility backend:
```bash
python -m ru_tts_port --backend compat --build-compat --text "Тест" --out out.wav
```

Legacy argument example:
```bash
python -m ru_tts_port --backend nvda --text "Тест" --out out.wav -- -r 0.9 -p 1.1 -e 0.7
```

### Single-File Build
PyInstaller builds an executable for the OS where the build is run:
- Linux: `dist/ru-tts-python`
- Windows: `dist\ru-tts-python.exe`

Install PyInstaller:
```bash
python -m pip install pyinstaller
```

Build the native backend and one executable:
```bash
python build_executable.py
```

The script always builds and bundles the `nvda` backend. It also builds and bundles the `compat` backend when the current environment can build it.

You can also build from the checked-in spec file after the native backend exists:
```bash
python -m PyInstaller --clean ru-tts-python.spec
```

The native library is named `bin/libru_tts_nvda.so` on Linux and `bin\ru_tts_nvda.dll` on Windows.
