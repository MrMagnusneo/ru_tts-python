import argparse
import sys
from pathlib import Path

from .build_local import build_local_binary
from .build_nvda_backend import build_nvda_backend
from .engine import RuTTSPythonEngine


def main() -> int:
    parser = argparse.ArgumentParser(description="ru_tts Python (NVDA-based backend)")
    parser.add_argument("--text", help="Input text. If not set, text is read from stdin.")
    parser.add_argument("--out", default="ru_tts.wav", help="Output path")
    parser.add_argument("--format", choices=["wav", "raw"], default="wav", help="Output audio format")
    parser.add_argument("--backend", choices=["nvda", "compat"], default="nvda")
    parser.add_argument("--bin", help="Path to ru_tts executable (compat backend)")
    parser.add_argument("--lib", help="Path to libru_tts_nvda.so (nvda backend)")
    parser.add_argument("--build-local", action="store_true", help="Build local compatible ru_tts binary first")
    parser.add_argument("--build-nvda", action="store_true", help="Force rebuild NVDA backend library before synthesis")
    parser.add_argument("--sonic-speed", type=float, default=1.0, help="Post-processing speed factor for nvda backend")
    parser.add_argument("--volume", type=float, default=1.0, help="Post-processing volume factor for nvda backend")
    parser.add_argument("tts_args", nargs=argparse.REMAINDER, help="Legacy ru_tts args: -r -p -e -g -a -d.")
    args = parser.parse_args()

    text = args.text if args.text is not None else sys.stdin.read().strip()
    if not text:
        parser.error("No input text provided")

    extra_args = args.tts_args
    if extra_args and extra_args[0] == "--":
        extra_args = extra_args[1:]

    binary = args.bin
    if args.build_local:
        binary = str(build_local_binary())
        print(f"Built local binary: {binary}")
    if args.build_nvda and args.backend == "nvda":
        lib_path = build_nvda_backend()
        if not args.lib:
            args.lib = str(lib_path)
        print(f"Built NVDA backend: {args.lib}")

    auto_build = True
    engine = RuTTSPythonEngine(
        backend=args.backend,
        lib_path=args.lib,
        binary=binary,
        auto_build=auto_build,
    )

    if args.format == "raw":
        audio = engine.synthesize_raw(text, args=extra_args, sonic_speed=args.sonic_speed, volume=args.volume)
    else:
        audio = engine.synthesize_wav(text, args=extra_args, sonic_speed=args.sonic_speed, volume=args.volume)

    out_path = Path(args.out)
    out_path.write_bytes(audio)
    print(f"{args.format.upper()} audio saved to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
