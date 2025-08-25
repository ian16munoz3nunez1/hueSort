#!python3

import socket
import numpy as np
from time import sleep
from colorama import init
from colorama.ansi import Fore

init(autoreset=True)

host = '192.168.1.32'
port = 9999
addr = (host, port)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.connect(addr)
print(Fore.GREEN + f"[+] Conexion establecida con {addr[0]}")

while True:
    try:
        v = np.random.randint(low=-255, high=255, size=3)
        v = ''.join([str(x).zfill(4) for x in v])

        sock.send(f"{v}\n".encode())
        print(f"Velocidades enviadas: {v}")

        sleep(2)

    except KeyboardInterrupt:
        sock.send("q\n".encode())
        break

sock.close()

print(Fore.RED + "[!] Programa finalizado")

