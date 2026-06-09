import yaml
from pathlib import Path


def load_inventory(path: str) -> list[dict]:
    inventory_path = Path(path)

    if not inventory_path.exists():
        raise FileNotFoundError(f"Inventory fajl ne postoji: {path}")

    with inventory_path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    devices = data.get("devices", [])

    if not devices:
        raise ValueError("Inventory ne sadrži nijedan uređaj.")

    return devices


if __name__ == "__main__":
    devices = load_inventory("inventories/devices.yaml")

    for device in devices:
        print(f"{device['name']} -> {device['host']}:{device['port']} ({device['platform']})")
