from datetime import datetime
from pathlib import Path


BACKUPS_DIR = Path("backups")
REPORTS_DIR = Path("reports")


def get_latest_backup(device_dir: Path) -> Path | None:
    backup_files = list(device_dir.glob("*.txt"))

    if not backup_files:
        return None

    return max(backup_files, key=lambda file: file.stat().st_mtime)


def generate_summary_report() -> Path:
    REPORTS_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    report_file = REPORTS_DIR / f"network-automation-summary-{timestamp}.md"

    with report_file.open("w", encoding="utf-8") as report:
        report.write("# Network Automation Summary Report\n\n")
        report.write(f"Generated at: `{timestamp}`\n\n")

        if not BACKUPS_DIR.exists():
            report.write("No backups directory found.\n")
            return report_file

        device_dirs = [path for path in BACKUPS_DIR.iterdir() if path.is_dir()]

        report.write("## Backup Overview\n\n")
        report.write(f"Total devices with backups: `{len(device_dirs)}`\n\n")

        for device_dir in sorted(device_dirs):
            backup_files = list(device_dir.glob("*.txt"))
            latest_backup = get_latest_backup(device_dir)

            report.write(f"### Device: `{device_dir.name}`\n\n")
            report.write(f"- Backup count: `{len(backup_files)}`\n")

            if latest_backup:
                size_kb = latest_backup.stat().st_size / 1024
                modified_time = datetime.fromtimestamp(
                    latest_backup.stat().st_mtime
                ).strftime("%Y-%m-%d %H:%M:%S")

                report.write(f"- Latest backup: `{latest_backup}`\n")
                report.write(f"- Latest backup size: `{size_kb:.2f} KB`\n")
                report.write(f"- Last modified: `{modified_time}`\n")
            else:
                report.write("- Latest backup: `N/A`\n")

            report.write("\n")

    return report_file


def main():
    report_file = generate_summary_report()
    print(f"[+] Summary report generated: {report_file}")


if __name__ == "__main__":
    main()
