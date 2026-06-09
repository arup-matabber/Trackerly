import sys
import os
import json
import threading
import webbrowser
from flask import Flask, render_template, request, jsonify

# Support PyInstaller frozen bundle
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
    TEMPLATE_DIR = os.path.join(sys._MEIPASS, 'templates')
    STATIC_DIR = os.path.join(sys._MEIPASS, 'static')
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
    STATIC_DIR = os.path.join(BASE_DIR, 'static')

DATA_FILE = os.path.join(BASE_DIR, 'applications.json')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/apps', methods=['GET'])
def get_apps():
    return jsonify(load_data())

@app.route('/api/apps', methods=['POST'])
def add_app():
    apps = load_data()
    new_app = request.json
    new_app['id'] = int(__import__('time').time() * 1000)
    apps.insert(0, new_app)
    save_data(apps)
    return jsonify(new_app)

@app.route('/api/apps/<int:app_id>', methods=['PUT'])
def update_app(app_id):
    apps = load_data()
    for i, a in enumerate(apps):
        if a['id'] == app_id:
            apps[i].update(request.json)
            save_data(apps)
            return jsonify(apps[i])
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/apps/<int:app_id>', methods=['DELETE'])
def delete_app(app_id):
    apps = load_data()
    apps = [a for a in apps if a['id'] != app_id]
    save_data(apps)
    return jsonify({'ok': True})

def open_browser():
    webbrowser.open('http://127.0.0.1:5765')

if __name__ == '__main__':
    threading.Timer(1.2, open_browser).start()
    print("Starting Internship Tracker on http://127.0.0.1:5765")
    print("Press Ctrl+C to quit.")
    app.run(host='127.0.0.1', port=5765, debug=False, use_reloader=False)
