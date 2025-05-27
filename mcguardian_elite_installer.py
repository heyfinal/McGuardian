# mcguardian_elite_installer.py
# Installs McGuardian Elite + Dashboard Script (Fixed Background Launch)

import subprocess
import sys
import os
from pathlib import Path

REQUIRED_PACKAGES = [
    "watchdog",
    "psutil",
    "flask",
    "cryptography",
    "requests",
    "click",
    "jinja2",
    "werkzeug"
]

INSTALL_DIR = Path("/Users/daniel/Applications/McGuardian Elite")
VENV_DIR = INSTALL_DIR / ".mcguardian_venv"
DASHBOARD_SCRIPT = INSTALL_DIR / "McGuardian.py"

DASHBOARD_CODE = """# McGuardian.py
from flask import Flask, render_template_string
import os
import sys

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template_string("""
<html>
<head><title>McGuardian Elite</title></head>
<body style='font-family:sans-serif;'>
    <h1>🔐 McGuardian Elite Dashboard</h1>
    <p>Status: <strong>Online</strong></p>
    <p>Log Directory: {{ logs }}</p>
</body>
</html>
""", logs=os.path.expanduser("~/Applications/McGuardian Elite/technical_logs"))

if __name__ == '__main__':
    app.run(debug=True, port=4242, use_reloader=False)
"""


def create_directory_structure():
    print("\n📁 Creating secure directory structure...")
    folders = [
        "Contents", "MacOS", "Resources", "lib", "bin", "config", "docs",
        "McGuardianElite", "human_readable", "analytics", "technical_logs",
        ".mcguardian_elite", ".sys_backup_ZcvxvmeGc6RpYGxGPq5Y", "adult", ".confidential"
    ]
    for folder in folders:
        (INSTALL_DIR / folder).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {folder}")
    print("✅ Directory structure created")


def create_virtualenv():
    if not VENV_DIR.exists():
        print("\n📁 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)
        print("✅ Virtual environment created.")


def upgrade_pip(python_bin):
    try:
        subprocess.run([
            python_bin, "-m", "pip", "install", "--upgrade", "pip"
        ], check=True)
        print("🔄 pip upgraded.")
    except subprocess.CalledProcessError:
        print("⚠️ Failed to upgrade pip. Proceeding anyway.")


def get_venv_python():
    if sys.platform == "win32":
        return str(VENV_DIR / "Scripts" / "python.exe")
    else:
        return str(VENV_DIR / "bin" / "python3")


def install_packages():
    failed = []
    python_bin = get_venv_python()
    upgrade_pip(python_bin)

    print("\n📦 Installing Python dependencies...")
    for package in REQUIRED_PACKAGES:
        print(f"\n   📥 Installing {package}...")
        try:
            subprocess.run([
                python_bin, "-m", "pip", "install", package
            ], check=True)
            print(f"   ✅ {package} installed successfully.")
        except subprocess.CalledProcessError:
            print(f"   ❌ {package} failed to install.")
            failed.append(package)

    print("\n📊 Installation Summary:")
    print(f"   ✅ Successful: {len(REQUIRED_PACKAGES) - len(failed)}/{len(REQUIRED_PACKAGES)}")
    if failed:
        print(f"   ❌ Failed: {len(failed)} packages")
        for pkg in failed:
            print(f"      • {pkg}")
    else:
        print("   🎉 All packages installed successfully!")


def write_dashboard_script():
    print("\n📝 Writing dashboard script...")
    with open(DASHBOARD_SCRIPT, "w") as f:
        f.write(DASHBOARD_CODE)
    print("✅ Dashboard script written.")


def launch_dashboard():
    python_bin = get_venv_python()
    import webbrowser
    if DASHBOARD_SCRIPT.exists():
        print("
🚀 Launching McGuardian dashboard...")
        subprocess.Popen([python_bin, str(DASHBOARD_SCRIPT)])
        webbrowser.open("http://127.0.0.1:4242")
        print("✅ Dashboard launched.")
    else:
        print(f"⚠️ Dashboard file not found: {DASHBOARD_SCRIPT}")


if __name__ == "__main__":
    print("\n✅ Installation configured: full mode")
    create_directory_structure()
    create_virtualenv()
    install_packages()
    write_dashboard_script()
    launch_dashboard()
