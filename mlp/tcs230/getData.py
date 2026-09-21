import serial
from time import sleep
from colorama import init
from colorama.ansi import Fore
import sys

init(autoreset=True)

mode, color = int(sys.argv[1]), int(sys.argv[2])
colors = ['Rojo', 'Verde', 'Azul', 'Amarillo']

esp = serial.Serial('/dev/ttyUSB0', 115200)
sleep(2)

filename = 'color.csv'
if mode == 0:
    file = open(filename, 'w')
    file.write("name,r,g,b,color\n")
else:
    file = open(filename, 'a+')

i = 0
while i < 200:
    try:
        data = str(esp.readline(), encoding='utf-8')
        data = data.replace('\r\n', '')
        data = data.split('-')

        r, g, b = data
        print(r, g, b, "<==>", i+1)
        file.write(f"{colors[color]},{r},{g},{b},{color}\n")
        sleep(0.2)

        i += 1

    except KeyboardInterrupt as e:
        print(e)
        break

esp.close()
print(Fore.YELLOW + "[!] Conexion terminada")
file.close()
