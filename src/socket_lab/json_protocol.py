import json
import struct

HEADER_SIZE = 4


def send_all(sock, data: bytes) -> None:
    total_sent = 0

    while total_sent < len(data):
        sent = sock.send(data[total_sent:])

        if sent == 0:
            raise ConnectionError("Socket connection was broken during send.")

        total_sent += sent


def recv_exact(sock, size: int) -> bytes:
    data = b""

    while len(data) < size:
        chunk = sock.recv(size - len(data))

        if chunk == b"":
            raise ConnectionError("Socket connection was closed during receive.")

        data += chunk

    return data


def send_json(sock, payload: dict) -> None:
    body = json.dumps(payload).encode("utf-8")
    header = struct.pack("!I", len(body))

    send_all(sock, header + body)


def recv_json(sock) -> dict:
    header = recv_exact(sock, HEADER_SIZE)
    body_length = struct.unpack("!I", header)[0]

    body = recv_exact(sock, body_length)
    return json.loads(body.decode("utf-8"))
