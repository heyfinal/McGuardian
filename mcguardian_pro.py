# File: mcguardian_elite_launcher.py
# Revision: 4
# McGuardian Elite Main Application Launcher

#!/usr/bin/env python3
"""
███╗   ███╗ ██████╗ ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗ ██╗ █████╗ ███╗   ██╗
████╗ ████║██╔════╝██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗██║██╔══██╗████╗  ██║
██╔████╔██║██║     ██║  ███╗██║   ██║███████║██████╔╝██║  ██║██║███████║██╔██╗ ██║
██║╚██╔╝██║██║     ██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║██║██╔══██║██║╚██╗██║
██║ ╚═╝ ██║╚██████╗╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝██║██║  ██║██║ ╚████║
╚═╝     ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
                            
               McGuardian Elite Main Launcher v3.0.0 Rev 4
          Component Coordination • Auto-Launch • Error Recovery
"""

import os
import sys
import subprocess
import threading
import time
import signal
import json
from pathlib import Path
from datetime import datetime
import tempfile

class McGuardianEliteLauncher:
    """Main application launcher that coordinates all components"""
    
    def __init__(self):
        self.version = "3.0.0"
        self.revision = "4"
        self.app_name = "McGuardian Elite"
        
        # Initialize paths
        self.setup_paths()
        
        # Component tracking
        self.components = {
            'security_engine': {'process': None, 'status': 'stopped', 'restarts': 0},
            'web_dashboard': {'process': None, 'status': 'stopped', 'restarts': 0},
            'system_tray': {'process': None, 'status': 'stopped', 'restarts': 0}
        }
        
        # Configuration
        self.config = self.load_config()
        
        # Status tracking
        self.running = True
        self.startup_complete = False
        
        # Setup signal handlers
        self.setup_signal_handlers()
        
        print(f"🚀 {self.app_name} Launcher v{self.version} Rev {self.revision} initialized")
    
    def setup_paths(self):
        """Setup all necessary paths"""
        try:
            # Determine if running from .app bundle or standalone
            if getattr(sys, 'frozen', False):
                # Running as compiled application
                self.bundle_path = Path(sys.executable).parent.parent
            else:
                # Running as script - try to find bundle or use current directory
                current_path = Path(__file__).parent
                potential_bundle = current_path.parent.parent
                
                if (potential_bundle / "Contents" / "Info.plist").exists():
                    self.bundle_path = potential_bundle
                else:
                    self.bundle_path = current_path
            
            # Define all paths
            self.contents_path = self.bundle_path / "Contents"
            self.resources_path = self.contents_path / "Resources"
            self.macos_path = self.contents_path / "MacOS"
            
            # User directories
            self.home_dir = Path.home()
            self.config_dir = self.home_dir / ".mcguardian_elite"
            self.log_dir = self.home_dir / "Library" / "Logs" / "McGuardianElite"
            self.config_file = self.config_dir / "config.json"
            
            # Ensure directories exist
            self.config_dir.mkdir(exist_ok=True)
            self.log_dir.mkdir(parents=True, exist_ok=True)
            
            # Component script paths
            self.component_scripts = {
                'security_engine': self.resources_path / "mcguardian_pro.py",
                'web_dashboard': self.resources_path / "mcguardian_gui.py", 
                'system_tray': self.resources_path / "mcguardian_systray.py"
            }
            
            print(f"✅ Paths initialized - Bundle: {self.bundle_path}")
            
        except Exception as e:
            print(f"❌ Path setup failed: {e}")
            # Fallback to current directory
            self.resources_path = Path(__file__).parent
            self.component_scripts = {
                'security_engine': self.resources_path / "mcguardian_pro.py",
                'web_dashboard': self.resources_path / "mcguardian_gui.py",
                'system_tray': self.resources_path / "mcguardian_systray.py"
            }
    
    def load_config(self):
        """Load configuration with defaults"""
        default_config = {
            "auto_launch_dashboard": True,
            "auto_launch_systray": True,
            "restart_components": True,
            "max_restarts": 3,
            "restart_delay": 5,
            "alert_level": "MEDIUM",
            "debug_mode": False,
            "browser_auto_open": True,
            "systray_enabled": True
        }
        
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    default_config.update(loaded_config)
                    print("✅ Configuration loaded successfully")
        except Exception as e:
            print(f"⚠️  Config load error: {e} - using defaults")
        
        return default_config
    
    def save_config(self):
        """Save current configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"⚠️  Config save error: {e}")
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            print(f"\n🛑 Received signal {signum}, shutting down gracefully...")
            self.shutdown()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def launch_component(self, component_name):
        """Launch a specific component"""
        try:
            script_path = self.component_scripts.get(component_name)
            
            if not script_path or not script_path.exists():
                print(f"❌ Component script not found: {component_name} ({script_path})")
                return False
            
            print(f"🔄 Launching {component_name}...")
            
            # Launch the component
            process = subprocess.Popen([
                sys.executable, str(script_path)
            ], 
            cwd=str(self.resources_path),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
            )
            
            # Store process information
            self.components[component_name]['process'] = process
            self.components[component_name]['status'] = 'running'
            
            print(f"✅ {component_name} launched successfully (PID: {process.pid})")
            
            # Start monitoring thread for this component
            monitor_thread = threading.Thread(
                target=self.monitor_component, 
                args=(component_name,), 
                daemon=True
            )
            monitor_thread.start()
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to launch {component_name}: {e}")
            self.components[component_name]['status'] = 'failed'
            return False
    
    def monitor_component(self, component_name):
        """Monitor a component and restart if necessary"""
        component = self.components[component_name]
        
        while self.running and component['process']:
            try:
                # Check if process is still running
                return_code = component['process'].poll()
                
                if return_code is not None:
                    # Process has terminated
                    print(f"⚠️  {component_name} terminated with code {return_code}")
                    component['status'] = 'stopped'
                    
                    # Handle restart if enabled and under limit
                    if (self.config.get('restart_components', True) and 
                        component['restarts'] < self.config.get('max_restarts', 3) and
                        self.running):
                        
                        component['restarts'] += 1
                        restart_delay = self.config.get('restart_delay', 5)
                        
                        print(f"🔄 Restarting {component_name} in {restart_delay} seconds (attempt {component['restarts']})")
                        time.sleep(restart_delay)
                        
                        if self.launch_component(component_name):
                            print(f"✅ {component_name} restarted successfully")
                        else:
                            print(f"❌ Failed to restart {component_name}")
                            component['status'] = 'failed'
                    
                    break
                
                # Wait before next check
                time.sleep(10)
                
            except Exception as e:
                print(f"⚠️  Error monitoring {component_name}: {e}")
                time.sleep(30)  # Wait longer on error
    
    def launch_all_components(self):
        """Launch all components in proper order"""
        print("🚀 Starting McGuardian Elite components...")
        
        # Always launch security engine first
        success_count = 0
        
        if self.launch_component('security_engine'):
            success_count += 1
            # Wait for engine to initialize
            time.sleep(3)
        
        # Launch web dashboard if enabled
        if self.config.get('auto_launch_dashboard', True):
            if self.launch_component('web_dashboard'):
                success_count += 1
                # Wait for dashboard to start
                time.sleep(2)
                
                # Open browser if enabled
                if self.config.get('browser_auto_open', True):
                    threading.Thread(target=self.open_browser_delayed, daemon=True).start()
        
        # Launch system tray if enabled
        if self.config.get('systray_enabled', True):
            if self.launch_component('system_tray'):
                success_count += 1
        
        self.startup_complete = True
        print(f"✅ Startup complete - {success_count}/3 components launched successfully")
        
        return success_count > 0
    
    def open_browser_delayed(self):
        """Open browser after dashboard has time to start"""
        try:
            time.sleep(5)  # Wait for dashboard to fully start
            
            import webbrowser
            webbrowser.open("http://localhost:5000")
            print("🌐 Web dashboard opened in browser")
            
        except Exception as e:
            print(f"⚠️  Browser auto-open failed: {e}")
    
    def get_status(self):
        """Get current status of all components"""
        status = {
            'launcher': {
                'version': f"{self.version} Rev {self.revision}",
                'uptime': self.get_uptime(),
                'startup_complete': self.startup_complete
            },
            'components': {}
        }
        
        for name, component in self.components.items():
            status['components'][name] = {
                'status': component['status'],
                'restarts': component['restarts'],
                'pid': component['process'].pid if component['process'] else None
            }
        
        return status
    
    def get_uptime(self):
        """Get launcher uptime"""
        if hasattr(self, 'start_time'):
            uptime_seconds = time.time() - self.start_time
            hours = int(uptime_seconds // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
        return "Unknown"
    
    def print_status(self):
        """Print current status"""
        status = self.get_status()
        
        print(f"\n📊 {self.app_name} Status:")
        print(f"   Version: {status['launcher']['version']}")
        print(f"   Uptime: {status['launcher']['uptime']}")
        print(f"   Startup: {'Complete' if status['launcher']['startup_complete'] else 'In Progress'}")
        
        print(f"\n🔧 Components:")
        for name, info in status['components'].items():
            status_icon = {
                'running': '🟢',
                'stopped': '🔴', 
                'failed': '❌'
            }.get(info['status'], '❓')
            
            print(f"   {status_icon} {name}: {info['status']}")
            if info['restarts'] > 0:
                print(f"      Restarts: {info['restarts']}")
            if info['pid']:
                print(f"      PID: {info['pid']}")
    
    def stop_component(self, component_name):
        """Stop a specific component"""
        component = self.components.get(component_name)
        if not component or not component['process']:
            return False
        
        try:
            process = component['process']
            print(f"🛑 Stopping {component_name} (PID: {process.pid})")
            
            # Try graceful termination first
            process.terminate()
            
            # Wait up to 10 seconds for graceful shutdown
            for _ in range(10):
                if process.poll() is not None:
                    break
                time.sleep(1)
            
            # Force kill if still running
            if process.poll() is None:
                print(f"⚠️  Force killing {component_name}")
                process.kill()
                process.wait()
            
            component['process'] = None
            component['status'] = 'stopped'
            print(f"✅ {component_name} stopped successfully")
            
            return True
            
        except Exception as e:
            print(f"❌ Error stopping {component_name}: {e}")
            return False
    
    def restart_component(self, component_name):
        """Restart a specific component"""
        print(f"🔄 Restarting {component_name}...")
        
        if self.stop_component(component_name):
            time.sleep(2)  # Brief pause
            return self.launch_component(component_name)
        
        return False
    
    def shutdown(self):
        """Graceful shutdown of all components"""
        print("🛑 Initiating graceful shutdown...")
        self.running = False
        
        # Stop all components
        for component_name in self.components.keys():
            self.stop_component(component_name)
        
        # Save configuration
        self.save_config()
        
        print("✅ McGuardian Elite shutdown complete")
        sys.exit(0)
    
    def run_interactive_mode(self):
        """Run interactive command mode"""
        print(f"""
