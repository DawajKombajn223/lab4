import socket
import struct
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


def handle_client(conn: socket.socket, address: tuple[str, int]) -> None:
    try:
        data = recv_message(conn)
        message, _ = ChatMessage.deserialize_from(data)
        print(f"Otrzymano wiadomość od {message.sender} do {message.recipient}:")
        print(f"  timestamp: {message.timestamp}")
        print(f"  body: {message.body}")

        ack = Ack(status=0, message="Wiadomość odebrana")
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
        print(f"Serwer nasłuchuje na {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            print(f"Połączono z {addr}")
            handle_client(conn, addr)


if __name__ == "__main__":
    main()
