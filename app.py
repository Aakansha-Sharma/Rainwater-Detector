import serial
import time

# Open serial port
ser = serial.Serial('COM6', 9600, timeout=1)

# Give Arduino time to reset
time.sleep(2)

print("Reading from Arduino...\n")

while True:
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            
            if line:
                print(line)

    except KeyboardInterrupt:
        print("\nStopped by user")
        break

    except Exception as e:
        print("Error:", e)