🛡️  {self.app_name} Interactive Console
📋 Available commands:
   status  - Show component status
   restart <component> - Restart component (engine/dashboard/tray)
   stop <component> - Stop component
   config - Show configuration
   quit - Shutdown application
""")
        
        while self.running:
            try:
                command = input(f"\n{self.app_name}> ").strip().lower()
                
                if command == 'status':
                    self.print_status()
                    
                elif command.startswith('restart '):
                    component = command.split(' ', 1)[1]
                    if component in ['engine', 'security_engine']:
                        self.restart_component('security_engine')
                    elif component in ['dashboard', 'web_dashboard']:
                        self.restart_component('web_dashboard')
                    elif component in ['tray', 'system_tray']:
                        self.restart_component('system_tray')
                    else:
                        print(f"❌ Unknown component: {component}")
                        
                elif command.startswith('stop '):
                    component = command.split(' ', 1)[1]
                    if component in ['engine', 'security_engine']:
                        self.stop_component('security_engine')
                    elif component in ['dashboard', 'web_dashboard']:
                        self.stop_component('web_dashboard')
                    elif component in ['tray', 'system_tray']:
                        self.stop_component('system_tray')
                    else:
                        print(f"❌ Unknown component: {component}")
                        
                elif command == 'config':
                    print(f"\n⚙️  Configuration:")
                    for key, value in self.config.items():
                        print(f"   {key}: {value}")
                        
                elif command in ['quit', 'exit', 'q']:
                    break
                    
                elif command == 'help':
                    print("Commands: status, restart <component>, stop <component>, config, quit")
                    
                else:
                    print(f"❓ Unknown command: {command}")
                    
            except (EOFError, KeyboardInterrupt):
                break
            except Exception as e:
                print(f"⚠️  Command error: {e}")
        
        self.shutdown()
    
    def run(self):
        """Main run method"""
        self.start_time = time.time()
        
        print(f"""
