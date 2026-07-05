import socket
import struct
import time
from generated_protocol import Ack, ChatMessage

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
    message = ChatMessage(
        sender="Alice",
        recipient="Server",
        timestamp=int(time.time()),
        body="Wiadomość testowa z klienta."
    )

    with socket.create_connection((HOST, PORT)) as client:
        print(f"Wysyłam wiadomość do serwera {HOST}:{PORT}")
        send_message(client, message.serialize())

        data = recv_message(client)
        ack, _ = Ack.deserialize_from(data)
        print(f"Otrzymano potwierdzenie: status={ack.status}, message={ack.message}")


if __name__ == "__main__":
    main()
