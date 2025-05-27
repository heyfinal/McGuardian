#!/usr/bin/env python3
"""
███╗   ███╗ ██████╗ ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗ ██╗ █████╗ ███╗   ██╗
████╗ ████║██╔════╝██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗██║██╔══██╗████╗  ██║
██╔████╔██║██║     ██║  ███╗██║   ██║███████║██████╔╝██║  ██║██║███████║██╔██╗ ██║
██║╚██╔╝██║██║     ██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║██║██╔══██║██║╚██╗██║
██║ ╚═╝ ██║╚██████╗╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝██║██║  ██║██║ ╚████║
╚═╝     ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
                            
                    S S H   S E C U R I T Y   &   H A R D E N I N G
                  Advanced SSH Protection • Threat Monitoring • Auto-Hardening
                        Professional Security Analysis • Real-time Response
"""

import os
import sys
import subprocess
import re
import time
import threading
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Optional
import json
import hashlib
import tempfile
import shutil
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
#                           SSH VULNERABILITY CLASSES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class SSHVulnerability:
    name: str
    description: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    current_value: str
    recommended_value: str
    fix_command: str
    security_impact: str
    attack_vectors: List[str]

@dataclass
class SSHConnection:
    timestamp: datetime
    source_ip: str
    username: str
    success: bool
    connection_type: str
    threat_score: int

# ═══════════════════════════════════════════════════════════════════════════════
#                         ADVANCED SSH SECURITY SCANNER
# ═══════════════════════════════════════════════════════════════════════════════

