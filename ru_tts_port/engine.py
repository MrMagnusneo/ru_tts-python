from __future__ import annotations

import os
import shutil
import subprocess
import sys
import wave
from ctypes import CFUNCTYPE, CDLL, POINTER, Structure, byref, c_char_p, c_float, c_int, c_size_t, c_void_p, string_at
from pathlib import Path
from typing import List, Optional

from .build_nvda_backend import build_nvda_backend, nvda_library_name


DEC_SEP_POINT = 1
DEC_SEP_COMMA = 2
USE_ALTERNATIVE_VOICE = 4


class RU_TTS_CONF_T(Structure):
    _fields_ = [
        ("speech_rate", c_int),
        ("voice_pitch", c_int),
        ("intonation", c_int),
        ("general_gap_factor", c_int),
        ("comma_gap_factor", c_int),
        ("dot_gap_factor", c_int),
        ("semicolon_gap_factor", c_int),
        ("colon_gap_factor", c_int),
        ("question_gap_factor", c_int),
        ("exclamation_gap_factor", c_int),
        ("intonational_gap_factor", c_int),
        ("flags", c_int),
    ]


def _clamp_i(value: float, lo: int, hi: int) -> int:
    iv = int(round(value))
    if iv < lo:
        return lo
    if iv > hi:
        return hi
    return iv


def _app_base() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)  # type: ignore[attr-defined]
    return Path(__file__).resolve().parents[1]


