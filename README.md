# Python Network Automation Lab

Python Network Automation Lab is a hands-on learning and portfolio project focused on Python network programming and network automation.

The project starts with low-level socket programming concepts such as TCP, UDP and JSON communication over sockets. It then gradually moves into practical network automation workflows using YAML inventory files, SSH, Paramiko, Netmiko, backup automation, parallel execution and Markdown report generation.

The goal is to build a realistic foundation for network automation, DevOps, SRE and infrastructure engineering work.

---

## Main Goals

This project was created to practice and demonstrate:

* how TCP and UDP communication work in Python
* how client/server applications exchange data
* how to build a simple JSON protocol over TCP
* how to scan/check TCP ports
* how to load devices from a YAML inventory
* how to connect to Linux/network devices over SSH
* how to run remote commands with Paramiko and Netmiko
* how to generate device backups
* how to run backups in parallel
* how to generate Markdown summary reports
* how to create a central CLI controller for automation tasks

---

## Technologies Used

* Python 3.12
* TCP sockets
* UDP sockets
* JSON
* YAML
* Paramiko
* Netmiko
* NAPALM
* AsyncSSH
* PyYAML
* Rich
* Tabulate
* Pytest
* Linux
* SSH
* Git and GitHub

---

## Project Structure

```text
python-network-automation-lab/
├── inventories/
│   └── devices.yaml
├── src/
│   ├── socket_lab/
│   │   ├── tcp_server.py
│   │   ├── tcp_client.py
│   │   ├── udp_server.py
│   │   ├── udp_client.py
│   │   ├── json_protocol.py
│   │   ├── json_server.py
│   │   └── json_client.py
│   ├── tools/
│   │   └── port_checker.py
│   └── automation/
│       ├── inventory_loader.py
│       ├── paramiko_linux_check.py
│       ├── netmiko_command_runner.py
│       ├── netmiko_backup.py
│       ├── parallel_backup.py
│       ├── report_generator.py
│       └── network_controller.py
├── backups/
├── reports/
├── logs/
├── tests/
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Current Features

### 1. TCP Client and Server

The TCP lab demonstrates basic reliable client/server communication.

The server listens on a local TCP port, accepts a client connection, receives a message and sends a response back to the client.

Run TCP server:

```bash
python src/socket_lab/tcp_server.py
```

Run TCP client:

```bash
python src/socket_lab/tcp_client.py
```

Example result:

```text
TCP server received: Hello from Python TCP client
```

---

### 2. UDP Client and Server

The UDP lab demonstrates connectionless communication.

Unlike TCP, UDP does not establish a persistent connection. The client sends a datagram and the server responds to the sender address.

Run UDP server:

```bash
python src/socket_lab/udp_server.py
```

Run UDP client:

```bash
python src/socket_lab/udp_client.py
```

Example result:

```text
UDP server received: Hello over UDP
```

---

### 3. JSON Protocol over TCP

This module demonstrates how to send structured JSON messages over TCP.

It uses a 4-byte message length header before the JSON payload. This avoids problems with partial socket reads and makes the communication more reliable.

Main files:

```text
src/socket_lab/json_protocol.py
src/socket_lab/json_server.py
src/socket_lab/json_client.py
```

Run JSON server:

```bash
python src/socket_lab/json_server.py
```

Run JSON client:

```bash
python src/socket_lab/json_client.py
```

Example response:

```python
{'type': 'pong', 'payload': {'message': 'server alive'}}
```

---

### 4. TCP Port Checker

The port checker scans a target host and checks which TCP ports are open.

It uses Python sockets and ThreadPoolExecutor for concurrent checking.

Run port checker:

```bash
python src/tools/port_checker.py 127.0.0.1 --start 1 --end 10000
```

Example output:

```text
[OPEN] 127.0.0.1:22
[OPEN] 127.0.0.1:80
[OPEN] 127.0.0.1:443
[OPEN] 127.0.0.1:3306
```

This is useful for understanding how TCP connection attempts work and how basic service discovery can be automated.

---

## Inventory

Devices are defined in a YAML inventory file.

Example:

```yaml
devices:
  - name: local-linux
    host: 127.0.0.1
    platform: linux
    username: labuser
    password_env: LAB_SSH_PASSWORD
    port: 22
