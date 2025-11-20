# 🔍 Port-Stat — Real-Time Port Activity Monitor

Port-Stat is a lightweight, cross-platform, real-time port monitoring tool designed for security analysts, developers, and incident responders. It continuously watches for newly opened listening ports and instantly alerts you when any process starts a new network listener. This helps detect suspicious activity, reverse shells, rogue services, or unexpected dev server launches.

## ✨ Features

* ⚡ Real-time detection of newly opened ports
* 🧠 Process-aware alerts (process name + PID)
* 🎛 Ignore lists for ports & processes
* 🗂 Optional JSON logging (NDJSON format)
* 🔁 Unbuffered, live output (Windows/Linux/macOS)
* 🪶 Requires only one dependency (`psutil`)

## 📦 Installation

```bash
git clone https://github.com/Alexander-50/Port-Stat.git
cd Port-Stat
pip install -r requirements.txt
```

## 🛠 Usage

### Basic monitoring

```bash
python monitor.py
```

### Scan every 2 seconds

```bash
python monitor.py --interval 2
```

### Ignore specific ports

```bash
python monitor.py --ignore-ports 3000,5000,8000
```

### Ignore specific processes

```bash
python monitor.py --ignore-procs python,node
```

### Enable JSON logging

```bash
python monitor.py --json-log logs/events.json
```

## 📌 Example Output

```
[2025-11-20 18:22:12.144921] Port Monitor started...
Baseline ports: [22, 3001, 3306, 5000, 5357, 6379, 8000, 49152, 49153]

[OK] No new ports...

2025-11-20 18:22:25.882104 [ALERT] New port opened: 8080 (Process: python.exe, PID: 9214)
2025-11-20 18:22:33.441552 [ALERT] New port opened: 9999 (Process: python.exe, PID: 10482)
```

## 📁 Project Structure

```
Port-Stat/
│── monitor.py
│── requirements.txt
│── README.md
│── .gitignore
│
├── samples/
│   ├── sample_output.txt
│   └── events_sample.json
│
└── logs/   (auto-created when using --json-log)
```

## 🧪 Sample Logs (JSON)

```
{"timestamp": "2025-11-20T18:22:25.882104", "port": 8080, "process": "python.exe", "pid": 9214, "type": "new_port"}
{"timestamp": "2025-11-20T18:22:33.441552", "port": 9999, "process": "python.exe", "pid": 10482, "type": "new_port"}
```

## 🎯 Use Cases

* Debug dev servers (Flask, Node, Django, etc.)
* Catch reverse shells / malware activity
* Monitor real-time system behavior
* Helpful for SOC, IR, Pentesting, DevOps


## 🤝 Contributing

Pull requests are welcome! Improve features, add monitoring modes, or enhance detection logic.

## ⭐ Support the Project

If you find Port-Stat useful, consider starring ⭐ the repository.

---

## 👨‍💻 Author

**Alexander P.B.**  
*Cybersecurity Researcher & Penetration Tester*  
*Red Team & IoT Security Specialist*  

📧 *Reach out via [GitHub](https://github.com/Alexander-50) for research collaborations.*

---

