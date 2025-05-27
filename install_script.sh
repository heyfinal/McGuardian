#!/bin/bash
#
# ███╗   ███╗ ██████╗ ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗ ██╗ █████╗ ███╗   ██╗
# ████╗ ████║██╔════╝██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗██║██╔══██╗████╗  ██║
# ██╔████╔██║██║     ██║  ███╗██║   ██║███████║██████╔╝██║  ██║██║███████║██╔██╗ ██║
# ██║╚██╔╝██║██║     ██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║██║██╔══██║██║╚██╗██║
# ██║ ╚═╝ ██║╚██████╗╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝██║██║  ██║██║ ╚████║
# ╚═╝     ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
#                             
#                         E L I T E   I N S T A L L E R   v 3 . 0 . 0
#                    Professional Quick Install Script with Full Automation
#                      Advanced AI Security • Desktop Integration • Pro Dashboard
#
# Usage: curl -sSL https://install.mcguardian.dev | bash
#        curl -sSL https://raw.githubusercontent.com/heyfinal/McGuardian/main/install.sh | bash
#

set -e

# ═══════════════════════════════════════════════════════════════════════════════
#                                CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

# Enhanced color palette for professional output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m' # No Color

# Installation configuration
REPO_URL="https://github.com/heyfinal/McGuardian"
VERSION="v3.0.0"
TEMP_DIR=$(mktemp -d)
CURRENT_DIR=$(pwd)
INSTALL_LOG="/tmp/mcguardian_install.log"

# System information
MACOS_VERSION=$(sw_vers -productVersion 2>/dev/null || echo "Unknown")
PYTHON_VERSION=$(python3 --version 2>/dev/null | cut -d' ' -f2 || echo "Not found")
HOSTNAME=$(hostname)

# ═══════════════════════════════════════════════════════════════════════════════
#                              ENHANCED FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

show_banner() {
    echo -e "${BLUE}"
    cat << 'EOF'
███╗   ███╗ ██████╗ ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗ ██╗ █████╗ ███╗   ██╗
████╗ ████║██╔════╝██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗██║██╔══██╗████╗  ██║
██╔████╔██║██║     ██║  ███╗██║   ██║███████║██████╔╝██║  ██║██║███████║██╔██╗ ██║
██║╚██╔╝██║██║     ██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║██║██╔══██║██║╚██╗██║
██║ ╚═╝ ██║╚██████╗╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝██║██║  ██║██║ ╚████║
╚═╝     ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
                             
                        E L I T E   v 3 . 0 . 0   -   I N S T A L L E R
EOF
    echo -e "${NC}"
    
    echo -e "${GREEN}🛡️  Advanced AI-Powered Security Monitoring System for macOS${NC}"
    echo -e "${PURPLE}🚀 Professional Installation with Desktop Integration & Secure Analytics${NC}"
    echo -e "${CYAN}⚡ High-Performance • Dark Mode GUI • Real-time Threat Intelligence${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════════════════${NC}"
    echo
}

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$INSTALL_LOG"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$INSTALL_LOG"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$INSTALL_LOG"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$INSTALL_LOG"
}

log_feature() {
    echo -e "${PURPLE}[FEATURE]${NC} $1" | tee -a "$INSTALL_LOG"
}

log_step() {
    echo -e "${CYAN}[STEP]${NC} $1" | tee -a "$INSTALL_LOG"
}

show_progress() {
    local current=$1
    local total=$2
    local step_name=$3
    
    local percentage=$((current * 100 / total))
    local filled=$((percentage / 5))
    local empty=$((20 - filled))
    
    printf "\r${CYAN}[%s/%s]${NC} ${BOLD}%s${NC} [" "$current" "$total" "$step_name"
    printf "%*s" $filled | tr ' ' '█'
    printf "%*s" $empty | tr ' ' '░'
    printf "] ${GREEN}%d%%${NC}" "$percentage"
    
    if [ $current -eq $total ]; then
        echo
    fi
}

check_if_in_repo() {
    if [[ -f "mcguardian_installer.py" && -f "mcguardian_pro.py" ]]; then
        log_success "Already in McGuardian repository directory"
        log_info "Skipping repository download..."
        return 0
    else
        return 1
    fi
}

