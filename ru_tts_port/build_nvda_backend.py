from __future__ import annotations

import os
import sys
import subprocess
from pathlib import Path


def nvda_library_name() -> str:
    if sys.platform == "win32":
        return "ru_tts_nvda.dll"
    if sys.platform == "darwin":
        return "libru_tts_nvda.dylib"
    return "libru_tts_nvda.so"


def build_nvda_backend() -> Path:
    base = Path(__file__).resolve().parents[1]
    vendor = base / "ru_tts_port" / "vendor_nvda"

    bridge = vendor / "bridge"
    sonic = vendor / "sonic"
    ru_tts = vendor / "ru_tts"

    out_dir = base / "bin"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_lib = out_dir / nvda_library_name()

    sources = [
        bridge / "ru_tts_nvda.c",
        sonic / "sonic.c",
        ru_tts / "utterance.c",
        ru_tts / "transcription.c",
        ru_tts / "time_planner.c",
        ru_tts / "text2speech.c",
        ru_tts / "synth.c",
        ru_tts / "speechrate_control.c",
        ru_tts / "soundproducer.c",
        ru_tts / "sink.c",
        ru_tts / "numerics.c",
        ru_tts / "male.c",
        ru_tts / "intonator.c",
        ru_tts / "female.c",
    ]

    cmd = [
        "gcc",
        "-shared",
        "-O3",
        "-std=c11",
        "-Wall",
        "-Wextra",
        "-Wno-sign-compare",
        "-Wno-implicit-fallthrough",
        "-Wno-unused-parameter",
        "-o",
        str(out_lib),
        *[str(s) for s in sources],
        "-I" + str(bridge),
        "-I" + str(sonic),
        "-I" + str(ru_tts),
    ]
    if sys.platform != "win32":
        cmd[2:2] = ["-fPIC"]
        cmd.append("-lm")
    else:
        cmd.append("-static-libgcc")
    if os.name != "nt":
        cmd[5:5] = ["-D_GNU_SOURCE"]

    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"Failed to build {out_lib.name}\n{proc.stdout}\n{proc.stderr}")

    if os.name != "nt":
        out_lib.chmod(0o755)
    return out_lib
