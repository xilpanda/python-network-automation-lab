import socket
from json_protocol import send_json, recv_json

HOST = "127.0.0.1"
PORT = 9002


def main():
    request = {
        "type": "ping",
        "payload": {
            "message": "hello from JSON client"
        }
    }

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))

        send_json(client, request)
        response = recv_json(client)

        print(response)


if __name__ == "__main__":
    main()
