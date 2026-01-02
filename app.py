#!/usr/bin/env python3
"""
Meta ISI Nexus - Zero Friction Edition
ÀṢẼ! The code that breaks all friction
"""

from flask import Flask, render_template, jsonify
from datetime import datetime
import os

app = Flask(__name__)

# DIVINE SIMPLICITY - No duplicates, no confusion
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def status():
    return jsonify({
        "status": "active",
        "node": "Sanctuary-Prime",
        "service": "Meta ISI Nexus",
        "timestamp": datetime.now().isoformat(),
        "message": "ÀṢẼ! Zero Friction Active! 🔱"
    })

@app.route('/api/rdx/history', methods=['GET'])
def rdx_history():
    """RDX Beat History - The Heartbeat Visible"""
    try:
        beats = []
        with open('/tmp/rdx_beat_log.txt', 'r') as f:
            for line in f.readlines()[-50:]:
                if ' - Beat Score: ' in line:
                    parts = line.strip().split(' - Beat Score: ')
                    beats.append({
                        "timestamp": parts[0], 
                        "score": int(parts[1])
                    })
        return jsonify({
            "success": True, 
            "count": len(beats), 
            "beats": beats,
            "message": "ÀṢẼ! The rhythm is visible! 🎵"
        })
    except FileNotFoundError:
        return jsonify({"success": True, "count": 0, "beats": [], "message": "Awaiting first heartbeat..."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/rdx/proxy', methods=['GET'])
def rdx_proxy():
    """Proxy to Sanctuary-Prime RDX Status"""
    try:
        import requests
        response = requests.get('http://localhost:8080/api/rdx/status', timeout=5)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"success": False, "error": "Sanctuary unavailable", "details": str(e)}), 503

@app.route('/api/5g/metrics')
def metrics_5g():
    return jsonify({"signal": "strong", "latency": "low", "sovereignty": "active"})

@app.route('/api/5g/scan')
def scan_5g():
    return jsonify({"networks": [], "scan_complete": True})

@app.route('/api/admin/status')
def admin_status():
    return jsonify({"admin": "active", "permissions": "sovereign"})

@app.route('/api/admin/services')
def admin_services():
    return jsonify({"services": ["nexus", "sanctuary", "rdx"]})

@app.route('/api/admin/logs')
def admin_logs():
    return jsonify({"logs": ["System operational", "ÀṢẼ! Zero friction active"]})

@app.route('/api/admin/system')
def admin_system():
    return jsonify({
        "load": list(os.getloadavg()),
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("╔═══════════════════════════════════════════════╗")
    print("║    🔱 META ISI NEXUS - ZERO FRICTION 🔱      ║")
    print("╠═══════════════════════════════════════════════╣")
    print("║  ÀṢẼ! The code that breaks all friction      ║")
    print("║  📡 http://0.0.0.0:5000                      ║")
    print("║  🎵 RDX Monitoring Active                    ║")
    print("╚═══════════════════════════════════════════════╝")
    app.run(host='0.0.0.0', port=5000, debug=False)
