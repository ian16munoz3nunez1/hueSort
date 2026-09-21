import numpy as np
import re
import socket

host = '4.4.0.32'
port = 9999
addr = (host, port)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.connect(addr)
print("Conexion establecida")

minimum = np.array([0, 0])
maximum = np.array([90, 120])

while True:
    in_theta = input("Insert angles: ")

    match = re.match(r"\d{1,4}\s\d{1,4}", in_theta, re.IGNORECASE)
    if in_theta.lower() == 'q':
        break
    elif match:
        theta = np.array(list(map(int, match.group(0).rstrip().lstrip().split())))

        theta = np.maximum(minimum, theta)
        theta = np.minimum(maximum, theta)
        print(chr(theta[0]))
        print(chr(theta[1]))

        sock.send(f"{chr(theta[0])}{chr(theta[1])}\n".encode())
    else:
        print("Error capturing valid input")

sock.close()

# import numpy as np
# import re
# import serial
# 
# try:
#     esp32 = serial.Serial('/dev/ttyUSB0', 115200, write_timeout=10)
# except Exception as e:
#     print(f"Error connecting to board: {e}")
# 
# minimum = np.array([0, 0])
# maximum = np.array([90, 120])
# 
# while True:
#     in_theta = input("Insert angles: ")
# 
#     match = re.match(r"\d{1,4}\s\d{1,4}", in_theta, re.IGNORECASE)
#     if in_theta.lower() == 'q':
#         break
#     elif match:
#         theta = np.array(list(map(int, match.group(0).rstrip().lstrip().split())))
# 
#         theta = np.maximum(minimum, theta)
#         theta = np.minimum(maximum, theta)
#         print(chr(theta[0]))
#         print(chr(theta[1]))
# 
#         esp32.write(f"{chr(theta[0])}".encode())
#         esp32.write(f"{chr(theta[1])}".encode())
#     else:
#         print("Error capturing valid input")
# 
# esp32.close()
