from concurrent.futures import ThreadPoolExecutor, as_completed

from inventory_loader import load_inventory
from netmiko_backup import backup_device


MAX_WORKERS = 10


def main():
    devices = load_inventory("inventories/devices.yaml")

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


if __name__ == "__main__":
    main()
