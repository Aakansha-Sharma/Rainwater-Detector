import serial
import time

try:
    ser = serial.Serial('COM6', 9600, timeout=1)
    print("Connected to COM6. Reading for 5 seconds...")
    end_time = time.time() + 5
    while time.time() < end_time:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                print(f"Data: {line}")
    ser.close()
except Exception as e:
    print(f"Error: {e}")
