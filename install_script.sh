#!/bin/bash
#
# McGuardian Elite - Quick Install Script
# Downloads and runs the main Python installer
#
# Usage: curl -sSL https://install.mcguardian.dev | bash
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# McGuardian Elite branding
echo -e "${BLUE}"
cat << "EOF"
    ███╗   ███╗ ██████╗ ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗ ██╗ █████╗ ███╗   ██╗
    ████╗ ████║██╔════╝██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗██║██╔══██╗████╗  ██║
    ██╔████╔██║██║     ██║  ███╗██║   ██║███████║██████╔╝██║  ██║██║███████║██╔██╗ ██║
    ██║╚██╔╝██║██║     ██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║██║██╔══██║██║╚██╗██║
    ██║ ╚═╝ ██║╚██████╗╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝██║██║  ██║██║ ╚████║
    ╚═╝     ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
                                    
                                E L I T E   v 3 . 0 . 0
EOF
echo -e "${NC}"

echo -e "${GREEN}🛡️  Advanced AI-Powered Security Monitoring System for macOS${NC}"
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

# Quick system check
check_requirements() {
    log_info "Checking system requirements..."
    
    if [[ "$OSTYPE" != "darwin"* ]]; then
        log_error "This installer requires macOS"
        exit 1
    fi
    
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is required. Install from https://www.python.org/downloads/"
        exit 1
    fi
    
    log_success "System requirements met"
}

# Download and run main installer
main() {
    log_info "Starting McGuardian Elite installation..."
    
    # Quick checks
    check_requirements
    
    # Download the project
    log_info "Downloading McGuardian Elite..."
    cd "$TEMP_DIR"
    
    if command -v git &> /dev/null; then
        git clone --depth 1 "$REPO_URL.git" McGuardian
        cd McGuardian
    else
        curl -sSL "$REPO_URL/archive/refs/heads/main.zip" -o mcguardian.zip
        unzip -q mcguardian.zip
        cd McGuardian-main
    fi
    
    log_success "Downloaded successfully"
    
    # Check if installer exists
    if [[ ! -f "mcguardian_installer.py" ]]; then
        log_error "Installer file not found in repository"
        log_info "Available files:"
        ls -la
        exit 1
    fi
    
    # Run the main Python installer
    log_info "Launching main installer..."
    chmod +x mcguardian_installer.py
    
    # Check if user wants interactive or auto install
    echo
    echo -e "${YELLOW}Choose installation method:${NC}"
    echo "  1) Quick Install (recommended) - Full installation with defaults"
    echo "  2) Custom Install - Choose specific options"
    echo
    read -p "Enter choice (1-2): " choice
    
    case $choice in
        1)
            python3 mcguardian_installer.py --auto-install
            ;;
        2)
            python3 mcguardian_installer.py
            ;;
        *)
            log_info "Defaulting to quick install..."
            python3 mcguardian_installer.py --auto-install
            ;;
    esac
    
    # Cleanup
    cd /
    rm -rf "$TEMP_DIR"
    
    echo
    log_success "Installation completed!"
    echo -e "${BLUE}🚀 Run 'mcguardian_elite' to start monitoring your Mac!${NC}"
}

# Handle arguments
case "${1:-}" in
    --help|-h)
        echo "McGuardian Elite Quick Installer"
        echo
        echo "This script downloads and runs the main Python installer."
        echo "The Python installer provides full installation options."
        echo
        echo "Usage: $0 [options]"
        echo "  --help, -h     Show this help"
        echo "  --version, -v  Show version"
        exit 0
        ;;
    --version|-v)
        echo "McGuardian Elite Quick Installer $VERSION"
        echo "Downloads and runs: mcguardian_installer.py"
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac
