import socket

HOST = "127.0.0.1"
PORT = 9000


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(5)

        print(f"[+] TCP server sluša na {HOST}:{PORT}")

        while True:
            client_socket, client_address = server.accept()

            with client_socket:
                print(f"[+] Konekcija od: {client_address}")

                data = client_socket.recv(1024)

                if not data:
                    continue

                message = data.decode("utf-8", errors="ignore")
                print(f"[>] Primljeno: {message}")

                response = f"Server primio: {message}"
                client_socket.sendall(response.encode("utf-8"))


if __name__ == "__main__":
    main()
