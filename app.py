from flask import Flask, render_template, jsonify
import serial
import threading
import time
import sys

app = Flask(__name__)

latest_data = {
    "value": "---",
    "status": "Starting...",
    "port": "COM6",
    "connected": False
}

def read_serial():
    global latest_data
    while True:
        ser = None
        try:
            print("Connecting to COM6...", flush=True)
            ser = serial.Serial('COM6', 9600, timeout=1)
            ser.setDTR(False)
            time.sleep(1)
            ser.setDTR(True)
            
            latest_data["connected"] = True
            latest_data["status"] = "Connected"
            print("Connected to COM6", flush=True)
            
            while True:
                if ser.in_waiting > 0:
                    raw_line = ser.readline()
                    print(f"Raw: {raw_line}", flush=True)
                    line = raw_line.decode('utf-8', errors='ignore').strip()
                    if line:
                        print(f"Line: {line}", flush=True)
                        if "Value:" in line:
                            parts = line.split("-->")
                            value_part = parts[0].split("Value:")[1].strip()
                            status_part = parts[1].strip() if len(parts) > 1 else "Checking"
                            latest_data["value"] = value_part
                            latest_data["status"] = status_part
                        else:
                            # Fallback: if it's just a number or something else
                            latest_data["status"] = f"Raw: {line}"
                time.sleep(0.1)
        except Exception as e:
            latest_data["connected"] = False
            latest_data["status"] = f"Error: {e}"
            print(f"Serial Error: {e}", flush=True)
            if ser:
                ser.close()
            time.sleep(5)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    return jsonify(latest_data)

if __name__ == '__main__':
    serial_thread = threading.Thread(target=read_serial, daemon=True)
    serial_thread.start()
    app.run(debug=False, port=5000, host='0.0.0.0')