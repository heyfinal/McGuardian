#!/usr/bin/env python3
"""
McGuardian Elite Installer v1.0.0
Professional installer for McGuardian Elite Security System
Handles dependencies, permissions, configuration, and deployment
"""

import os
import sys
import subprocess
import shutil
import json
import getpass
import platform
from pathlib import Path
import requests
import zipfile
import tempfile

class McGuardianInstaller:
    def __init__(self):
        self.version = "3.0.0"
        self.install_dir = "/Applications/McGuardian Elite.app" if self.is_admin() else os.path.expanduser("~/Applications/McGuardian Elite")
        self.data_dir = os.path.expanduser("~/Library/Logs/McGuardianElite")
        self.config_dir = os.path.expanduser("~/.mcguardian_elite")
        self.current_user = getpass.getuser()
        self.errors = []
        self.warnings = []
        
    def is_admin(self):
        """Check if running with admin privileges"""
        return os.getuid() == 0
    
    def check_system_requirements(self):
        """Verify system meets requirements"""
        print("🔍 Checking system requirements...")
        
        # Check macOS version
        macos_version = platform.mac_ver()[0]
        if not macos_version:
            self.errors.append("This installer requires macOS")
            return False
        
        # Check Python version
        python_version = sys.version_info
        if python_version < (3, 8):
            self.errors.append(f"Python 3.8+ required (found {python_version.major}.{python_version.minor})")
            return False
        
        # Check available disk space (need at least 100MB)
        statvfs = os.statvfs('/')
        free_space = statvfs.f_frsize * statvfs.f_bavail
        if free_space < 100 * 1024 * 1024:  # 100MB
            self.errors.append("Insufficient disk space (need at least 100MB)")
            return False
        
        # Check for required system tools
        required_tools = ['launchctl', 'log', 'pip3']
        for tool in required_tools:
            if not shutil.which(tool):
                self.errors.append(f"Required system tool missing: {tool}")
        
        if self.errors:
            return False
        
        print("✅ System requirements met")
        return True
    
    def get_installation_options(self):
        """Get user preferences for installation"""
        print("\n🛠️ McGuardian Elite Installation Options")
        print("=" * 50)
        
        # Installation type
        print("1. Full Installation (Recommended)")
        print("   - Main security engine")
        print("   - Web dashboard")
        print("   - Auto-start on boot")
        print("   - Desktop shortcuts")
        print()
        print("2. Security Engine Only")
        print("   - Main security engine only")
        print("   - Command line interface")
        print()
        print("3. Custom Installation")
        print("   - Choose specific components")
        
        while True:
            choice = input("\nSelect installation type (1-3): ").strip()
            if choice in ['1', '2', '3']:
                break
            print("Please enter 1, 2, or 3")
        
        options = {
            'install_type': choice,
            'install_engine': True,
            'install_dashboard': choice in ['1', '3'],
            'auto_start': choice == '1',
            'create_shortcuts': choice == '1',
            'install_location': self.install_dir
        }
        
        if choice == '3':
            options['install_dashboard'] = self.ask_yes_no("Install web dashboard?", True)
            options['auto_start'] = self.ask_yes_no("Auto-start on boot?", True)
            options['create_shortcuts'] = self.ask_yes_no("Create desktop shortcuts?", True)
        
        # Custom installation directory
        if self.ask_yes_no(f"Install to {self.install_dir}?", True):
            options['install_location'] = self.install_dir
        else:
            custom_path = input("Enter installation directory: ").strip()
            options['install_location'] = os.path.expanduser(custom_path)
        
        return options
    
    def ask_yes_no(self, question, default=True):
        """Ask yes/no question with default"""
        suffix = "[Y/n]" if default else "[y/N]"
        while True:
            answer = input(f"{question} {suffix}: ").strip().lower()
            if not answer:
                return default
            if answer in ['y', 'yes']:
                return True
            if answer in ['n', 'no']:
                return False
            print("Please enter 'yes' or 'no'")
    
    def create_directories(self, install_location):
        """Create necessary directories"""
        print("📁 Creating directories...")
        
        directories = [
            install_location,
            os.path.join(install_location, "bin"),
            os.path.join(install_location, "lib"),
            os.path.join(install_location, "config"),
            os.path.join(install_location, "templates"),
            self.data_dir,
            os.path.join(self.data_dir, "human_readable"),
            os.path.join(self.data_dir, "analytics"),
            os.path.join(self.data_dir, "file_backups"),
            self.config_dir,
            os.path.expanduser("~/.cache/system_logs"),
            os.path.expanduser("~/Library/adult"),
            os.path.expanduser("~/Documents/.confidential")
        ]
        
        for directory in directories:
            try:
                os.makedirs(directory, exist_ok=True)
                # Set restrictive permissions
                os.chmod(directory, 0o700)
                print(f"  ✅ Created: {directory}")
            except Exception as e:
                self.errors.append(f"Failed to create directory {directory}: {e}")
                print(f"  ❌ Failed: {directory}")
    
    def install_dependencies(self, install_location):
        """Install Python dependencies"""
        print("📦 Installing dependencies...")
        
        # Create virtual environment in installation directory
        venv_dir = os.path.join(install_location, "venv")
        
        try:
            import venv
            print("  🔧 Creating virtual environment...")
            venv.create(venv_dir, with_pip=True)
            
            pip_path = os.path.join(venv_dir, "bin", "pip")
            
            dependencies = [
                'watchdog==3.0.0',
                'psutil==5.9.6',
                'cryptography==41.0.7',
                'flask==2.3.3',
                'requests==2.31.0'
            ]
            
            for dep in dependencies:
                print(f"  📥 Installing {dep}...")
                result = subprocess.run([pip_path, 'install', '--quiet', dep], 
                                      capture_output=True, text=True)
                if result.returncode != 0:
                    self.warnings.append(f"Failed to install {dep}: {result.stderr}")
                else:
                    print(f"    ✅ {dep}")
                    
        except Exception as e:
            self.errors.append(f"Failed to install dependencies: {e}")
    
    def install_files(self, install_location):
        """Install application files"""
        print("📄 Installing application files...")
        
        # In a real installer, these would be bundled files
        # For now, we'll create the file structure
        
        bin_dir = os.path.join(install_location, "bin")
        
        # Create main application script
        main_script = os.path.join(bin_dir, "mcguardian_elite")
        with open(main_script, 'w') as f:
            f.write(f'''#!/bin/bash
# McGuardian Elite Launcher
export MCGUARDIAN_HOME="{install_location}"
export PATH="{os.path.join(install_location, 'venv', 'bin')}:$PATH"
cd "{install_location}"
python3 "$MCGUARDIAN_HOME/lib/mcguardian_pro.py" "$@"
''')
        os.chmod(main_script, 0o755)
        
        # Create dashboard launcher
        dashboard_script = os.path.join(bin_dir, "mcguardian_dashboard")
        with open(dashboard_script, 'w') as f:
            f.write(f'''#!/bin/bash
# McGuardian Elite Dashboard Launcher
export MCGUARDIAN_HOME="{install_location}"
export PATH="{os.path.join(install_location, 'venv', 'bin')}:$PATH"
cd "{install_location}"
python3 "$MCGUARDIAN_HOME/lib/mcguardian_gui.py" "$@"
''')
        os.chmod(dashboard_script, 0o755)
        
        # Create uninstaller
        uninstaller = os.path.join(bin_dir, "uninstall")
        with open(uninstaller, 'w') as f:
            f.write(f'''#!/bin/bash
# McGuardian Elite Uninstaller
echo "🗑️ Uninstalling McGuardian Elite..."

# Stop services
launchctl unload ~/Library/LaunchAgents/com.mcguardianpro.plist 2>/dev/null

# Remove files
rm -rf "{install_location}"
rm -f ~/Library/LaunchAgents/com.mcguardianpro.plist
rm -rf ~/.mcguardian_elite_venv
rm -rf ~/.mcguardian_elite

echo "✅ McGuardian Elite uninstalled"
echo "⚠️ Log files in ~/Library/Logs/McGuardianElite preserved for security"
''')
        os.chmod(uninstaller, 0o755)
        
        print("  ✅ Application scripts created")
    
    def setup_autostart(self, install_location):
        """Setup auto-start service"""
        print("🚀 Setting up auto-start service...")
        
        plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.mcguardianelite</string>
    <key>ProgramArguments</key>
    <array>
        <string>{os.path.join(install_location, "bin", "mcguardian_elite")}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>{os.path.join(self.data_dir, "service.log")}</string>
    <key>StandardErrorPath</key>
    <string>{os.path.join(self.data_dir, "service_error.log")}</string>
    <key>WorkingDirectory</key>
    <string>{install_location}</string>