🚀 Starting {self.app_name} v{self.version} Rev {self.revision}
📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🖥️  Bundle Path: {self.bundle_path}
""")
        
        # Launch all components
        if not self.launch_all_components():
            print("❌ Failed to launch components - entering recovery mode")
        
        # Check command line arguments
        if len(sys.argv) > 1:
            arg = sys.argv[1].lower()
            
            if arg in ['--interactive', '-i']:
                self.run_interactive_mode()
                return
            elif arg in ['--status', '-s']:
                self.print_status()
                return
            elif arg in ['--help', '-h']:
                self.show_help()
                return
        
        # Main monitoring loop
        try:
            print("✅ McGuardian Elite is now running")
            print("🌐 Dashboard: http://localhost:5000")
            print("🖥️  System Tray: Look for shield icon in menu bar")
            print("📊 Logs: ~/Library/Logs/McGuardianElite/")
            print("💡 Press Ctrl+C to shutdown gracefully")
            
            # Keep launcher alive and monitor
            while self.running:
                time.sleep(30)
                
                # Periodic status check
                if self.config.get('debug_mode', False):
                    self.print_status()
                
        except KeyboardInterrupt:
            print("\n🛑 Shutdown requested by user")
        except Exception as e:
            print(f"💥 Launcher error: {e}")
        finally:
            self.shutdown()
    
    def show_help(self):
        """Show help information"""
        print(f"""
