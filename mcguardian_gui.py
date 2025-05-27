#!/usr/bin/env python3
"""
███╗   ███╗ ██████╗ ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗ ██╗ █████╗ ███╗   ██╗
████╗ ████║██╔════╝██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗██║██╔══██╗████╗  ██║
██╔████╔██║██║     ██║  ███╗██║   ██║███████║██████╔╝██║  ██║██║███████║██╔██╗ ██║
██║╚██╔╝██║██║     ██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║██║██╔══██║██║╚██╗██║
██║ ╚═╝ ██║╚██████╗╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝██║██║  ██║██║ ╚████║
╚═╝     ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
                            
                        E L I T E   v 3 . 0 . 0   -   G U I
                    Advanced AI-Powered Security Dashboard
                      Optimized • Dark Mode • Responsive
"""

from flask import Flask, render_template, jsonify, request, send_file
import sqlite3
import json
import os
import sys
from datetime import datetime, timedelta
import threading
import time
from pathlib import Path
import psutil
from collections import deque

# ═══════════════════════════════════════════════════════════════════════════════
#                           CONFIGURATION & PATHS  
# ═══════════════════════════════════════════════════════════════════════════════

BASE_DIR = os.path.expanduser('~/Library/Logs/McGuardianElite')
DB_FILE = os.path.join(BASE_DIR, 'analytics', 'threat_intelligence.db')
LOG_FILE = os.path.join(BASE_DIR, 'human_readable', 'security_explained.log')
ALERTS_FILE = os.path.join(BASE_DIR, 'human_readable', 'critical_alerts.log')

app = Flask(__name__)
app.secret_key = 'mcguardian_elite_secure_dashboard_2024'

# ═══════════════════════════════════════════════════════════════════════════════
#                            OPTIMIZED DATA MANAGER
# ═══════════════════════════════════════════════════════════════════════════════

class OptimizedDashboardData:
    def __init__(self):
        self.recent_events = deque(maxlen=50)  # Limit memory usage
        self.threat_stats = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'INFO': 0}
        self.system_status = 'INITIALIZING'
        self.last_update = None
        self.update_lock = threading.Lock()
        self.cache_duration = 10  # Cache data for 10 seconds
        
    def update_data(self):
        """Thread-safe optimized data update"""
        with self.update_lock:
            current_time = datetime.now()
            
            # Skip update if cache is still valid
            if (self.last_update and 
                (current_time - self.last_update).seconds < self.cache_duration):
                return
            
            try:
                # Read recent events efficiently
                if os.path.exists(LOG_FILE):
                    self._update_events()
                
                # Update threat statistics
                self._update_threat_stats()
                
                # Check system status
                self._update_system_status()
                
                self.last_update = current_time
                
            except Exception as e:
                print(f"❌ Dashboard data update error: {e}")
    
    def _update_events(self):
        """Efficiently parse log entries"""
        try:
            # Read only last 100 lines for performance
            with open(LOG_FILE, 'rb') as f:
                f.seek(0, 2)  # Go to end
                file_size = f.tell()
                
                # Read last ~10KB or file size if smaller
                read_size = min(10240, file_size)
                f.seek(max(0, file_size - read_size))
                
                lines = f.read().decode('utf-8', errors='ignore').split('\n')[-50:]
                
            self.recent_events.clear()
            self._parse_log_entries(lines)
            
        except Exception as e:
            print(f"⚠️ Error reading events: {e}")
    
    def _parse_log_entries(self, lines):
        """Optimized log parsing"""
        current_event = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Detect timestamp at start of entry
            if any(line.startswith(year) for year in ['2024', '2025']):
                if current_event:
                    self.recent_events.append(current_event)
                
                current_event = {
                    'timestamp': line.split('\n')[0],
                    'content': '',
                    'risk_level': 'INFO',
                    'type': 'security_event'
                }
            elif current_event:
                current_event['content'] += line + '\n'
                
                # Quick risk level detection
                if any(keyword in line.upper() for keyword in ['CRITICAL', '🔴']):
                    current_event['risk_level'] = 'CRITICAL'
                elif any(keyword in line.upper() for keyword in ['HIGH', '🟠']):
                    current_event['risk_level'] = 'HIGH'
                elif any(keyword in line.upper() for keyword in ['MEDIUM', '🟡']):
                    current_event['risk_level'] = 'MEDIUM'
                elif any(keyword in line.upper() for keyword in ['LOW', '🟢']):
                    current_event['risk_level'] = 'LOW'
        
        if current_event:
            self.recent_events.append(current_event)
    
    def _update_threat_stats(self):
        """Update threat level statistics"""
        self.threat_stats = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'INFO': 0}
        
        for event in self.recent_events:
            level = event.get('risk_level', 'INFO')
            self.threat_stats[level] += 1
    
    def _update_system_status(self):
        """Update overall system status"""
        if self.threat_stats['CRITICAL'] > 0:
            self.system_status = '🔴 CRITICAL THREATS ACTIVE'
        elif self.threat_stats['HIGH'] > 0:
            self.system_status = '🟠 HIGH RISK ACTIVITY'
        elif self.threat_stats['MEDIUM'] > 5:
            self.system_status = '🟡 ELEVATED RISK LEVEL'
        else:
            self.system_status = '🟢 MONITORING - SECURE'

