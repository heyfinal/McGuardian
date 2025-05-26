#!/usr/bin/env python3
"""
McGuardian Elite - Standalone SSH Security Tool
Comprehensive SSH hardening, monitoring, and threat response
Can be used independently or as part of McGuardian Elite

Usage:
    python3 ssh_security.py scan           # Scan SSH configuration
    python3 ssh_security.py harden         # Interactive SSH hardening  
    python3 ssh_security.py harden --auto  # Automatic SSH hardening
    python3 ssh_security.py monitor        # Real-time SSH monitoring
    python3 ssh_security.py lockdown       # Emergency SSH lockdown
    python3 ssh_security.py status         # Show SSH security status
"""

# Import the SSH security module
from ssh_security_module import (
    SSHSecurityScanner, 
    SSHHardeningEngine, 
    SSHThreatMonitor, 
    SSHLockdownManager,
    show_help
)

import sys
import time

def main():
    """Main SSH security tool entry point"""
    print("🔐 McGuardian Elite - SSH Security & Lockdown Tool")
    print("=" * 55)
    print("🛡️ Comprehensive SSH protection for macOS")
    print()
    
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'scan':
        print("🔍 Starting comprehensive SSH security scan...")
        scanner = SSHSecurityScanner()
        vulnerabilities = scanner.scan_ssh_configuration()
        
        print(f"\n📊 SSH Security Scan Results:")
        print(f"Security Score: {scanner.security_score}/100")
        
        if scanner.security_score >= 90:
            print("🟢 EXCELLENT - Your SSH configuration is highly secure!")
        elif scanner.security_score >= 70:
            print("🟡 GOOD - Your SSH has decent security with some improvements needed")
        elif scanner.security_score >= 50:
            print("🟠 FAIR - Your SSH security needs significant improvements")
        else:
            print("🔴 POOR - Your SSH configuration has serious security vulnerabilities!")
        
        if vulnerabilities:
            print(f"\n⚠️ Found {len(vulnerabilities)} vulnerabilities:")
            
            # Group by severity
            critical = [v for v in vulnerabilities if v.severity == 'CRITICAL']
            high = [v for v in vulnerabilities if v.severity == 'HIGH']
            medium = [v for v in vulnerabilities if v.severity == 'MEDIUM']
            low = [v for v in vulnerabilities if v.severity == 'LOW']
            
            for severity, vulns in [('CRITICAL', critical), ('HIGH', high), ('MEDIUM', medium), ('LOW', low)]:
                if vulns:
                    print(f"\n🔍 {severity} ({len(vulns)} issues):")
                    for vuln in vulns:
                        print(f"  • {vuln.description}")
                        print(f"    Current: {vuln.current_value}")
                        print(f"    Recommended: {vuln.recommended_value}")
                        print(f"    Fix: {vuln.fix_command}")
                        print()
            
            print("💡 To fix these issues automatically, run:")
            print("   python3 ssh_security.py harden --auto")
        else:
            print("\n✅ No vulnerabilities found! Your SSH is properly secured.")
            
    elif command == 'harden':
        print("🔧 Starting SSH security hardening...")
        
        # First scan for vulnerabilities
        scanner = SSHSecurityScanner()
        vulnerabilities = scanner.scan_ssh_configuration()
        
        if not vulnerabilities:
            print("✅ SSH is already properly secured! No hardening needed.")
            return
        
        print(f"Found {len(vulnerabilities)} security issues to fix.")
        
        # Apply hardening
        hardener = SSHHardeningEngine()
        auto_fix = '--auto' in sys.argv
        
        if auto_fix:
            print("🔄 Applying automatic security fixes...")
        else:
            print("🖥️ Starting interactive hardening process...")
            print("💾 Backups will be created before making any changes.")
        
        hardener.apply_ssh_hardening(vulnerabilities, auto_fix)
        
        # Re-scan to show improvement
        print("\n🔄 Re-scanning to verify improvements...")
        new_scanner = SSHSecurityScanner()
        new_vulnerabilities = new_scanner.scan_ssh_configuration()
        
        print(f"📊 Security improvement:")
        print(f"   Before: {scanner.security_score}/100")
        print(f"   After:  {new_scanner.security_score}/100")
        
        improvement = new_scanner.security_score - scanner.security_score
        if improvement > 0:
            print(f"   🎉 Improved by {improvement} points!")
        
        remaining = len(new_vulnerabilities)
        fixed = len(vulnerabilities) - remaining
        print(f"   🔧 Fixed {fixed} vulnerabilities, {remaining} remaining")
        
        if remaining == 0:
            print("\n🎉 SSH is now fully secured!")
        else:
            print(f"\n⚠️ {remaining} issues require manual attention:")
            for vuln in new_vulnerabilities:
                print(f"   • {vuln.description}")
                
    elif command == 'monitor':
        print("🔍 Starting real-time SSH threat monitoring...")
        print("This will monitor SSH connections and automatically block threats.")
        print("Press Ctrl+C to stop monitoring")
        print()
        
        # Initialize SSH security components
        lockdown_manager = SSHLockdownManager()
        monitor = SSHThreatMonitor(lockdown_manager)
        
        print("🚀 SSH threat monitoring active...")
        print("   • Monitoring authentication logs")
        print("   • Tracking failed login attempts")
        print("   • Detecting brute force attacks")
        print("   • Automatic IP blocking enabled")
        print()
        
        # Start monitoring
        monitor.start_monitoring()
        
        try:
            print("🔍 Monitoring SSH threats... (Ctrl+C to stop)")
            while True:
                time.sleep(10)
                
                # Show monitoring status every minute
                blocked_count = len(lockdown_manager.blocked_ips)
                if blocked_count > 0:
                    print(f"📊 Status: {blocked_count} IPs currently blocked")
                    
        except KeyboardInterrupt:
            print("\n🛑 SSH monitoring stopped")
            monitor.monitoring = False
            
            # Show final status
            if lockdown_manager.blocked_ips:
                print(f"\n📋 Final Status:")
                lockdown_manager.show_blocked_ips()
                print("\n💡 To unblock IPs manually, you can use firewall commands")
                
    elif command == 'lockdown':
        print("🚨 EMERGENCY SSH LOCKDOWN")
        print("This will completely disable SSH access to your system!")
        print()
        
        confirm = input("⚠️ Are you sure you want to proceed? [yes/NO]: ")
        if confirm.lower() != 'yes':
            print("❌ Emergency lockdown cancelled")
            return
        
        print("🔄 Initiating emergency SSH lockdown...")
        lockdown_manager = SSHLockdownManager()
        lockdown_manager.emergency_lockdown()
        
        print("\n🔴 SSH LOCKDOWN COMPLETE")
        print("⚠️ SSH is now completely disabled on this system")
        print("💡 To re-enable SSH later:")
        print("   sudo brew services start openssh")
        print("   sudo launchctl load /System/Library/LaunchDaemons/ssh.plist")
        
    elif command == 'status':
        print("📊 SSH Security Status Report")
        print("-" * 30)
        
        # Run security scan
        scanner = SSHSecurityScanner()
        vulnerabilities = scanner.scan_ssh_configuration()
        
        # Check lockdown status
        lockdown_manager = SSHLockdownManager()
        
        print(f"🔐 SSH Security Score: {scanner.security_score}/100")
        
        if scanner.security_score >= 90:
            status_icon = "🟢"
            status_text = "EXCELLENT"
        elif scanner.security_score >= 70:
            status_icon = "🟡"
            status_text = "GOOD"  
        elif scanner.security_score >= 50:
            status_icon = "🟠"
            status_text = "FAIR"
        else:
            status_icon = "🔴"
            status_text = "POOR"
        
        print(f"{status_icon} Overall Status: {status_text}")
        print(f"⚠️ Vulnerabilities: {len(vulnerabilities)}")
        print(f"🚫 Blocked IPs: {len(lockdown_manager.blocked_ips)}")
        
        # Show vulnerability breakdown
        if vulnerabilities:
            severity_counts = {}
            for vuln in vulnerabilities:
                severity_counts[vuln.severity] = severity_counts.get(vuln.severity, 0) + 1
            
            print("\n📋 Vulnerability Breakdown:")
            for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
                count = severity_counts.get(severity, 0)
                if count > 0:
                    icon = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡', 'LOW': '🟢'}[severity]
                    print(f"   {icon} {severity}: {count}")
        
        # Show blocked IPs
        if lockdown_manager.blocked_ips:
            lockdown_manager.show_blocked_ips()
        else:
            print("\n✅ No IPs currently blocked")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        if vulnerabilities:
            print(f"   • Run 'python3 ssh_security.py harden --auto' to fix issues")
        if scanner.security_score < 70:
            print(f"   • Enable SSH monitoring: 'python3 ssh_security.py monitor'")
        if scanner.security_score >= 90:
            print(f"   • Your SSH security is excellent! Consider monitoring for threats.")
            
    elif command == 'help' or command == '--help':
        show_help()
        
    else:
        print(f"❌ Unknown command: {command}")
        print()
        show_help()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Operation interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 For help, run: python3 ssh_security.py help")
