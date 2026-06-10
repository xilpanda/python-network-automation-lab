import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

from inventory_loader import load_inventory
from netmiko_command_runner import run_command
from netmiko_backup import backup_device
from report_generator import generate_summary_report


MAX_WORKERS = 10
INVENTORY_PATH = "inventories/devices.yaml"


def show_inventory() -> None:
    devices = load_inventory(INVENTORY_PATH)

    print(f"[+] Loaded devices: {len(devices)}")

    for device in devices:
        print(
            f"- {device['name']} | "
            f"{device['platform']} | "
            f"{device['host']}:{device.get('port', 22)}"
        )


def run_inventory_command(command: str, device_name: str | None = None) -> None:
    devices = load_inventory(INVENTORY_PATH)

    for device in devices:
        if device_name and device["name"] != device_name:
            continue

        print(f"\n===== {device['name']} ({device['host']}) =====")

        try:
            output = run_command(device, command)
            print(output)
        except Exception as error:
            print(f"[ERROR] {device['name']}: {error}")


def run_backup(device_name: str | None = None) -> None:
    devices = load_inventory(INVENTORY_PATH)

    for device in devices:
        if device_name and device["name"] != device_name:
            continue

        print(f"[+] Backup device: {device['name']} ({device['host']})")

        try:
            backup_file = backup_device(device)
            print(f"[OK] Backup saved: {backup_file}")
        except Exception as error:
            print(f"[ERROR] {device['name']}: {error}")


def run_parallel_backup() -> None:
    devices = load_inventory(INVENTORY_PATH)

    print(f"[+] Loaded devices: {len(devices)}")
    print(f"[+] Running parallel backup with max_workers={MAX_WORKERS}")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_device = {
            executor.submit(backup_device, device): device
            for device in devices
        }

        for future in as_completed(future_to_device):
            device = future_to_device[future]

            try:
                backup_file = future.result()
                print(f"[OK] {device['name']} -> {backup_file}")
            except Exception as error:
                print(f"[ERROR] {device['name']} -> {error}")


def run_report() -> None:
    report_file = generate_summary_report()
    print(f"[+] Summary report generated: {report_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Python Network Automation Lab Controller"
    )

    subparsers = parser.add_subparsers(dest="command_name", required=True)

    subparsers.add_parser("inventory", help="Show devices from inventory")

    command_parser = subparsers.add_parser(
        "command",
        help="Run command on devices from inventory",
    )
    command_parser.add_argument(
        "--cmd",
        required=True,
        help="Command to execute, example: hostname",
    )
    command_parser.add_argument(
        "--device",
        help="Optional device name, example: local-linux",
    )

    backup_parser = subparsers.add_parser(
        "backup",
        help="Run backup on devices",
    )
    backup_parser.add_argument(
        "--device",
        help="Optional device name, example: local-linux",
    )

    subparsers.add_parser(
        "parallel-backup",
        help="Run backup in parallel on all devices",
    )

    subparsers.add_parser(
        "report",
        help="Generate backup summary report",
    )

    args = parser.parse_args()

    if args.command_name == "inventory":
        show_inventory()

    elif args.command_name == "command":
        run_inventory_command(args.cmd, args.device)

    elif args.command_name == "backup":
        run_backup(args.device)

    elif args.command_name == "parallel-backup":
        run_parallel_backup()

    elif args.command_name == "report":
        run_report()


if __name__ == "__main__":
    main()