```

The password is not stored directly in the repository. Instead, the project reads it from an environment variable.

Set the SSH password:

```bash
read -s LAB_SSH_PASSWORD
export LAB_SSH_PASSWORD
```

Check if the variable is set:

```bash
test -n "$LAB_SSH_PASSWORD" && echo "LAB_SSH_PASSWORD is set"
```

---

## Automation Modules

### 1. Inventory Loader

File:

```text
src/automation/inventory_loader.py
```

This module reads the YAML inventory and returns a list of devices.

Run:

```bash
python src/automation/inventory_loader.py
```

Example output:

```text
local-linux -> 127.0.0.1:22 (linux)
```

---

### 2. Paramiko Linux Healthcheck

File:

```text
src/automation/paramiko_linux_check.py
```

This script connects to Linux over SSH using Paramiko and runs healthcheck commands such as:

```text
hostname
uptime
whoami
ip -br addr
df -h
free -m
ss -tulpn
```

Run:

```bash
python src/automation/paramiko_linux_check.py
```

The script generates a Markdown report in the `reports/` directory.

Example:

```text
reports/linux-healthcheck-YYYYMMDD-HHMMSS.md
```

---

### 3. Netmiko Command Runner

File:

```text
src/automation/netmiko_command_runner.py
```

This script runs a command on devices from the YAML inventory using Netmiko.

Run command on all devices:

```bash
python src/automation/netmiko_command_runner.py --command "hostname"
```

Run command on a specific device:

```bash
python src/automation/netmiko_command_runner.py --device local-linux --command "uptime"
```

Example output:

```text
===== local-linux (127.0.0.1) =====

lab-linux-vm
```

---

### 4. Netmiko Backup Tool

File:

```text
src/automation/netmiko_backup.py
```

This script connects to devices from inventory and saves command output into backup files.

For Linux, it collects commands such as:

```text
hostname
uname -a
ip -br addr
ip route
df -h
free -m
ss -tulpn
```

Run:

```bash
python src/automation/netmiko_backup.py
```

Example output:

```text
[+] Backup device: local-linux (127.0.0.1)
[OK] Backup saved: backups/local-linux/local-linux-YYYYMMDD-HHMMSS.txt
```

Backup files are saved locally under:

```text
backups/device-name/
```

The `backups/` directory is ignored by Git.

---

### 5. Parallel Backup

File:

```text
src/automation/parallel_backup.py
```

This script runs backups in parallel using ThreadPoolExecutor.

Run:

```bash
python src/automation/parallel_backup.py
```

Example output:

```text
[+] Loaded devices: 1
[+] Running parallel backup with max_workers=10
[OK] local-linux -> backups/local-linux/local-linux-YYYYMMDD-HHMMSS.txt
```

This is useful because real network environments can contain many devices. Running backups sequentially is slow, while parallel execution allows multiple devices to be processed at the same time.

---

### 6. Backup Summary Report Generator

File:

```text
src/automation/report_generator.py
```

This script reads the `backups/` directory and generates a Markdown summary report.

Run:

```bash
python src/automation/report_generator.py
```

Example output:

```text
[+] Summary report generated: reports/network-automation-summary-YYYYMMDD-HHMMSS.md
```

Example report content:

```text
# Network Automation Summary Report

Generated at: 20260610-131104

## Backup Overview

Total devices with backups: 1

### Device: local-linux

