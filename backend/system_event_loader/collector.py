from datetime import datetime, timezone
import json
import os
import platform
import psutil
import socket
import sqlite3
import subprocess
import glob
import subprocess
# Optional vendor imports handled safely per OS
try:
    import GPUtil
except ImportError:
    GPUtil = None

try:
    import win32evtlog
except ImportError:
    win32evtlog = None


"""
Unified telemetry, log, and peripheral collector for Linux & Windows.
"""

import glob
import json
import os
import platform
import socket
import sqlite3
import subprocess
from datetime import datetime, timezone

import psutil

try:
    import GPUtil
except ImportError:
    GPUtil = None

try:
    import win32evtlog
except ImportError:
    win32evtlog = None


class SystemCollector:
    """Unified telemetry, log, and peripheral collector for Linux & Windows."""

    def __init__(self, db_path: str = "telemetry_edge.db"):
        self.hostname = socket.gethostname()
        self.os_type = platform.system()
        self.db_path = db_path
        self._init_sqlite_db()

    def _init_sqlite_db(self):
        """Initialize local SQLite edge buffer with WAL mode enabled for safe concurrency."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS telemetry_buffer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                payload TEXT NOT NULL,
                synced INTEGER DEFAULT 0
            );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_unsynced ON telemetry_buffer (synced, timestamp);")
        conn.commit()
        conn.close()

    # -------------------------------------------------------------------------
    # 1. HARDWARE TELEMETRY
    # -------------------------------------------------------------------------
    def get_hardware_metrics(self) -> dict:
        """Fetch CPU, RAM, and GPU status with multi-vendor fallbacks."""
        cpu_usage = psutil.cpu_percent(interval=0.5)
        memory = psutil.virtual_memory()

        # Load Averages (Linux natively supports 1, 5, 15 min; Windows fallback)
        try:
            load_1, load_5, load_15 = os.getloadavg()
        except AttributeError:
            load_1, load_5, load_15 = None, None, None

        # GPU Metrics
        gpu_data = []
        if GPUtil:
            try:
                gpus = GPUtil.getGPUs()
                for gpu in gpus:
                    gpu_data.append({
                        "id": gpu.id,
                        "name": gpu.name,
                        "load_pct": round(gpu.load * 100, 2),
                        "memory_used_mb": gpu.memoryUsed,
                        "memory_total_mb": gpu.memoryTotal,
                        "temperature_c": gpu.temperature
                    })
            except Exception:
                gpu_data = []

        return {
            "hostname": self.hostname,
            "platform": self.os_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "cpu": {
                "usage_percent": cpu_usage,
                "cores_logical": psutil.cpu_count(logical=True),
                "load_avg_1min": load_1
            },
            "memory": {
                "total_gb": round(memory.total / (1024**3), 2),
                "used_percent": memory.percent,
                "available_gb": round(memory.available / (1024**3), 2)
            },
            "gpus": gpu_data
        }

    # -------------------------------------------------------------------------
    # 2. OS EVENT LOGS
    # -------------------------------------------------------------------------
    def get_system_logs(self, max_records: int = 10) -> list:
        """Extract recent event logs from journalctl (Linux) or Event Viewer (Windows)."""
        if self.os_type == "Linux":
            return self._get_linux_logs(max_records)
        elif self.os_type == "Windows":
            return self._get_windows_logs(max_records)
        return [{"warning": f"Log extraction not supported on {self.os_type}"}]

    def _get_linux_logs(self, max_records: int) -> list:
        events = []
        try:
            cmd = ["journalctl", "-n", str(max_records), "-o", "json", "--no-pager"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.strip().split("\n"):
                    if not line:
                        continue
                    entry = json.loads(line)
                    raw_ts = entry.get("__REALTIME_TIMESTAMP")
                    formatted_ts = None
                    if raw_ts:
                        formatted_ts = datetime.fromtimestamp(
                            int(raw_ts) / 1_000_000, tz=timezone.utc
                        ).isoformat()

                    events.append({
                        "source_name": entry.get("_SYSTEMD_UNIT", entry.get("SYSLOG_IDENTIFIER", "kernel")),
                        "timestamp": formatted_ts or raw_ts,
                        "priority": entry.get("PRIORITY"),
                        "message": entry.get("MESSAGE", "")
                    })
        except Exception as e:
            events.append({"error": f"Failed to query journalctl: {str(e)}"})
        return events

    def _get_windows_logs(self, max_records: int) -> list:
        if not win32evtlog:
            return [{"error": "pywin32 library is not installed."}]
        events = []
        try:
            hand = win32evtlog.OpenEventLog(None, "System")
            flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
            raw_events = win32evtlog.ReadEventLog(hand, flags, 0)
            for ev in raw_events[:max_records]:
                events.append({
                    "event_id": ev.EventID & 0xFFFF,
                    "source_name": ev.SourceName,
                    "time_generated": str(ev.TimeGenerated),
                    "event_type": ev.EventType
                })
            win32evtlog.CloseEventLog(hand)
        except Exception as e:
            events.append({"error": f"Failed to read Windows logs: {str(e)}"})
        return events

    # -------------------------------------------------------------------------
    # 3. ATTACHED PERIPHERALS (Printers, Scanners, USB)
    # -------------------------------------------------------------------------
    def get_attached_peripherals(self) -> dict:
        """Detect connected printers, ID/barcode scanners, and USB peripherals."""
        if self.os_type == "Windows":
            return self._get_windows_peripherals()
        elif self.os_type == "Linux":
            return self._get_linux_peripherals()
        return {"error": f"Unsupported OS: {self.os_type}"}

    def _get_windows_peripherals(self) -> dict:
        devices = {"printers": [], "usb_devices": []}
        try:
            cmd_p = "Get-CimInstance Win32_Printer | Select-Object Name, PrinterStatus, WorkOffline | ConvertTo-Json"
            res_p = subprocess.run(["powershell", "-Command", cmd_p], capture_output=True, text=True)
            if res_p.returncode == 0 and res_p.stdout.strip():
                devices["printers"] = json.loads(res_p.stdout)

            cmd_u = (
                "Get-PnpDevice -PresentOnly | "
                "Where-Object { $_.Class -match 'USB|Printer|Image' } | "
                "Select-Object FriendlyName, InstanceId, Status | ConvertTo-Json"
            )
            res_u = subprocess.run(["powershell", "-Command", cmd_u], capture_output=True, text=True)
            if res_u.returncode == 0 and res_u.stdout.strip():
                devices["usb_devices"] = json.loads(res_u.stdout)
        except Exception as e:
            devices["error"] = str(e)
        return devices

    def _get_linux_peripherals(self) -> dict:
        devices = {"printers": [], "usb_devices": []}

        # 1. USB Devices: Direct read from /sys/bus/usb/devices/ (No lsusb needed)
        try:
            usb_paths = glob.glob("/sys/bus/usb/devices/*")
            for path in usb_paths:
                product_file = os.path.join(path, "product")
                id_vendor_file = os.path.join(path, "idVendor")
                id_product_file = os.path.join(path, "idProduct")

                if os.path.exists(product_file):
                    try:
                        with open(product_file, "r") as f:
                            name = f.read().strip()

                        # Optional: read IDs if available
                        vendor_id, product_id = "", ""
                        if os.path.exists(id_vendor_file) and os.path.exists(id_product_file):
                            with open(id_vendor_file, "r") as vf, open(id_product_file, "r") as pf:
                                vendor_id = vf.read().strip()
                                product_id = pf.read().strip()

                        device_str = f"ID {vendor_id}:{product_id} {name}".strip()
                        if device_str and device_str not in devices["usb_devices"]:
                            devices["usb_devices"].append(device_str)
                    except (PermissionError, OSError):
                        continue
        except Exception as e:
            devices["usb_error"] = str(e)

        # 2. Printers: CUPS lpstat check
        try:
            res_lp = subprocess.run(["lpstat", "-p"], capture_output=True, text=True)
            if res_lp.returncode == 0:
                devices["printers"] = [line for line in res_lp.stdout.strip().split("\n") if line]
        except Exception as e:
            devices["printer_error"] = str(e)

        return devices

    # -------------------------------------------------------------------------
    # 4. BUFFERING & PAYLOAD AGGREGATION
    # -------------------------------------------------------------------------
    def collect_full_telemetry(self) -> dict:
        """Aggregate hardware metrics, recent logs, and peripheral state into one payload."""
        return {
            "metrics": self.get_hardware_metrics(),
            "peripherals": self.get_attached_peripherals(),
            "logs": self.get_system_logs(max_records=5)
        }

    def save_to_local_db(self, payload: dict):
        """Save telemetry payload to local SQLite buffer for offline reliability."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO telemetry_buffer (payload) VALUES (?);", (json.dumps(payload),))

        # Purge buffer records older than 7 days to conserve disk space
        cursor.execute("DELETE FROM telemetry_buffer WHERE timestamp < datetime('now', '-7 days');")
        conn.commit()
        conn.close()

if __name__ == "__main__":
    collector = SystemCollector()
    
    # 1. Capture snapshot
    payload = collector.collect_full_telemetry()
    print("--- Aggregated Telemetry Payload ---")
    print(json.dumps(payload, indent=2))

    # 2. Buffer to local SQLite DB
    collector.save_to_local_db(payload)
    print("\n[✓] Payload successfully buffered to local SQLite database.")