🛡️  {self.app_name} Launcher v{self.version} Rev {self.revision}

USAGE:
    python3 mcguardian_elite_launcher.py [OPTIONS]

OPTIONS:
    --interactive, -i    Run in interactive mode
    --status, -s         Show current status and exit
    --help, -h           Show this help message

FEATURES:
    • Automatic component launching and monitoring  
    • Crash recovery with configurable restart limits
    • Interactive command console for management
    • Graceful shutdown handling
    • Configuration management
    • Status monitoring and reporting

COMPONENTS:
    • Security Engine: Core threat detection and monitoring
    • Web Dashboard: Browser-based management interface
    • System Tray: Menu bar integration and quick controls

CONFIGURATION:
    • File: ~/.mcguardian_elite/config.json
    • Auto-restart: Enabled by default with 3 attempt limit
    • Browser auto-open: Opens dashboard automatically
    • System tray: Enabled by default

For support: Check ~/Library/Logs/McGuardianElite/ for detailed logs
""")

def main():
    """Main entry point with comprehensive error handling"""
    try:
        launcher = McGuardianEliteLauncher()
        launcher.run()
        
    except KeyboardInterrupt:
        print("\n🛑 Launcher interrupted by user")
    except Exception as e:
        print(f"💥 Launcher failed with error: {e}")
        print("📋 Troubleshooting:")
        print("   • Check Python version (3.8+ required)")
        print("   • Verify all component files are present")
        print("   • Check file permissions")
        print("   • Review logs in ~/Library/Logs/McGuardianElite/")

if __name__ == '__main__':
    main()
