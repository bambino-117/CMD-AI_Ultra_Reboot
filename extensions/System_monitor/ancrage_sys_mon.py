from flask import Flask, jsonify, render_template
from flask_cors import CORS
from flask_socketio import SocketIO
from System_monitor import SystemMonitorExtension
import psutil
import time
import threading

app = Flask(__name__, template_folder='.')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
monitor = SystemMonitorExtension()
monitor.initialize(None)

def background_thread():
    """Example of how to send server generated events to clients."""
    while True:
        socketio.sleep(1)
        cpu_percent = psutil.cpu_percent(interval=None)
        memory = psutil.virtual_memory()
        
        socketio.emit('system_update', {
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "temperatures": monitor.get_temperatures_data()
        })

@app.route('/')
def index():
    return render_template('interface_sys_mon.html')

@app.route('/api/status')
def get_status_json():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    
    return jsonify({
        "cpu_percent": cpu_percent,
        "memory_percent": memory.percent,
        "temperatures": monitor.get_temperatures_data()
    })

@app.route('/api/system')
def get_system_json():
    return jsonify(monitor.get_system_info())

@app.route('/api/cpu')
def get_cpu_json():
    return jsonify(monitor.get_cpu_info())

@app.route('/api/memory')
def get_memory_json():
    return jsonify(monitor.get_memory_info())

@app.route('/api/disk')
def get_disk_json():
    return jsonify(monitor.get_disk_info())

@app.route('/api/network')
def get_network_json():
    return jsonify(monitor.get_network_info())

@app.route('/api/services')
def get_services_json():
    return jsonify(monitor.get_services_info())

@app.route('/api/battery')
def get_battery_json():
    return jsonify(monitor.get_battery_info())

@app.route('/api/processes')
def get_processes_json():
    return jsonify(monitor.get_top_processes_data())

if __name__ == '__main__':
    thread = threading.Thread(target=background_thread)
    thread.daemon = True
    thread.start()
    socketio.run(app, port=5001, debug=True)
