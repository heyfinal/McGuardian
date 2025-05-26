#!/bin/bash
#
# McGuardian Elite - Enhanced Quick Install Script
# Downloads and runs the comprehensive Python installer
#
# Usage: curl -sSL https://install.mcguardian.dev | bash
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# McGuardian Elite enhanced branding
echo -e "${BLUE}"
cat << "EOF"
    ███╗   ███╗ ██████╗ ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗ ██╗ █████╗ ███╗   ██╗
    ████╗ ████║██╔════╝██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗██║██╔══██╗████╗  ██║
    ██╔████╔██║██║     ██║  ███╗██║   ██║███████║██████╔╝██║  ██║██║███████║██╔██╗ ██║
    ██║╚██╔╝██║██║     ██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║██║██╔══██║██║╚██╗██║
    ██║ ╚═╝ ██║╚██████╗╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝██║██║  ██║██║ ╚████║
    ╚═╝     ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
                                    
                           E L I T E   v 3 . 0 . 0   -   E N H A N C E D
EOF
echo -e "${NC}"

echo -e "${GREEN}🛡️  Advanced AI-Powered Security Monitoring System for macOS${NC}"
echo -e "${PURPLE}🚀 Fully Automated Installation with Desktop Launcher & Secure Backups${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo

# Configuration
REPO_URL="https://github.com/heyfinal/McGuardian"
TEMP_DIR=$(mktemp -d)
VERSION="v3.0.0"

# Functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_feature() {
    echo -e "${PURPLE}🎯 $1${NC}"
}

# Enhanced system check
check_requirements() {
    log_info "Performing comprehensive system check..."
    
    # Check macOS
    if [[ "$OSTYPE" != "darwin"* ]]; then
        log_error "This installer requires macOS (Darwin)"
        log_info "Detected OS: $OSTYPE"
        exit 1
    fi
    
    # Get macOS version
    MACOS_VERSION=$(sw_vers -productVersion)
    log_success "macOS $MACOS_VERSION detected"
    
    # Check if macOS version is supported (10.15+)
    MAJOR_VERSION=$(echo $MACOS_VERSION | cut -d. -f1)
    MINOR_VERSION=$(echo $MACOS_VERSION | cut -d. -f2)
    
    if [[ $MAJOR_VERSION -lt 10 ]] || [[ $MAJOR_VERSION -eq 10 && $MINOR_VERSION -lt 15 ]]; then
        log_error "macOS 10.15 (Catalina) or later required"
        log_info "Your version: $MACOS_VERSION"
        exit 1
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is required but not found"
        log_info "Install Python 3.8+ from: https://www.python.org/downloads/"
        log_info "Or install via Homebrew: brew install python"
        exit 1
    fi
    
    # Check Python version
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [[ $PYTHON_MAJOR -lt 3 ]] || [[ $PYTHON_MAJOR -eq 3 && $PYTHON_MINOR -lt 8 ]]; then
        log_error "Python 3.8+ required (found Python $PYTHON_VERSION)"
        log_info "Update Python from: https://www.python.org/downloads/"
        exit 1
    fi
    
    log_success "Python $PYTHON_VERSION - Compatible"
    
    # Check pip
    if ! python3 -m pip --version &> /dev/null; then
        log_error "pip is required but not found"
        log_info "Install pip: python3 -m ensurepip --upgrade"
        exit 1
    fi
    
    log_success "pip available"
    
    # Check disk space
    AVAILABLE_SPACE=$(df -h . | tail -1 | awk '{print $4}' | sed 's/[^0-9.]//g')
    log_info "Available disk space: $(df -h . | tail -1 | awk '{print $4}')"
    
    # Check if we have write permissions
    if ! touch "${TEMP_DIR}/write_test" 2>/dev/null; then
        log_error "Cannot write to temporary directory"
        exit 1
    fi
    rm -f "${TEMP_DIR}/write_test"
    
    log_success "System requirements verified"
}

