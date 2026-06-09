import socket

HOST = "127.0.0.1"
PORT = 9000


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))

        message = "Pozdrav iz Python TCP klijenta"
        client.sendall(message.encode("utf-8"))

        response = client.recv(1024)
        print(response.decode("utf-8", errors="ignore"))


if __name__ == "__main__":
    main()
