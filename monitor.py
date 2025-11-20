import psutil
import time
import argparse
import json
from datetime import datetime
import sys

# Force real-time flushing on Windows
try:
    sys.stdout.reconfigure(line_buffering=True)
except:
    pass

# Colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def get_listening_ports():
    """Return a map of port -> (process_name, pid)."""
    port_map = {}
    for conn in psutil.net_connections(kind="inet"):
        if conn.status == psutil.CONN_LISTEN and conn.laddr.port:
            try:
                proc = psutil.Process(conn.pid)
                port_map[conn.laddr.port] = (proc.name(), conn.pid)
            except:
                port_map[conn.laddr.port] = ("Unknown", conn.pid)
    return port_map


def log_json_event(filepath, event):
    """Append a JSON event to file."""
    with open(filepath, "a") as f:
        json.dump(event, f)
        f.write("\n")


def main(interval, ignore_ports, ignore_procs, json_log):
    print(f"{YELLOW}[{datetime.now()}] Port Monitor started...{RESET}", flush=True)

    baseline = get_listening_ports()
    print(f"{YELLOW}Baseline ports: {sorted(baseline.keys())}{RESET}\n", flush=True)

    while True:
        time.sleep(interval)
        current = get_listening_ports()

        new_ports = set(current.keys()) - set(baseline.keys())

        findings = []
        for port in new_ports:
            pname, pid = current[port]

            if port in ignore_ports:
                continue
            if pname.lower() in ignore_procs:
                continue

            findings.append((port, pname, pid))

        if findings:
            for port, pname, pid in findings:
                msg = f"[ALERT] New port opened: {port} (Process: {pname}, PID: {pid})"
                print(f"{RED}{datetime.now()} {msg}{RESET}", flush=True)

                if json_log:
                    event = {
                        "timestamp": datetime.now().isoformat(),
                        "port": port,
                        "process": pname,
                        "pid": pid,
                        "type": "new_port"
                    }
                    log_json_event(json_log, event)

        else:
            print(f"{GREEN}[OK] No new ports...{RESET}", flush=True)

        baseline = current


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Port Monitor (Intermediate Edition)")
    parser.add_argument("--interval", type=int, default=5, help="Scan interval (seconds)")
    parser.add_argument("--ignore-ports", type=str, default="", help="Comma-separated ports to ignore")
    parser.add_argument("--ignore-procs", type=str, default="", help="Comma-separated process names to ignore")
    parser.add_argument("--json-log", type=str, help="Enable JSON logging to a file")

    args = parser.parse_args()

    ignore_ports = {int(x.strip()) for x in args.ignore_ports.split(",") if x.strip().isdigit()}
    ignore_procs = {x.strip().lower() for x in args.ignore_procs.split(",") if x.strip()}

    main(args.interval, ignore_ports, ignore_procs, args.json_log)
