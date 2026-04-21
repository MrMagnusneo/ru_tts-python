from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional


SinkFn = Callable[[bytes, object], int]


@dataclass
class Sink:
    bufsize: int
    function: Optional[SinkFn] = None
    user_data: object = None
    custom_reset: Optional[Callable[["Sink"], None]] = None
    status: int = 0
    _buffer: bytearray = field(default_factory=bytearray)

    def reset(self) -> None:
        if self.custom_reset is not None:
            self.custom_reset(self)
        else:
            self._buffer.clear()

    def flush(self) -> None:
        if self.function and self._buffer:
            self.status |= int(self.function(bytes(self._buffer), self.user_data))
        self.reset()

    def put(self, value: int) -> None:
        self._buffer.append(value & 0xFF)
        if len(self._buffer) >= self.bufsize:
            self.flush()

    def write(self, block: bytes | bytearray | list[int]) -> None:
        self._buffer.extend(int(v) & 0xFF for v in block)
        if len(self._buffer) >= self.bufsize:
            self.flush()

    def back(self) -> None:
        if self._buffer:
            self._buffer.pop()

    def replace(self, value: int) -> None:
        self.back()
        self.put(value)

    def last(self) -> int:
        return self._buffer[-1] if self._buffer else -1
