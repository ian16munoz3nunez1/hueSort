#!/bin/python3

import socket
import struct
import cv2 as cv
import numpy as np

# Server details
addr = ('192.168.4.101', 10001)

# Connect to the ESP32-CAM server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(addr)

try:
    while True:
        # Read the frame length
        length = sock.recv(4)
        if not length:
            break
        length = struct.unpack('<I', length)[0]

        # Read the frame data
        data = b''
        while len(data) < length:
            packet = sock.recv(length - len(data))
            if not packet:
                break
            data += packet

        # Convert the data to an OpenCV image
        matrix = np.frombuffer(data, np.uint8)
        frame = cv.imdecode(matrix, cv.IMREAD_COLOR)

        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv, (45, 100, 100), (65, 250, 250))

        if frame is not None:
            cv.imshow("101 cam", frame)
            cv.imshow("mask", mask)

        if cv.waitKey(1) == 27:
            break

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    sock.close()
    cv.destroyAllWindows()

