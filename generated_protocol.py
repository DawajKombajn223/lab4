"""Generated protocol classes for binary serialization and deserialization."""

from __future__ import annotations

import struct
from dataclasses import dataclass
from typing import Tuple


def _encode_string(value: str) -> bytes:
    encoded = value.encode("utf-8")
    return struct.pack("<I", len(encoded)) + encoded


def _decode_string(data: bytes, offset: int) -> Tuple[str, int]:
    length = struct.unpack_from("<I", data, offset)[0]
    offset += 4
    value = data[offset:offset + length].decode("utf-8")
    return value, offset + length

@dataclass
class ChatMessage:
    sender: str
    recipient: str
    timestamp: uint32
    body: str

    def serialize(self) -> bytes:
        parts = []
        parts.append(_encode_string(self.sender))
        parts.append(_encode_string(self.recipient))
        parts.append(struct.pack("<I", self.timestamp))
        parts.append(_encode_string(self.body))
        return b"".join(parts)

    @classmethod
    def deserialize_from(cls, data: bytes, offset: int = 0) -> Tuple["ChatMessage", int]:
        sender, offset = _decode_string(data, offset)
        recipient, offset = _decode_string(data, offset)
        timestamp = struct.unpack_from("<I", data, offset)[0]
        offset += struct.calcsize("<I")
        body, offset = _decode_string(data, offset)
        return cls(
            sender=sender,
            recipient=recipient,
            timestamp=timestamp,
            body=body
        ), offset

@dataclass
class Ack:
    status: uint8
    message: str

    def serialize(self) -> bytes:
        parts = []
        parts.append(struct.pack("<B", self.status))
        parts.append(_encode_string(self.message))
        return b"".join(parts)

    @classmethod
    def deserialize_from(cls, data: bytes, offset: int = 0) -> Tuple["Ack", int]:
        status = struct.unpack_from("<B", data, offset)[0]
        offset += struct.calcsize("<B")
        message, offset = _decode_string(data, offset)
        return cls(
            status=status,
            message=message
        ), offset