class RuTTSPythonEngine:
    def __init__(
        self,
        backend: str = "nvda",
        lib_path: Optional[str] = None,
        binary: Optional[str] = None,
        auto_build: bool = True,
    ):
        self.backend = backend
        self._compat_binary = binary

        self._lib = None
        self._tts = None
        self._audio_chunks: list[bytes] = []
        self._callback = None

        if self.backend == "nvda":
            self._init_nvda_backend(lib_path=lib_path, auto_build=auto_build)
        elif self.backend == "compat":
            self._compat_binary = binary or self._detect_compat_binary()
        else:
            raise ValueError("backend must be 'nvda' or 'compat'")

    def _init_nvda_backend(self, lib_path: Optional[str], auto_build: bool) -> None:
        base = _app_base()
        default_lib = base / "bin" / nvda_library_name()

        if lib_path is not None:
            so_path = Path(lib_path)
        else:
            env_lib = os.environ.get("RU_TTS_NVDA_LIB")
            so_path = Path(env_lib) if env_lib else default_lib

        if not so_path.exists():
            if not auto_build:
                raise FileNotFoundError(f"NVDA backend library not found: {so_path}")
            so_path = build_nvda_backend()

        self._lib = CDLL(str(so_path))

        cb_type = CFUNCTYPE(c_int, c_void_p, c_size_t, c_void_p)

        def _audio_callback(buffer: c_void_p, size: int, _user_data: c_void_p) -> int:
            try:
                # size is number of int16 samples.
                self._audio_chunks.append(string_at(buffer, int(size) * 2))
                return 0
            except Exception:
                return 1

        self._callback = cb_type(_audio_callback)

        self._lib.tts_create.argtypes = (cb_type,)
        self._lib.tts_create.restype = c_void_p
        self._lib.tts_destroy.argtypes = (c_void_p,)
        self._lib.tts_destroy.restype = None
        self._lib.tts_speak.argtypes = (c_void_p, POINTER(RU_TTS_CONF_T), c_char_p)
        self._lib.tts_speak.restype = None
        self._lib.tts_setVolume.argtypes = (c_void_p, c_float)
        self._lib.tts_setVolume.restype = None
        self._lib.tts_setSpeed.argtypes = (c_void_p, c_float)
        self._lib.tts_setSpeed.restype = None
        self._lib.ru_tts_config_init.argtypes = (POINTER(RU_TTS_CONF_T),)
        self._lib.ru_tts_config_init.restype = None

        self._tts = self._lib.tts_create(self._callback)
        if not self._tts:
            raise RuntimeError("Failed to create NVDA ru_tts instance")

    @staticmethod
    def _detect_compat_binary() -> str:
        env_bin = os.environ.get("RU_TTS_BIN")
        if env_bin and Path(env_bin).exists():
            return env_bin

        base = _app_base()
        exe_name = "ru_tts_compat.exe" if sys.platform == "win32" else "ru_tts_compat"
        local_candidates = [
            base / "bin" / exe_name,
        ]
        for candidate in local_candidates:
            if candidate.exists() and os.access(candidate, os.X_OK):
                return str(candidate)

        global_bin = shutil.which("ru_tts")
        if global_bin:
            return global_bin

        raise FileNotFoundError("ru_tts compat binary was not found. Build local binary or set RU_TTS_BIN.")

    def _apply_legacy_args(self, conf: RU_TTS_CONF_T, args: Optional[List[str]]) -> None:
        if not args:
            return

        i = 0
        while i < len(args):
            a = args[i]
            if a == "-a":
                conf.flags |= USE_ALTERNATIVE_VOICE
            elif a in ("-d.", "-d,", "-d-"):
                conf.flags &= ~(DEC_SEP_POINT | DEC_SEP_COMMA)
                if a == "-d.":
                    conf.flags |= DEC_SEP_POINT
                elif a == "-d,":
                    conf.flags |= DEC_SEP_COMMA
            elif a in ("-r", "-p", "-e", "-g") and i + 1 < len(args):
                value = float(args[i + 1])
                if a == "-r":
                    conf.speech_rate = _clamp_i(conf.speech_rate * value, 20, 500)
                elif a == "-p":
                    conf.voice_pitch = _clamp_i(conf.voice_pitch * value, 50, 300)
                elif a == "-e":
                    conf.intonation = _clamp_i(conf.intonation * value, 0, 140)
                elif a == "-g":
                    conf.general_gap_factor = max(0, _clamp_i(conf.general_gap_factor * value, 0, 2000))
                i += 1
            i += 1

    def synthesize_raw(
        self,
        text: str,
        args: Optional[List[str]] = None,
        sonic_speed: float = 1.0,
        volume: float = 1.0,
    ) -> bytes:
        if self.backend == "compat":
            cmd = [self._compat_binary]
            if args:
                cmd.extend(args)
            proc = subprocess.run(
                cmd,
                input=text.encode("koi8-r", errors="replace"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            if proc.returncode != 0:
                raise RuntimeError(proc.stderr.decode("utf-8", errors="replace").strip() or "compat ru_tts failed")
            return proc.stdout

        self._audio_chunks.clear()

        conf = RU_TTS_CONF_T()
        self._lib.ru_tts_config_init(byref(conf))
        self._apply_legacy_args(conf, args)

        self._lib.tts_setSpeed(self._tts, c_float(max(0.5, min(4.0, sonic_speed))))
        self._lib.tts_setVolume(self._tts, c_float(max(0.0, min(3.0, volume))))

        payload = text.encode("koi8-r", errors="replace")
        self._lib.tts_speak(self._tts, byref(conf), c_char_p(payload))

        return b"".join(self._audio_chunks)

    def synthesize_wav(
        self,
        text: str,
        args: Optional[List[str]] = None,
        sonic_speed: float = 1.0,
        volume: float = 1.0,
    ) -> bytes:
        raw = self.synthesize_raw(text=text, args=args, sonic_speed=sonic_speed, volume=volume)

        if self.backend == "compat":
            # 8-bit unsigned mono PCM, 10kHz
            import io

            bio = io.BytesIO()
            with wave.open(bio, "wb") as w:
                w.setnchannels(1)
                w.setsampwidth(1)
                w.setframerate(10000)
                w.writeframes(raw)
            return bio.getvalue()

        # NVDA backend returns 16-bit signed little-endian mono PCM, 10kHz
        import io

        bio = io.BytesIO()
        with wave.open(bio, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(10000)
            w.writeframes(raw)
        return bio.getvalue()

    def close(self) -> None:
        if self._tts and self._lib:
            self._lib.tts_destroy(self._tts)
            self._tts = None

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass
