#!/usr/bin/env python3
"""
McGuardian Elite v3.0.0 - Advanced Threat Intelligence & Response System
Features: Comprehensive threat intelligence, attack pattern analysis, file integrity monitoring,
countermeasure recommendations, secret backup logging, and advanced forensics.
"""

__version__ = '3.0.0'
__revision__ = '1'

import os
import sys
import threading
import time
import subprocess
import logging
import logging.handlers
import json
import hashlib
import hmac
import venv
import sqlite3
import statistics
import re
import socket
import struct
import math
import shutil
import gzip
import pickle
from datetime import datetime, timedelta
from collections import defaultdict, deque, Counter
from pathlib import Path
import base64
import zipfile
import tempfile
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import uuid

# ------------------ Enhanced Data Classes ------------------
@dataclass
class ThreatEvent:
    timestamp: datetime
    event_type: str
    source: str
    description: str
    risk_score: int
    risk_factors: List[str]
    raw_data: Dict
    file_backup_path: Optional[str] = None
    related_events: List[str] = None

@dataclass
class AttackScenario:
    scenario_id: str
    attack_type: str
    confidence: float
    events: List[ThreatEvent]
    timeline: List[datetime]
    description: str
    countermeasures: List[str]
    severity: str

# ------------------ Comprehensive Threat Intelligence Database ------------------
class ThreatIntelligence:
    def __init__(self):
        self.penetration_tools = {
            'nmap': {
                'category': 'Network Scanner',
                'description': 'Network Mapper (Nmap) is a powerful network discovery and security auditing tool. Attackers use it to scan networks and discover open ports, running services, operating systems, and potential vulnerabilities. It can perform stealth scans to avoid detection and is often the first step in network reconnaissance.',
                'attack_uses': [
                    'Port scanning to find open services',
                    'Operating system fingerprinting',
                    'Service version detection',
                    'Vulnerability scanning with NSE scripts',
                    'Network topology discovery',
                    'Firewall evasion techniques'
                ],
                'detection_indicators': ['nmap', 'zenmap'],
                'risk_level': 'HIGH',
                'countermeasures': [
                    'Block scanning attempts at firewall level',
                    'Monitor for port scan patterns in logs',
                    'Use intrusion detection systems (IDS)',
                    'Implement port knocking for sensitive services'
                ]
            },
            'nc': {
                'category': 'Network Utility/Backdoor',
                'description': 'Netcat (nc) is known as the "Swiss Army knife" of networking. While legitimate for network troubleshooting, attackers heavily abuse it for establishing reverse shells, transferring files, and maintaining persistent access to compromised systems.',
                'attack_uses': [
                    'Creating reverse shells for remote access',
                    'Establishing bind shells on compromised systems',
                    'File transfer between attacker and victim',
                    'Port redirection and tunneling',
                    'Banner grabbing and service enumeration',
                    'Chat sessions between attackers'
                ],
                'detection_indicators': ['nc', 'netcat', 'ncat'],
                'risk_level': 'CRITICAL',
                'countermeasures': [
                    'Block netcat traffic at network perimeter',
                    'Monitor for suspicious network connections',
                    'Restrict execution of network utilities',
                    'Use application whitelisting'
                ]
            },
            'ssh': {
                'category': 'Remote Access',
                'description': 'Secure Shell (SSH) provides encrypted remote access to systems. While legitimate, attackers use SSH for lateral movement, persistent access, and tunneling traffic through compromised systems.',
                'attack_uses': [
                    'Lateral movement between compromised systems',
                    'Maintaining persistent access',
                    'Tunneling traffic through compromised hosts',
                    'File transfer using SCP/SFTP',
                    'Port forwarding for accessing internal services',
                    'Privilege escalation attempts'
                ],
                'detection_indicators': ['ssh', 'sshd'],
                'risk_level': 'MEDIUM',
                'countermeasures': [
                    'Use key-based authentication only',
                    'Monitor failed authentication attempts',
                    'Implement connection rate limiting',
                    'Use fail2ban for brute force protection'
                ]
            },
            'masscan': {
                'category': 'High-Speed Scanner',
                'description': 'Masscan is an extremely fast port scanner capable of scanning the entire internet in under 6 minutes. Attackers use it for rapid reconnaissance of large network ranges to identify potential targets.',
                'attack_uses': [
                    'Rapid scanning of large IP ranges',
                    'Internet-wide reconnaissance',
                    'Identifying exposed services quickly',
                    'Banner grabbing at scale'
                ],
                'detection_indicators': ['masscan'],
                'risk_level': 'HIGH',
                'countermeasures': [
                    'Rate limit incoming connections',
                    'Deploy honeypots to detect scanning',
                    'Use geographic IP blocking'
                ]
            },
            'metasploit': {
                'category': 'Exploitation Framework',
                'description': 'Metasploit is a comprehensive penetration testing framework containing hundreds of exploits, payloads, and auxiliary modules. Attackers use it to exploit known vulnerabilities and gain system access.',
                'attack_uses': [
                    'Exploiting known vulnerabilities',
                    'Generating custom payloads',
                    'Post-exploitation activities',
                    'Privilege escalation',
                    'Persistence mechanisms'
                ],
                'detection_indicators': ['msfconsole', 'msfvenom', 'metasploit'],
                'risk_level': 'CRITICAL',
                'countermeasures': [
                    'Keep systems fully patched',
                    'Use endpoint detection and response (EDR)',
                    'Implement application sandboxing'
                ]
            },
            'wireshark': {
                'category': 'Network Analyzer',
                'description': 'Wireshark is a network protocol analyzer that captures and analyzes network traffic. Attackers use it to intercept sensitive data, analyze network protocols, and understand network topology.',
                'attack_uses': [
                    'Capturing sensitive network traffic',
                    'Password sniffing on unsecured protocols',
                    'Network reconnaissance',
                    'Man-in-the-middle attack analysis'
                ],
                'detection_indicators': ['wireshark', 'tshark'],
                'risk_level': 'MEDIUM',
                'countermeasures': [
                    'Use encrypted protocols (HTTPS, SSH, VPN)',
                    'Implement network segmentation',
                    'Monitor for promiscuous mode interfaces'
                ]
            }
        }
        
        self.attack_patterns = {
            'reconnaissance': {
                'indicators': ['nmap', 'masscan', 'wireshark', 'ping sweep'],
                'description': 'Attacker is gathering information about network topology, open services, and potential vulnerabilities',
                'next_steps': ['exploitation', 'lateral_movement'],
                'urgency': 'HIGH'
            },
            'initial_access': {
                'indicators': ['ssh brute force', 'exploit attempt', 'malicious file execution'],
                'description': 'Attacker has gained initial foothold in the system',
                'next_steps': ['privilege_escalation', 'persistence'],
                'urgency': 'CRITICAL'
            },
            'persistence': {
                'indicators': ['launchd modification', 'cron job creation', 'startup item'],
                'description': 'Attacker is establishing persistent access to survive reboots',
                'next_steps': ['lateral_movement', 'data_exfiltration'],
                'urgency': 'CRITICAL'
            },
            'lateral_movement': {
                'indicators': ['ssh lateral', 'smb enumeration', 'credential dumping'],
                'description': 'Attacker is moving through the network to access additional systems',
                'next_steps': ['privilege_escalation', 'data_exfiltration'],
                'urgency': 'HIGH'
            },
            'data_exfiltration': {
                'indicators': ['large file transfers', 'compression activity', 'external connections'],
                'description': 'Attacker is stealing sensitive data from the system',
                'next_steps': ['cover_tracks'],
                'urgency': 'CRITICAL'
            }
        }

