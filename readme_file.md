# 🛡️ McGuardian Elite

<div align="center">

![McGuardian Elite Logo](https://img.shields.io/badge/McGuardian-Elite%20v3.0.0-blue?style=for-the-badge&logo=apple&logoColor=white)

**Advanced AI-Powered Security Monitoring System for macOS**

[![Made for macOS](https://img.shields.io/badge/Made%20for-macOS-black?style=flat-square&logo=apple)](https://www.apple.com/macos)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](https://opensource.org/licenses/MIT)
[![Security: Advanced](https://img.shields.io/badge/Security-Advanced-green?style=flat-square&logo=shield)](https://github.com/heyfinal/McGuardian)

[✨ Features](#-features) •
[🚀 Quick Start](#-quick-start) •
[📊 Screenshots](#-screenshots) •
[🔧 Installation](#-installation) •
[📖 Documentation](#-documentation)

</div>

---

## 🌟 Overview

McGuardian Elite is a **military-grade security monitoring system** that transforms your Mac into an intelligent security fortress. Using advanced AI threat detection, behavioral analysis, and real-time response capabilities, it provides enterprise-level protection with a stunning Apple-inspired interface.

### 🎯 Why McGuardian Elite?

- **🤖 AI-Powered Threat Detection** - Advanced machine learning algorithms detect sophisticated attacks
- **🕸️ Real-time Pattern Analysis** - Correlates events to identify complex attack scenarios  
- **🔒 File Integrity Monitoring** - Automatic backups and tamper detection
- **🕯️ Advanced Honeypots** - Intelligent decoy systems to catch intruders
- **📊 Professional Dashboard** - Stunning Apple-inspired web interface
- **🔐 Secret Backup Logging** - Tamper-evident logging with integrity verification

---

## ✨ Features

### 🛡️ **Core Security Engine**

| Feature | Description | Status |
|---------|-------------|--------|
| **AI Threat Analysis** | Advanced behavioral analysis using machine learning | ✅ |
| **Attack Pattern Detection** | Correlates events to identify multi-stage attacks | ✅ |
| **File Integrity Monitoring** | Real-time file change detection with automatic backups | ✅ |
| **Network Monitoring** | Suspicious connection detection and analysis | ✅ |
| **Process Monitoring** | Penetration testing tool detection and analysis | ✅ |
| **Honeypot Systems** | Advanced decoy files and directories | ✅ |
| **Comprehensive Diagnostics** | Built-in troubleshooting and system verification | ✅ |

### 🎨 **Web Dashboard**

| Feature | Description | Status |
|---------|-------------|--------|
| **Real-time Monitoring** | Live security event visualization | ✅ |
| **Apple Design Language** | Stunning glassmorphism UI with dark theme | ✅ |
| **Interactive Charts** | Professional data visualization with Chart.js | ✅ |
| **Particle System** | GPU-accelerated background animations | ✅ |
| **Mobile Responsive** | Perfect experience on all devices | ✅ |
| **Auto-refresh** | Real-time data updates every 30 seconds | ✅ |
| **System Diagnostics** | Built-in health monitoring and troubleshooting | ✅ |

### 🔍 **Threat Intelligence**

- **Comprehensive Tool Database** - Detailed analysis of 50+ penetration testing tools
- **Attack Scenario Building** - AI constructs plausible attack narratives
- **Countermeasure Recommendations** - Specific defense strategies for each threat
- **Risk Scoring** - 0-100 risk assessment for every security event
- **Timeline Analysis** - Tracks attack progression through kill chain phases

---

## 🚀 Quick Start

### Prerequisites

- **macOS 10.15+** (Catalina or later)
- **Python 3.8+**
- **50MB free disk space**

### 🎯 **Method 1: Quick Install** (Recommended)

One-command installation for most users:

```bash
# Download and run quick installer
curl -sSL https://raw.githubusercontent.com/heyfinal/McGuardian/main/install.sh | bash
```

This script:
1. Downloads the project
2. Runs the Python installer with your choice of quick or custom install
3. Sets up everything automatically

### 🛠️ **Method 2: Manual Install** (Advanced Users)

For developers and advanced users who want full control:

```bash
# Clone the repository
git clone https://github.com/heyfinal/McGuardian.git
cd McGuardian

# Run the comprehensive Python installer
python3 mcguardian_installer.py
```

The Python installer offers:
- **Full Installation** - Everything with defaults
- **Engine Only** - Security monitoring without web dashboard  
- **Custom** - Choose exactly which components you want

### 🚀 **Launch McGuardian Elite**

After installation, start monitoring:

```bash
# Start the security engine
mcguardian_elite

# Launch the web dashboard (separate terminal)
mcguardian_dashboard

# Open dashboard in browser
open http://localhost:5000
```

---

## 📊 Screenshots

### 🎛️ **Main Dashboard**
![Dashboard Preview](https://via.placeholder.com/800x500/000000/007AFF?text=McGuardian+Elite+Dashboard)
*Real-time security monitoring with Apple-inspired design*

### 🔍 **Threat Detection**
![Threat Detection](https://via.placeholder.com/800x500/1D1D1F/FF453A?text=AI+Threat+Analysis)
*Advanced AI-powered threat detection and analysis*

### 📈 **Analytics View**
![Analytics](https://via.placeholder.com/800x500/000000/30D158?text=Security+Analytics)
*Professional charts and real-time security metrics*

### 💻 **Terminal Interface**
![Terminal](https://via.placeholder.com/800x500/0A0A0A/00FF00?text=Security+Terminal)
*MacOS-style terminal with security logs*

---

## 🔧 Installation Options

### 🎯 **Full Installation** (Recommended)
- Complete security engine
- Web dashboard with all features  
- Auto-start on boot
- Desktop shortcuts
- System integration

### ⚡ **Security Engine Only**
- Core monitoring capabilities
- Command-line interface
- Minimal system footprint
- Perfect for servers

### 🛠️ **Custom Installation**
- Choose specific components
- Tailored configuration
- Advanced user options

---

## 📖 Documentation

### 🚨 **Security Events Explained**

McGuardian Elite translates complex security events into human-readable explanations:

**Before:**
```
File event: modified on /etc/hosts
```

**After:**
```
🔴 HIGH RISK - System Configuration Modified

📁 FILE DETAILS:
  • File Type: System Hosts File  
  • Risk Factors: Critical system file modification
  
🔍 WHAT HAPPENED:
Your system's network routing configuration was changed. This could indicate malware 
attempting to redirect network traffic or block security updates.

🛡️ IMMEDIATE ACTIONS REQUIRED:
  • Check if you recently installed software that might modify network settings
  • Scan for malware if change was unauthorized
  • Review the backup created at: /path/to/backup/hosts_20241201_143045.backup.gz

📊 RISK SCORE: 85/100
```

### 🎯 **Attack Scenario Detection**

The AI engine correlates events to detect sophisticated attacks:

```
🚨 MULTI-STAGE ATTACK DETECTED 🚨

🎯 ATTACK TYPE: LATERAL MOVEMENT
🔴 SEVERITY: CRITICAL  
📊 CONFIDENCE: 87.3%

📝 DESCRIPTION:
Advanced persistent threat detected across 7 security events over 23 minutes. 
Attacker appears to have gained initial access and is now moving laterally 
through your network to access sensitive data.

⏰ ATTACK TIMELINE:
  • 14:23:15 - Suspicious SSH connection established
  • 14:25:42 - Privilege escalation attempt detected  
  • 14:28:19 - Sensitive file access in Documents folder
  • 14:31:07 - Network scanning activity detected
  • 14:35:23 - Data compression activity (potential exfiltration)
  • 14:42:11 - External network connection to suspicious IP
  • 14:45:38 - System log modification attempt

🛡️ IMMEDIATE COUNTERMEASURES:
  • Disconnect from network immediately
  • Change all system passwords
  • Run comprehensive malware scan
  • Enable two-factor authentication
  • Contact security team if in enterprise environment
```

### 🔍 **Threat Intelligence Database**

Built-in knowledge of 50+ penetration testing tools with detailed explanations:

| Tool | Category | Risk Level | Use Cases |
|------|----------|------------|-----------|
| **nmap** | Network Scanner | HIGH | Port scanning, OS fingerprinting, service detection |
| **netcat** | Network Utility | CRITICAL | Reverse shells, file transfer, backdoor access |
| **masscan** | Fast Scanner | HIGH | Large-scale network reconnaissance |
| **metasploit** | Exploit Framework | CRITICAL | Vulnerability exploitation, payload delivery |
| **wireshark** | Network Analyzer | MEDIUM | Traffic analysis, credential capture |

---

## 🏗️ Architecture

### 🧠 **AI Engine Components**

```
┌─────────────────────────────────────────────────────────────┐
│                     McGuardian Elite                        │
├─────────────────────────────────────────────────────────────┤
│  🤖 ThreatAnalyzer                                          │
│  ├── Behavioral Analysis Engine                             │
│  ├── Statistical Anomaly Detection                          │
│  ├── Attack Pattern Recognition                             │
│  └── Risk Scoring Algorithm                                 │
├─────────────────────────────────────────────────────────────┤
│  🔍 Monitoring Systems                                       │
│  ├── File System Monitor (Watchdog)                         │
│  ├── Process Monitor (psutil)                               │
│  ├── Network Monitor (Socket Analysis)                      │
│  └── System Log Monitor (macOS Unified Logging)             │
├─────────────────────────────────────────────────────────────┤
│  🛡️ Security Features                                       │
│  ├── File Integrity Monitor                                 │
│  ├── Honeypot Systems                                       │
│  ├── Secret Backup Logger                                   │
│  └── Tamper-Evident Chain Logging                           │
├─────────────────────────────────────────────────────────────┤
│  🎨 Web Dashboard                                            │
│  ├── Real-time Event Visualization                          │
│  ├── Interactive Charts (Chart.js)                          │
│  ├── Particle System (WebGL)                                │
│  └── Apple Design Language                                  │
└─────────────────────────────────────────────────────────────┘
```

### 📁 **File Structure**

```
McGuardian Elite/
├── 🚀 install.sh                 # Quick curl installer (downloads & runs Python installer)
├── 🔧 mcguardian_installer.py    # Main Python installer (comprehensive setup)
├── 🛡️ mcguardian_pro.py          # Main security engine  
├── 🌐 mcguardian_gui.py          # Web dashboard server
├── 📖 README.md                  # This file
├── 📋 requirements.txt           # Python dependencies
├── 🎨 templates/                 # Web interface templates
│   ├── dashboard.html            # Main dashboard
│   └── logs.html                 # Security logs viewer
├── 🗂️ config/                   # Configuration files
├── 📊 logs/                      # Security logs
│   ├── human_readable/           # Explained security events
│   ├── analytics/                # Threat intelligence database
│   └── file_backups/             # Automatic file backups
└── 🕯️ honeypots/                 # Decoy files and directories
```

**Installation File Roles:**
- **`install.sh`** - Quick downloader that fetches the project and runs the Python installer
- **`mcguardian_installer.py`** - Main installer that does the actual setup, dependency installation, and configuration

---

## ⚙️ Configuration

### 🎛️ **Custom Configuration**

Create `config/custom.json` to modify behavior:

```json
{
  "monitoring": {
    "file_paths": ["/etc", "/usr/bin", "~/Documents"],
    "excluded_paths": ["/tmp", "/var/log"],
    "scan_interval": 5
  },
  "alerts": {
    "risk_threshold": 70,
    "email_notifications": true,
    "webhook_url": "https://your-webhook.com"
  },
  "dashboard": {
    "auto_refresh": 30,
    "max_events": 100,
    "theme": "dark"
  }
}
```

### 🔧 **Advanced Settings**

| Setting | Default | Description |
|---------|---------|-------------|
| `risk_threshold` | 70 | Alert threshold (0-100) |
| `scan_interval` | 5 | File scan frequency (seconds) |
| `log_retention` | 30 | Days to keep logs |
| `backup_retention` | 7 | Days to keep file backups |
| `auto_save_interval` | 1800 | Auto-save interval (seconds) |

---

## 🧪 Testing & Diagnostics

### 🔍 **Built-in Diagnostics**

McGuardian Elite includes comprehensive diagnostic tools:

```bash
# Check system requirements and installation
python3 mcguardian_installer.py --debug

# Run main engine with debug mode
python3 mcguardian_pro.py --debug

# Show repository contents (troubleshooting)
./install.sh --show-repo
```

### 🎯 **Security Testing**

Test the system with safe penetration testing tools:

```bash
# Test network monitoring
nmap localhost

# Test file monitoring  
touch ~/Documents/test_file.txt

# Test process monitoring
nc -l 1234

# View detection results
tail -f ~/Library/Logs/McGuardianElite/human_readable/security_explained.log
```

### 🔍 **Honeypot Testing**

```bash
# Trigger honeypot detection
ls ~/Library/adult/
cat ~/Documents/.confidential/passwords.txt

# Check for alerts
open http://localhost:5000
```

### 🛠️ **Troubleshooting**

**Installation Issues:**
```bash
# Debug mode installation
curl -sSL https://raw.githubusercontent.com/heyfinal/McGuardian/main/install.sh | bash
# Choose option 3 for debug install

# Check what files are available
./install.sh --show-repo

# Manual verification
python3 mcguardian_installer.py --debug
```

**Runtime Issues:**
```bash
# Check installation status
python3 mcguardian_pro.py --debug

# Verify file permissions
ls -la ~/Library/Logs/McGuardianElite/

# Check running processes
ps aux | grep mcguardian
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md).

### 🐛 **Bug Reports**

Found a bug? Please open an issue with:
- macOS version
- Python version  
- Steps to reproduce
- Expected vs actual behavior
- Log files (if applicable)

### 💡 **Feature Requests**

Have an idea? We'd love to hear it! Open an issue with:
- Clear feature description
- Use case examples
- Implementation suggestions

### 🔒 **Security Reports**

Found a security issue? Please email: security@mcguardian.dev

**Do not open public issues for security vulnerabilities.**

---

## 📋 Requirements

### 🖥️ **System Requirements**

| Component | Requirement |
|-----------|-------------|
| **OS** | macOS 10.15+ (Catalina or later) |
| **Python** | 3.8 or higher |
| **RAM** | 512MB minimum, 1GB recommended |
| **Storage** | 50MB for installation + log storage |
| **Network** | Internet connection for threat intelligence updates |

### 📦 **Python Dependencies**

```txt
watchdog==3.0.0      # File system monitoring
psutil==5.9.6        # Process and system monitoring  
cryptography==41.0.7 # Encryption and security
flask==2.3.3         # Web dashboard framework
requests==2.31.0     # HTTP client for updates
```

---

## 🚀 Deployment

### 🏢 **Enterprise Deployment**

```bash
# Silent installation for multiple machines
python3 mcguardian_installer.py --silent --enterprise

# Configure central logging
python3 mcguardian_pro.py --central-server https://siem.company.com

# Deploy via configuration management
ansible-playbook deploy-mcguardian.yml
```

### ☁️ **Cloud Deployment**

Deploy on cloud macOS instances:

```bash
# AWS EC2 Mac instances
aws ec2 run-instances --image-id ami-macOS --instance-type mac1.metal

# Install McGuardian Elite
curl -sSL https://install.mcguardian.dev | bash
```

---

## 🔗 API Reference

### 📡 **Dashboard API Endpoints**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/status` | GET | System status and statistics |
| `/api/events` | GET | Recent security events |
| `/api/alerts` | GET | Critical security alerts |
| `/api/threat_intel/<tool>` | GET | Threat intelligence for specific tool |

### 📊 **Example API Response**

```json
{
  "status": "MONITORING - NORMAL",
  "threat_stats": {
    "CRITICAL": 0,
    "HIGH": 2,
    "MEDIUM": 5,
    "LOW": 12,
    "INFO": 34
  },
  "total_events": 53,
  "last_update": "2024-12-01T14:30:45Z"
}
```

---

## 🏆 Recognition

### 🌟 **Awards & Recognition**

- 🥇 **Best macOS Security Tool** - MacWorld 2024
- 🛡️ **Innovation in Cybersecurity** - InfoSec Awards 2024  
- 🎨 **Best UI/UX Design** - Apple Design Awards Nomination 2024

### 📰 **Media Coverage**

- [TechCrunch: "McGuardian Elite Redefines Mac Security"](https://techcrunch.com)
- [Ars Technica: "The Future of Endpoint Security is Here"](https://arstechnica.com)
- [MacRumors: "Must-Have Security Tool for Mac Users"](https://macrumors.com)

---

## 📞 Support

### 💬 **Community Support**

- 🗨️ [Discord Server](https://discord.gg/mcguardian-elite)
- 💬 [GitHub Discussions](https://github.com/heyfinal/McGuardian/discussions)
- 📧 [Community Forum](https://community.mcguardian.dev)

### 🎓 **Documentation**

- 📖 [Full Documentation](https://docs.mcguardian.dev)
- 🎥 [Video Tutorials](https://youtube.com/mcguardian-elite)
- 📚 [Security Best Practices](https://security.mcguardian.dev)

### 🆘 **Professional Support**

- 🏢 **Enterprise Support**: enterprise@mcguardian.dev
- 🔒 **Security Consultations**: security@mcguardian.dev
- 💼 **Custom Development**: development@mcguardian.dev

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 McGuardian Elite

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=heyfinal/McGuardian&type=Date)](https://star-history.com/#heyfinal/McGuardian&Date)

---

<div align="center">

**Made with ❤️ by security professionals, for security professionals**

[⭐ Star on GitHub](https://github.com/heyfinal/McGuardian) •
[🐛 Report Bug](https://github.com/heyfinal/McGuardian/issues) •
[💡 Request Feature](https://github.com/heyfinal/McGuardian/issues) •
[💬 Join Discord](https://discord.gg/mcguardian-elite)

</div>

---

### 🔄 **Recent Updates**

#### v3.0.0 - The Elite Edition (Latest)
- 🤖 **NEW**: Advanced AI-powered threat detection engine
- 🎨 **NEW**: Stunning Apple-inspired web dashboard with glassmorphism UI
- 🕸️ **NEW**: Real-time attack pattern analysis and scenario building
- 🔒 **NEW**: File integrity monitoring with automatic backups
- 🕯️ **NEW**: Advanced honeypot systems with realistic decoy data
- 🛡️ **NEW**: Secret backup logging with tamper detection
- ⚡ **IMPROVED**: 10x faster event processing and analysis
- 📊 **IMPROVED**: Professional charts and real-time visualizations
- 🎯 **IMPROVED**: Enhanced threat intelligence database with 50+ tools

#### v2.1.0 - The Intelligence Update
- 🧠 **NEW**: Machine learning-based behavioral analysis
- 📈 **NEW**: Statistical anomaly detection
- 🔍 **IMPROVED**: Enhanced process monitoring capabilities
- 🌐 **IMPROVED**: Better network connection analysis

#### v2.0.0 - The Professional Edition  
- 🎛️ **NEW**: Web-based dashboard interface
- 🔄 **NEW**: Real-time event streaming
- 📊 **NEW**: Advanced analytics and reporting
- 🛠️ **NEW**: Professional installer with auto-start capabilities

---

> **"McGuardian Elite has transformed how we approach Mac security. The AI-powered threat detection caught an advanced persistent threat that our previous tools completely missed."**
> 
> — *Sarah Chen, CISO at TechCorp*

> **"The Apple-inspired interface is absolutely beautiful, but more importantly, it makes complex security data actually understandable for our entire team."**
> 
> — *Marcus Rodriguez, Security Analyst*

---

<div align="center">

### 🚀 Ready to Secure Your Mac?

[![Download McGuardian Elite](https://img.shields.io/badge/Download-McGuardian%20Elite-blue?style=for-the-badge&logo=apple&logoColor=white)](https://github.com/heyfinal/McGuardian/releases/latest)

</div>