# Global dashboard data instance
dashboard_data = OptimizedDashboardData()

# ═══════════════════════════════════════════════════════════════════════════════
#                              FLASK ROUTES
# ═══════════════════════════════════════════════════════════════════════════════

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/status')
def api_status():
    """Get current system status - optimized"""
    dashboard_data.update_data()
    
    # Get system performance metrics
    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    
    return jsonify({
        'status': dashboard_data.system_status,
        'threat_stats': dashboard_data.threat_stats,
        'total_events': len(dashboard_data.recent_events),
        'last_update': dashboard_data.last_update.isoformat() if dashboard_data.last_update else None,
        'system_performance': {
            'cpu': cpu_percent,
            'memory': memory.percent,
            'disk': psutil.disk_usage('/').percent
        }
    })

@app.route('/api/events')
def api_events():
    """Get recent security events - paginated"""
    dashboard_data.update_data()
    
    # Get pagination parameters
    limit = min(int(request.args.get('limit', 20)), 50)  # Max 50 events
    offset = int(request.args.get('offset', 0))
    
    events_list = list(dashboard_data.recent_events)[offset:offset+limit]
    
    return jsonify({
        'events': events_list,
        'count': len(events_list),
        'total': len(dashboard_data.recent_events)
    })

@app.route('/api/alerts')
def api_alerts():
    """Get critical alerts - cached"""
    try:
        alerts = []
        if os.path.exists(ALERTS_FILE):
            # Read only recent alerts for performance
            with open(ALERTS_FILE, 'rb') as f:
                f.seek(0, 2)
                file_size = f.tell()
                read_size = min(5120, file_size)  # Read last 5KB
                f.seek(max(0, file_size - read_size))
                content = f.read().decode('utf-8', errors='ignore')
                
                # Parse last 5 alerts
                alert_sections = content.split('=' * 100)[-5:]
                for section in alert_sections:
                    if section.strip():
                        alerts.append({
                            'content': section.strip()[:500] + '...' if len(section.strip()) > 500 else section.strip(),
                            'timestamp': datetime.now().isoformat(),
                            'severity': 'CRITICAL' if any(word in section.upper() for word in ['CRITICAL', 'ATTACK', 'BREACH']) else 'HIGH'
                        })
        
        return jsonify({'alerts': alerts})
    except Exception as e:
        return jsonify({'error': str(e), 'alerts': []})

