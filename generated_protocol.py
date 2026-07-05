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
class SensorReading:
    sensor_id: str
    location: str
    temperature_c: float
    humidity_pct: float
    timestamp: int
    battery_pct: int

    def serialize(self) -> bytes:
        parts = []
        parts.append(_encode_string(self.sensor_id))
        parts.append(_encode_string(self.location))
        parts.append(struct.pack("<f", self.temperature_c))
        parts.append(struct.pack("<f", self.humidity_pct))
        parts.append(struct.pack("<I", self.timestamp))
        parts.append(struct.pack("<B", self.battery_pct))
        return b"".join(parts)

    @classmethod
    def deserialize_from(cls, data: bytes, offset: int = 0) -> Tuple["SensorReading", int]:
        sensor_id, offset = _decode_string(data, offset)
        location, offset = _decode_string(data, offset)
        temperature_c = struct.unpack_from("<f", data, offset)[0]
        offset += struct.calcsize("<f")
        humidity_pct = struct.unpack_from("<f", data, offset)[0]
        offset += struct.calcsize("<f")
        timestamp = struct.unpack_from("<I", data, offset)[0]
        offset += struct.calcsize("<I")
        battery_pct = struct.unpack_from("<B", data, offset)[0]
        offset += struct.calcsize("<B")
        return cls(
            sensor_id=sensor_id,
            location=location,
            temperature_c=temperature_c,
            humidity_pct=humidity_pct,
            timestamp=timestamp,
            battery_pct=battery_pct
        ), offset

@dataclass
class ReceiverAck:
    receiver_id: str
    status_code: int
    message: str

    def serialize(self) -> bytes:
        parts = []
        parts.append(_encode_string(self.receiver_id))
        parts.append(struct.pack("<B", self.status_code))
        parts.append(_encode_string(self.message))
        return b"".join(parts)

    @classmethod
    def deserialize_from(cls, data: bytes, offset: int = 0) -> Tuple["ReceiverAck", int]:
        receiver_id, offset = _decode_string(data, offset)
        status_code = struct.unpack_from("<B", data, offset)[0]
        offset += struct.calcsize("<B")
        message, offset = _decode_string(data, offset)
        return cls(
            receiver_id=receiver_id,
            status_code=status_code,
            message=message
        ), offset