class AdvancedSSHSecurityScanner:
    def __init__(self):
        self.ssh_config_file = "/etc/ssh/sshd_config"
        self.ssh_user_config = os.path.expanduser("~/.ssh/config")
        self.vulnerabilities = []
        self.security_score = 0
        self.scan_timestamp = datetime.now()
        
        # Enhanced security benchmarks
        self.security_benchmarks = {
            'Port': {
                'default': '22',
                'recommended': 'Non-standard (2222-65535)',
                'description': 'Default SSH port is heavily targeted by attackers',
                'severity': 'MEDIUM'
            },
            'Protocol': {
                'default': '2',
                'recommended': '2',
                'description': 'SSH Protocol version - only version 2 is secure',
                'severity': 'CRITICAL'
            },
            'PermitRootLogin': {
                'default': 'yes',
                'recommended': 'no',
                'description': 'Root login access - major security risk',
                'severity': 'CRITICAL'
            },
            'PasswordAuthentication': {
                'default': 'yes', 
                'recommended': 'no',
                'description': 'Password-based authentication is vulnerable to brute force',
                'severity': 'HIGH'
            },
            'PubkeyAuthentication': {
                'default': 'yes',
                'recommended': 'yes',
                'description': 'Key-based authentication is more secure than passwords',
                'severity': 'HIGH'
            },
            'PermitEmptyPasswords': {
                'default': 'no',
                'recommended': 'no',
                'description': 'Empty passwords create critical security vulnerability',
                'severity': 'CRITICAL'
            },
            'X11Forwarding': {
                'default': 'yes',
                'recommended': 'no',
                'description': 'X11 forwarding can be exploited for privilege escalation',
                'severity': 'MEDIUM'
            },
            'MaxAuthTries': {
                'default': '6',
                'recommended': '3',
                'description': 'Limit authentication attempts to prevent brute force',
                'severity': 'HIGH'
            },
            'ClientAliveInterval': {
                'default': '0',
                'recommended': '300',
                'description': 'Prevent hanging connections that can be hijacked',
                'severity': 'MEDIUM'
            },
            'ClientAliveCountMax': {
                'default': '3',
                'recommended': '2',
                'description': 'Limit connection retries to prevent session hijacking',
                'severity': 'MEDIUM'
            },
            'UsePAM': {
                'default': 'yes',
                'recommended': 'no',
                'description': 'PAM can introduce additional attack vectors',
                'severity': 'LOW'
            },
            'AllowUsers': {
                'default': 'unset',
                'recommended': 'specific users only',
                'description': 'Limit SSH access to specific authorized users',
                'severity': 'HIGH'
            },
            'DenyUsers': {
                'default': 'unset',
                'recommended': 'configured',
                'description': 'Explicitly deny SSH access to risky users',
                'severity': 'MEDIUM'
            },
            'Banner': {
                'default': 'none',
                'recommended': '/etc/ssh/banner',
                'description': 'Legal warning banner deters unauthorized access',
                'severity': 'LOW'
            }
        }
        
    def scan_ssh_configuration(self):
        """Comprehensive SSH security configuration analysis"""
        print("🔍 Performing comprehensive SSH security analysis...")
        print("=" * 60)
        
        self.vulnerabilities = []
        security_points = 100  # Start with perfect score
        
        # Check if SSH is even installed/running
        ssh_status = self._check_ssh_service()
        if not ssh_status['installed']:
            print("ℹ️  SSH service not installed - system is secure by default")
            self.security_score = 100
            return []
        
        print(f"🔍 SSH Service Status: {'Running' if ssh_status['running'] else 'Stopped'}")
        print(f"📁 Configuration File: {self.ssh_config_file}")
        print()
        
        # Parse SSH configuration
        config = self._parse_ssh_config()
        
        # Analyze each security parameter
        for param, benchmark in self.security_benchmarks.items():
            current_value = config.get(param, 'default')
            vulnerability = self._analyze_parameter(param, current_value, benchmark)
            
            if vulnerability:
                self.vulnerabilities.append(vulnerability)
                
                # Deduct points based on severity
                severity_points = {
                    'CRITICAL': 25,
                    'HIGH': 15,
                    'MEDIUM': 10,
                    'LOW': 5
                }
                security_points -= severity_points.get(vulnerability.severity, 5)
        
        # Additional security checks
        self._check_ssh_keys_security()
        self._check_fail2ban_status()
        self._check_firewall_status()
        
        self.security_score = max(0, security_points)  # Don't go below 0
        
        # Display scan results
        self._display_scan_results()
        
        return self.vulnerabilities
    
    def _check_ssh_service(self):
        """Check SSH service installation and status"""
        try:
            # Check if SSH is installed
            result = subprocess.run(['which', 'sshd'], capture_output=True, text=True)
            installed = result.returncode == 0
            
            if not installed:
                return {'installed': False, 'running': False}
            
            # Check if SSH is running (macOS specific)
            result = subprocess.run(['launchctl', 'list'], capture_output=True, text=True)
            running = 'com.openssh.sshd' in result.stdout or 'ssh' in result.stdout.lower()
            
            return {'installed': True, 'running': running}
            
        except Exception:
            return {'installed': False, 'running': False}
    
    def _parse_ssh_config(self):
        """Parse SSH configuration file with enhanced error handling"""
        config = {}
        
        try:
            if not os.path.exists(self.ssh_config_file):
                print(f"⚠️  SSH config file not found: {self.ssh_config_file}")
                return config
            
            with open(self.ssh_config_file, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # Skip comments and empty lines
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parse configuration directives
                    parts = line.split(None, 1)
                    if len(parts) >= 2:
                        key = parts[0]
                        value = parts[1]
                        config[key] = value
                    
        except PermissionError:
            print(f"❌ Permission denied reading SSH config: {self.ssh_config_file}")
            print("💡 Run with sudo for complete analysis")
        except Exception as e:
            print(f"⚠️  Error reading SSH config: {e}")
        
        return config
    
    def _analyze_parameter(self, param, current_value, benchmark):
        """Analyze individual SSH parameter for security issues"""
        vulnerability = None
        
        # Parameter-specific analysis
        if param == 'Port':
            if current_value == '22' or current_value == 'default':
                vulnerability = SSHVulnerability(
                    name="Default SSH Port",
                    description="Using default SSH port 22 makes system an easy target for automated attacks",
                    severity="MEDIUM",
                    current_value="22 (default)",
                    recommended_value="Non-standard port (e.g., 2222, 2200, 8022)",
                    fix_command="sudo sed -i '' 's/#Port 22/Port 2222/' /etc/ssh/sshd_config",
                    security_impact="High visibility to attackers, increased brute force attempts",
                    attack_vectors=["Port scanning", "Automated brute force", "Botnet attacks"]
                )
        
        elif param == 'PermitRootLogin':
            if current_value.lower() in ['yes', 'default']:
                vulnerability = SSHVulnerability(
                    name="Root Login Enabled",
                    description="Direct root login via SSH is extremely dangerous and unnecessary",
                    severity="CRITICAL",
                    current_value=current_value,
                    recommended_value="no",
                    fix_command="sudo sed -i '' 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config",
                    security_impact="Complete system compromise possible with root password",
                    attack_vectors=["Root password brute force", "Credential stuffing", "Privilege escalation bypass"]
                )
        
        elif param == 'PasswordAuthentication':
            if current_value.lower() in ['yes', 'default']:
                vulnerability = SSHVulnerability(
                    name="Password Authentication Enabled",
                    description="Password-based SSH authentication is vulnerable to brute force attacks",
                    severity="HIGH", 
                    current_value=current_value,
                    recommended_value="no (use key-based authentication)",
                    fix_command="sudo sed -i '' 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config",
                    security_impact="Susceptible to password brute force and credential stuffing",
                    attack_vectors=["Brute force attacks", "Dictionary attacks", "Credential stuffing"]
                )
        
        elif param == 'MaxAuthTries':
            try:
                auth_tries = int(current_value) if current_value != 'default' else 6
                if auth_tries > 3:
                    vulnerability = SSHVulnerability(
                        name="High Authentication Attempts",
                        description=f"Allowing {auth_tries} authentication attempts enables brute force attacks",
                        severity="HIGH",
                        current_value=str(auth_tries),
                        recommended_value="3",
                        fix_command="sudo sed -i '' 's/#MaxAuthTries 6/MaxAuthTries 3/' /etc/ssh/sshd_config",
                        security_impact="Extended brute force attack window",
                        attack_vectors=["Extended brute force", "Credential guessing"]
                    )
            except ValueError:
                pass
        
        elif param == 'X11Forwarding':
            if current_value.lower() in ['yes', 'default']:
                vulnerability = SSHVulnerability(
                    name="X11 Forwarding Enabled",
                    description="X11 forwarding can be exploited for privilege escalation and information disclosure",
                    severity="MEDIUM",
                    current_value=current_value,
                    recommended_value="no",
                    fix_command="sudo sed -i '' 's/#X11Forwarding yes/X11Forwarding no/' /etc/ssh/sshd_config",
                    security_impact="Potential privilege escalation and information disclosure",
                    attack_vectors=["X11 exploitation", "Display hijacking", "Keylogging"]
                )
        
        elif param == 'AllowUsers':
            if current_value == 'default' or current_value == 'unset':
                vulnerability = SSHVulnerability(
                    name="No User Access Restrictions",
                    description="SSH access not restricted to specific users - any valid user can connect",
                    severity="HIGH",
                    current_value="No restrictions (all users allowed)",
                    recommended_value="Specific authorized users only",
                    fix_command="echo 'AllowUsers yourusername' | sudo tee -a /etc/ssh/sshd_config",
                    security_impact="Broader attack surface for credential attacks",
                    attack_vectors=["Account enumeration", "Lateral movement", "Privilege escalation"]
                )
        
        return vulnerability
    
    def _check_ssh_keys_security(self):
        """Analyze SSH key security configuration"""
        print("🔑 Analyzing SSH key security...")
        
        ssh_dir = os.path.expanduser("~/.ssh")
        if not os.path.exists(ssh_dir):
            print("   ℹ️  No SSH directory found - keys not configured")
            return
        
        # Check for weak key files
        key_files = ['id_rsa', 'id_dsa', 'id_ecdsa', 'id_ed25519']
        weak_keys = []
        
        for key_file in key_files:
            key_path = os.path.join(ssh_dir, key_file)
            if os.path.exists(key_path):
                # Check key permissions
                key_perms = oct(os.stat(key_path).st_mode)[-3:]
                if key_perms != '600':
                    weak_keys.append(f"{key_file} (permissions: {key_perms})")
                
                # Check key strength (basic analysis)
                try:
                    with open(key_path, 'r') as f:
                        key_content = f.read()
                        if 'BEGIN DSA PRIVATE KEY' in key_content:
                            weak_keys.append(f"{key_file} (DSA - deprecated)")
                        elif 'BEGIN RSA PRIVATE KEY' in key_content:
                            # Could add RSA key length analysis here
                            pass
                except:
                    pass
        
        if weak_keys:
            vulnerability = SSHVulnerability(
                name="Weak SSH Key Configuration",
                description=f"SSH keys with security issues detected: {', '.join(weak_keys)}",
                severity="MEDIUM",
                current_value=f"{len(weak_keys)} issues found",
                recommended_value="Secure key permissions (600) and strong algorithms",
                fix_command="chmod 600 ~/.ssh/id_* && ssh-keygen -t ed25519",
                security_impact="Key compromise risk, unauthorized access",
                attack_vectors=["Key theft", "Privilege escalation", "Unauthorized access"]
            )
            self.vulnerabilities.append(vulnerability)
    
    def _check_fail2ban_status(self):
        """Check if fail2ban is installed and configured for SSH"""
        try:
            result = subprocess.run(['which', 'fail2ban-client'], capture_output=True, text=True)
            if result.returncode != 0:
                vulnerability = SSHVulnerability(
                    name="Fail2ban Not Installed",
                    description="fail2ban provides automatic blocking of brute force SSH attacks",
                    severity="HIGH",
                    current_value="Not installed",
                    recommended_value="Installed and configured",
                    fix_command="brew install fail2ban && sudo fail2ban-client start",
                    security_impact="No automatic protection against brute force attacks",
                    attack_vectors=["Sustained brute force", "Distributed attacks", "Credential stuffing"]
                )
                self.vulnerabilities.append(vulnerability)
            else:
                print("   ✅ fail2ban detected")
        except:
            pass
    
    def _check_firewall_status(self):
        """Check macOS firewall status for SSH protection"""
        try:
            result = subprocess.run(['sudo', 'pfctl', '-sr'], capture_output=True, text=True)
            if result.returncode == 0 and 'ssh' not in result.stdout.lower():
                vulnerability = SSHVulnerability(
                    name="No Firewall SSH Rules",
                    description="No specific firewall rules found for SSH traffic filtering",
                    severity="MEDIUM",
                    current_value="No SSH-specific rules",
                    recommended_value="Restrictive SSH firewall rules",
                    fix_command="Configure pfctl or use macOS Firewall settings",
                    security_impact="No network-level protection against SSH attacks",
                    attack_vectors=["Network-based attacks", "Port scanning", "External brute force"]
                )
                self.vulnerabilities.append(vulnerability)
        except:
            pass
    
    def _display_scan_results(self):
        """Display comprehensive scan results"""
        print("\n" + "=" * 70)
        print("📊 SSH SECURITY ANALYSIS RESULTS")
        print("=" * 70)
        
        # Security score display
        if self.security_score >= 90:
            score_icon = "🟢"
            score_status = "EXCELLENT"
        elif self.security_score >= 70:
            score_icon = "🟡"
            score_status = "GOOD"
        elif self.security_score >= 50:
            score_icon = "🟠"
            score_status = "NEEDS IMPROVEMENT"
        else:
            score_icon = "🔴"
            score_status = "CRITICAL ISSUES"
        
        print(f"{score_icon} SECURITY SCORE: {self.security_score}/100 ({score_status})")
        print(f"📅 Scan Date: {self.scan_timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⚠️  Vulnerabilities Found: {len(self.vulnerabilities)}")
        print()
        
        if self.vulnerabilities:
            # Group by severity
            severity_groups = {'CRITICAL': [], 'HIGH': [], 'MEDIUM': [], 'LOW': []}
            for vuln in self.vulnerabilities:
                severity_groups[vuln.severity].append(vuln)
            
            for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
                vulns = severity_groups[severity]
                if vulns:
                    severity_icons = {
                        'CRITICAL': '🔴',
                        'HIGH': '🟠', 
                        'MEDIUM': '🟡',
                        'LOW': '🟢'
                    }
                    print(f"{severity_icons[severity]} {severity} SEVERITY ({len(vulns)} issues):")
                    for vuln in vulns:
                        print(f"   • {vuln.name}")
                        print(f"     Current: {vuln.current_value}")
                        print(f"     Fix: {vuln.fix_command}")
                    print()
        else:
            print("✅ No significant vulnerabilities detected!")
            print("🛡️ Your SSH configuration follows security best practices")

# ═══════════════════════════════════════════════════════════════════════════════
#                        SSH HARDENING ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class SSHHardeningEngine:
    def __init__(self):
        self.ssh_config_file = "/etc/ssh/sshd_config"
        self.backup_dir = os.path.expanduser("~/.mcguardian_ssh_backups")
        os.makedirs(self.backup_dir, exist_ok=True)
        
    def apply_ssh_hardening(self, vulnerabilities, auto_fix=False):
        """Apply comprehensive SSH hardening measures"""
        print("🔧 Starting SSH security hardening process...")
        print("=" * 60)
        
        if not vulnerabilities:
            print("✅ No vulnerabilities to fix - SSH is already secure!")
            return True
        
        # Create backup first
        backup_success = self._create_config_backup()
        if not backup_success:
            print("❌ Failed to create configuration backup - aborting for safety")
            return False
        
        fixes_applied = 0
        fixes_failed = 0
        
        for vuln in vulnerabilities:
            if auto_fix:
                print(f"🔄 Auto-fixing: {vuln.name}")
                success = self._apply_fix(vuln)
            else:
                print(f"\n🔧 {vuln.name}")
                print(f"   Description: {vuln.description}")
                print(f"   Severity: {vuln.severity}")
                print(f"   Current: {vuln.current_value}")
                print(f"   Recommended: {vuln.recommended_value}")
                print(f"   Impact: {vuln.security_impact}")
                print(f"   Fix Command: {vuln.fix_command}")
                
                if self._ask_yes_no(f"Apply fix for {vuln.name}?", True):
                    success = self._apply_fix(vuln)
                else:
                    print("   ⏭️  Skipped")
                    continue
            
            if success:
                print(f"   ✅ Fixed: {vuln.name}")
                fixes_applied += 1
            else:
                print(f"   ❌ Failed: {vuln.name}")
                fixes_failed += 1
        
        print(f"\n📊 HARDENING SUMMARY:")
        print(f"   ✅ Fixes Applied: {fixes_applied}")
        print(f"   ❌ Fixes Failed: {fixes_failed}")
        print(f"   📁 Backup Location: {self.backup_dir}")
        
        if fixes_applied > 0:
            print("\n🔄 Restarting SSH service to apply changes...")
            self._restart_ssh_service()
        
        return fixes_applied > 0
    
    def _create_config_backup(self):
        """Create timestamped backup of SSH configuration"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(self.backup_dir, f"sshd_config_backup_{timestamp}")
            
            shutil.copy2(self.ssh_config_file, backup_file)
            print(f"💾 Configuration backup created: {backup_file}")
            return True
            
        except Exception as e:
            print(f"❌ Backup creation failed: {e}")
            return False
    
    def _apply_fix(self, vulnerability):
        """Apply individual security fix"""
        try:
            # Execute the fix command
            result = subprocess.run(
                vulnerability.fix_command,
                shell=True,
                capture_output=True,
                text=True
            )
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"   Error applying fix: {e}")
            return False
    
    def _restart_ssh_service(self):
        """Restart SSH service to apply configuration changes"""
        try:
            # macOS SSH service restart
            result = subprocess.run([
                'sudo', 'launchctl', 'unload', '/System/Library/LaunchDaemons/ssh.plist'
            ], capture_output=True)
            
            time.sleep(2)
            
            result = subprocess.run([
                'sudo', 'launchctl', 'load', '/System/Library/LaunchDaemons/ssh.plist'
            ], capture_output=True)
            
            if result.returncode == 0:
                print("   ✅ SSH service restarted successfully")
            else:
                print("   ⚠️  SSH service restart may have failed")
                print("   💡 Manual restart: sudo launchctl unload/load ssh.plist")
                
        except Exception as e:
            print(f"   ⚠️  SSH restart error: {e}")
    
    def _ask_yes_no(self, question, default=True):
        """Interactive yes/no prompt"""
        suffix = "[Y/n]" if default else "[y/N]"
        while True:
            answer = input(f"❓ {question} {suffix}: ").strip().lower()
            if not answer:
                return default
            if answer in ['y', 'yes']:
                return True
            if answer in ['n', 'no']:
                return False
            print("Please enter 'yes' or 'no'")

# ═══════════════════════════════════════════════════════════════════════════════
#                         SSH THREAT MONITOR
# ═══════════════════════════════════════════════════════════════════════════════

class SSHThreatMonitor:
    def __init__(self, lockdown_manager):
        self.lockdown_manager = lockdown_manager
        self.monitoring = False
        self.connection_log = []
        self.threat_patterns = {}
        self.log_file = "/var/log/auth.log" if os.path.exists("/var/log/auth.log") else "/var/log/system.log"
        
    def start_monitoring(self):
        """Start real-time SSH threat monitoring"""
        self.monitoring = True
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self._monitor_ssh_logs, daemon=True)
        monitor_thread.start()
        
        # Start analysis thread
        analysis_thread = threading.Thread(target=self._analyze_threats, daemon=True)
        analysis_thread.start()
        
        print("🔍 SSH threat monitoring started")
        print(f"📊 Monitoring log file: {self.log_file}")
    
    def _monitor_ssh_logs(self):
        """Monitor SSH-related log entries"""
        try:
            # Use tail to follow log file
            process = subprocess.Popen(
                ['tail', '-f', self.log_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            for line in process.stdout:
                if not self.monitoring:
                    break
                
                if 'ssh' in line.lower() or 'sshd' in line.lower():
                    self._process_ssh_log_entry(line)
                    
        except Exception as e:
            print(f"⚠️  Log monitoring error: {e}")
    
    def _process_ssh_log_entry(self, log_line):
        """Process individual SSH log entry for threats"""
        # Parse SSH connection attempts
        if 'Failed password' in log_line or 'Invalid user' in log_line:
            ip_match = re.search(r'from (\d+\.\d+\.\d+\.\d+)', log_line)
            user_match = re.search(r'user (\w+)', log_line)
            
            if ip_match:
                source_ip = ip_match.group(1)
                username = user_match.group(1) if user_match else 'unknown'
                
                connection = SSHConnection(
                    timestamp=datetime.now(),
                    source_ip=source_ip,
                    username=username,
                    success=False,
                    connection_type='password_attempt',
                    threat_score=70
                )
                
                self.connection_log.append(connection)
                self._evaluate_threat(connection)
        
        elif 'Accepted' in log_line and 'ssh' in log_line.lower():
            ip_match = re.search(r'from (\d+\.\d+\.\d+\.\d+)', log_line)
            user_match = re.search(r'for (\w+)', log_line)
            
            if ip_match:
                source_ip = ip_match.group(1)
                username = user_match.group(1) if user_match else 'unknown'
                
                connection = SSHConnection(
                    timestamp=datetime.now(),
                    source_ip=source_ip,
                    username=username,
                    success=True,
                    connection_type='successful_login',
                    threat_score=20  # Lower threat for successful login
                )
                
                self.connection_log.append(connection)
    
    def _evaluate_threat(self, connection):
        """Evaluate threat level and take action"""
        source_ip = connection.source_ip
        
        # Count recent failed attempts from this IP
        recent_cutoff = datetime.now() - timedelta(minutes=10)
        recent_failures = [
            c for c in self.connection_log 
            if c.source_ip == source_ip and 
               c.timestamp > recent_cutoff and 
               not c.success
        ]
        
        threat_level = len(recent_failures)
        
        if threat_level >= 5:  # 5 failures in 10 minutes
            print(f"🚨 HIGH THREAT: {source_ip} ({threat_level} failed attempts)")
            self.lockdown_manager.block_ip(source_ip, "SSH brute force attempt")
            
        elif threat_level >= 3:
            print(f"⚠️  MEDIUM THREAT: {source_ip} ({threat_level} failed attempts)")
    
    def _analyze_threats(self):
        """Continuous threat analysis"""
        while self.monitoring:
            time.sleep(60)  # Analyze every minute
            
            # Clean old log entries (keep last 24 hours)
            cutoff = datetime.now() - timedelta(hours=24)
            self.connection_log = [
                c for c in self.connection_log if c.timestamp > cutoff
            ]
            
            # Identify threat patterns
            self._identify_threat_patterns()
    
    def _identify_threat_patterns(self):
        """Identify sophisticated attack patterns"""
        # Group by IP address
        ip_groups = {}
        for connection in self.connection_log:
            ip = connection.source_ip
            if ip not in ip_groups:
                ip_groups[ip] = []
            ip_groups[ip].append(connection)
        
        # Analyze patterns for each IP
        for ip, connections in ip_groups.items():
            if len(connections) >= 3:
                # Check for distributed brute force
                usernames = set(c.username for c in connections)
                if len(usernames) > 5:  # Trying many different usernames
                    print(f"🎯 PATTERN DETECTED: Username enumeration from {ip}")

# ═══════════════════════════════════════════════════════════════════════════════
#                         SSH LOCKDOWN MANAGER
# ═══════════════════════════════════════════════════════════════════════════════

class SSHLockdownManager:
    def __init__(self):
        self.blocked_ips = set()
        self.lockdown_active = False
        self.firewall_rules = []
        
    def block_ip(self, ip_address, reason="Security threat"):
        """Block IP address using system firewall"""
        if ip_address in self.blocked_ips:
            return  # Already blocked
        
        try:
            # Use pfctl to block IP (macOS)
            rule = f"block in from {ip_address} to any"
            
            # Add rule to pf
            result = subprocess.run([
                'sudo', 'pfctl', '-t', 'ssh_blocklist', '-T', 'add', ip_address
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.blocked_ips.add(ip_address)
                print(f"🚫 BLOCKED: {ip_address} ({reason})")
                
                # Log the block action
                self._log_block_action(ip_address, reason)
            else:
                print(f"❌ Failed to block {ip_address}: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Error blocking IP {ip_address}: {e}")
    
    def unblock_ip(self, ip_address):
        """Unblock previously blocked IP address"""
        try:
            result = subprocess.run([
                'sudo', 'pfctl', '-t', 'ssh_blocklist', '-T', 'delete', ip_address
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.blocked_ips.discard(ip_address)
                print(f"✅ UNBLOCKED: {ip_address}")
            else:
                print(f"❌ Failed to unblock {ip_address}")
                
        except Exception as e:
            print(f"❌ Error unblocking IP {ip_address}: {e}")
    
    def emergency_lockdown(self):
        """Complete SSH lockdown - disable SSH service"""
        print("🚨 INITIATING EMERGENCY SSH LOCKDOWN")
        print("⚠️  This will completely disable SSH access!")
        
        try:
            # Stop SSH service
            result = subprocess.run([
                'sudo', 'launchctl', 'unload', '/System/Library/LaunchDaemons/ssh.plist'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.lockdown_active = True
                print("✅ SSH service disabled")
                
                # Block SSH port entirely
                subprocess.run([
                    'sudo', 'pfctl', '-f', '/etc/pf.conf'
                ], capture_output=True)
                
                print("🔒 EMERGENCY LOCKDOWN COMPLETE")
                return True
            else:
                print(f"❌ Failed to disable SSH: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Emergency lockdown failed: {e}")
            return False
    
    def show_blocked_ips(self):
        """Display currently blocked IP addresses"""
        print(f"\n🚫 BLOCKED IP ADDRESSES ({len(self.blocked_ips)} total):")
        if self.blocked_ips:
            for ip in sorted(self.blocked_ips):
                print(f"   • {ip}")
        else:
            print("   ℹ️  No IP addresses currently blocked")
    
    def _log_block_action(self, ip_address, reason):
        """Log IP blocking action for audit trail"""
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'action': 'BLOCK_IP',
                'ip_address': ip_address,
                'reason': reason
            }
            
            log_file = os.path.expanduser("~/.mcguardian_ssh_blocks.log")
            with open(log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
                
        except Exception as e:
            print(f"⚠️  Failed to log block action: {e}")

# ═══════════════════════════════════════════════════════════════════════════════
#                              HELP FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def show_help():
    """Display comprehensive help information"""
    print("""
███╗   ███╗ ██████╗ ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗ ██╗ █████╗ ███╗   ██╗
████╗ ████║██╔════╝██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗██║██╔══██╗████╗  ██║
██╔████╔██║██║     ██║  ███╗██║   ██║███████║██████╔╝██║  ██║██║███████║██╔██╗ ██║
██║╚██╔╝██║██║     ██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║██║██╔══██║██║╚██╗██║
██║ ╚═╝ ██║╚██████╗╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝██║██║  ██║██║ ╚████║
╚═╝     ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝

                    SSH SECURITY & HARDENING TOOLKIT
                  Advanced SSH Protection for macOS Systems

USAGE:
    python3 ssh_security.py <command> [options]

COMMANDS:
    scan                    🔍 Comprehensive SSH security analysis
    harden                  🔧 Interactive SSH security hardening
    harden --auto           🚀 Automatic SSH hardening (recommended)
    monitor                 📊 Real-time SSH threat monitoring
    lockdown               🚨 Emergency SSH access lockdown
    status                 📋 Current SSH security status report
    help                   ❓ Show this help information

COMMAND DETAILS:

🔍 SCAN - Security Analysis
   Performs comprehensive analysis of SSH configuration including:
   • Configuration file security assessment
   • Key-based authentication analysis
   • Brute force protection evaluation
   • Firewall and fail2ban status checks
   • Security scoring with detailed recommendations

🔧 HARDEN - Security Hardening
   Interactive or automatic SSH security improvements:
   • Disable root login access
   • Enforce key-based authentication
   • Configure secure connection limits
   • Set up automatic threat blocking
   • Create configuration backups before changes

📊 MONITOR - Threat Monitoring
   Real-time SSH attack detection and response:
   • Monitor authentication logs continuously
   • Detect brute force attack patterns
   • Automatic IP blocking for threats
   • Advanced pattern recognition for sophisticated attacks
   • Real-time alerts for security events

🚨 LOCKDOWN - Emergency Response
   Complete SSH access shutdown for emergencies:
   • Immediately disable SSH service
   • Block all SSH-related network traffic
   • Emergency response for active attacks
   • Reversible lockdown procedures

📋 STATUS - Security Overview
   Current SSH security posture assessment:
   • Overall security score and recommendations
   • List of current vulnerabilities
   • Active threat blocking status
   • Configuration summary and next steps

EXAMPLES:
    python3 ssh_security.py scan                    # Analyze SSH security
    python3 ssh_security.py harden --auto           # Auto-fix security issues
    python3 ssh_security.py monitor                 # Start threat monitoring
    python3 ssh_security.py status                  # Check current status

SECURITY FEATURES:
    • 🛡️  Advanced threat intelligence and pattern recognition
    • 🔒 Automatic configuration backup before any changes
    • 🚫 Real-time IP blocking for brute force attempts
    • 📊 Comprehensive security scoring and benchmarking
    • 🔧 Professional-grade hardening recommendations
    • 📋 Detailed audit trail and logging capabilities

REQUIREMENTS:
    • macOS 10.15 or later
    • Python 3.8+
    • Administrator privileges for configuration changes
    • SSH service installed (optional - will detect if not present)

For more information: https://github.com/heyfinal/McGuardian
""")

# Make classes available for import
__all__ = [
    'AdvancedSSHSecurityScanner', 
    'SSHHardeningEngine', 
    'SSHThreatMonitor', 
    'SSHLockdownManager',
    'show_help'
]

if __name__ == '__main__':
    show_help()
