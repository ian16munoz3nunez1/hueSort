import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from colorama import init
from colorama.ansi import Fore

init(autoreset=True)

class WaveFront:
    def __init__(self, imagen):
        self.__imagen = imagen

    def calcPath(self, mask, start, goal):
        mask = cv.normalize(mask.astype(float), None, 0.0, 1.0, cv.NORM_MINMAX)

        h, w = mask.shape[0:2]
        moves = np.array([[-1, 0, +1, 0],
                          [0, +1, 0, -1]])
        m = moves.shape[1]

        cola = deque()
        visitados = np.copy(mask)
        wfMask = np.copy(mask)
        s = np.array([[], []], dtype=np.uint8)
        t = np.array([[], []], dtype=np.uint8)

        cola.append(goal)
        visitados[goal[0], goal[1]] = -1

        while len(cola) > 0:
            actual = cola[0]
            cola.popleft()

            s_node = actual
            wfValue = 2

            while np.sum(abs(s_node-goal)) != 0:
                wfValue += 1
                s_node = s[:, (t[0,:]==s_node[0])&(t[1,:]==s_node[1])]

            wfMask[actual[0], actual[1]] = wfValue

            for i in range(m):
                p = actual + moves[:, i].reshape(-1, 1)

                if 1 <= p[0] and p[0] <= h and 1 <= p[1] and p[1] <= w:
                    if mask[p[0], p[1]] != 1 and visitados[p[0], p[1]] != -1:
                        cola.append(p)
                        visitados[p[0], p[1]] = -1

                        s = np.hstack((s, actual))
                        t = np.hstack((t, p))

            print(Fore.CYAN + "[*] Calculando ruta...", end='\r')
        print('\r')

        moves = np.array([[-1, -1, -1, 0, 1, 1,  1,  0],
                          [-1,  0,  1, 1, 1, 0, -1, -1]])
        m = moves.shape[1]

        actual = start
        path = np.array([[], []], dtype=np.uint8)

        value = wfMask[actual[0], actual[1]]
        path = np.hstack((path, actual))

        while value != 2:
            iBest = -1

            for i in range(m):
                p = actual + moves[:, i].reshape(-1, 1)

                if 1 <= p[0] and p[0] <= h and 1 <= p[1] and p[1] <= w:
                    wfValue = wfMask[p[0], p[1]]

                    if wfMask[p[0], p[1]] > 1 and wfValue < value:
                        iBest = i
                        value = wfValue

            p = actual + moves[:, iBest].reshape(-1, 1)
            path = np.hstack((path, p))
            actual = p
            print(Fore.CYAN + "[*] Creando ruta...", end='\r')
        print('\r')

        return path

    def cr2xy(self, crPath, m_x, m_y):
        xyPath = np.array([[], []])
        R, C = self.__imagen.shape[0:2]

        i = 0
        while i < crPath.shape[1]:
            c = crPath[1, i]
            r = crPath[0, i]

            x = -m_x * ((C-2*c)/C)
            y = m_y * ((R-2*r)/R)

            xyPath = np.hstack((xyPath, np.array([[x], [y]])))

            i += 1

        return xyPath

    def mainMask(self, minColor, maxColor, k, n=None):
        kernel = np.ones((k, k), dtype=np.uint8)

        hsv = cv.cvtColor(self.__imagen, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv, minColor, maxColor)
        mask = cv.dilate(mask, kernel)

        mask[:, 0] = 255
        mask[:, -1] = 255
        mask[0, :] = 255
        mask[-1, :] = 255

        if n:
            return mask, cv.normalize(mask.astype(float), None, 0.0, 1.0, cv.NORM_MINMAX)
        else:
            return mask, None

    def appMask(self, minColor, maxColor, n=None):
        hsv = cv.cvtColor(self.__imagen, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv, minColor, maxColor)

        if n:
            return mask, cv.normalize(mask.astype(float), None, 0.0, 1.0, cv.NORM_MINMAX)
        else:
            return mask, None

    def centroide(self, norm):
        posy, posx = np.where(norm==1)
        m, n = norm.shape[0:2]

        try:
            cy = int(np.sum(posy)/np.sum(norm))
            cx = int(np.sum(posx)/np.sum(norm))
        except:
            cy = int(m/2)
            cx = int(n/2)

        return cy, cx

    def plotPath(self, path, start, goal):
        plt.figure()
        plt.grid()

        plt.imshow(cv.cvtColor(self.__imagen, cv.COLOR_BGR2RGB))
        plt.plot(path[1, :], path[0, :], 'r.-', linewidth=2)
        plt.plot(start[1], start[0], 'yo', linewidth=2, markersize=8)
        plt.plot(goal[1], goal[0], 'mo', linewidth=2, markersize=8)

        plt.show()