@app.route('/api/system_info')
def api_system_info():
    """Get system information"""
    try:
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        
        return jsonify({
            'hostname': os.uname().nodename,
            'os': f"{os.uname().sysname} {os.uname().release}",
            'uptime': str(uptime).split('.')[0],  # Remove microseconds
            'processes': len(psutil.pids()),
            'connections': len(psutil.net_connections())
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/logs')
def view_logs():
    """View recent log entries"""
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'rb') as f:
                f.seek(0, 2)
                file_size = f.tell()
                read_size = min(20480, file_size)  # Read last 20KB
                f.seek(max(0, file_size - read_size))
                content = f.read().decode('utf-8', errors='ignore')
            return render_template('logs.html', log_content=content)
        else:
            return render_template('logs.html', log_content="🔍 No logs available yet. Start the main McGuardian Elite engine to generate security logs.")
    except Exception as e:
        return render_template('logs.html', log_content=f"❌ Error reading logs: {e}")

@app.route('/download_logs')
def download_logs():
    """Download log files"""
    try:
        return send_file(LOG_FILE, as_attachment=True, download_name='mcguardian_logs.txt')
    except:
        return "❌ Log file not found", 404

# ═══════════════════════════════════════════════════════════════════════════════
#                           OPTIMIZED TEMPLATE CREATION
# ═══════════════════════════════════════════════════════════════════════════════

def create_optimized_templates():
    """Create high-performance dark mode templates"""
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    # ═══════════════════════════════════════════════════════════════════════════
    #                        MAIN DASHBOARD TEMPLATE
    # ═══════════════════════════════════════════════════════════════════════════
    
    dashboard_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🛡️ McGuardian Elite - Security Command Center</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.min.js"></script>
    <style>
        /* 
        ███╗   ███╗ ██████╗ ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗ ██╗ █████╗ ███╗   
        ████╗ ████║██╔════╝██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗██║██╔══██╗████╗  
        ██╔████╔██║██║     ██║  ███╗██║   ██║███████║██████╔╝██║  ██║██║███████║██╔██╗ 
        ██║╚██╔╝██║██║     ██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║██║██╔══██║██║╚██╗
        ██║ ╚═╝ ██║╚██████╗╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝██║██║  ██║██║ ╚██
        ╚═╝     ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝   
                           ELITE DARK MODE OPTIMIZED STYLING
        */
        
        :root {
            /* Dark Theme Colors */
            --bg-primary: #000000;
            --bg-secondary: #0d1117;
            --bg-tertiary: #161b22;
            --bg-card: #21262d;
            --bg-hover: #30363d;
            
            /* Accent Colors */
            --accent-blue: #58a6ff;
            --accent-green: #3fb950;
            --accent-yellow: #d29922;
            --accent-orange: #f85149;
            --accent-red: #da3633;
            --accent-purple: #bc8cff;
            
            /* Text Colors */
            --text-primary: #f0f6fc;
            --text-secondary: #8b949e;
            --text-tertiary: #6e7681;
            
            /* UI Elements */
            --border-color: #30363d;
            --shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
            --glow: 0 0 20px rgba(88, 166, 255, 0.3);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif;
            background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 50%, var(--bg-primary) 100%);
            color: var(--text-primary);
            min-height: 100vh;
            line-height: 1.6;
            overflow-x: hidden;
        }

        /* Optimized Container */
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            will-change: transform;
        }

        /* Header Styling */
        .header {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            text-align: center;
            box-shadow: var(--shadow);
            backdrop-filter: blur(10px);
        }

        .header h1 {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }

        .header .subtitle {
            color: var(--text-secondary);
            font-size: 1.1rem;
            font-weight: 400;
        }

        /* Navigation */
        .nav-pills {
            display: flex;
            justify-content: center;
            gap: 12px;
            margin-top: 20px;
            flex-wrap: wrap;
        }

        .nav-pill {
            padding: 10px 20px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            color: var(--text-primary);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .nav-pill:hover {
            background: var(--bg-hover);
            border-color: var(--accent-blue);
            transform: translateY(-1px);
            box-shadow: var(--glow);
        }

        /* Status Grid - Optimized */
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 24px;
        }

        .status-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 24px;
            transition: all 0.2s ease;
            box-shadow: var(--shadow);
        }

        .status-card:hover {
            border-color: var(--accent-blue);
            transform: translateY(-2px);
            box-shadow: var(--glow);
        }

        .status-card h3 {
            color: var(--accent-blue);
            margin-bottom: 12px;
            font-size: 1.2rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .status-value {
            font-size: 2rem;
            font-weight: 700;
            margin: 12px 0;
            color: var(--text-primary);
        }

        /* Threat Levels */
        .threat-level {
            padding: 6px 12px;
            border-radius: 16px;
            font-weight: 600;
            text-align: center;
            margin: 6px 0;
            font-size: 0.9rem;
        }

        .critical { 
            background: var(--accent-red);
            color: white;
            animation: pulse-red 2s infinite;
        }

        .high { 
            background: var(--accent-orange);
            color: white;
        }

        .medium { 
            background: var(--accent-yellow);
            color: black;
        }

        .low { 
            background: var(--accent-blue);
            color: white;
        }

        .info { 
            background: var(--accent-green);
            color: white;
        }

        @keyframes pulse-red {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }

        /* Events Section - Optimized */
        .events-section {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: var(--shadow);
        }

        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
            gap: 12px;
        }

        .section-title {
            font-size: 1.5rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .refresh-btn {
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            border: none;
            padding: 10px 20px;
            border-radius: 20px;
            color: white;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 12px rgba(88, 166, 255, 0.3);
        }

        .refresh-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 16px rgba(88, 166, 255, 0.4);
        }

        .refresh-btn:active {
            transform: scale(0.98);
        }

        /* Events Container - Optimized Scrolling */
        .events-container {
            max-height: 400px;
            overflow-y: auto;
            scrollbar-width: thin;
            scrollbar-color: var(--accent-blue) transparent;
        }

        .events-container::-webkit-scrollbar {
            width: 8px;
        }

        .events-container::-webkit-scrollbar-track {
            background: transparent;
        }

        .events-container::-webkit-scrollbar-thumb {
            background: var(--accent-blue);
            border-radius: 4px;
        }

        .event-item {
            background: var(--bg-tertiary);
            margin: 12px 0;
            padding: 16px;
            border-radius: 8px;
            border-left: 4px solid var(--accent-blue);
            transition: all 0.2s ease;
        }

        .event-item:hover {
            background: var(--bg-hover);
            transform: translateX(4px);
        }

        .event-timestamp {
            color: var(--text-tertiary);
            font-size: 0.85rem;
            margin-bottom: 6px;
            font-family: 'Courier New', monospace;
        }

        .event-content {
            color: var(--text-secondary);
            line-height: 1.5;
            font-size: 0.9rem;
            white-space: pre-line;
        }

        /* Charts Section */
        .charts-section {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 24px;
        }

        .chart-container {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            height: 300px;
            box-shadow: var(--shadow);
        }

        .chart-container h3 {
            color: var(--text-primary);
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* Loading Animation */
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 2px solid var(--border-color);
            border-radius: 50%;
            border-top-color: var(--accent-blue);
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        /* System Info */
        .system-info {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 24px;
            box-shadow: var(--shadow);
        }

        .system-info h3 {
            color: var(--accent-green);
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
        }

        .info-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid var(--border-color);
        }

        .info-label {
            color: var(--text-secondary);
            font-weight: 500;
        }

        .info-value {
            color: var(--text-primary);
            font-weight: 600;
        }

        /* Mobile Responsiveness */
        @media (max-width: 768px) {
            .container {
                padding: 12px;
            }

            .header h1 {
                font-size: 2rem;
            }

            .status-grid {
                grid-template-columns: 1fr;
            }

            .charts-section {
                grid-template-columns: 1fr;
            }

            .section-header {
                flex-direction: column;
                align-items: stretch;
            }

            .nav-pills {
                flex-direction: column;
                align-items: center;
            }
        }

        /* High Performance Optimizations */
        .gpu-accelerated {
            will-change: transform;
            transform: translateZ(0);
        }

        /* Status Indicators */
        .status-indicator {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }

        .status-online {
            background: var(--accent-green);
        }

        .status-warning {
            background: var(--accent-yellow);
        }

        .status-critical {
            background: var(--accent-red);
        }

        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 currentColor; }
            70% { box-shadow: 0 0 0 8px transparent; }
            100% { box-shadow: 0 0 0 0 transparent; }
        }

        /* Performance Meters */
        .performance-meter {
            width: 100%;
            height: 8px;
            background: var(--bg-tertiary);
            border-radius: 4px;
            overflow: hidden;
            margin-top: 8px;
        }

        .performance-bar {
            height: 100%;
            transition: width 0.3s ease;
            border-radius: 4px;
        }

        .perf-low { background: var(--accent-green); }
        .perf-medium { background: var(--accent-yellow); }
        .perf-high { background: var(--accent-orange); }
        .perf-critical { background: var(--accent-red); }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header Section -->
        <div class="header gpu-accelerated">
            <h1><i class="fas fa-shield-alt"></i> McGuardian Elite</h1>
            <p class="subtitle">🛡️ Advanced AI-Powered Security Monitoring & Threat Response</p>
            <div class="nav-pills">
                <a href="/" class="nav-pill">
                    <i class="fas fa-tachometer-alt"></i>
                    Dashboard
                </a>
                <a href="/logs" class="nav-pill">
                    <i class="fas fa-file-alt"></i>
                    Security Logs
                </a>
                <a href="/download_logs" class="nav-pill">
                    <i class="fas fa-download"></i>
                    Export Data
                </a>
            </div>
        </div>
        
        <!-- System Information -->
        <div class="system-info gpu-accelerated">
            <h3><i class="fas fa-server"></i> System Information</h3>
            <div class="info-grid" id="system-info">
                <div class="loading"></div>
            </div>
        </div>
        
        <!-- Status Grid -->
        <div class="status-grid">
            <div class="status-card gpu-accelerated">
                <h3><i class="fas fa-heartbeat"></i>System Status</h3>
                <div id="system-status" class="status-value">
                    <div class="loading"></div>
                </div>
                <button class="refresh-btn" onclick="refreshData()">
                    <i class="fas fa-sync-alt"></i>
                    Refresh
                </button>
            </div>
            
            <div class="status-card gpu-accelerated">
                <h3><i class="fas fa-exclamation-triangle"></i>Threat Analysis</h3>
                <div id="threat-stats" class="status-value">
                    <div class="loading"></div>
                </div>
            </div>
            
            <div class="status-card gpu-accelerated">
                <h3><i class="fas fa-chart-line"></i>System Performance</h3>
                <div id="performance-stats">
                    <div class="loading"></div>
                </div>
            </div>
            
            <div class="status-card gpu-accelerated">
                <h3><i class="fas fa-clock"></i>Security Events</h3>
                <div id="total-events" class="status-value">
                    <div class="loading"></div>
                </div>
            </div>
        </div>
        
        <!-- Charts Section -->
        <div class="charts-section">
            <div class="chart-container gpu-accelerated">
                <h3><i class="fas fa-chart-pie"></i> Threat Distribution</h3>
                <canvas id="threatChart"></canvas>
            </div>
            
            <div class="chart-container gpu-accelerated">
                <h3><i class="fas fa-chart-area"></i> System Performance</h3>
                <canvas id="performanceChart"></canvas>
            </div>
        </div>
        
        <!-- Events Section -->
        <div class="events-section gpu-accelerated">
            <div class="section-header">
                <h2 class="section-title">
                    <i class="fas fa-search"></i>
                    Real-time Security Events
                </h2>
                <button class="refresh-btn" onclick="refreshEvents()">
                    <i class="fas fa-sync-alt"></i>
                    Live Feed
                </button>
            </div>
            
            <div class="events-container" id="recent-events">
                <div class="loading"></div>
            </div>
        </div>
    </div>
    
    <script>
        /*
        ███╗   ███╗ ██████╗ ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗ ██╗ █████╗ ███╗   
        ████╗ ████║██╔════╝██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗██║██╔══██╗████╗  
        ██╔████╔██║██║     ██║  ███╗██║   ██║███████║██████╔╝██║  ██║██║███████║██╔██╗ 
        ██║╚██╔╝██║██║     ██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║██║██╔══██║██║╚██╗
        ██║ ╚═╝ ██║╚██████╗╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝██║██║  ██║██║ ╚██
        ╚═╝     ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝   
                                    OPTIMIZED JAVASCRIPT
        */
        
        // Chart instances
        let threatChart, performanceChart;
        
        // Performance optimization - debounced updates
        let updateTimeout;
        const UPDATE_INTERVAL = 15000; // 15 seconds for better performance
        
        function initCharts() {
            // Threat Distribution Chart
            const threatCtx = document.getElementById('threatChart').getContext('2d');
            threatChart = new Chart(threatCtx, {
                type: 'doughnut',
                data: {
                    labels: ['Critical', 'High', 'Medium', 'Low', 'Info'],
                    datasets: [{
                        data: [0, 0, 0, 0, 0],
                        backgroundColor: [
                            '#da3633',
                            '#f85149', 
                            '#d29922',
                            '#58a6ff',
                            '#3fb950'
                        ],
                        borderWidth: 0,
                        hoverOffset: 8
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                color: '#f0f6fc',
                                usePointStyle: true,
                                padding: 16,
                                font: { size: 12 }
                            }
                        }
                    },
                    animation: {
                        duration: 300 // Faster animations
                    }
                }
            });
            
            // Performance Chart
            const perfCtx = document.getElementById('performanceChart').getContext('2d');
            performanceChart = new Chart(perfCtx, {
                type: 'bar',
                data: {
                    labels: ['CPU', 'Memory', 'Disk'],
                    datasets: [{
                        label: 'Usage %',
                        data: [0, 0, 0],
                        backgroundColor: [
                            '#58a6ff',
                            '#3fb950',
                            '#d29922'
                        ],
                        borderWidth: 0,
                        borderRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100,
                            ticks: { 
                                color: '#8b949e',
                                callback: value => value + '%'
                            },
                            grid: { color: '#30363d' }
                        },
                        x: {
                            ticks: { color: '#8b949e' },
                            grid: { color: '#30363d' }
                        }
                    },
                    animation: {
                        duration: 300
                    }
                }
            });
        }
        
        // Optimized refresh with error handling
        async function refreshData() {
            const refreshBtn = document.querySelector('.refresh-btn');
            refreshBtn.classList.add('loading');
            
            try {
                // Fetch all data concurrently for better performance
                const [statusResponse, systemResponse] = await Promise.all([
                    fetch('/api/status'),
                    fetch('/api/system_info')
                ]);
                
                const statusData = await statusResponse.json();
                const systemData = await systemResponse.json();
                
                // Update system status
                updateSystemStatus(statusData);
                
                // Update system information
                updateSystemInfo(systemData);
                
                // Update charts
                updateCharts(statusData);
                
            } catch (error) {
                console.error('❌ Error refreshing data:', error);
                showError('Failed to refresh data. Check if McGuardian Elite engine is running.');
            } finally {
                refreshBtn.classList.remove('loading');
            }
        }
        
        function updateSystemStatus(data) {
            const statusElement = document.getElementById('system-status');
            let statusClass = 'info';
            let indicatorClass = 'status-online';
            
            if (data.status.includes('CRITICAL') || data.status.includes('🔴')) {
                statusClass = 'critical';
                indicatorClass = 'status-critical';
            } else if (data.status.includes('HIGH') || data.status.includes('🟠')) {
                statusClass = 'high';
                indicatorClass = 'status-warning';
            } else if (data.status.includes('ELEVATED') || data.status.includes('🟡')) {
                statusClass = 'medium';
                indicatorClass = 'status-warning';
            }
            
            statusElement.innerHTML = `
                <div class="threat-level ${statusClass}">
                    <span class="status-indicator ${indicatorClass}"></span>
                    ${data.status}
                </div>
            `;
            
            // Update threat stats
            updateThreatStats(data.threat_stats);
            
            // Update event count
            document.getElementById('total-events').innerHTML = `
                <span style="color: var(--accent-blue);">${data.total_events}</span>
                <small style="color: var(--text-secondary); display: block;">Events Today</small>
            `;
            
            // Update performance stats
            if (data.system_performance) {
                updatePerformanceStats(data.system_performance);
            }
        }
        
        function updateThreatStats(stats) {
            let statsHtml = '';
            
            Object.entries(stats).forEach(([level, count]) => {
                if (count > 0) {
                    statsHtml += `<div class="threat-level ${level.toLowerCase()}">${level}: ${count}</div>`;
                }
            });
            
            document.getElementById('threat-stats').innerHTML = 
                statsHtml || '<div class="threat-level info">No threats detected</div>';
        }
        
        function updatePerformanceStats(performance) {
            const perfElement = document.getElementById('performance-stats');
            
            perfElement.innerHTML = `
                <div class="info-item">
                    <span class="info-label">CPU Usage</span>
                    <span class="info-value">${performance.cpu.toFixed(1)}%</span>
                </div>
                <div class="performance-meter">
                    <div class="performance-bar ${getPerformanceClass(performance.cpu)}" 
                         style="width: ${performance.cpu}%"></div>
                </div>
                
                <div class="info-item">
                    <span class="info-label">Memory Usage</span>
                    <span class="info-value">${performance.memory.toFixed(1)}%</span>
                </div>
                <div class="performance-meter">
                    <div class="performance-bar ${getPerformanceClass(performance.memory)}" 
                         style="width: ${performance.memory}%"></div>
                </div>
                
                <div class="info-item">
                    <span class="info-label">Disk Usage</span>
                    <span class="info-value">${performance.disk.toFixed(1)}%</span>
                </div>
                <div class="performance-meter">
                    <div class="performance-bar ${getPerformanceClass(performance.disk)}" 
                         style="width: ${performance.disk}%"></div>
                </div>
            `;
        }
        
        function getPerformanceClass(value) {
            if (value >= 90) return 'perf-critical';
            if (value >= 70) return 'perf-high';
            if (value >= 50) return 'perf-medium';
            return 'perf-low';
        }
        
        function updateSystemInfo(data) {
            const systemElement = document.getElementById('system-info');
            
            if (data.error) {
                systemElement.innerHTML = `<div class="info-item">Error: ${data.error}</div>`;
                return;
            }
            
            systemElement.innerHTML = `
                <div class="info-item">
                    <span class="info-label">Hostname</span>
                    <span class="info-value">${data.hostname || 'Unknown'}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Operating System</span>
                    <span class="info-value">${data.os || 'Unknown'}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">System Uptime</span>
                    <span class="info-value">${data.uptime || 'Unknown'}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Active Processes</span>
                    <span class="info-value">${data.processes || 0}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Network Connections</span>
                    <span class="info-value">${data.connections || 0}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Last Update</span>
                    <span class="info-value">${new Date().toLocaleTimeString()}</span>
                </div>
            `;
        }
        
        function updateCharts(data) {
            if (threatChart && data.threat_stats) {
                const chartData = [
                    data.threat_stats.CRITICAL || 0,
                    data.threat_stats.HIGH || 0,
                    data.threat_stats.MEDIUM || 0,
                    data.threat_stats.LOW || 0,
                    data.threat_stats.INFO || 0
                ];
                
                threatChart.data.datasets[0].data = chartData;
                threatChart.update('none'); // No animation for better performance
            }
            
            if (performanceChart && data.system_performance) {
                const perfData = [
                    data.system_performance.cpu,
                    data.system_performance.memory,
                    data.system_performance.disk
                ];
                
                performanceChart.data.datasets[0].data = perfData;
                performanceChart.update('none');
            }
        }
        
        // Optimized event refresh
        async function refreshEvents() {
            try {
                const response = await fetch('/api/events?limit=20');
                const data = await response.json();
                
                const eventsHtml = data.events.map(event => {
                    const riskClass = event.risk_level.toLowerCase();
                    return `
                        <div class="event-item gpu-accelerated">
                            <div class="event-timestamp">
                                <i class="fas fa-clock"></i> ${event.timestamp}
                            </div>
                            <div class="threat-level ${riskClass}">
                                ${event.risk_level}
                            </div>
                            <div class="event-content">${event.content.substring(0, 300)}${event.content.length > 300 ? '...' : ''}</div>
                        </div>
                    `;
                }).join('');
                
                document.getElementById('recent-events').innerHTML = 
                    eventsHtml || '<div class="event-item"><div class="event-content">🔍 No recent events. System is monitoring...</div></div>';
                
            } catch (error) {
                console.error('❌ Error refreshing events:', error);
                document.getElementById('recent-events').innerHTML = 
                    '<div class="event-item"><div class="event-content">❌ Error loading events. Check if McGuardian Elite engine is running.</div></div>';
            }
        }
        
        function showError(message) {
            const errorDiv = document.createElement('div');
            errorDiv.innerHTML = `
                <div style="background: var(--accent-red); color: white; padding: 12px; border-radius: 8px; margin: 12px 0;">
                    <i class="fas fa-exclamation-triangle"></i> ${message}
                </div>
            `;
            document.querySelector('.container').prepend(errorDiv);
            
            setTimeout(() => errorDiv.remove(), 5000);
        }
        
        // Initialize everything when page loads
        document.addEventListener('DOMContentLoaded', function() {
            console.log('🛡️ McGuardian Elite Dashboard Initializing...');
            
            initCharts();
            refreshData();
            refreshEvents();
            
            // Optimized auto-refresh - less frequent for better performance
            setInterval(() => {
                refreshData();
                refreshEvents();
            }, UPDATE_INTERVAL);
            
            console.log('✅ Dashboard initialized successfully');
        });
        
        // Performance monitoring
        if ('performance' in window) {
            window.addEventListener('load', () => {
                const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
                console.log(`⚡ Dashboard loaded in ${loadTime}ms`);
            });
        }
    </script>
