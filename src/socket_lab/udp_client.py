import socket

HOST = "127.0.0.1"
PORT = 9001


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        message = "Pozdrav preko UDP-a"

        client.sendto(message.encode("utf-8"), (HOST, PORT))

        response, server_address = client.recvfrom(1024)
        print(f"[<] Odgovor od {server_address}: {response.decode('utf-8', errors='ignore')}")


if __name__ == "__main__":
    main()
