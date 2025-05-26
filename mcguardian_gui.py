#!/usr/bin/env python3
"""
McGuardian Elite Web Dashboard v1.0.0
Real-time security monitoring dashboard with threat intelligence visualization
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

# Configuration - adjust paths to match main application
BASE_DIR = os.path.expanduser('~/Library/Logs/McGuardianElite')
DB_FILE = os.path.join(BASE_DIR, 'analytics', 'threat_intelligence.db')
LOG_FILE = os.path.join(BASE_DIR, 'human_readable', 'security_explained.log')
ALERTS_FILE = os.path.join(BASE_DIR, 'human_readable', 'critical_alerts.log')

app = Flask(__name__)
app.secret_key = 'mcguardian_elite_dashboard_2024'

class DashboardData:
    def __init__(self):
        self.recent_events = []
        self.threat_stats = {'high': 0, 'medium': 0, 'low': 0}
        self.attack_scenarios = []
        self.system_status = 'MONITORING'
        
    def update_data(self):
        """Update dashboard data from logs and database"""
        try:
            # Read recent events from log
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, 'r') as f:
                    lines = f.readlines()[-50:]  # Last 50 lines
                    self.recent_events = self.parse_log_entries(lines)
            
            # Update threat statistics
            self.update_threat_stats()
            
            # Check system status
            self.update_system_status()
            
        except Exception as e:
            print(f"Error updating dashboard data: {e}")
    
    def parse_log_entries(self, lines):
        """Parse log entries for display"""
        events = []
        current_event = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check for timestamp at start of entry
            if line.startswith('2024') or line.startswith('2025'):
                if current_event:
                    events.append(current_event)
                
                current_event = {
                    'timestamp': line.split('\n')[0],
                    'content': '',
                    'risk_level': 'INFO',
                    'type': 'file_event'
                }
            elif current_event:
                current_event['content'] += line + '\n'
                
                # Determine risk level from content
                if '🔴 CRITICAL' in line or 'CRITICAL' in line:
                    current_event['risk_level'] = 'CRITICAL'
                    current_event['type'] = 'critical_alert'
                elif '🟠 HIGH' in line or 'HIGH RISK' in line:
                    current_event['risk_level'] = 'HIGH'
                elif '🟡 MEDIUM' in line or 'MEDIUM RISK' in line:
                    current_event['risk_level'] = 'MEDIUM'
                elif '🟢 LOW' in line or 'LOW RISK' in line:
                    current_event['risk_level'] = 'LOW'
        
        if current_event:
            events.append(current_event)
            
        return events[-20:]  # Return last 20 events
    
    def update_threat_stats(self):
        """Update threat level statistics"""
        self.threat_stats = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'INFO': 0}
        
        for event in self.recent_events:
            level = event.get('risk_level', 'INFO')
            self.threat_stats[level] = self.threat_stats.get(level, 0) + 1
    
    def update_system_status(self):
        """Update overall system status"""
        if self.threat_stats.get('CRITICAL', 0) > 0:
            self.system_status = 'CRITICAL THREATS DETECTED'
        elif self.threat_stats.get('HIGH', 0) > 0:
            self.system_status = 'HIGH RISK ACTIVITY'
        elif self.threat_stats.get('MEDIUM', 0) > 5:
            self.system_status = 'ELEVATED RISK'
        else:
            self.system_status = 'MONITORING - NORMAL'

dashboard_data = DashboardData()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/status')
def api_status():
    """Get current system status"""
    dashboard_data.update_data()
    return jsonify({
        'status': dashboard_data.system_status,
        'threat_stats': dashboard_data.threat_stats,
        'total_events': len(dashboard_data.recent_events),
        'last_update': datetime.now().isoformat()
    })

@app.route('/api/events')
def api_events():
    """Get recent security events"""
    dashboard_data.update_data()
    return jsonify({
        'events': dashboard_data.recent_events,
        'count': len(dashboard_data.recent_events)
    })

@app.route('/api/alerts')
def api_alerts():
    """Get critical alerts"""
    try:
        alerts = []
        if os.path.exists(ALERTS_FILE):
            with open(ALERTS_FILE, 'r') as f:
                content = f.read()
                # Parse alerts from the file
                alert_sections = content.split('=' * 100)
                for section in alert_sections[-10:]:  # Last 10 alerts
                    if section.strip():
                        alerts.append({
                            'content': section.strip(),
                            'timestamp': datetime.now().isoformat()
                        })
        
        return jsonify({'alerts': alerts})
    except Exception as e:
        return jsonify({'error': str(e), 'alerts': []})

@app.route('/api/threat_intel/<tool_name>')
def api_threat_intel(tool_name):
    """Get threat intelligence for specific tool"""
    # This would connect to the threat intelligence system
    threat_intel = {
        'nmap': {
            'name': 'Network Mapper (Nmap)',
            'category': 'Network Scanner', 
            'risk_level': 'HIGH',
            'description': 'Powerful network discovery and security auditing tool used for reconnaissance',
            'countermeasures': ['Block scanning attempts', 'Monitor for port scan patterns', 'Use IDS']
        },
        'nc': {
            'name': 'Netcat',
            'category': 'Network Utility/Backdoor',
            'risk_level': 'CRITICAL', 
            'description': 'Swiss Army knife of networking, often used for reverse shells',
            'countermeasures': ['Block netcat traffic', 'Monitor network connections', 'Use application whitelisting']
        }
    }
    
    return jsonify(threat_intel.get(tool_name, {'error': 'Tool not found'}))

@app.route('/logs')
def view_logs():
    """View recent log entries"""
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                content = f.read()[-10000:]  # Last 10KB
            return render_template('logs.html', log_content=content)
        else:
            return render_template('logs.html', log_content="No logs available")
    except Exception as e:
        return render_template('logs.html', log_content=f"Error reading logs: {e}")

@app.route('/download_logs')
def download_logs():
    """Download log files"""
    try:
        return send_file(LOG_FILE, as_attachment=True, download_name='mcguardian_logs.txt')
    except:
        return "Log file not found", 404

def create_templates():
    """Create stunning Apple-inspired HTML templates"""
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    # Main dashboard template with cutting-edge design
    dashboard_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>McGuardian Elite - Security Command Center</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        :root {
            --primary-bg: #000000;
            --secondary-bg: #1d1d1f;
            --tertiary-bg: #2d2d30;
            --accent-blue: #007aff;
            --accent-purple: #af52de;
            --accent-green: #30d158;
            --accent-orange: #ff9f0a;
            --accent-red: #ff453a;
            --text-primary: #ffffff;
            --text-secondary: #a1a1a6;
            --text-tertiary: #636366;
            --glass-bg: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1);
            --shadow-light: rgba(255, 255, 255, 0.1);
            --shadow-dark: rgba(0, 0, 0, 0.3);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@100;200;300;400;500;600;700;800;900&display=swap');

        body {
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #000000 0%, #1a1a1a 25%, #2d2d30 50%, #1a1a1a 75%, #000000 100%);
            background-size: 400% 400%;
            animation: gradientShift 20s ease infinite;
            color: var(--text-primary);
            min-height: 100vh;
            overflow-x: hidden;
            position: relative;
        }

        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Particle System Background */
        #particles-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            opacity: 0.3;
        }

        /* Glassmorphism Container */
        .glass-container {
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            position: relative;
            overflow: hidden;
        }

        .glass-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--shadow-light), transparent);
        }

        /* Main Layout */
        .container {
            max-width: 1600px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 1;
        }

        /* Header with Apple-style navigation */
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding: 30px;
            position: relative;
        }

        .header .glass-container {
            padding: 30px;
            background: linear-gradient(135deg, var(--glass-bg), rgba(0, 122, 255, 0.1));
        }

        .header h1 {
            font-size: 3.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
            animation: titlePulse 3s ease-in-out infinite;
        }

        @keyframes titlePulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.02); }
        }

        .header .subtitle {
            font-size: 1.2rem;
            color: var(--text-secondary);
            font-weight: 300;
            margin-bottom: 20px;
        }

        /* Navigation Pills */
        .nav-pills {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 20px;
        }

        .nav-pill {
            padding: 12px 24px;
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 25px;
            color: var(--text-primary);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
        }

        .nav-pill::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, var(--shadow-light), transparent);
            transition: left 0.5s;
        }

        .nav-pill:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 122, 255, 0.3);
            border-color: var(--accent-blue);
        }

        .nav-pill:hover::before {
            left: 100%;
        }

        /* Status Grid with Advanced Cards */
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }

        .status-card {
            padding: 30px;
            position: relative;
            transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            cursor: pointer;
        }

        .status-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }

        .status-card h3 {
            color: var(--accent-blue);
            margin-bottom: 15px;
            font-size: 1.4rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .status-card .icon {
            font-size: 1.6rem;
            animation: iconFloat 3s ease-in-out infinite;
        }

        @keyframes iconFloat {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-3px); }
        }

        .status-value {
            font-size: 2.5rem;
            font-weight: 700;
            margin: 15px 0;
            background: linear-gradient(135deg, var(--text-primary), var(--text-secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Threat Level Indicators */
        .threat-level {
            padding: 8px 16px;
            border-radius: 15px;
            font-weight: 600;
            text-align: center;
            margin: 8px 0;
            position: relative;
            overflow: hidden;
            animation: levelPulse 2s ease-in-out infinite;
        }

        @keyframes levelPulse {
            0%, 100% { box-shadow: 0 0 0 0 currentColor; }
            50% { box-shadow: 0 0 0 8px transparent; }
        }

        .critical { 
            background: linear-gradient(135deg, var(--accent-red), #ff6b6b);
            color: white;
            animation: criticalAlert 1s ease-in-out infinite alternate;
        }

        @keyframes criticalAlert {
            0% { opacity: 1; }
            100% { opacity: 0.7; }
        }

        .high { 
            background: linear-gradient(135deg, var(--accent-orange), #ffb347);
            color: white;
        }

        .medium { 
            background: linear-gradient(135deg, #ffd60a, #ffbe0b);
            color: black;
        }

        .low { 
            background: linear-gradient(135deg, var(--accent-blue), #74c0fc);
            color: white;
        }

        .info { 
            background: linear-gradient(135deg, var(--accent-green), #51cf66);
            color: white;
        }

        /* Advanced Events Section */
        .events-section {
            margin-bottom: 40px;
            position: relative;
        }

        .events-section .glass-container {
            padding: 30px;
        }

        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
        }

        .section-title {
            font-size: 2rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .refresh-btn {
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            color: white;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 15px rgba(0, 122, 255, 0.3);
        }

        .refresh-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 20px rgba(0, 122, 255, 0.4);
        }

        .refresh-btn:active {
            transform: scale(0.98);
        }

        .refresh-btn .icon {
            animation: spin 2s linear infinite paused;
        }

        .refresh-btn.loading .icon {
            animation-play-state: running;
        }

        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        /* Event Items with Advanced Styling */
        .events-container {
            max-height: 500px;
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
            background: linear-gradient(135deg, var(--tertiary-bg), rgba(45, 45, 48, 0.5));
            margin: 15px 0;
            padding: 20px;
            border-radius: 15px;
            border-left: 4px solid var(--accent-blue);
            position: relative;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }

        .event-item:hover {
            transform: translateX(5px);
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
        }

        .event-timestamp {
            color: var(--text-tertiary);
            font-size: 0.9rem;
            margin-bottom: 8px;
            font-weight: 500;
        }

        .event-content {
            color: var(--text-secondary);
            line-height: 1.6;
            white-space: pre-wrap;
            font-family: 'SF Mono', Monaco, monospace;
            font-size: 0.95rem;
        }

        /* Charts Section */
        .charts-section {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 25px;
            margin-bottom: 40px;
        }

        .chart-container {
            padding: 25px;
            height: 300px;
            position: relative;
        }

        /* Loading Animation */
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,.3);
            border-radius: 50%;
            border-top-color: var(--accent-blue);
            animation: spin 1s ease-in-out infinite;
        }

        /* Mobile Responsiveness */
        @media (max-width: 768px) {
            .container {
                padding: 15px;
            }

            .header h1 {
                font-size: 2.5rem;
            }

            .status-grid {
                grid-template-columns: 1fr;
            }

            .charts-section {
                grid-template-columns: 1fr;
            }

            .nav-pills {
                flex-direction: column;
                align-items: center;
            }
        }

        /* Advanced Animations */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .fade-in-up {
            animation: fadeInUp 0.6s ease-out;
        }

        /* Status Indicators */
        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }

        .status-online {
            background: var(--accent-green);
        }

        .status-warning {
            background: var(--accent-orange);
        }

        .status-critical {
            background: var(--accent-red);
        }

        @keyframes pulse {
            0% {
                box-shadow: 0 0 0 0 currentColor;
            }
            70% {
                box-shadow: 0 0 0 10px transparent;
            }
            100% {
                box-shadow: 0 0 0 0 transparent;
            }
        }

        /* Terminal-style code blocks */
        .code-block {
            background: #1a1a1a;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 15px;
            font-family: 'SF Mono', Monaco, monospace;
            font-size: 0.9rem;
            overflow-x: auto;
            margin: 10px 0;
        }

        .code-block::before {
            content: '$ ';
            color: var(--accent-green);
            font-weight: bold;
        }
    </style>
</head>
<body>
    <canvas id="particles-canvas"></canvas>
    
    <div class="container">
        <div class="header fade-in-up">
            <div class="glass-container">
                <h1><i class="fas fa-shield-alt"></i> McGuardian Elite</h1>
                <p class="subtitle">Advanced Threat Intelligence & Response System</p>
                <div class="nav-pills">
                    <a href="/" class="nav-pill">
                        <i class="fas fa-tachometer-alt"></i> Dashboard
                    </a>
                    <a href="/logs" class="nav-pill">
                        <i class="fas fa-file-alt"></i> Security Logs
                    </a>
                    <a href="/download_logs" class="nav-pill">
                        <i class="fas fa-download"></i> Export Data
                    </a>
                </div>
            </div>
        </div>
        
        <div class="status-grid">
            <div class="status-card glass-container fade-in-up">
                <h3><i class="fas fa-heartbeat icon"></i>System Status</h3>
                <div id="system-status" class="status-value">
                    <div class="loading"></div>
                </div>
                <button class="refresh-btn" onclick="refreshData()">
                    <i class="fas fa-sync-alt icon"></i>
                    <span>Refresh</span>
                </button>
            </div>
            
            <div class="status-card glass-container fade-in-up">
                <h3><i class="fas fa-exclamation-triangle icon"></i>Threat Analysis</h3>
                <div id="threat-stats" class="status-value">
                    <div class="loading"></div>
                </div>
            </div>
            
            <div class="status-card glass-container fade-in-up">
                <h3><i class="fas fa-clock icon"></i>Last Update</h3>
                <div id="last-update" class="status-value">
                    <div class="loading"></div>
                </div>
            </div>
            
            <div class="status-card glass-container fade-in-up">
                <h3><i class="fas fa-chart-line icon"></i>Event Volume</h3>
                <div id="total-events" class="status-value">
                    <div class="loading"></div>
                </div>
            </div>
        </div>
        
        <div class="charts-section">
            <div class="chart-container glass-container fade-in-up">
                <h3><i class="fas fa-chart-pie"></i> Threat Distribution</h3>
                <canvas id="threatChart"></canvas>
            </div>
            
            <div class="chart-container glass-container fade-in-up">
                <h3><i class="fas fa-chart-area"></i> Activity Timeline</h3>
                <canvas id="timelineChart"></canvas>
            </div>
        </div>
        
        <div class="events-section fade-in-up">
            <div class="glass-container">
                <div class="section-header">
                    <h2 class="section-title">
                        <i class="fas fa-search"></i>
                        Real-time Security Events
                    </h2>
                    <button class="refresh-btn" onclick="refreshEvents()">
                        <i class="fas fa-sync-alt icon"></i>
                        Live Feed
                    </button>
                </div>
                
                <div class="events-container" id="recent-events">
                    <div class="loading"></div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Particle System
        class ParticleSystem {
            constructor() {
                this.canvas = document.getElementById('particles-canvas');
                this.ctx = this.canvas.getContext('2d');
                this.particles = [];
                this.resize();
                this.createParticles();
                this.animate();
                
                window.addEventListener('resize', () => this.resize());
            }
            
            resize() {
                this.canvas.width = window.innerWidth;
                this.canvas.height = window.innerHeight;
            }
            
            createParticles() {
                for (let i = 0; i < 50; i++) {
                    this.particles.push({
                        x: Math.random() * this.canvas.width,
                        y: Math.random() * this.canvas.height,
                        vx: (Math.random() - 0.5) * 0.5,
                        vy: (Math.random() - 0.5) * 0.5,
                        size: Math.random() * 2 + 1,
                        opacity: Math.random() * 0.5 + 0.2
                    });
                }
            }
            
            animate() {
                this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
                
                this.particles.forEach(particle => {
                    particle.x += particle.vx;
                    particle.y += particle.vy;
                    
                    if (particle.x < 0 || particle.x > this.canvas.width) particle.vx *= -1;
                    if (particle.y < 0 || particle.y > this.canvas.height) particle.vy *= -1;
                    
                    this.ctx.beginPath();
                    this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
                    this.ctx.fillStyle = `rgba(0, 122, 255, ${particle.opacity})`;
                    this.ctx.fill();
                });
                
                // Draw connections
                this.particles.forEach((particle, i) => {
                    this.particles.slice(i + 1).forEach(otherParticle => {
                        const dx = particle.x - otherParticle.x;
                        const dy = particle.y - otherParticle.y;
                        const distance = Math.sqrt(dx * dx + dy * dy);
                        
                        if (distance < 100) {
                            this.ctx.beginPath();
                            this.ctx.moveTo(particle.x, particle.y);
                            this.ctx.lineTo(otherParticle.x, otherParticle.y);
                            this.ctx.strokeStyle = `rgba(0, 122, 255, ${0.1 * (1 - distance / 100)})`;
                            this.ctx.stroke();
                        }
                    });
                });
                
                requestAnimationFrame(() => this.animate());
            }
        }
        
        // Initialize particle system
        new ParticleSystem();
        
        // Chart instances
        let threatChart, timelineChart;
        
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
                            '#ff453a',
                            '#ff9f0a', 
                            '#ffd60a',
                            '#007aff',
                            '#30d158'
                        ],
                        borderWidth: 0,
                        hoverOffset: 10
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                color: '#ffffff',
                                usePointStyle: true,
                                padding: 20
                            }
                        }
                    }
                }
            });
            
            // Timeline Chart
            const timelineCtx = document.getElementById('timelineChart').getContext('2d');
            timelineChart = new Chart(timelineCtx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Security Events',
                        data: [],
                        borderColor: '#007aff',
                        backgroundColor: 'rgba(0, 122, 255, 0.1)',
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            labels: {
                                color: '#ffffff'
                            }
                        }
                    },
                    scales: {
                        x: {
                            ticks: { color: '#a1a1a6' },
                            grid: { color: 'rgba(255, 255, 255, 0.1)' }
                        },
                        y: {
                            ticks: { color: '#a1a1a6' },
                            grid: { color: 'rgba(255, 255, 255, 0.1)' }
                        }
                    }
                }
            });
        }
        
        function refreshData() {
            const refreshBtn = document.querySelector('.refresh-btn');
            refreshBtn.classList.add('loading');
            
            // Update system status
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    const statusElement = document.getElementById('system-status');
                    let statusClass = 'info';
                    
                    if (data.status.includes('CRITICAL')) statusClass = 'critical';
                    else if (data.status.includes('HIGH')) statusClass = 'high';
                    else if (data.status.includes('ELEVATED')) statusClass = 'medium';
                    
                    statusElement.innerHTML = `
                        <div class="threat-level ${statusClass}">
                            <span class="status-indicator status-${statusClass === 'info' ? 'online' : statusClass === 'medium' ? 'warning' : 'critical'}"></span>
                            ${data.status}
                        </div>
                    `;
                    
                    document.getElementById('last-update').innerHTML = `
                        <small style="color: var(--text-secondary);">
                            ${new Date(data.last_update).toLocaleString()}
                        </small>
                    `;
                    
                    document.getElementById('total-events').innerHTML = `
                        <span style="color: var(--accent-blue);">${data.total_events}</span>
                        <small style="color: var(--text-secondary); display: block;">Events Today</small>
                    `;
                    
                    // Update threat stats
                    let statsHtml = '';
                    const chartData = [0, 0, 0, 0, 0];
                    
                    Object.entries(data.threat_stats).forEach(([level, count]) => {
                        if (count > 0) {
                            statsHtml += `<div class="threat-level ${level.toLowerCase()}">${level}: ${count}</div>`;
                            
                            // Update chart data
                            switch(level) {
                                case 'CRITICAL': chartData[0] = count; break;
                                case 'HIGH': chartData[1] = count; break;
                                case 'MEDIUM': chartData[2] = count; break;
                                case 'LOW': chartData[3] = count; break;
                                case 'INFO': chartData[4] = count; break;
                            }
                        }
                    });
                    
                    document.getElementById('threat-stats').innerHTML = 
                        statsHtml || '<div class="threat-level info">No threats detected</div>';
                    
                    // Update charts
                    if (threatChart) {
                        threatChart.data.datasets[0].data = chartData;
                        threatChart.update('active');
                    }
                })
                .finally(() => {
                    refreshBtn.classList.remove('loading');
                });
        }
        
        function refreshEvents() {
            fetch('/api/events')
                .then(response => response.json())
                .then(data => {
                    const eventsHtml = data.events.map(event => {
                        const riskClass = event.risk_level.toLowerCase();
                        return `
                            <div class="event-item fade-in-up">
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
                        eventsHtml || '<div class="event-item"><div class="event-content">No recent events</div></div>';
                });
        }
        
        // Initialize everything
        document.addEventListener('DOMContentLoaded', function() {
            initCharts();
            refreshData();
            refreshEvents();
            
            // Auto-refresh every 30 seconds
            setInterval(() => {
                refreshData();
                refreshEvents();
            }, 30000);
            
            // Add staggered animation to cards
            document.querySelectorAll('.fade-in-up').forEach((element, index) => {
                element.style.animationDelay = `${index * 0.1}s`;
            });
        });
        
        // Smooth scrolling for navigation
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
    </script>
</body>
</html>'''
    
    # Enhanced logs template
    logs_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>McGuardian Elite - Security Logs</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary-bg: #000000;
            --secondary-bg: #1d1d1f;
            --tertiary-bg: #2d2d30;
            --accent-blue: #007aff;
            --accent-green: #30d158;
            --text-primary: #ffffff;
            --text-secondary: #a1a1a6;
            --glass-bg: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@100;200;300;400;500;600;700;800;900&display=swap');

        body {
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, var(--primary-bg) 0%, #1a1a1a 50%, var(--primary-bg) 100%);
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
            margin-bottom: 30px;
            padding: 30px;
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
        }

        .header h1 {
            color: var(--accent-blue);
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 15px;
        }

        .nav-menu {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 20px;
        }

        .nav-menu a {
            color: var(--accent-blue);
            text-decoration: none;
            padding: 12px 24px;
            border-radius: 25px;
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }

        .nav-menu a:hover {
            background: var(--accent-blue);
            color: white;
            transform: translateY(-2px);
        }

        .logs-container {
            background: #0a0a0a;
            border-radius: 15px;
            padding: 30px;
            max-height: 80vh;
            overflow-y: auto;
            border: 1px solid #333;
            box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.5);
            position: relative;
        }

        .logs-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, var(--accent-green), var(--accent-blue), var(--accent-green));
            border-radius: 15px 15px 0 0;
        }

        .log-content {
            font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace;
            font-size: 0.9rem;
            white-space: pre-wrap;
            color: var(--accent-green);
            text-shadow: 0 0 5px rgba(48, 209, 88, 0.3);
            line-height: 1.8;
        }

        .logs-container::-webkit-scrollbar {
            width: 12px;
        }

        .logs-container::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 6px;
        }

        .logs-container::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-green));
            border-radius: 6px;
        }

        .terminal-header {
            background: #1a1a1a;
            padding: 10px 20px;
            border-radius: 10px 10px 0 0;
            border-bottom: 1px solid #333;
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 20px;
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
        }

        @keyframes typing {
            from { width: 0; }
            to { width: 100%; }
        }

        .typing-effect {
            overflow: hidden;
            white-space: nowrap;
            animation: typing 2s steps(40, end);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-terminal"></i> McGuardian Elite - Security Logs</h1>
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
                    <i class="fas fa-shield-alt"></i> McGuardian Elite Security Terminal
                </div>
            </div>
            <div class="log-content typing-effect">{{ log_content }}</div>
        </div>
    </div>
</body>
</html>'''
    
    # Write templates
    with open(os.path.join(templates_dir, 'dashboard.html'), 'w') as f:
        f.write(dashboard_html)
    
    with open(os.path.join(templates_dir, 'logs.html'), 'w') as f:
        f.write(logs_html)

def run_dashboard():
    """Run the dashboard server"""
    create_templates()
    print("🌐 Starting McGuardian Elite Web Dashboard...")
    print("📊 Dashboard will be available at: http://localhost:5000")
    print("🔒 Access the dashboard to monitor security events in real-time")
    
    # Run Flask app
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)

def check_installation():
    """Verify McGuardian Elite is properly installed"""
    if not os.path.exists(BASE_DIR):
        print("❌ McGuardian Elite not found!")
        print("🔧 Please install McGuardian Elite first using the installer")
        print("   Run: python3 mcguardian_installer.py")
        sys.exit(1)
    
    # Check if main engine is running
    try:
        # Check for log files indicating the engine is active
        if os.path.exists(LOG_FILE):
            # Check if log was updated recently (within last 5 minutes)
            log_mtime = os.path.getmtime(LOG_FILE)
            if time.time() - log_mtime > 300:  # 5 minutes
                print("⚠️ Warning: McGuardian Elite engine may not be running")
                print("💡 Start the main engine first: mcguardian_elite")
    except:
        pass

if __name__ == '__main__':
    # Verify installation before starting dashboard
    check_installation()
    
    print("🌐 Starting McGuardian Elite Web Dashboard...")
    print("📊 Dashboard will be available at: http://localhost:5000")
    print("🔒 Access the dashboard to monitor security events in real-time")
    print("💡 Make sure the main McGuardian Elite engine is running for live data")
    
    run_dashboard()
