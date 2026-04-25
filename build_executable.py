from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from importlib.util import find_spec

from ru_tts_port.build_compat_backend import build_compat_backend
from ru_tts_port.build_nvda_backend import build_nvda_backend, nvda_library_name


def main() -> int:
    base = Path(__file__).resolve().parent
    if find_spec("PyInstaller") is None:
        print("PyInstaller is not installed. Run: python -m pip install pyinstaller", file=sys.stderr)
        return 1

    build_nvda_backend()
    try:
        build_compat_backend()
    except Exception as exc:
        print(f"Warning: compat backend was not built and will not be bundled: {exc}", file=sys.stderr)

    name = "ru-tts-python"

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--clean",
        str(base / "ru-tts-python.spec"),
    ]

    print(f"Bundling {nvda_library_name()} into dist/{name}{'.exe' if sys.platform == 'win32' else ''}")
    return subprocess.call(cmd, cwd=str(base))


if __name__ == "__main__":
    raise SystemExit(main())
