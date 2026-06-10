import os
import argparse
from netmiko import ConnectHandler

from inventory_loader import load_inventory


def get_device_password(device: dict) -> str:
    password_env = device.get("password_env")

    if not password_env:
        raise ValueError(f"Device {device['name']} nema password_env polje.")

    password = os.getenv(password_env)

    if not password:
        raise EnvironmentError(
            f"Environment varijabla {password_env} nije postavljena."
        )

    return password


def run_command(device: dict, command: str) -> str:
    password = get_device_password(device)

    connection_data = {
        "device_type": device["platform"],
        "host": device["host"],
        "username": device["username"],
        "password": password,
        "port": device.get("port", 22),
        "timeout": 20,
    }

    connection = ConnectHandler(**connection_data)

    try:
        output = connection.send_command(command, read_timeout=30)
        return output
    finally:
        connection.disconnect()


def main():
    parser = argparse.ArgumentParser(
        description="Run command on devices from YAML inventory using Netmiko"
    )
    parser.add_argument(
        "--command",
        required=True,
        help="Command to execute, example: 'hostname'",
    )
    parser.add_argument(
        "--device",
        help="Optional device name from inventory, example: local-linux",
    )

    args = parser.parse_args()

    devices = load_inventory("inventories/devices.yaml")

    for device in devices:
        if args.device and device["name"] != args.device:
            continue

        print(f"\n===== {device['name']} ({device['host']}) =====")

        try:
            output = run_command(device, args.command)
            print(output)
        except Exception as error:
            print(f"[ERROR] {device['name']}: {error}")


if __name__ == "__main__":
    main()
