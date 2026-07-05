import socket
import struct
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


def handle_client(conn: socket.socket, address: tuple[str, int]) -> None:
    try:
        data = recv_message(conn)
        reading, _ = SensorReading.deserialize_from(data)
        print(f"Otrzymano pomiar z sensora {reading.sensor_id}:")
        print(f"  lokalizacja: {reading.location}")
        print(f"  temperatura: {reading.temperature_c:.1f} C")
        print(f"  wilgotność: {reading.humidity_pct:.1f}%")
        print(f"  bateria: {reading.battery_pct}%")

        ack = ReceiverAck(receiver_id="RX-01", status_code=0, message="Pomiar odebrany")
        send_message(conn, ack.serialize())
    except Exception as exc:
        print(f"Błąd obsługi klienta {address}: {exc}")
    finally:
        conn.close()


def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(1)
        print(f"Serwer odbiornika nasłuchuje na {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            print(f"Połączono z {addr}")
            handle_client(conn, addr)


if __name__ == "__main__":
    main()