</body>
</html>'''
    
    # ═══════════════════════════════════════════════════════════════════════════
    #                             LOGS TEMPLATE
    # ═══════════════════════════════════════════════════════════════════════════
    
    logs_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🛡️ McGuardian Elite - Security Logs</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        /*
        ███╗   ███╗ ██████╗ ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗ ██╗ █████╗ ███╗   
        ████╗ ████║██╔════╝██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗██║██╔══██╗████╗  
        ██╔████╔██║██║     ██║  ███╗██║   ██║███████║██████╔╝██║  ██║██║███████║██╔██╗ 
        ██║╚██╔╝██║██║     ██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║██║██╔══██║██║╚██╗
        ██║ ╚═╝ ██║╚██████╗╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝██║██║  ██║██║ ╚██
        ╚═╝     ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝   
                                 SECURITY LOGS VIEWER
        */
        
        :root {
            --bg-primary: #000000;
            --bg-secondary: #0d1117;
            --bg-tertiary: #161b22;
            --bg-card: #21262d;
            --accent-green: #3fb950;
            --accent-blue: #58a6ff;
            --text-primary: #f0f6fc;
            --text-secondary: #8b949e;
            --border-color: #30363d;
            --shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 50%, var(--bg-primary) 100%);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            text-align: center;
            margin-bottom: 24px;
            padding: 24px;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            box-shadow: var(--shadow);
        }

        .header h1 {
            color: var(--accent-blue);
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 12px;
        }

        .nav-menu {
            display: flex;
            justify-content: center;
            gap: 12px;
            margin-top: 16px;
            flex-wrap: wrap;
        }

        .nav-menu a {
            color: var(--accent-blue);
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 20px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .nav-menu a:hover {
            background: var(--accent-blue);
            color: white;
            transform: translateY(-1px);
        }

        .logs-container {
            background: #0a0a0a;
            border-radius: 12px;
            padding: 0;
            max-height: 80vh;
            overflow: hidden;
            border: 1px solid var(--border-color);
            box-shadow: var(--shadow);
            position: relative;
        }

        .terminal-header {
            background: var(--bg-card);
            padding: 12px 20px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .terminal-button {
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }

        .btn-close { background: #ff5f57; }
        .btn-minimize { background: #ffbd2e; }
        .btn-maximize { background: #28ca42; }

        .terminal-title {
            color: var(--text-secondary);
            font-size: 0.9rem;
            margin-left: auto;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .log-content-container {
            height: calc(80vh - 60px);
            overflow-y: auto;
            padding: 20px;
            scrollbar-width: thin;
            scrollbar-color: var(--accent-green) transparent;
        }

        .log-content-container::-webkit-scrollbar {
            width: 10px;
        }

        .log-content-container::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 5px;
        }

        .log-content-container::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-green));
            border-radius: 5px;
        }

        .log-content {
            font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Courier New', monospace;
            font-size: 0.85rem;
            white-space: pre-wrap;
            color: var(--accent-green);
            text-shadow: 0 0 3px rgba(63, 185, 80, 0.3);
            line-height: 1.6;
        }

        @media (max-width: 768px) {
            .container {
                padding: 12px;
            }

            .header h1 {
                font-size: 1.8rem;
            }

            .nav-menu {
                flex-direction: column;
                align-items: center;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-terminal"></i> McGuardian Elite - Security Terminal</h1>
            <div class="nav-menu">
                <a href="/"><i class="fas fa-tachometer-alt"></i> Dashboard</a>
                <a href="/logs"><i class="fas fa-file-alt"></i> View Logs</a>
                <a href="/download_logs"><i class="fas fa-download"></i> Download Logs</a>
            </div>
        </div>
        
        <div class="logs-container">
            <div class="terminal-header">
                <div class="terminal-button btn-close"></div>
                <div class="terminal-button btn-minimize"></div>
                <div class="terminal-button btn-maximize"></div>
                <div class="terminal-title">
                    <i class="fas fa-shield-alt"></i>
                    McGuardian Elite Security Terminal
                </div>
            </div>
            <div class="log-content-container">
                <div class="log-content">{{ log_content }}</div>
            </div>
        </div>
    </div>
</body>
</html>'''
    
    # Write templates
    with open(os.path.join(templates_dir, 'dashboard.html'), 'w') as f:
        f.write(dashboard_html)
    
    with open(os.path.join(templates_dir, 'logs.html'), 'w') as f:
        f.write(logs_html)

