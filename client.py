import socket
import struct
import time
from generated_protocol import ReceiverAck, SensorReading

HOST = "127.0.0.1"
PORT = 50000


def recv_exact(sock: socket.socket, count: int) -> bytes:
    data = b""
    while len(data) < count:
        chunk = sock.recv(count - len(data))
        if not chunk:
            raise ConnectionError("Connection closed while receiving data")
        data += chunk
    return data


def recv_message(sock: socket.socket) -> bytes:
    header = recv_exact(sock, 4)
    length = struct.unpack("<I", header)[0]
    return recv_exact(sock, length)


def send_message(sock: socket.socket, payload: bytes) -> None:
    sock.sendall(struct.pack("<I", len(payload)) + payload)


def main() -> None:
    reading = SensorReading(
        sensor_id="S-001",
        location="Greenhouse-A",
        temperature_c=23.7,
        humidity_pct=61.2,
        timestamp=int(time.time()),
        battery_pct=82,
    )

    with socket.create_connection((HOST, PORT)) as client:
        print(f"Sensor {reading.sensor_id} wysyła dane do odbiornika {HOST}:{PORT}")
        send_message(client, reading.serialize())

        data = recv_message(client)
        ack, _ = ReceiverAck.deserialize_from(data)
        print(f"Odbiornik odpowiedział: [{ack.status_code}] {ack.message}")


if __name__ == "__main__":
    main()