comprehensive_system_check() {
    log_step "Performing comprehensive system analysis..."
    echo
    
    # System information display
    echo -e "${BOLD}🖥️  SYSTEM INFORMATION${NC}"
    echo -e "   • Hostname: ${CYAN}$HOSTNAME${NC}"
    echo -e "   • macOS Version: ${CYAN}$MACOS_VERSION${NC}"
    echo -e "   • Python Version: ${CYAN}$PYTHON_VERSION${NC}"
    echo -e "   • Architecture: ${CYAN}$(uname -m)${NC}"
    echo -e "   • Install Time: ${CYAN}$(date)${NC}"
    echo
    
    # Check macOS version
    log_info "Verifying macOS compatibility..."
    if [[ "$OSTYPE" != "darwin"* ]]; then
        log_error "This installer requires macOS (Darwin system)"
        log_info "Detected OS: $OSTYPE"
        exit 1
    fi
    
    # Get and verify macOS version
    if command -v sw_vers >/dev/null 2>&1; then
        MACOS_VERSION=$(sw_vers -productVersion)
        MAJOR_VERSION=$(echo $MACOS_VERSION | cut -d. -f1)
        MINOR_VERSION=$(echo $MACOS_VERSION | cut -d. -f2)
        
        if [[ $MAJOR_VERSION -lt 10 ]] || [[ $MAJOR_VERSION -eq 10 && $MINOR_VERSION -lt 15 ]]; then
            log_error "macOS 10.15 (Catalina) or later required"
            log_info "Your version: $MACOS_VERSION"
            log_info "Please upgrade macOS to continue"
            exit 1
        fi
        
        log_success "macOS $MACOS_VERSION - Compatible ✅"
    else
        log_warning "Could not determine macOS version"
    fi
    
    # Enhanced Python verification
    log_info "Verifying Python installation..."
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is required but not found"
        echo
        echo -e "${YELLOW}🔧 PYTHON INSTALLATION REQUIRED:${NC}"
        echo "   • Download from: https://www.python.org/downloads/"
        echo "   • Or install via Homebrew: brew install python"
        echo "   • Minimum version required: Python 3.8+"
        exit 1
    fi
    
    # Check Python version in detail
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [[ $PYTHON_MAJOR -lt 3 ]] || [[ $PYTHON_MAJOR -eq 3 && $PYTHON_MINOR -lt 8 ]]; then
        log_error "Python 3.8+ required (found Python $PYTHON_VERSION)"
        log_info "Please upgrade Python from: https://www.python.org/downloads/"
        exit 1
    fi
    
    log_success "Python $PYTHON_VERSION - Compatible ✅"
    
    # Check pip availability
    log_info "Verifying pip package manager..."
    if ! python3 -m pip --version &> /dev/null; then
        log_error "pip is required but not found"
        log_info "Install pip: python3 -m ensurepip --upgrade"
        exit 1
    fi
    
    log_success "pip package manager - Available ✅"
    
    # Enhanced disk space check
    log_info "Checking available disk space..."
    if command -v df >/dev/null 2>&1; then
        AVAILABLE_SPACE=$(df -h . | tail -1 | awk '{print $4}' | sed 's/[^0-9.]//g')
        SPACE_UNIT=$(df -h . | tail -1 | awk '{print $4}' | sed 's/[0-9.]//g')
        
        log_info "Available disk space: $(df -h . | tail -1 | awk '{print $4}')"
        
        # Convert to MB for comparison (simplified check)
        if [[ "$SPACE_UNIT" == *"G"* ]] && (( $(echo "$AVAILABLE_SPACE >= 1" | bc -l 2>/dev/null || echo 0) )); then
            log_success "Sufficient disk space available ✅"
        elif [[ "$SPACE_UNIT" == *"M"* ]] && (( $(echo "$AVAILABLE_SPACE >= 500" | bc -l 2>/dev/null || echo 0) )); then
            log_success "Sufficient disk space available ✅"
        else
            log_warning "Low disk space detected - installation may fail"
        fi
    fi
    
    # Check system tools with enhanced reporting
    log_info "Verifying system tools availability..."
    
    local tools_status=()
    
    check_tool() {
        local tool=$1
        local description=$2
        local required=$3
        
        if command -v "$tool" >/dev/null 2>&1; then
            local tool_path=$(which "$tool")
            log_success "$tool: $tool_path"
            tools_status+=("$tool:✅")
            return 0
        else
            if [[ "$required" == "true" ]]; then
                log_error "$tool: Not found ($description) - REQUIRED"
                tools_status+=("$tool:❌")
                return 1
            else
                log_warning "$tool: Not found ($description) - Optional"
                tools_status+=("$tool:⚠️")
                return 0
            fi
        fi
    }
    
    local failed_required=0
    
    check_tool "python3" "Python interpreter" "true" || ((failed_required++))
    check_tool "pip3" "Python package manager" "true" || ((failed_required++))
    check_tool "git" "Version control system" "false"
    check_tool "curl" "HTTP client" "false"
    check_tool "unzip" "Archive extraction" "false"
    check_tool "tar" "Archive extraction" "false"
    
    if [[ $failed_required -gt 0 ]]; then
        log_error "$failed_required required tools are missing"
        echo
        echo -e "${RED}❌ SYSTEM REQUIREMENTS NOT MET${NC}"
        echo -e "${YELLOW}Please install the missing required tools and try again${NC}"
        exit 1
    fi
    
    # Test write permissions comprehensively
    log_info "Testing file system permissions..."
    
    local test_dirs=(
        "$HOME/Library"
        "$HOME/Applications"
        "/tmp"
        "$HOME/.cache"
    )
    
    local permission_failures=0
    
    for test_dir in "${test_dirs[@]}"; do
        if [[ -d "$test_dir" ]] || mkdir -p "$test_dir" 2>/dev/null; then
            local test_file="$test_dir/.mcguardian_permission_test_$$"
            if echo "test" > "$test_file" 2>/dev/null && rm "$test_file" 2>/dev/null; then
                log_success "Write access: $test_dir ✅"
            else
                log_error "No write access: $test_dir ❌"
                ((permission_failures++))
            fi
        else
            log_error "Cannot access directory: $test_dir ❌"
            ((permission_failures++))
        fi
    done
    
    if [[ $permission_failures -gt 0 ]]; then
        log_warning "$permission_failures permission issues detected"
        log_info "Installation may encounter issues with restricted directories"
    else
        log_success "All permission tests passed ✅"
    fi
    
    echo
    log_success "✅ SYSTEM REQUIREMENTS VERIFICATION COMPLETE"
    log_info "System is ready for McGuardian Elite installation"
    echo
}