# Show available installation options
show_installation_options() {
    echo
    echo -e "${CYAN}🛠️ McGuardian Elite Installation Options${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo
    echo -e "${GREEN}1. 🎯 Quick Install (Recommended)${NC}"
    echo "   ✨ Full installation with all features"
    echo "   🛡️  AI-powered threat detection engine"
    echo "   📊 Beautiful Apple-inspired web dashboard"
    echo "   🔐 SSH security hardening tools"
    echo "   🖥️  Desktop launcher and shortcuts"
    echo "   🔒 Randomized secure backup locations"
    echo "   🕯️ Advanced honeypot systems"
    echo
    echo -e "${YELLOW}2. 🔧 Interactive Install${NC}"
    echo "   🎛️  Choose specific components"
    echo "   ⚙️  Custom configuration options"
    echo "   🎯 Tailored to your needs"
    echo
    echo -e "${PURPLE}3. 🛠️ Advanced Install${NC}"
    echo "   💻 Engine-only installation"
    echo "   🖥️  Command-line interface"
    echo "   ⚡ Minimal system footprint"
    echo
    echo -e "${CYAN}4. 🔍 Show Repository Contents${NC}"
    echo "   📂 List available files"
    echo "   🔍 Verify download integrity"
    echo
    
    while true; do
        echo -e "${BLUE}╭─────────────────────────────────────────╮${NC}"
        echo -e "${BLUE}│${NC} Select installation method (1-4):       ${BLUE}│${NC}"
        echo -e "${BLUE}╰─────────────────────────────────────────╯${NC}"
        read -p "Choice: " choice
        
        case $choice in
            1|2|3|4)
                return $choice
                ;;
            *)
                log_error "Please enter 1, 2, 3, or 4"
                ;;
        esac
    done
}

# Download and extract repository
download_repository() {
    log_info "Downloading McGuardian Elite from GitHub..."
    cd "$TEMP_DIR"
    
    # Try git clone first, then fallback to wget/curl
    if command -v git &> /dev/null; then
        log_info "Using git to clone repository..."
        if git clone --depth 1 "$REPO_URL.git" McGuardian 2>/dev/null; then
            log_success "Repository cloned successfully with git"
            cd McGuardian
            return 0
        else
            log_warning "Git clone failed, trying alternative download..."
        fi
    fi
    
    # Fallback to curl/wget
    ARCHIVE_URL="$REPO_URL/archive/refs/heads/main.zip"
    
    if command -v curl &> /dev/null; then
        log_info "Downloading with curl..."
        if curl -sSL "$ARCHIVE_URL" -o mcguardian.zip; then
            log_success "Downloaded with curl"
        else
            log_error "Failed to download with curl"
            exit 1
        fi
    elif command -v wget &> /dev/null; then
        log_info "Downloading with wget..."
        if wget -q "$ARCHIVE_URL" -O mcguardian.zip; then
            log_success "Downloaded with wget"
        else
            log_error "Failed to download with wget"
            exit 1
        fi
    else
        log_error "Neither curl nor wget found"
        log_info "Please install curl or wget to continue"
        exit 1
    fi
    
    # Extract archive
    if command -v unzip &> /dev/null; then
        log_info "Extracting archive..."
        unzip -q mcguardian.zip
        cd McGuardian-main
        log_success "Archive extracted successfully"
    else
        log_error "unzip command not found"
        log_info "Please install unzip to continue"
        exit 1
    fi
}

# Show repository contents for verification
show_repository_contents() {
    echo
    log_info "McGuardian Elite Repository Contents:"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo
    
    if [[ -f "README.md" ]]; then
        echo -e "${GREEN}📖 Documentation:${NC}"
        ls -la *.md 2>/dev/null | while read line; do
            echo "   📄 $line"
        done
        echo
    fi
    
    if [[ -f "mcguardian_installer.py" ]]; then
        echo -e "${GREEN}🔧 Installation Scripts:${NC}"
        ls -la install* mcguardian_installer.py 2>/dev/null | while read line; do
            echo "   🛠️  $line"
        done
        echo
    fi
    
    if [[ -f "mcguardian_pro.py" ]]; then
        echo -e "${GREEN}🛡️ Core Application Files:${NC}"
        ls -la mcguardian*.py ssh_security*.py 2>/dev/null | while read line; do
            echo "   🐍 $line"
        done
        echo
    fi
    
    echo -e "${GREEN}📁 All Files:${NC}"
    ls -la | while read line; do
        echo "   📄 $line"
    done
    echo
    
    # File integrity check
    echo -e "${BLUE}🔍 File Integrity Check:${NC}"
    
    REQUIRED_FILES=("mcguardian_installer.py" "mcguardian_pro.py" "mcguardian_gui.py")
    MISSING_FILES=0
    
    for file in "${REQUIRED_FILES[@]}"; do
        if [[ -f "$file" ]]; then
            SIZE=$(ls -lh "$file" | awk '{print $5}')
            echo -e "   ✅ $file (${SIZE})"
        else
            echo -e "   ❌ $file (missing)"
            ((MISSING_FILES++))
        fi
    done
    
    if [[ $MISSING_FILES -eq 0 ]]; then
        echo
        log_success "All required files are present"
    else
        echo
        log_error "$MISSING_FILES required files are missing"
        log_info "This may indicate a download issue"
    fi
    
    echo
    echo -e "${CYAN}Press Enter to continue with installation or Ctrl+C to exit...${NC}"
    read
}