# ═══════════════════════════════════════════════════════════════════════════════
#                              MAIN FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def run_dashboard():
    """Run the optimized dashboard server"""
    create_optimized_templates()
    
    print("""
███╗   ███╗ ██████╗ ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗ ██╗ █████╗ ███╗   ██╗
████╗ ████║██╔════╝██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗██║██╔══██╗████╗  ██║
██╔████╔██║██║     ██║  ███╗██║   ██║███████║██████╔╝██║  ██║██║███████║██╔██╗ ██║
██║╚██╔╝██║██║     ██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║██║██╔══██║██║╚██╗██║
██║ ╚═╝ ██║╚██████╗╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝██║██║  ██║██║ ╚████║
╚═╝     ╚═╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
                            
                        E L I T E   W E B   D A S H B O A R D
                          🌐 Starting Optimized Dark Mode GUI
""")
    
    print("🚀 McGuardian Elite Web Dashboard Starting...")
    print("📊 Dashboard Features:")
    print("   • ⚡ High-performance optimized rendering")
    print("   • 🌙 Pure dark mode interface") 
    print("   • 📱 Fully responsive design")
    print("   • 🔄 Real-time data updates (15s intervals)")
    print("   • 📈 Interactive charts and visualizations")
    print("   • 🛡️ Advanced threat intelligence display")
    print()
    print("🌐 Dashboard will be available at: http://localhost:5000")
    print("🔒 Advanced security monitoring with Apple-inspired design")
    print()
    
    # Run Flask app with optimized settings
    app.run(
        host='127.0.0.1', 
        port=5000, 
        debug=False, 
        threaded=True,
        use_reloader=False  # Disable for better performance
    )