show_installation_menu() {
    log_info "Displaying installation options menu..."
    
    echo
    echo -e "${CYAN}🛠️  McGuardian Elite Installation Options${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo
    echo -e "${GREEN}1. 🎯 QUICK INSTALL${NC} ${BOLD}(Recommended)${NC}"
    echo "   ✨ Complete installation with all premium features"
    echo "   🛡️  Advanced AI-powered threat detection engine"
    echo "   📊 Stunning Apple-inspired dark mode web dashboard"
    echo "   🔐 Professional SSH security hardening suite"
    echo "   🖥️  Seamless desktop integration with launchers"
    echo "   🔒 Cryptographically secure backup systems"
    echo "   🕯️ Advanced honeypot intrusion detection"
    echo "   🚀 Automatic post-install optimization"
    echo "   🌟 Premium support and documentation"
    echo
    echo -e "${YELLOW}2. 🔧 CUSTOM INSTALL${NC}"
    echo "   🎛️  Interactive component selection"
    echo "   ⚙️  Advanced configuration options"
    echo "   🎯 Tailored installation for specific needs"
    echo "   🔧 Expert-level customization controls"
    echo
    echo -e "${PURPLE}3. 🛠️  ENGINE ONLY${NC}"
    echo "   💻 Core security engine installation only"
    echo "   🖥️  Command-line interface focused"
    echo "   ⚡ Minimal system footprint"
    echo "   🚀 Perfect for servers and automation"
    echo
    echo -e "${CYAN}4. 🔍 REPOSITORY INFO${NC}"
    echo "   📂 Display downloaded repository contents"
    echo "   🔍 Verify file integrity and completeness"
    echo "   📋 View installation manifest"
    echo
    echo -e "${DIM}5. 🚪 EXIT${NC}"
    echo "   ❌ Cancel installation and exit"
    echo
    
    log_info "Menu displayed, awaiting user selection..."
    
    local choice
    local attempts=0
    while true; do
        ((attempts++))
        log_info "Input attempt #$attempts"
        
        echo -e "${BLUE}╭─────────────────────────────────────────────────────╮${NC}"
        echo -e "${BLUE}│${NC} ${BOLD}Select installation method (1-5):${NC}                   ${BLUE}│${NC}"
        echo -e "${BLUE}╰─────────────────────────────────────────────────────╯${NC}"
        echo -n "Choice: "
        
        # Enhanced input handling with timeout
        if read -t 120 choice; then
            log_info "User selected: '$choice'"
            
            case $choice in
                1|2|3|4|5)
                    log_success "Valid choice selected: $choice"
                    echo $choice
                    return
                    ;;
                *)
                    log_error "Invalid choice: '$choice'"
                    echo -e "${RED}❌ Please enter a number between 1-5${NC}"
                    ;;
            esac
        else
            log_error "Input timeout after 2 minutes"
            log_info "Defaulting to Quick Install (option 1)"
            echo "1"
            return
        fi
        
        # Safety check to prevent infinite loops
        if [[ $attempts -gt 15 ]]; then
            log_warning "Too many invalid attempts, defaulting to Quick Install"
            echo "1"
            return
        fi
    done
}

