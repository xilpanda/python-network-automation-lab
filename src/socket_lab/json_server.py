import socket
from json_protocol import recv_json, send_json

HOST = "127.0.0.1"
PORT = 9002


def handle_request(request: dict) -> dict:
    request_type = request.get("type")

    if request_type == "ping":
        return {
            "type": "pong",
            "payload": {
                "message": "server alive"
            }
        }

    if request_type == "echo":
        return {
            "type": "echo_response",
            "payload": request.get("payload", {})
        }

    return {
        "type": "error",
        "payload": {
            "message": f"Unknown request type: {request_type}"
        }
    }


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(5)

        print(f"[+] JSON TCP server sluša na {HOST}:{PORT}")

        while True:
            client_socket, client_address = server.accept()

            with client_socket:
                print(f"[+] Konekcija od: {client_address}")

                try:
                    request = recv_json(client_socket)
                    print(f"[>] Request: {request}")

                    response = handle_request(request)
                    send_json(client_socket, response)

                except Exception as error:
                    print(f"[ERROR] {client_address}: {error}")


if __name__ == "__main__":
    main()