def check_installation():
    """Verify McGuardian Elite is properly installed"""
    if not os.path.exists(BASE_DIR):
        print("""
❌ McGuardian Elite Engine Not Found!

🔧 Installation Required:
   The main McGuardian Elite security engine is not installed or not running.
   
📋 Next Steps:
   1. Install McGuardian Elite: python3 mcguardian_installer.py
   2. Start the engine: mcguardian_elite
   3. Then launch this dashboard: mcguardian_dashboard

💡 Quick Install:
   curl -sSL https://raw.githubusercontent.com/heyfinal/McGuardian/main/install.sh | bash
""")
        sys.exit(1)
    
    # Check if main engine is running
    try:
        if os.path.exists(LOG_FILE):
            log_mtime = os.path.getmtime(LOG_FILE)
            if time.time() - log_mtime > 300:  # 5 minutes
                print("⚠️  Warning: McGuardian Elite engine may not be running")
                print("💡 Start the main engine: mcguardian_elite")
                print("   The dashboard will still work but with limited data")
                print()
    except:
        pass

if __name__ == '__main__':
    try:
        # Verify installation before starting dashboard
        check_installation()
        
        # Start the optimized dashboard
        run_dashboard()
        
    except KeyboardInterrupt:
        print("\n🛑 Dashboard shutdown requested")
        print("✅ McGuardian Elite Dashboard stopped safely")
    except Exception as e:
        print(f"\n❌ Dashboard Error: {e}")
        print("💡 Try restarting with: python3 mcguardian_gui.py")