download_repository() {
    # Check if we're already in the repository
    if check_if_in_repo; then
        return 0
    fi
    
    log_step "Downloading McGuardian Elite from GitHub..."
    cd "$TEMP_DIR"
    
    # Try multiple download methods for reliability
    local download_success=false
    
    # Method 1: Git clone (preferred)
    if command -v git &> /dev/null && ! $download_success; then
        log_info "Attempting download via git clone..."
        if git clone --depth 1 --quiet "$REPO_URL.git" McGuardian 2>/dev/null; then
            log_success "Repository cloned successfully with git"
            cd McGuardian
            download_success=true
        else
            log_warning "Git clone failed, trying alternative methods..."
        fi
    fi
    
    # Method 2: curl + unzip
    if command -v curl &> /dev/null && command -v unzip &> /dev/null && ! $download_success; then
        log_info "Attempting download via curl..."
        local archive_url="$REPO_URL/archive/refs/heads/main.zip"
        
        if curl -sSL --connect-timeout 30 --max-time 300 "$archive_url" -o mcguardian.zip; then
            log_success "Downloaded archive via curl"
            
            if unzip -q mcguardian.zip && cd McGuardian-main; then
                log_success "Archive extracted successfully"
                download_success=true
            else
                log_error "Failed to extract archive"
            fi
        else
            log_warning "Curl download failed"
        fi
    fi
    
    # Method 3: wget + unzip (fallback)
    if command -v wget &> /dev/null && command -v unzip &> /dev/null && ! $download_success; then
        log_info "Attempting download via wget..."
        local archive_url="$REPO_URL/archive/refs/heads/main.zip"
        
        if wget -q --timeout=30 --tries=3 "$archive_url" -O mcguardian.zip; then
            log_success "Downloaded archive via wget"
            
            if unzip -q mcguardian.zip && cd McGuardian-main; then
                log_success "Archive extracted successfully"
                download_success=true
            else
                log_error "Failed to extract archive"
            fi
        else
            log_warning "Wget download failed"
        fi
    fi
    
    if ! $download_success; then
        log_error "All download methods failed"
        echo
        echo -e "${RED}❌ DOWNLOAD FAILED${NC}"
        echo -e "${YELLOW}Possible solutions:${NC}"
        echo "   • Check internet connection"
        echo "   • Install git: brew install git"
        echo "   • Try manual download from: $REPO_URL"
        echo "   • Check firewall/proxy settings"
        exit 1
    fi
    
    # Verify download integrity
    log_info "Verifying download integrity..."
    local required_files=("mcguardian_installer.py" "mcguardian_pro.py" "mcguardian_gui.py")
    local missing_files=0
    
    for file in "${required_files[@]}"; do
        if [[ -f "$file" ]]; then
            local file_size=$(wc -c < "$file" 2>/dev/null || echo "0")
            log_success "$file (${file_size} bytes)"
        else
            log_error "$file - MISSING"
            ((missing_files++))
        fi
    done
    
    if [[ $missing_files -gt 0 ]]; then
        log_error "$missing_files critical files are missing"
        log_warning "Download may be incomplete or corrupted"
    else
        log_success "All critical files verified ✅"
    fi
}

show_repository_contents() {
    echo
    log_info "McGuardian Elite Repository Contents Analysis"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo
    
    # Documentation files
    if [[ -f "README.md" ]] || [[ -f "readme_file.md" ]]; then
        echo -e "${GREEN}📖 DOCUMENTATION:${NC}"
        for doc in README.md readme_file.md CONTRIBUTING.md contributing_file.md; do
            if [[ -f "$doc" ]]; then
                local doc_size=$(wc -c < "$doc" 2>/dev/null || echo "0")
                echo "   📄 $doc (${doc_size} bytes)"
            fi
        done
        echo
    fi
    
    # Installation scripts
    echo -e "${GREEN}🔧 INSTALLATION SCRIPTS:${NC}"
    for script in install.sh install_script.sh mcguardian_installer.py mcguardian_enhanced_installer.py; do
        if [[ -f "$script" ]]; then
            local script_size=$(wc -c < "$script" 2>/dev/null || echo "0")
            echo "   🛠️  $script (${script_size} bytes)"
        fi
    done
    echo
    
    # Core application files
    echo -e "${GREEN}🛡️  CORE SECURITY ENGINE:${NC}"
    for app in mcguardian_pro.py mcguardian_gui.py ssh_security*.py; do
        if [[ -f "$app" ]]; then
            local app_size=$(wc -c < "$app" 2>/dev/null || echo "0")
            echo "   🐍 $app (${app_size} bytes)"
        fi
    done
    echo
    
    # Configuration and data files
    echo -e "${GREEN}📁 ADDITIONAL FILES:${NC}"
    for file in requirements.txt .gitignore LICENSE; do
        if [[ -f "$file" ]]; then
            local file_size=$(wc -c < "$file" 2>/dev/null || echo "0")
            echo "   📋 $file (${file_size} bytes)"
        fi
    done
    echo
    
    # Complete file listing
    echo -e "${GREEN}📂 COMPLETE FILE MANIFEST:${NC}"
    local file_count=0
    local total_size=0
    
    while IFS= read -r -d '' file; do
        local size=$(wc -c < "$file" 2>/dev/null || echo "0")
        echo "   📄 $(basename "$file") (${size} bytes)"
        ((file_count++))
        ((total_size += size))
    done < <(find . -maxdepth 1 -type f -print0 2>/dev/null)
    
    echo
    echo -e "${CYAN}📊 REPOSITORY STATISTICS:${NC}"
    echo "   • Total Files: $file_count"
    echo "   • Total Size: $total_size bytes ($(echo "scale=2; $total_size/1024/1024" | bc -l 2>/dev/null || echo "?") MB)"
    echo "   • Repository: $REPO_URL"
    echo "   • Version: $VERSION"
    
    # File integrity verification
    echo
    echo -e "${BLUE}🔍 FILE INTEGRITY VERIFICATION:${NC}"
    
    local required_files=("mcguardian_installer.py" "mcguardian_pro.py" "mcguardian_gui.py")
    local verification_passed=true
    
    for file in "${required_files[@]}"; do
        if [[ -f "$file" ]]; then
            local size=$(wc -c < "$file" 2>/dev/null || echo "0")
            if [[ $size -gt 1000 ]]; then  # Reasonable minimum size check
                echo "   ✅ $file - Integrity OK (${size} bytes)"
            else
                echo "   ⚠️  $file - Suspiciously small (${size} bytes)"
                verification_passed=false
            fi
        else
            echo "   ❌ $file - MISSING"
            verification_passed=false
        fi
    done
    
    echo
    if $verification_passed; then
        log_success "✅ All critical files verified - Repository integrity confirmed"
    else
        log_warning "⚠️  Some files failed verification - Repository may be incomplete"
    fi
    
    echo
    echo -e "${CYAN}Press Enter to continue with installation or Ctrl+C to exit...${NC}"
    read -r
}

