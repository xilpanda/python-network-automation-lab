import os
from datetime import datetime
from pathlib import Path

import paramiko

from inventory_loader import load_inventory


COMMANDS = [
    "hostname",
    "uptime",
    "whoami",
    "ip -br addr",
    "df -h",
    "free -m",
    "ss -tulpn | head -20",
]


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


def run_command(device: dict, command: str) -> tuple[str, str]:
    password = get_device_password(device)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(
            hostname=device["host"],
            port=device.get("port", 22),
            username=device["username"],
            password=password,
            timeout=10,
            look_for_keys=False,
            allow_agent=False,
        )

        _, stdout, stderr = client.exec_command(command)

        output = stdout.read().decode("utf-8", errors="ignore")
        error = stderr.read().decode("utf-8", errors="ignore")

        return output, error

    finally:
        client.close()


def main():
    devices = load_inventory("inventories/devices.yaml")

    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    report_file = report_dir / f"linux-healthcheck-{timestamp}.md"

    with report_file.open("w", encoding="utf-8") as report:
        report.write("# Linux Healthcheck Report\n\n")
        report.write(f"Generated at: `{timestamp}`\n\n")

        for device in devices:
            if device["platform"] != "linux":
                continue

            report.write(f"## Device: {device['name']} ({device['host']})\n\n")

            for command in COMMANDS:
                report.write(f"### Command: `{command}`\n\n")
                report.write("```text\n")

                try:
                    output, error = run_command(device, command)

                    if output:
                        report.write(output)

                    if error:
                        report.write("\nERROR:\n")
                        report.write(error)

                except Exception as exc:
                    report.write(f"FAILED: {exc}\n")

                report.write("\n```\n\n")

    print(f"[+] Report generated: {report_file}")


if __name__ == "__main__":
    main()
