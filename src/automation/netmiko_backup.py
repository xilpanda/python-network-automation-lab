import os
from datetime import datetime
from pathlib import Path

from netmiko import ConnectHandler

from inventory_loader import load_inventory


BACKUP_COMMANDS = {
    "linux": [
        "hostname",
        "uname -a",
        "ip -br addr",
        "ip route",
        "df -h",
        "free -m",
        "ss -tulpn",
    ],
    "cisco_ios": [
        "show running-config",
        "show version",
        "show ip interface brief",
    ],
    "arista_eos": [
        "show running-config",
        "show version",
        "show ip interface brief",
    ],
}


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


def connect_to_device(device: dict):
    password = get_device_password(device)

    connection_data = {
        "device_type": device["platform"],
        "host": device["host"],
        "username": device["username"],
        "password": password,
        "port": device.get("port", 22),
        "timeout": 20,
    }

    return ConnectHandler(**connection_data)


def backup_device(device: dict) -> Path:
    platform = device["platform"]
    commands = BACKUP_COMMANDS.get(platform)

    if not commands:
        raise ValueError(f"Nema definisanih backup komandi za platformu: {platform}")

    backup_dir = Path("backups") / device["name"]
    backup_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_file = backup_dir / f"{device['name']}-{timestamp}.txt"

    connection = connect_to_device(device)

    try:
        with backup_file.open("w", encoding="utf-8") as file:
            file.write(f"# Backup for {device['name']} ({device['host']})\n")
            file.write(f"# Platform: {platform}\n")
            file.write(f"# Generated at: {timestamp}\n\n")

            for command in commands:
                file.write(f"\n===== COMMAND: {command} =====\n\n")

                output = connection.send_command(command, read_timeout=60)
                file.write(output)
                file.write("\n")

    finally:
        connection.disconnect()

    return backup_file


def main():
    devices = load_inventory("inventories/devices.yaml")

    for device in devices:
        print(f"[+] Backup device: {device['name']} ({device['host']})")

        try:
            backup_file = backup_device(device)
            print(f"[OK] Backup saved: {backup_file}")

        except Exception as error:
            print(f"[ERROR] {device['name']}: {error}")


if __name__ == "__main__":
    main()
