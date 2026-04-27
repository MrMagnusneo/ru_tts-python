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
- Два голоса: мужской по умолчанию и женский через legacy-флаг `-a`.
- Legacy-аргументы `ru_tts` после `--`: `-r`, `-p`, `-e`, `-g`, `-a`, `-d.`, `-d,`, `-d-`.
- Post-processing: `--sonic-speed` и `--volume`.
- Python API через `RuTTSPythonEngine`.
- Сборка одного исполняемого файла для текущей ОС.

### Запуск из исходников
Требования:
- Python 3.9+
- `gcc` для сборки нативного backend.
- На Windows нужен MinGW-w64 `gcc` в `PATH`, например из MSYS2 MinGW.

```bash
cd /home/x13/VScodeProjects/tts/ru_tts-python
python -m ru_tts --text "Привет, мир" --out out.wav --format wav
```

Backend собирается автоматически при первом запуске, если библиотека еще не создана. Принудительная сборка:

```bash
python -m ru_tts --build-backend --text "Тест" --out out.wav
```

CLI после установки пакета:

```bash
ru-tts-python --text "Привет" --out out.wav
```

### Примеры голосов
| Голос | Параметры | Пример |
| --- | --- | --- |
| Мужской | По умолчанию | `python -m ru_tts --text "Привет, мир!" --out ru_male.wav` |
| Женский | `-- -a` | `python -m ru_tts --text "Привет, мир!" --out ru_female.wav -- -a` |

### Python API
```python
from ru_tts import RuTTSPythonEngine

engine = RuTTSPythonEngine()
wav_bytes = engine.synthesize_wav("Привет, мир!")
engine.close()
```

### Сборка исполняемого файла
PyInstaller собирает бинарник под текущую ОС:
- Linux: `dist/ru-tts-python`
- Windows: `dist\ru-tts-python.exe`

Сначала подготовьте нативный backend. Команды одинаковые для Linux и Windows:

```bash
python -m pip install pyinstaller
python -c "from ru_tts.build_backend import build_backend; build_backend()"
python -m PyInstaller --clean ru-tts-python.spec
```

На Windows можно заменить `python` на `py`, если так настроен Python Launcher. Нативная библиотека называется `bin/libru_tts_backend.so` на Linux, `bin\ru_tts_backend.dll` на Windows и `bin/libru_tts_backend.dylib` на macOS.

### Проверка
```bash
python -m ru_tts --help
python -m ru_tts --text "Тест" --out /tmp/ru-tts-python-test.wav
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
- Two voices: male by default and female with the legacy `-a` flag.
- Legacy `ru_tts` arguments after `--`: `-r`, `-p`, `-e`, `-g`, `-a`, `-d.`, `-d,`, `-d-`.
- Post-processing controls: `--sonic-speed` and `--volume`.
- Python API through `RuTTSPythonEngine`.
- Single-file executable builds for the current OS.

### Run From Source
Requirements:
- Python 3.9+
- `gcc` to build the native backend.
- On Windows, MinGW-w64 `gcc` must be available in `PATH`, for example from MSYS2 MinGW.

```bash
cd /home/x13/VScodeProjects/tts/ru_tts-python
python -m ru_tts --text "Привет, мир" --out out.wav --format wav
```

The backend is built automatically on first run if the native library does not exist. To force a rebuild:

```bash
python -m ru_tts --build-backend --text "Тест" --out out.wav
```

Installed CLI:

```bash
ru-tts-python --text "Привет" --out out.wav
```

### Voice Examples
| Voice | Parameters | Example |
| --- | --- | --- |
| Male | Default | `python -m ru_tts --text "Привет, мир!" --out ru_male.wav` |
| Female | `-- -a` | `python -m ru_tts --text "Привет, мир!" --out ru_female.wav -- -a` |

### Python API
```python
from ru_tts import RuTTSPythonEngine

engine = RuTTSPythonEngine()
wav_bytes = engine.synthesize_wav("Привет, мир!")
engine.close()
```

### Build Executable
PyInstaller builds for the current OS:
- Linux: `dist/ru-tts-python`
- Windows: `dist\ru-tts-python.exe`

Prepare the native backend first. The commands are the same on Linux and Windows:

```bash
python -m pip install pyinstaller
python -c "from ru_tts.build_backend import build_backend; build_backend()"
python -m PyInstaller --clean ru-tts-python.spec
```

On Windows, replace `python` with `py` if that is how Python Launcher is configured. The native library is named `bin/libru_tts_backend.so` on Linux, `bin\ru_tts_backend.dll` on Windows, and `bin/libru_tts_backend.dylib` on macOS.

### Checks
```bash
python -m ru_tts --help
python -m ru_tts --text "Тест" --out /tmp/ru-tts-python-test.wav
```