- Backup count: 3
- Latest backup: backups/local-linux/local-linux-20260610-130901.txt
- Latest backup size: 18.35 KB
- Last modified: 2026-06-10 13:09:09
```

The `reports/` directory is ignored by Git.

---

## Central CLI Controller

File:

```text
src/automation/network_controller.py
```

The central CLI controller provides one entry point for the main automation tasks.

Show inventory:

```bash
python src/automation/network_controller.py inventory
```

Run command:

```bash
python src/automation/network_controller.py command --cmd "hostname"
```

Run command on a specific device:

```bash
python src/automation/network_controller.py command --device local-linux --cmd "uptime"
```

Run backup:

```bash
python src/automation/network_controller.py backup
```

Run parallel backup:

```bash
python src/automation/network_controller.py parallel-backup
```

Generate report:

```bash
python src/automation/network_controller.py report
```

The controller makes the project easier to use because it hides individual script names behind a single CLI interface.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/xilpanda/python-network-automation-lab.git
cd python-network-automation-lab
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## SSH Setup for Local Testing

This project can be tested against the local Linux machine using SSH.

Check SSH service:

```bash
systemctl status ssh
```

Check if SSH is listening on port 22:

```bash
ss -tulpn | grep :22
```

Test manual SSH login:

```bash
ssh labuser@127.0.0.1
```

Exit SSH session:

```bash
exit
```

Set password environment variable:

```bash
read -s LAB_SSH_PASSWORD
export LAB_SSH_PASSWORD
```

Test Netmiko:

```bash
python src/automation/network_controller.py command --cmd "hostname"
```

---

## Git Ignore Strategy

The project ignores generated and sensitive local files:

```text
.venv/
__pycache__/
*.pyc
.env
backups/
logs/
reports/
.pytest_cache/
```

This keeps the repository clean and prevents local reports, backups and secrets from being committed.

---

## Example Workflow

A typical workflow looks like this:

```bash
source .venv/bin/activate

read -s LAB_SSH_PASSWORD
export LAB_SSH_PASSWORD

python src/automation/network_controller.py inventory
python src/automation/network_controller.py command --cmd "hostname"
python src/automation/network_controller.py backup
python src/automation/network_controller.py parallel-backup
python src/automation/network_controller.py report
```

Result:

```text
Inventory loaded
Command executed
Backup created
Parallel backup completed
Markdown report generated
```

---

## What This Project Demonstrates

This project demonstrates practical understanding of:

* Python socket programming
* TCP client/server communication
* UDP datagram communication
* message framing with JSON over TCP
* concurrent TCP port checking
* YAML inventory design
* SSH automation
* Paramiko usage
* Netmiko usage
* backup automation
* parallel execution
* Markdown report generation
* Python CLI design
* Git-based project workflow

---

## Current Status

Implemented:

* TCP server/client
* UDP server/client
* JSON protocol over TCP
* TCP port checker
* YAML inventory loader
* Paramiko Linux healthcheck
* Netmiko command runner
* Netmiko backup tool
* Parallel Netmiko backup
* Backup summary report generator
* Central CLI controller
* GitHub repository synchronization

---

## Planned Improvements

Next planned improvements:

* Add Cisco IOS device support through GNS3
* Add Arista EOS device support
* Add NAPALM facts collection
* Add Ansible playbooks
* Add structured JSON reports
* Add logging
* Add pytest tests
* Add Docker support
* Add SSH key authentication
* Add command output parsing
* Add backup comparison/diff feature
* Add device reachability checks before backup
* Add HTML report output

---

## Learning Path Covered

This project connects two important areas:

### 1. Network Programming

Low-level understanding:

* sockets
* TCP
* UDP
* client/server model
* message encoding/decoding
* message framing
* basic protocol design

### 2. Network Automation

Practical automation:

* inventories
* SSH connections
* command execution
* device backups
* parallel processing
* report generation
* CLI tooling

Together, these concepts create a strong foundation for network automation, DevOps, SRE and infrastructure engineering work.

---

## Author

Sandro Radinkovic

GitHub: xilpanda
