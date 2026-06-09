import socket

HOST = "127.0.0.1"
PORT = 9001


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((HOST, PORT))

        print(f"[+] UDP server sluša na {HOST}:{PORT}")

        while True:
            data, client_address = server.recvfrom(1024)
            message = data.decode("utf-8", errors="ignore")

            print(f"[{client_address}] {message}")

            response = f"UDP server primio: {message}"
            server.sendto(response.encode("utf-8"), client_address)


if __name__ == "__main__":
    main()