# ------------------ File Integrity Monitor ------------------
class FileIntegrityMonitor:
    def __init__(self, backup_dir):
        self.backup_dir = backup_dir
        self.file_hashes = {}
        self.backup_retention_days = 30
        os.makedirs(backup_dir, exist_ok=True)
        os.chmod(backup_dir, 0o700)
    
    def create_file_backup(self, file_path):
        """Create timestamped backup of file before modification"""
        try:
            if not os.path.exists(file_path) or os.path.isdir(file_path):
                return None
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"{os.path.basename(file_path)}_{timestamp}.backup"
            backup_path = os.path.join(self.backup_dir, backup_name)
            
            shutil.copy2(file_path, backup_path)
            
            # Compress backup to save space
            with open(backup_path, 'rb') as f_in:
                with gzip.open(f"{backup_path}.gz", 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(backup_path)
            
            return f"{backup_path}.gz"
        except Exception as e:
            logger.error(f"Failed to backup file {file_path}: {e}")
            return None
    
    def calculate_file_hash(self, file_path):
        """Calculate SHA-256 hash of file"""
        try:
            hash_sha256 = hashlib.sha256()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except:
            return None
    
    def check_file_integrity(self, file_path):
        """Check if file has been modified"""
        current_hash = self.calculate_file_hash(file_path)
        if file_path in self.file_hashes:
            return current_hash == self.file_hashes[file_path]
        else:
            self.file_hashes[file_path] = current_hash
            return True
    
    def restore_file(self, file_path, backup_path):
        """Restore file from backup"""
        try:
            with gzip.open(backup_path, 'rb') as f_in:
                with open(file_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            return True
        except Exception as e:
            logger.error(f"Failed to restore file {file_path}: {e}")
            return False

# ------------------ Attack Pattern Analyzer ------------------
class AttackPatternAnalyzer:
    def __init__(self):
        self.threat_intel = ThreatIntelligence()
        self.event_window = timedelta(hours=2)  # 2-hour window for pattern analysis
        self.events = deque()
        self.active_scenarios = []
    
    def add_event(self, event: ThreatEvent):
        """Add event and analyze patterns"""
        self.events.append(event)
        self.cleanup_old_events()
        self.analyze_attack_patterns()
    
    def cleanup_old_events(self):
        """Remove events older than analysis window"""
        cutoff = datetime.now() - self.event_window
        while self.events and self.events[0].timestamp < cutoff:
            self.events.popleft()
    
    def analyze_attack_patterns(self):
        """Analyze events for attack patterns"""
        if len(self.events) < 2:
            return
        
        # Group events by type and time proximity
        event_groups = self.group_events_by_proximity()
        
        for group in event_groups:
            scenario = self.identify_attack_scenario(group)
            if scenario:
                self.active_scenarios.append(scenario)
                self.log_attack_scenario(scenario)
    
    def group_events_by_proximity(self):
        """Group events that occur close in time"""
        groups = []
        current_group = []
        
        for event in sorted(self.events, key=lambda x: x.timestamp):
            if not current_group or (event.timestamp - current_group[-1].timestamp) < timedelta(minutes=15):
                current_group.append(event)
            else:
                if len(current_group) > 1:
                    groups.append(current_group)
                current_group = [event]
        
        if len(current_group) > 1:
            groups.append(current_group)
        
        return groups
    
    def identify_attack_scenario(self, events: List[ThreatEvent]) -> Optional[AttackScenario]:
        """Identify attack scenarios from grouped events"""
        event_types = [e.event_type.lower() for e in events]
        
        # Reconnaissance scenario
        if any('scan' in et or 'nmap' in et for et in event_types):
            return AttackScenario(
                scenario_id=str(uuid.uuid4()),
                attack_type='reconnaissance',
                confidence=0.8,
                events=events,
                timeline=[e.timestamp for e in events],
                description=f"Network reconnaissance detected with {len(events)} related events. Attacker is likely mapping network topology and identifying potential targets for exploitation.",
                countermeasures=[
                    "Immediately block source IP addresses",
                    "Enable enhanced logging on network devices", 
                    "Deploy honeypots to detect further scanning",
                    "Review firewall rules for unnecessary open ports"
                ],
                severity='HIGH'
            )
        
        # Lateral movement scenario
        if any('ssh' in et for et in event_types) and len(events) >= 3:
            return AttackScenario(
                scenario_id=str(uuid.uuid4()),
                attack_type='lateral_movement',
                confidence=0.7,
                events=events,
                timeline=[e.timestamp for e in events],
                description=f"Potential lateral movement detected with {len(events)} SSH-related events. Attacker may have compromised credentials and is moving between systems.",
                countermeasures=[
                    "Force password resets for all SSH-accessible accounts",
                    "Enable multi-factor authentication",
                    "Audit SSH key pairs and remove unauthorized keys",
                    "Implement network segmentation"
                ],
                severity='CRITICAL'
            )
        
        # Data exfiltration scenario  
        if any('file' in et for et in event_types) and len(events) >= 5:
            return AttackScenario(
                scenario_id=str(uuid.uuid4()),
                attack_type='data_exfiltration',
                confidence=0.6,
                events=events,
                timeline=[e.timestamp for e in events],
                description=f"Possible data exfiltration detected with {len(events)} file access events. Large amounts of data may be being accessed and potentially stolen.",
                countermeasures=[
                    "Monitor outbound network traffic for data transfers",
                    "Implement data loss prevention (DLP) controls",
                    "Audit file access permissions",
                    "Consider disconnecting from network temporarily"
                ],
                severity='CRITICAL'
            )
        
        return None
    
    def log_attack_scenario(self, scenario: AttackScenario):
        """Log detailed attack scenario"""
        msg = f"""
🚨 ATTACK SCENARIO DETECTED 🚨
═══════════════════════════════════════════════════════════════

🎯 ATTACK TYPE: {scenario.attack_type.upper()}
🔴 SEVERITY: {scenario.severity}
📊 CONFIDENCE: {scenario.confidence*100:.1f}%
🆔 SCENARIO ID: {scenario.scenario_id}

📝 DESCRIPTION:
{scenario.description}

⏰ TIMELINE ({len(scenario.events)} events):
{chr(10).join([f"  • {e.timestamp.strftime('%H:%M:%S')} - {e.event_type}: {e.description}" for e in scenario.events[-5:]])}

🛡️ IMMEDIATE COUNTERMEASURES:
{chr(10).join([f"  • {cm}" for cm in scenario.countermeasures])}

⚠️ THREAT ASSESSMENT:
This attack pattern suggests an active threat. Immediate action is required to prevent further compromise.

═══════════════════════════════════════════════════════════════
"""
        alert.critical(msg)
        lay.critical(f"🚨 CRITICAL SECURITY ALERT: {scenario.attack_type.upper()} attack detected! Check security alerts log immediately.")

# ------------------ Secret Backup Logger ------------------
class SecretBackupLogger:
    def __init__(self, secret_dir):
        self.secret_dir = secret_dir
        self.secret_log_file = os.path.join(secret_dir, '.system_cache.log')
        os.makedirs(secret_dir, exist_ok=True)
        os.chmod(secret_dir, 0o700)
        
    def log_secret(self, message):
        """Log to secret backup location"""
        timestamp = datetime.now().isoformat()
        entry = f"{timestamp} | {message}\n"
        
        # Append to secret log
        with open(self.secret_log_file, 'a') as f:
            f.write(entry)
        os.chmod(self.secret_log_file, 0o600)
    
    def verify_log_integrity(self, main_log_file):
        """Compare main log with secret backup to detect tampering"""
        try:
            # Simple comparison - in production would use more sophisticated methods
            if not os.path.exists(main_log_file) or not os.path.exists(self.secret_log_file):
                return True  # Can't verify if files don't exist
            
            main_size = os.path.getsize(main_log_file)
            secret_size = os.path.getsize(self.secret_log_file)
            
            # If main log is significantly smaller, might be tampered
            if main_size < secret_size * 0.8:
                return False
            
            return True
        except:
            return True

# ------------------ Enhanced Configuration ------------------
BASE_DIR = os.path.expanduser('~/Library/Logs/McGuardianElite')
LAYMEM_DIR = os.path.join(BASE_DIR, 'human_readable')
ANALYTICS_DIR = os.path.join(BASE_DIR, 'analytics')
BACKUP_DIR = os.path.join(BASE_DIR, 'file_backups')
SECRET_DIR = os.path.expanduser('~/.cache/system_logs')

LOG_FILE = os.path.join(BASE_DIR, 'technical.log')
LAYMEM_FILE = os.path.join(LAYMEM_DIR, 'security_explained.log')
ALERTS_FILE = os.path.join(LAYMEM_DIR, 'critical_alerts.log')
CHAIN_FILE = os.path.join(BASE_DIR, 'integrity.chain')
DB_FILE = os.path.join(ANALYTICS_DIR, 'threat_intelligence.db')

HONEYPOT_DIR = os.path.expanduser('~/Library/adult')
ADVANCED_HONEYPOT_DIR = os.path.expanduser('~/Documents/.confidential')
VENV_DIR = os.path.expanduser('~/.mcguardian_elite_venv')

REQUIREMENTS = [
    'watchdog==3.0.0',
    'psutil==5.9.6', 
    'cryptography==41.0.7',
    'flask==2.3.3',
    'requests==2.31.0'
]

HMAC_KEY_FILE = os.path.expanduser('~/.mcguardian_elite_hmac')

# Initialize components
file_monitor = None
pattern_analyzer = None
secret_logger = None

def secure_dirs():
    """Create and secure all directories"""
    for d in [BASE_DIR, LAYMEM_DIR, ANALYTICS_DIR, BACKUP_DIR, SECRET_DIR, HONEYPOT_DIR, ADVANCED_HONEYPOT_DIR]:
        os.makedirs(d, exist_ok=True)
        os.chmod(d, 0o700)

def setup_honeypots():
    """Create comprehensive honeypot files"""
    honeypot_content = {
        'passwords.txt': 'admin:SuperSecret123\nroot:RootPassword456\ndbadmin:DatabasePass789',
        'financial_data.xlsx': 'Account,Balance,SSN\n123456789,$50000,123-45-6789\n987654321,$75000,987-65-4321',
        'ssh_keys.pem': '-----BEGIN OPENSSH PRIVATE KEY-----\nb3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAA...',
        'company_secrets.docx': 'CONFIDENTIAL: Project Aurora budget $5M, Client: Government, Classification: SECRET',
        'bitcoin_wallet.dat': '{"version": 1, "private_key": "5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTJ"}',
        'customer_database.sql': 'INSERT INTO customers VALUES (1, "John Doe", "john@email.com", "4532-1234-5678-9012");',
        'vpn_config.ovpn': 'client\nremote vpn.company.com 1194\nauth-user-pass credentials.txt',
        'network_diagram.png': 'Binary file simulating network topology diagram',
        'incident_response.pdf': 'INCIDENT RESPONSE PLAN - FOR AUTHORIZED PERSONNEL ONLY',
        'backup_credentials.json': '{"aws_key": "AKIAIOSFODNN7EXAMPLE", "secret": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"}'
    }
    
    for filename, content in honeypot_content.items():
        for directory in [HONEYPOT_DIR, ADVANCED_HONEYPOT_DIR]:
            filepath = os.path.join(directory, filename)
            with open(filepath, 'w') as f:
                f.write(content)
            os.chmod(filepath, 0o600)

def bootstrap_venv():
    """Enhanced virtual environment setup"""
    if not os.path.isdir(VENV_DIR):
        print("🔧 Creating virtual environment...")
        venv.create(VENV_DIR, with_pip=True)
    
    pip_bin = os.path.join(VENV_DIR, 'bin', 'pip')
    print("📦 Installing enhanced dependencies...")
    
    for req in REQUIREMENTS:
        try:
            subprocess.check_call([pip_bin, 'install', '--quiet', req], 
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Warning: Failed to install {req}")

# Initialize everything
secure_dirs()
setup_honeypots() 
bootstrap_venv()

# Import after venv setup
import sys as _sys
_major, _minor = _sys.version_info.major, _sys.version_info.minor
_sitepkg = os.path.join(VENV_DIR, 'lib', f'python{_major}.{_minor}', 'site-packages')
if os.path.isdir(_sitepkg): 
    _sys.path.insert(0, _sitepkg)

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    import psutil
    from cryptography.fernet import Fernet
except ImportError as e:
    print(f"❌ Critical dependencies missing: {e}")
    sys.exit(1)

# Initialize components after imports
file_monitor = FileIntegrityMonitor(BACKUP_DIR)
pattern_analyzer = AttackPatternAnalyzer()
secret_logger = SecretBackupLogger(SECRET_DIR)

# Enhanced logging setup
logger = logging.getLogger('McGuardianElite')
logger.setLevel(logging.INFO)

file_hdl = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=20*1024*1024, backupCount=10)
file_hdl.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_hdl)

lay = logging.getLogger('EliteExplanations') 
lay.setLevel(logging.INFO)
lay_hdl = logging.handlers.RotatingFileHandler(LAYMEM_FILE, maxBytes=10*1024*1024, backupCount=10)
lay_hdl.setFormatter(logging.Formatter('%(asctime)s\n%(message)s\n' + '='*80 + '\n'))
lay.addHandler(lay_hdl)

alert = logging.getLogger('EliteAlerts')
alert.setLevel(logging.WARNING)
alert_hdl = logging.handlers.RotatingFileHandler(ALERTS_FILE, maxBytes=5*1024*1024, backupCount=5)
alert_hdl.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s\n%(message)s\n' + '='*100 + '\n'))
alert.addHandler(alert_hdl)

# Auto-save thread
def auto_save_logs():
    """Auto-save logs every 30 minutes"""
    while True:
        time.sleep(1800)  # 30 minutes
        try:
            # Force log rotation
            for handler in [file_hdl, lay_hdl, alert_hdl]:
                handler.doRollover()
            logger.info("Auto-save: Logs rotated successfully")
        except Exception as e:
            logger.error(f"Auto-save failed: {e}")

# Enhanced file system handler
class EliteFileSystemHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return
            
        file_path = event.src_path
        
        # Create backup before modification
        backup_path = None
        if event.event_type in ['modified', 'deleted']:
            backup_path = file_monitor.create_file_backup(file_path)
        
        # Detailed file analysis
        file_info = self.analyze_file_change(file_path, event.event_type)
        risk_score = file_info['risk_score']
        
        # Create threat event
        threat_event = ThreatEvent(
            timestamp=datetime.now(),
            event_type=f"file_{event.event_type}",
            source=file_path,
            description=file_info['description'],
            risk_score=risk_score,
            risk_factors=file_info['risk_factors'],
            raw_data={'event': event.__dict__, 'file_info': file_info},
            file_backup_path=backup_path
        )
        
        # Add to pattern analyzer
        pattern_analyzer.add_event(threat_event)
        
        # Detailed logging
        technical_msg = f"File {event.event_type}: {file_path}"
        logger.info(f"{technical_msg} (Risk: {risk_score}/100)")
        
        # Human-readable explanation
        explanation = self.create_detailed_explanation(file_info, backup_path)
        lay.info(explanation)
        
        # Secret backup logging
        secret_logger.log_secret(f"FILE_{event.event_type.upper()}|{file_path}|{risk_score}")
        
        # High-risk alerts
        if risk_score >= 70:
            alert.critical(f"🚨 CRITICAL FILE EVENT: {explanation}")
    
    def analyze_file_change(self, file_path, event_type):
        """Comprehensive file change analysis"""
        risk_score = 10  # Base risk
        risk_factors = []
        description = f"File {event_type} detected"
        
        try:
            file_stats = os.stat(file_path) if os.path.exists(file_path) else None
            file_size = file_stats.st_size if file_stats else 0
            
            # Critical system files
            critical_paths = ['/etc/', '/usr/bin/', '/usr/sbin/', '/System/', '/Library/LaunchDaemons/']
            if any(file_path.startswith(path) for path in critical_paths):
                risk_score += 40
                risk_factors.append("Critical system file modification")
                description += " - CRITICAL SYSTEM FILE AFFECTED"
            
            # Executable files
            if file_path.endswith(('.app', '.dmg', '.pkg', '.sh', '.py', '.pl', '.rb')):
                risk_score += 25
                risk_factors.append("Executable file modification")
            
            # Configuration files
            if any(file_path.endswith(ext) for ext in ['.plist', '.conf', '.cfg', '.ini']):
                risk_score += 20
                risk_factors.append("Configuration file modification")
            
            # Large files (potential data staging)
            if file_size > 50 * 1024 * 1024:  # 50MB
                risk_score += 15
                risk_factors.append("Large file operation (potential data staging)")
            
            # Hidden files
            if '/.' in file_path:
                risk_score += 15
                risk_factors.append("Hidden file activity")
            
            # File integrity check
            if not file_monitor.check_file_integrity(file_path):
                risk_score += 30
                risk_factors.append("File integrity violation detected")
            
        except Exception as e:
            risk_factors.append(f"Analysis error: {e}")
        
        return {
            'risk_score': min(risk_score, 100),
            'risk_factors': risk_factors,
            'description': description,
            'file_size': file_size,
            'file_type': self.identify_file_type(file_path)
        }
    
    def identify_file_type(self, file_path):
        """Identify file type and purpose"""
        ext = os.path.splitext(file_path)[1].lower()
        
        file_types = {
            '.plist': 'macOS Property List (Configuration)',
            '.dmg': 'macOS Disk Image (Software Package)',
            '.app': 'macOS Application Bundle',
            '.pkg': 'macOS Installer Package',
            '.sh': 'Shell Script (Executable)',
            '.py': 'Python Script',
            '.js': 'JavaScript File',
            '.log': 'Log File',
            '.conf': 'Configuration File',
            '.key': 'Cryptographic Key File',
            '.pem': 'Certificate/Key File',
            '.sql': 'Database File',
            '.db': 'Database File'
        }
        
        return file_types.get(ext, 'Unknown File Type')
    
    def create_detailed_explanation(self, file_info, backup_path):
        """Create comprehensive human-readable explanation"""
        risk_score = file_info['risk_score']
        
        if risk_score >= 70:
            risk_level = "🔴 CRITICAL RISK"
            urgency = "IMMEDIATE ACTION REQUIRED"
        elif risk_score >= 40:
            risk_level = "🟠 HIGH RISK"
            urgency = "Investigation needed soon"
        elif risk_score >= 20:
            risk_level = "🟡 MEDIUM RISK"
            urgency = "Monitor for patterns"
        else:
            risk_level = "🟢 LOW RISK"
            urgency = "Normal system activity"
        
        explanation = f"""
{risk_level} - File System Event Detected

📁 FILE DETAILS:
  • File Type: {file_info['file_type']}
  • File Size: {file_info['file_size']:,} bytes
  • Risk Factors: {', '.join(file_info['risk_factors']) if file_info['risk_factors'] else 'None'}

📋 WHAT HAPPENED:
{file_info['description']}

🔍 DETAILED ANALYSIS:
This file operation was detected by the monitoring system. """
        
        if risk_score >= 40:
            explanation += """This is considered a high-risk event that requires investigation. 
System files, executables, or sensitive data may have been affected."""
        elif risk_score >= 20:
            explanation += """This file change is potentially suspicious and should be monitored."""
        else:
            explanation += """This appears to be normal system activity but is being logged for completeness."""
        
        if backup_path:
            explanation += f"""

💾 FILE BACKUP:
A backup copy was automatically created at: {backup_path}
This backup can be used to restore the file if needed."""
        
        explanation += f"""

⚡ URGENCY LEVEL: {urgency}
📊 RISK SCORE: {risk_score}/100

🛡️ RECOMMENDED ACTIONS:"""
        
        if risk_score >= 70:
            explanation += """
  • Immediately investigate this file change
  • Check if you authorized this modification
  • Scan system for malware if change was unauthorized
  • Consider restoring from backup if file was compromised"""
        elif risk_score >= 40:
            explanation += """
  • Review what programs were running when this occurred
  • Verify the file change was authorized
  • Monitor for related suspicious activity"""
        else:
            explanation += """
  • Continue monitoring for patterns
  • No immediate action required unless part of broader suspicious activity"""
        
        return explanation

# Enhanced process monitoring
def elite_process_monitor():
    """Advanced process monitoring with threat intelligence"""
    seen_processes = set()
    threat_intel = ThreatIntelligence()
    
    while True:
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_info', 'create_time']):
                try:
                    pid = proc.info['pid']
                    if pid in seen_processes:
                        continue
                    
                    seen_processes.add(pid)
                    name = proc.info['name'].lower()
                    cmdline = ' '.join(proc.info['cmdline'] or [])
                    
                    # Check against threat intelligence
                    threat_info = None
                    for tool_name, tool_info in threat_intel.penetration_tools.items():
                        if any(indicator in name for indicator in tool_info['detection_indicators']):
                            threat_info = tool_info
                            break
                    
                    if threat_info or any(keyword in name for keyword in ['nc', 'nmap', 'masscan', 'wireshark']):
                        risk_score = 80 if threat_info else 60
                        
                        # Create detailed threat event
                        threat_event = ThreatEvent(
                            timestamp=datetime.now(),
                            event_type=f"process_launch_{name}",
                            source=f"PID {pid}",
                            description=f"Potential penetration testing tool detected: {name}",
                            risk_score=risk_score,
                            risk_factors=["Known penetration testing tool"],
                            raw_data={'pid': pid, 'name': name, 'cmdline': cmdline}
                        )
                        
                        pattern_analyzer.add_event(threat_event)
                        
                        # Detailed logging with threat intelligence
                        detailed_explanation = create_process_threat_explanation(name, threat_info, cmdline)
                        
                        logger.warning(f"THREAT DETECTED: {name} (PID {pid}) - {cmdline[:100]}")
                        lay.warning(detailed_explanation)
                        secret_logger.log_secret(f"THREAT_PROCESS|{name}|{pid}|{risk_score}")
                        
                        if risk_score >= 70:
                            alert.critical(f"🚨 PENETRATION TESTING TOOL DETECTED: {detailed_explanation}")
                
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except Exception as e:
            logger.error(f"Process monitoring error: {e}")
        
        time.sleep(5)

def create_process_threat_explanation(process_name, threat_info, cmdline):
    """Create detailed threat explanation for processes"""
    if not threat_info:
        return f"⚠️ Suspicious process detected: {process_name}"
    
    explanation = f"""
🚨 PENETRATION TESTING TOOL DETECTED: {process_name.upper()}

🎯 TOOL CATEGORY: {threat_info['category']}
🔴 RISK LEVEL: {threat_info['risk_level']}

📋 WHAT THIS TOOL DOES:
{threat_info['description']}

⚔️ HOW ATTACKERS USE THIS TOOL:
"""
    for use in threat_info['attack_uses']:
        explanation += f"  • {use}\n"
    
    explanation += f"""
💻 COMMAND LINE DETECTED:
{cmdline[:200]}{'...' if len(cmdline) > 200 else ''}

🛡️ IMMEDIATE COUNTERMEASURES:
"""
    for countermeasure in threat_info['countermeasures']:
        explanation += f"  • {countermeasure}\n"
    
    explanation += """
🚨 CRITICAL RECOMMENDATIONS:
  • Immediately determine if this tool was launched by an authorized user
  • If unauthorized, disconnect the system from the network
  • Run a comprehensive malware scan
  • Check for signs of system compromise
  • Review system logs for other suspicious activity
  • Consider forensic analysis if this appears to be an attack

⚠️ This detection indicates potential penetration testing or malicious activity. Take immediate action to secure your system."""
    
    return explanation

# Network monitoring
def elite_network_monitor():
    """Enhanced network monitoring"""
    while True:
        try:
            connections = psutil.net_connections(kind='inet')
            suspicious_connections = []
            
            for conn in connections:
                if conn.status == 'ESTABLISHED' and conn.raddr:
                    # Check for suspicious connections
                    remote_ip = conn.raddr.ip
                    remote_port = conn.raddr.port
                    
                    risk_score = 0
                    risk_factors = []
                    
                    # Suspicious ports
                    if remote_port in [22, 23, 1337, 31337, 4444, 5555, 6666, 7777, 8080, 9999]:
                        risk_score += 30
                        risk_factors.append(f"Connection to suspicious port {remote_port}")
                    
                    # External connections
                    if not any(remote_ip.startswith(prefix) for prefix in ['127.', '192.168.', '10.', '172.']):
                        risk_score += 20
                        risk_factors.append("External network connection")
                    
                    if risk_score >= 30:
                        threat_event = ThreatEvent(
                            timestamp=datetime.now(),
                            event_type="suspicious_network_connection",
                            source=f"{conn.laddr.ip}:{conn.laddr.port}",
                            description=f"Suspicious network connection to {remote_ip}:{remote_port}",
                            risk_score=risk_score,
                            risk_factors=risk_factors,
                            raw_data={'connection': conn._asdict()}
                        )
                        
                        pattern_analyzer.add_event(threat_event)
                        
                        msg = f"Suspicious connection: {conn.laddr.ip}:{conn.laddr.port} -> {remote_ip}:{remote_port}"
                        logger.warning(msg)
                        lay.warning(f"🌐 NETWORK ALERT: {msg}\nRisk factors: {', '.join(risk_factors)}")
                        secret_logger.log_secret(f"NETWORK_SUSPICIOUS|{remote_ip}|{remote_port}|{risk_score}")
        
        except Exception as e:
            logger.error(f"Network monitoring error: {e}")
        
        time.sleep(60)

# Main function
def main():
    """Main execution with enhanced monitoring"""
    print(f"🛡️ McGuardian Elite v{__version__} - Advanced Threat Intelligence System")
    print("🔧 Initializing comprehensive security monitoring...")
    
    logger.info(f"McGuardian Elite v{__version__} starting with advanced threat intelligence")
    lay.info("🛡️ McGuardian Elite Security System Activated\n\nThis advanced system will monitor your Mac for security threats and provide detailed explanations of any suspicious activity.")
    
    # Start file monitoring
    observer = Observer()
    elite_handler = EliteFileSystemHandler()
    
    monitor_paths = [
        '/etc', '/usr/bin', '/usr/sbin', '/System/', '/Library/',
        os.path.expanduser('~/Documents'), os.path.expanduser('~/Downloads'),
        HONEYPOT_DIR, ADVANCED_HONEYPOT_DIR
    ]
    
    for path in monitor_paths:
        if os.path.exists(path):
            observer.schedule(elite_handler, path, recursive=True)
            print(f"🔍 Monitoring: {path}")
    
    # Start monitoring threads
    threads = [
        threading.Thread(target=elite_process_monitor, daemon=True, name="EliteProcessMonitor"),
        threading.Thread(target=elite_network_monitor, daemon=True, name="EliteNetworkMonitor"), 
        threading.Thread(target=auto_save_logs, daemon=True, name="AutoSaveManager")
    ]
    
    for thread in threads:
        thread.start()
        print(f"✅ Started {thread.name}")
    
    observer.start()
    print("✅ File System Monitor Active")
    
    print(f"""
🎯 McGuardian Elite is now providing comprehensive protection!

📊 Monitoring Dashboard:
  • Human-readable logs: {LAYMEM_FILE}
  • Critical alerts: {ALERTS_FILE}  
  • Technical logs: {LOG_FILE}
  • File backups: {BACKUP_DIR}

🔐 Advanced Features Active:
  • Real-time threat intelligence analysis
  • Attack pattern recognition
  • File integrity monitoring with backups
  • Secret backup logging for tamper detection
  • 30-minute auto-save intervals

Press Ctrl+C to stop (NOT recommended for continuous protection)
""")
    
    try:
        while True:
            time.sleep(30)
            # Verify log integrity every 30 seconds
            if not secret_logger.verify_log_integrity(LOG_FILE):
                alert.critical("🚨 LOG TAMPERING DETECTED! Main logs may have been modified!")
    except KeyboardInterrupt:
        print("\n🛑 Shutting down McGuardian Elite...")
        observer.stop()
        observer.join()
        logger.info("McGuardian Elite stopped by user")

if __name__ == '__main__':
    main()