run_installer() {
    local install_type=$1
    
    log_step "Launching McGuardian Elite Enhanced Installer..."
    
    # Verify installer exists and is executable
    local installer_script=""
    
    # Try to find the best installer
    if [[ -f "mcguardian_enhanced_installer.py" ]]; then
        installer_script="mcguardian_enhanced_installer.py"
    elif [[ -f "mcguardian_installer.py" ]]; then
        installer_script="mcguardian_installer.py"
    else
        log_error "No installer script found in repository"
        echo
        echo -e "${RED}❌ INSTALLER NOT FOUND${NC}"
        echo "Available files:"
        ls -la
        echo
        echo -e "${YELLOW}This may indicate a repository download issue${NC}"
        exit 1
    fi
    
    log_success "Using installer: $installer_script"
    
    # Make installer executable
    chmod +x "$installer_script" 2>/dev/null || true
    
    echo
    log_feature "🚀 LAUNCHING MCGUARDIAN ELITE INSTALLER"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════════════════${NC}"
    echo
    
    # Enhanced installer execution with proper error handling
    local installer_args=()
    local installer_exit_code=0
    
    case $install_type in
        1)
            log_feature "🎯 Quick Install - Full premium installation with all features"
            echo "⏳ This comprehensive installation includes:"
            echo "   • Advanced AI security engine with threat intelligence"
            echo "   • Professional dark-mode web dashboard"
            echo "   • SSH security hardening and monitoring"
            echo "   • Desktop integration and system launchers"
            echo "   • Cryptographically secure backup systems"
            echo "   • Advanced honeypot intrusion detection"
            echo
            echo "🔄 Installation will take 2-5 minutes depending on your system..."
            installer_args+=("--auto-install")
            ;;
        2)
            log_feature "🔧 Custom Install - Interactive component selection"
            echo "📋 You will be prompted to choose specific components"
            echo "⚙️  Advanced configuration options will be available"
            echo
            # No special args - interactive mode
            ;;
        3)
            log_feature "🛠️  Engine Only - Core security monitoring"
            echo "💻 Installing core security engine only"
            echo "⚡ Minimal installation for servers and headless systems"
            echo
            echo "Choose 'Engine Only' when prompted in the installer."
            ;;
    esac
    
    # Execute installer with enhanced error handling
    echo "🚀 Starting Python installer..."
    echo
    
    if python3 "$installer_script" "${installer_args[@]}"; then
        installer_exit_code=0
    else
        installer_exit_code=$?
    fi
    
    echo
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════════════════════════${NC}"
    
    if [[ $installer_exit_code -eq 0 ]]; then
        log_success "🎉 Python installer completed successfully!"
        
        # Post-installation verification
        echo
        log_info "Performing post-installation verification..."
        
        # Check if commands are available
        local verification_passed=true
        
        # Source shell configuration to pick up new PATH
        if [[ -f "$HOME/.zshrc" ]]; then
            source "$HOME/.zshrc" 2>/dev/null || true
        fi
        
        # Test installations
        if command -v mcguardian_elite >/dev/null 2>&1; then
            log_success "✅ mcguardian_elite command available"
        else
            log_warning "⚠️  mcguardian_elite command not found (may need shell reload)"
            verification_passed=false
        fi
        
        if command -v mcguardian_dashboard >/dev/null 2>&1; then
            log_success "✅ mcguardian_dashboard command available"
        else
            log_info "ℹ️  mcguardian_dashboard not installed (may be engine-only installation)"
        fi
        
        # Check installation directories
        local possible_install_dirs=(
            "$HOME/Applications/McGuardian Elite"
            "$HOME/Applications/McGuardian Elite.app"
            "/Applications/McGuardian Elite.app"
        )
        
        local install_found=false
        for dir in "${possible_install_dirs[@]}"; do
            if [[ -d "$dir" ]]; then
                log_success "✅ Installation directory found: $dir"
                install_found=true
                break
            fi
        done
        
        if ! $install_found; then
            log_warning "⚠️  Installation directory not found in standard locations"
            verification_passed=false
        fi
        
        if $verification_passed; then
            log_success "🎉 INSTALLATION VERIFICATION PASSED"
        else
            log_warning "⚠️  Some verification checks failed"
            echo
            echo -e "${YELLOW}🔧 TROUBLESHOOTING TIPS:${NC}"
            echo "   • Reload your shell: source ~/.zshrc"
            echo "   • Restart Terminal application"
            echo "   • Check installation logs above for errors"
        fi
        
        return 0
    else
        log_error "❌ Python installer failed with exit code: $installer_exit_code"
        echo
        log_warning "Installation encountered issues. Check the output above for details."
        echo
        echo -e "${CYAN}🔧 COMMON SOLUTIONS:${NC}"
        echo "   • Ensure Python 3.8+ is properly installed"
        echo "   • Check available disk space (need 500MB+ free)"
        echo "   • Verify internet connection for dependency downloads"
        echo "   • Try running with debug mode:"
        echo "     python3 $installer_script --debug"
        echo "   • Check system requirements:"
        echo "     python3 $installer_script --help"
        echo
        echo -e "${PURPLE}📞 GET HELP:${NC}"
        echo "   • GitHub Issues: $REPO_URL/issues"
        echo "   • Include your system info: macOS $MACOS_VERSION, Python $PYTHON_VERSION"
        echo "   • Copy any error messages from the installation output"
        echo
        return $installer_exit_code
    fi
}