# Run the appropriate installer
run_installer() {
    local install_type=$1
    
    # Verify installer exists
    if [[ ! -f "mcguardian_installer.py" ]]; then
        log_error "Enhanced installer not found in repository"
        log_info "Available files:"
        ls -la
        exit 1
    fi
    
    log_success "Enhanced installer found"
    
    # Make installer executable
    chmod +x mcguardian_installer.py
    
    echo
    log_info "Launching McGuardian Elite Enhanced Installer..."
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo
    
    case $install_type in
        1)
            log_feature "Running Quick Install with all features..."
            python3 mcguardian_installer.py --auto-install
            ;;
        2)
            log_feature "Starting Interactive Installation..."
            python3 mcguardian_installer.py
            ;;
        3)
            log_feature "Running Advanced Installation..."
            echo "This will open the installer in custom mode..."
            echo "Choose 'Security Engine Only' when prompted."
            echo
            python3 mcguardian_installer.py
            ;;
    esac
}

# Show post-installation information
show_completion_info() {
    echo
    echo -e "${GREEN}🎉 McGuardian Elite Installation Process Complete!${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo
    echo -e "${CYAN}🚀 How to Launch McGuardian Elite:${NC}"
    echo -e "${GREEN}   • Desktop App:${NC} Double-click 'McGuardian Elite' on your desktop"
    echo -e "${GREEN}   • Terminal:${NC} Type 'mcguardian_elite' in any terminal"
    echo -e "${GREEN}   • Web Dashboard:${NC} Type 'mcguardian_dashboard' then visit http://localhost:5000"
    echo
    echo -e "${CYAN}🔐 SSH Security Tools:${NC}"
    echo -e "${GREEN}   • Security Scan:${NC} mcguardian_ssh scan"
    echo -e "${GREEN}   • Auto Harden:${NC} mcguardian_ssh harden --auto"
    echo -e "${GREEN}   • Monitor Threats:${NC} mcguardian_ssh monitor"
    echo
    echo -e "${CYAN}📖 Documentation & Support:${NC}"
    echo -e "${GREEN}   • GitHub:${NC} https://github.com/heyfinal/McGuardian"
    echo -e "${GREEN}   • Issues:${NC} https://github.com/heyfinal/McGuardian/issues"
    echo -e "${GREEN}   • Discussions:${NC} https://github.com/heyfinal/McGuardian/discussions"
    echo
    echo -e "${PURPLE}🛡️ Your Mac is now protected by McGuardian Elite!${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# Main installation function
main() {
    # Handle command line arguments
    case "${1:-}" in
        --help|-h)
            echo "McGuardian Elite Quick Installer"
            echo
            echo "This script downloads and installs McGuardian Elite with full automation."
            echo
            echo "Usage: $0 [options]"
            echo "  --help, -h          Show this help"
            echo "  --version, -v       Show version"
            echo "  --auto              Quick install without prompts"
            echo "  --show-repo         Download and show repository contents"
            echo
            echo "Features:"
            echo "  • Fully automated installation"
            echo "  • Desktop launcher creation"
            echo "  • Secure randomized backup locations"
            echo "  • Advanced honeypot systems"
            echo "  • SSH security hardening"
            echo "  • Beautiful web dashboard"
            echo
            exit 0
            ;;
        --version|-v)
            echo "McGuardian Elite Quick Installer $VERSION"
            echo "Enhanced installer with full automation"
            exit 0
            ;;
        --auto)
            AUTO_INSTALL=true
            ;;
        --show-repo)
            SHOW_REPO_ONLY=true
            ;;
    esac
    
    # Initial system check
    check_requirements
    
    # Download repository
    download_repository
    
    # Handle show repository contents only
    if [[ "${SHOW_REPO_ONLY:-}" == "true" ]]; then
        show_repository_contents
        exit 0
    fi
    
    # Handle auto install
    if [[ "${AUTO_INSTALL:-}" == "true" ]]; then
        log_feature "Auto-install mode selected"
        run_installer 1
        show_completion_info
        return
    fi
    
    # Show installation options and get user choice
    choice=$(show_installation_options)
    
    # Handle repository contents viewing
    if [[ $choice -eq 4 ]]; then
        show_repository_contents
        echo
        choice=$(show_installation_options)
    fi
    
    # Run the selected installation
    run_installer $choice
    
    # Show completion information
    show_completion_info
}

# Cleanup function
cleanup() {
    log_info "Cleaning up temporary files..."
    cd /
    rm -rf "$TEMP_DIR"
}

# Set trap for cleanup
trap cleanup EXIT

# Handle interruption
trap 'echo -e "\n${YELLOW}⚠️ Installation interrupted by user${NC}"; exit 1' INT

# Run main function
main "$@"
