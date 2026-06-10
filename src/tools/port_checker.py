import socket
import argparse
from concurrent.futures import ThreadPoolExecutor


def check_port(host: str, port: int, timeout: float = 1.0) -> tuple[int, bool]:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return port, True
    except OSError:
        return port, False


def main():
    parser = argparse.ArgumentParser(description="Simple TCP port checker for lab environments")
    parser.add_argument("host", help="Target host, example: 127.0.0.1")
    parser.add_argument("--start", type=int, default=1, help="Start port")
    parser.add_argument("--end", type=int, default=1024, help="End port")
    parser.add_argument("--workers", type=int, default=50, help="Number of concurrent workers")
    parser.add_argument("--timeout", type=float, default=1.0, help="Connection timeout in seconds")

    args = parser.parse_args()

    print(f"[+] Checking TCP ports on {args.host} from {args.start} to {args.end}")

    ports = range(args.start, args.end + 1)

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        results = executor.map(
            lambda port: check_port(args.host, port, args.timeout),
            ports,
        )

    for port, is_open in results:
        if is_open:
            print(f"[OPEN] {args.host}:{port}")


if __name__ == "__main__":
    main()
