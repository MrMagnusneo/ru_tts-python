# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path


base = Path(SPECPATH)
lib_name = "ru_tts_nvda.dll" if sys.platform == "win32" else "libru_tts_nvda.dylib" if sys.platform == "darwin" else "libru_tts_nvda.so"
binary_specs = [(str(base / "bin" / lib_name), "bin")]

compat_name = "ru_tts_compat.exe" if sys.platform == "win32" else "ru_tts_compat"
compat_path = base / "bin" / compat_name
if compat_path.exists():
    binary_specs.append((str(compat_path), "bin"))


a = Analysis(
    [str(base / "pyinstaller_entry.py")],
    pathex=[str(base)],
    binaries=binary_specs,
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="ru-tts-python",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
