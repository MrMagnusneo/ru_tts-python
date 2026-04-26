# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path


base = Path(SPECPATH)
lib_name = "ru_tts_backend.dll" if sys.platform == "win32" else "libru_tts_backend.dylib" if sys.platform == "darwin" else "libru_tts_backend.so"
binary_specs = [(str(base / "bin" / lib_name), "bin")]


a = Analysis(
    [str(base / "ru_tts" / "__main__.py")],
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