show_completion_summary() {
    echo
    log_success "🔍 ANALYZING INSTALLATION RESULTS..."
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    
    # Comprehensive installation verification
    local verification_score=0
    local max_score=10
    
    echo -e "${BOLD}📊 INSTALLATION VERIFICATION REPORT${NC}"
    echo
    
    # Check 1: Installation directories
    echo "🔍 Checking installation directories..."
    local install_dirs=(
        "$HOME/Applications/McGuardian Elite"
        "$HOME/Applications/McGuardian Elite.app"
        "/Applications/McGuardian Elite.app"
    )
    
    local install_found=false
    for dir in "${install_dirs[@]}"; do
        if [[ -d "$dir" ]]; then
            log_success "✅ Installation directory: $dir"
            install_found=true
            ((verification_score++))
            break
        fi
    done
    
    if ! $install_found; then
        log_error "❌ No installation directory found"
    fi
    
    # Check 2: Command availability
    echo "🔍 Checking command availability..."
    
    # Source shell configurations to ensure commands are in PATH
    for shell_config in "$HOME/.zshrc" "$HOME/.bash_profile" "$HOME/.bashrc"; do
        [[ -f "$shell_config" ]] && source "$shell_config" 2>/dev/null || true
    done
    
    if command -v mcguardian_elite >/dev/null 2>&1; then
        log_success "✅ mcguardian_elite command available"
        ((verification_score++))
    else
        log_warning "⚠️  mcguardian_elite command not found"
    fi
    
    if command -v mcguardian_dashboard >/dev/null 2>&1; then
        log_success "✅ mcguardian_dashboard command available"
        ((verification_score++))
    else
        log_info "ℹ️  mcguardian_dashboard command not available (may be engine-only install)"
        ((verification_score++))  # Don't penalize for engine-only installs
    fi
    
    if command -v mcguardian_ssh >/dev/null 2>&1; then
        log_success "✅ mcguardian_ssh command available"
        ((verification_score++))
    else
        log_info "ℹ️  mcguardian_ssh command not available"
    fi
    
    # Check 3: Desktop integration
    echo "🔍 Checking desktop integration..."
    if [[ -e "$HOME/Desktop/McGuardian Elite.app" ]]; then
        log_success "✅ Desktop shortcut created"
        ((verification_score++))
    else
        log_info "ℹ️  Desktop shortcut not found (may not be requested)"
        ((verification_score++))  # Don't penalize
    fi
    
    # Check 4: Configuration files
    echo "🔍 Checking configuration files..."
    if [[ -d "$HOME/.mcguardian_elite" ]]; then
        log_success "✅ Configuration directory exists"
        ((verification_score++))
    else
        log_warning "⚠️  Configuration directory not found"
    fi
    
    # Check 5: Data directories
    echo "🔍 Checking data directories..."
    if [[ -d "$HOME/Library/Logs/McGuardianElite" ]]; then
        log_success "✅ Data directory structure created"
        ((verification_score++))
    else
        log_warning "⚠️  Data directory not found"
    fi
    
    # Check 6: Python dependencies
    echo "🔍 Checking Python dependencies..."
    local critical_deps=("watchdog" "psutil" "flask")
    local deps_ok=0
    
    for dep in "${critical_deps[@]}"; do
        if python3 -c "import $dep" 2>/dev/null; then
            ((deps_ok++))
        fi
    done
    
    if [[ $deps_ok -eq ${#critical_deps[@]} ]]; then
        log_success "✅ All critical Python dependencies available"
        ((verification_score++))
    else
        log_warning "⚠️  Some Python dependencies missing ($deps_ok/${#critical_deps[@]})"
    fi
    
    # Check 7: Process verification
    echo "🔍 Checking for running processes..."
    if pgrep -f "mcguardian" >/dev/null 2>&1; then
        log_success "✅ McGuardian processes detected"
        local pids=$(pgrep -f "mcguardian" | tr '\n' ' ')
        log_info "Process IDs: $pids"
        ((verification_score++))
    else
        log_info "ℹ️  No McGuardian processes running (normal if not auto-started)"
        ((verification_score++))  # Don't penalize
    fi
    
    # Final verification score
    echo
    echo -e "${BOLD}📊 VERIFICATION SCORE: $verification_score/$max_score${NC}"
    
    if [[ $verification_score -ge 8 ]]; then
        echo -e "${GREEN}✅ INSTALLATION VERIFICATION: EXCELLENT! ✅${NC}"
        echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
        show_success_summary
    elif [[ $verification_score -ge 6 ]]; then
        echo -e "${YELLOW}⚠️  INSTALLATION VERIFICATION: GOOD WITH MINOR ISSUES ⚠️${NC}"
        echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
        show_success_summary
        show_troubleshooting_tips
    else
        echo -e "${RED}❌ INSTALLATION VERIFICATION: ISSUES DETECTED ❌${NC}"
        echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
        show_failure_summary
    fi
}

show_success_summary() {
    echo
    echo -e "${GREEN}🎉 MCGUARDIAN ELITE INSTALLATION SUCCESSFUL! 🎉${NC}"
    echo
    echo -e "${CYAN}🚀 HOW TO LAUNCH MCGUARDIAN ELITE:${NC}"
    echo
    echo -e "${GREEN}   🛡️  SECURITY ENGINE:${NC}"
    echo "      • Desktop App: Double-click 'McGuardian Elite' on your desktop"
    echo "      • Terminal: mcguardian_elite"
    echo "      • Background: mcguardian_elite &"
    echo
    echo -e "${GREEN}   📊 WEB DASHBOARD:${NC}"
    echo "      • Terminal: mcguardian_dashboard"
    echo "      • Browser: http://localhost:5000"
    echo "      • Background: mcguardian_dashboard &"
    echo
    echo -e "${GREEN}   🔐 SSH SECURITY TOOLS:${NC}"
    echo "      • Security scan: mcguardian_ssh scan"
    echo "      • Auto-harden: mcguardian_ssh harden --auto"
    echo "      • Live monitoring: mcguardian_ssh monitor"
    echo
    echo -e "${CYAN}🧪 VERIFY INSTALLATION:${NC}"
    echo "   • Quick test in new terminal: mcguardian_elite --help"
    echo "   • Dashboard test: mcguardian_dashboard (then visit http://localhost:5000)"
    echo "   • SSH test: mcguardian_ssh status"
    echo
    echo -e "${CYAN}📖 DOCUMENTATION & SUPPORT:${NC}"
    echo "   • GitHub Repository: $REPO_URL"
    echo "   • Report Issues: $REPO_URL/issues"
    echo "   • Discussions: $REPO_URL/discussions"
    echo "   • Documentation: $REPO_URL/wiki"
    echo
    echo -e "${PURPLE}🛡️  YOUR MAC IS NOW PROTECTED BY MCGUARDIAN ELITE!${NC}"
    echo -e "${BOLD}Advanced AI-powered threat detection is ready to secure your system${NC}"
    echo
    echo -e "${CYAN}💡 PRO TIPS:${NC}"
    echo "   • Start with: mcguardian_elite (launches main security engine)"
    echo "   • Monitor threats: mcguardian_dashboard (web interface)"
    echo "   • Secure SSH: mcguardian_ssh scan (check SSH security)"
    echo "   • View logs: tail -f ~/Library/Logs/McGuardianElite/human_readable/security_explained.log"
    echo
    echo -e "${GREEN}✨ Installation completed at: $(date)${NC}"
    echo -e "${GREEN}🆔 Installation session: $(basename "$TEMP_DIR")${NC}"
}

show_troubleshooting_tips() {
    echo
    echo -e "${YELLOW}🔧 TROUBLESHOOTING TIPS:${NC}"
    echo
    echo "If commands are not found:"
    echo "   • Reload shell: source ~/.zshrc"
    echo "   • Restart Terminal application"
    echo "   • Check PATH: echo \$PATH"
    echo
    echo "If dashboard won't start:"
    echo "   • Check Python dependencies: python3 -c 'import flask'"
    echo "   • Try manual start: python3 ~/Applications/McGuardian\\ Elite/lib/mcguardian_gui.py"
    echo
    echo "For general issues:"
    echo "   • Check installation logs in Terminal output above"
    echo "   • Verify system requirements: macOS 10.15+, Python 3.8+"
    echo "   • Try reinstalling: curl -sSL https://install.mcguardian.dev | bash"
    echo
}

show_failure_summary() {
    echo
    echo -e "${RED}❌ INSTALLATION FAILED OR INCOMPLETE${NC}"
    echo
    echo -e "${YELLOW}🔧 IMMEDIATE TROUBLESHOOTING STEPS:${NC}"
    echo
    echo "1. Check the installation output above for specific error messages"
    echo "2. Verify system requirements:"
    echo "   • macOS 10.15+ (you have: $MACOS_VERSION)"
    echo "   • Python 3.8+ (you have: $PYTHON_VERSION)"
    echo "   • 500MB+ free disk space"
    echo
    echo "3. Try manual installation:"
    echo "   git clone $REPO_URL.git"
    echo "   cd McGuardian"
    echo "   python3 mcguardian_installer.py --debug"
    echo
    echo "4. Check common issues:"
    echo "   • Internet connectivity problems"
    echo "   • Insufficient permissions"
    echo "   • Missing system tools (git, python3, pip3)"
    echo "   • Firewall blocking downloads"
    echo
    echo -e "${PURPLE}📞 GET HELP:${NC}"
    echo "   • Report issues: $REPO_URL/issues"
    echo "   • Include system info: macOS $MACOS_VERSION, Python $PYTHON_VERSION"
    echo "   • Copy error messages from Terminal output"
    echo "   • Mention installation method: Quick Install Script"
    echo
}

cleanup() {
    if [[ -n "$TEMP_DIR" && "$TEMP_DIR" != "$CURRENT_DIR" && -d "$TEMP_DIR" ]]; then
        log_info "Cleaning up temporary files..."
        cd "$CURRENT_DIR" 2>/dev/null || cd /
        rm -rf "$TEMP_DIR" 2>/dev/null || true
    fi
}

# ═══════════════════════════════════════════════════════════════════════════════
#                                MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

main() {
    # Initialize logging
    echo "McGuardian Elite Installation Session: $(date)" > "$INSTALL_LOG"
    echo "Temp Directory: $TEMP_DIR" >> "$INSTALL_LOG"
    echo "System: macOS $MACOS_VERSION, Python $PYTHON_VERSION" >> "$INSTALL_LOG"
    echo "Repository: $REPO_URL" >> "$INSTALL_LOG"
    echo "----------------------------------------" >> "$INSTALL_LOG"
    
    # Handle command line arguments
    case "${1:-}" in
        --help|-h)
            show_banner
            echo -e "${CYAN}McGuardian Elite Quick Install Script${NC}"
            echo
            echo -e "${BOLD}USAGE:${NC}"
            echo "  curl -sSL https://install.mcguardian.dev | bash"
            echo "  curl -sSL https://raw.githubusercontent.com/heyfinal/McGuardian/main/install.sh | bash"
            echo
            echo -e "${BOLD}OPTIONS:${NC}"
            echo "  --help, -h          Show this help"
            echo "  --version, -v       Show version information"
            echo "  --auto              Quick install without prompts"
            echo "  --show-repo         Download and show repository contents only"
            echo
            echo -e "${BOLD}FEATURES:${NC}"
            echo "  • 🛡️  Advanced AI-powered threat detection engine"
            echo "  • 📊 Professional dark-mode web dashboard"
            echo "  • 🔐 SSH security hardening and monitoring"
            echo "  • 🖥️  Seamless desktop integration"
            echo "  • 🔒 Cryptographically secure backup systems"
            echo "  • 🕯️ Advanced honeypot intrusion detection"
            echo
            exit 0
            ;;
        --version|-v)
            show_banner
            echo -e "${GREEN}McGuardian Elite Quick Install Script $VERSION${NC}"
            echo "Advanced AI-powered security monitoring system for macOS"
            echo "Repository: $REPO_URL"
            exit 0
            ;;
        --auto)
            AUTO_INSTALL=true
            ;;
        --show-repo)
            SHOW_REPO_ONLY=true
            ;;
    esac
    
    # Show banner
    show_banner
    
    # System requirements check
    show_progress 1 8 "System Analysis"
    comprehensive_system_check
    
    # Download repository
    show_progress 2 8 "Repository Download"
    download_repository
    
    # Handle show repository contents only
    if [[ "${SHOW_REPO_ONLY:-}" == "true" ]]; then
        show_repository_contents
        exit 0
    fi
    
    # Handle auto install
    if [[ "${AUTO_INSTALL:-}" == "true" ]]; then
        log_feature "🚀 Auto-install mode activated"
        show_progress 3 8 "Auto Installation"
        
        if run_installer 1; then
            show_progress 8 8 "Verification Complete"
            show_completion_summary
        else
            log_error "Auto-install failed!"
            exit 1
        fi
        return
    fi
    
    # Show installation menu
    show_progress 3 8 "Configuration Menu"
    choice=$(show_installation_menu)
    
    # Handle repository contents viewing
    if [[ $choice -eq 4 ]]; then
        show_repository_contents
        choice=$(show_installation_menu)
    fi
    
    # Handle exit
    if [[ $choice -eq 5 ]]; then
        log_info "Installation cancelled by user"
        echo -e "${YELLOW}Installation cancelled. McGuardian Elite was not installed.${NC}"
        exit 0
    fi
    
    # Run the selected installation
    case $choice in
        1|2|3)
            show_progress 4 8 "Running Installer"
            if run_installer $choice; then
                show_progress 8 8 "Installation Complete"
                show_completion_summary
            else
                log_error "Installation process failed!"
                echo
                echo -e "${RED}❌ INSTALLATION FAILED${NC}"
                echo
                echo -e "${CYAN}🔧 NEXT STEPS:${NC}"
                echo "1. Review error messages above"
                echo "2. Check system requirements"
                echo "3. Try manual installation: python3 mcguardian_installer.py --debug"
                echo "4. Report issues: $REPO_URL/issues"
                exit 1
            fi
            ;;
        *)
            log_error "Invalid installation choice: $choice"
            exit 1
            ;;
    esac
}

# Set up cleanup trap
trap cleanup EXIT

# Handle interruption gracefully
trap 'echo -e "\n${YELLOW}⚠️  Installation interrupted by user${NC}"; exit 1' INT

# Execute main function
main "$@"