</dict>
</plist>'''
        
        plist_path = os.path.expanduser("~/Library/LaunchAgents/com.mcguardianelite.plist")
        
        try:
            # Create LaunchAgents directory if it doesn't exist
            os.makedirs(os.path.dirname(plist_path), exist_ok=True)
            
            with open(plist_path, 'w') as f:
                f.write(plist_content)
            
            os.chmod(plist_path, 0o644)
            
            # Load the service
            result = subprocess.run(['launchctl', 'load', plist_path], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("  ✅ Auto-start service configured")
            else:
                self.warnings.append(f"Failed to load auto-start service: {result.stderr}")
                
        except Exception as e:
            self.warnings.append(f"Failed to setup auto-start: {e}")
    
    def create_shortcuts(self, install_location):
        """Create desktop shortcuts and menu items"""
        print("🔗 Creating shortcuts...")
        
        # Create Applications folder shortcut for easy access
        apps_dir = os.path.expanduser("~/Applications")
        os.makedirs(apps_dir, exist_ok=True)
        
        # Create symlink to main application
        main_link = os.path.join(apps_dir, "McGuardian Elite")
        try:
            if os.path.exists(main_link):
                os.remove(main_link)
            os.symlink(os.path.join(install_location, "bin", "mcguardian_elite"), main_link)
            print("  ✅ Main application shortcut")
        except Exception as e:
            self.warnings.append(f"Failed to create main shortcut: {e}")
        
        # Create dashboard shortcut
        dashboard_link = os.path.join(apps_dir, "McGuardian Dashboard")
        try:
            if os.path.exists(dashboard_link):
                os.remove(dashboard_link)
            os.symlink(os.path.join(install_location, "bin", "mcguardian_dashboard"), dashboard_link)
            print("  ✅ Dashboard shortcut")
        except Exception as e:
            self.warnings.append(f"Failed to create dashboard shortcut: {e}")
        
        # Create desktop aliases (macOS-style)
        desktop_dir = os.path.expanduser("~/Desktop")
        if os.path.exists(desktop_dir):
            try:
                # Create .command files for easy double-click execution
                main_command = os.path.join(desktop_dir, "McGuardian Elite.command")
                with open(main_command, 'w') as f:
                    f.write(f'''#!/bin/bash
