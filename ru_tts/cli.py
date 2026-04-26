import argparse
import sys
from pathlib import Path

from .build_backend import build_backend
from .engine import RuTTSPythonEngine


def main() -> int:
    parser = argparse.ArgumentParser(description="ru_tts Python")
    parser.add_argument("--text", help="Input text. If not set, text is read from stdin.")
    parser.add_argument("--out", default="ru_tts.wav", help="Output path")
    parser.add_argument("--format", choices=["wav", "raw"], default="wav", help="Output audio format")
    parser.add_argument("--lib", help="Path to ru_tts backend library")
    parser.add_argument("--build-backend", action="store_true", help="Force rebuild backend library before synthesis")
    parser.add_argument("--sonic-speed", type=float, default=1.0, help="Post-processing speed factor")
    parser.add_argument("--volume", type=float, default=1.0, help="Post-processing volume factor")
    parser.add_argument("tts_args", nargs=argparse.REMAINDER, help="Legacy ru_tts args: -r -p -e -g -a -d.")
    args = parser.parse_args()

    text = args.text if args.text is not None else sys.stdin.read().strip()
    if not text:
        parser.error("No input text provided")

    extra_args = args.tts_args
    if extra_args and extra_args[0] == "--":
        extra_args = extra_args[1:]

    if args.build_backend:
        lib_path = build_backend()
        if not args.lib:
            args.lib = str(lib_path)
        print(f"Built backend: {args.lib}")

    auto_build = True
    engine = RuTTSPythonEngine(
        lib_path=args.lib,
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
