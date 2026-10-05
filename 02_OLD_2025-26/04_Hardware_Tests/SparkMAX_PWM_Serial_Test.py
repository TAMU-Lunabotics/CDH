import serial
import time

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
time.sleep(2)  # wait for Pico to arm
ser.flush()

def send_command(cmd):
    ser.write(f"{cmd}\n".encode())
    time.sleep(0.1)
    response = ser.readline().decode('utf-8').strip()
    print(f"Pico: {response}")

while True:
    print("\nEnter command: FORWARD / REVERSE / STOP / QUIT")
    cmd = input("> ").strip().upper()

    if cmd == "QUIT":
        send_command("STOP")
        ser.close()
        break

    send_command(cmd)