cd "{install_location}"
open -a Terminal "{os.path.join(install_location, 'bin', 'mcguardian_elite')}"
''')
                os.chmod(main_command, 0o755)
                
                dashboard_command = os.path.join(desktop_dir, "McGuardian Dashboard.command")
                with open(dashboard_command, 'w') as f:
                    f.write(f'''#!/bin/bash
cd "{install_location}"
"{os.path.join(install_location, 'bin', 'mcguardian_dashboard')}" &
sleep 2
open http://localhost:5000
''')
                os.chmod(dashboard_command, 0o755)
                
                print("  ✅ Desktop shortcuts")
            except Exception as e:
                self.warnings.append(f"Failed to create desktop shortcuts: {e}")
    
    def configure_permissions(self, install_location):
        """Set proper file permissions"""
        print("🔐 Configuring permissions...")
        
        try:
            # Set directory permissions
            for root, dirs, files in os.walk(install_location):
                for d in dirs:
                    os.chmod(os.path.join(root, d), 0o755)
                for f in files:
                    file_path = os.path.join(root, f)
                    if f.endswith(('.py', '.sh')) or '/bin/' in file_path:
                        os.chmod(file_path, 0o755)  # Executable
                    else:
                        os.chmod(file_path, 0o644)  # Read-only
            
            # Set restrictive permissions on data directories
            os.chmod(self.data_dir, 0o700)
            os.chmod(self.config_dir, 0o700)
            
            print("  ✅ Permissions configured")
        except Exception as e:
            self.warnings.append(f"Failed to configure permissions: {e}")
    
    def create_config_file(self, install_location, options):
        """Create configuration file"""
        print("⚙️ Creating configuration...")
        
        config = {
            'version': self.version,
            'install_location': install_location,
            'data_directory': self.data_dir,
            'config_directory': self.config_dir,
            'installed_components': {
                'engine': options['install_engine'],
                'dashboard': options['install_dashboard'],
                'auto_start': options['auto_start']
            },
            'installation_date': str(subprocess.check_output(['date'], text=True).strip()),
            'installed_by': self.current_user
        }
        
        config_file = os.path.join(self.config_dir, "config.json")
        try:
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            os.chmod(config_file, 0o600)
            print("  ✅ Configuration saved")
        except Exception as e:
            self.errors.append(f"Failed to create config: {e}")
    
    def run_post_install_checks(self, install_location):
        """Run post-installation verification"""
        print("🔍 Running post-installation checks...")
        
        # Check if main script is executable
        main_script = os.path.join(install_location, "bin", "mcguardian_elite")
        if not os.access(main_script, os.X_OK):
            self.errors.append("Main script is not executable")
        
        # Check if virtual environment was created
        venv_python = os.path.join(install_location, "venv", "bin", "python3")
        if not os.path.exists(venv_python):
            self.errors.append("Virtual environment not created properly")
        
        # Test Python imports
        try:
            import subprocess
            result = subprocess.run([venv_python, '-c', 'import watchdog, psutil, flask'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                self.warnings.append("Some Python dependencies may not be properly installed")
        except:
            self.warnings.append("Could not verify Python dependencies")
        
        if not self.errors:
            print("  ✅ All checks passed")
    
    def show_installation_summary(self, install_location, options):
        """Show installation summary"""
        print("\n" + "="*60)
        print("🎉 INSTALLATION COMPLETE!")
        print("="*60)
        print(f"📍 Installation Location: {install_location}")
        print(f"📊 Data Directory: {self.data_dir}")
        print(f"⚙️ Configuration: {self.config_dir}")
        print()
        
        print("🚀 How to Start McGuardian Elite:")
        if options['auto_start']:
            print("  • Auto-start is enabled - McGuardian will start automatically")
            print("  • To start manually: launchctl start com.mcguardianelite")
        else:
            print(f"  • Run: {os.path.join(install_location, 'bin', 'mcguardian_elite')}")
        
        if options['install_dashboard']:
            print(f"  • Dashboard: {os.path.join(install_location, 'bin', 'mcguardian_dashboard')}")
            print("  • Then open: http://localhost:5000")
        
        if options['create_shortcuts']:
            print("\n🔗 Shortcuts Created:")
            print("  • ~/Applications/McGuardian Elite")
            print("  • ~/Applications/McGuardian Dashboard")
            print("  • Desktop shortcuts (.command files)")
        
        print(f"\n🗑️ To Uninstall:")
        print(f"  • Run: {os.path.join(install_location, 'bin', 'uninstall')}")
        
        if self.warnings:
            print(f"\n⚠️ Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        print("\n✅ McGuardian Elite is ready to protect your Mac!")
        print("📖 Check the logs in ~/Library/Logs/McGuardianElite for security events")
    
    def install(self):
        """Main installation process"""
        print("🛡️ McGuardian Elite Professional Installer")
        print(f"Version {self.version}")
        print("="*50)
        
        # Check system requirements
        if not self.check_system_requirements():
            print("\n❌ Installation failed - System requirements not met:")
            for error in self.errors:
                print(f"  • {error}")
            return False
        
        # Get installation options
        options = self.get_installation_options()
        install_location = options['install_location']
        
        print(f"\n🔧 Installing McGuardian Elite to: {install_location}")
        if not self.ask_yes_no("Continue with installation?", True):
            print("Installation cancelled.")
            return False
        
        try:
            # Installation steps
            self.create_directories(install_location)
            self.install_dependencies(install_location)
            self.install_files(install_location)
            
            if options['auto_start']:
                self.setup_autostart(install_location)
            
            if options['create_shortcuts']:
                self.create_shortcuts(install_location)
            
            self.configure_permissions(install_location)
            self.create_config_file(install_location, options)
            self.run_post_install_checks(install_location)
            
            # Show summary
            self.show_installation_summary(install_location, options)
            
            return len(self.errors) == 0
            
        except KeyboardInterrupt:
            print("\n\n⚠️ Installation interrupted by user")
            return False
        except Exception as e:
            print(f"\n❌ Installation failed with error: {e}")
            self.errors.append(str(e))
            return False

def main():
    """Main installer entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == '--uninstall':
        print("🗑️ Uninstalling McGuardian Elite...")
        # Run uninstaller if it exists
        uninstaller = os.path.expanduser("~/Applications/McGuardian Elite/bin/uninstall")
        if os.path.exists(uninstaller):
            subprocess.run(['bash', uninstaller])
        else:
            print("❌ Uninstaller not found. Manual removal required.")
        return
    
    # Check if already installed
    existing_install = os.path.expanduser("~/Applications/McGuardian Elite")
    if os.path.exists(existing_install):
        print("⚠️ McGuardian Elite appears to already be installed.")
        if not input("Continue with reinstallation? [y/N]: ").lower().startswith('y'):
            print("Installation cancelled.")
            return
    
    installer = McGuardianInstaller()
    success = installer.install()
    
    if success:
        print("\n🎉 Installation completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Installation failed!")
        if installer.errors:
            print("Errors:")
            for error in installer.errors:
                print(f"  • {error}")
        sys.exit(1)

if __name__ == '__main__':
    main()
