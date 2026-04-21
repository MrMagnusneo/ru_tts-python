import subprocess
from pathlib import Path


def build_local_binary() -> Path:
    base = Path(__file__).resolve().parents[1]
    src_dir = base / "ru_tts_port" / "vendor_nvda" / "ru_tts"
    out_dir = base / "bin"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_bin = out_dir / "ru_tts_compat"

    compat_header = Path(__file__).resolve().with_name("compat_config.h")
    config_h = src_dir / "config.h"
    config_h.write_text(compat_header.read_text(encoding="utf-8"), encoding="utf-8")
    c_files = sorted(str(p) for p in src_dir.glob("*.c"))

    cmd = [
        "gcc",
        "-O2",
        "-Wall",
        "-Wextra",
        "-std=gnu11",
        "-DWITHOUT_DICTIONARY",
        "-o",
        str(out_bin),
        *c_files,
        "-lm",
        "-ldl",
    ]
    proc = subprocess.run(cmd, cwd=str(src_dir), check=False, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"Build failed:\n{proc.stdout}\n{proc.stderr}")

    out_bin.chmod(0o755)
    return out_bin
