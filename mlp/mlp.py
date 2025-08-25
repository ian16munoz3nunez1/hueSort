import numpy as np
from colorama import init
from colorama.ansi import Fore

init(autoreset=True)

class MLP:
    def __init__(self, k):
        functions = ['step', 'linear', 'relu', 'tanh', 'logistic', 'softmax'] # Funciones de activacion para la red
        self.L = len(k)-1 # Numero de capas ocultas

        # self.w = [None]*(n+1)
        # self.b = [None]*(n+1)
        # self.f = [None]*(n+1)
        # self.phi = [None]*(n+1)
        # self.dphi = [None]*(n+1)
        # self.delta = [None]*(n+1)

        self.w = {} # Arreglo para los pesos sinapticos de las capas
        self.b = {} # Arreglo para los bias de las capas
        self.f = {} # Arreglo para las funciones de activacion
        self.phi = {} # Arreglo para las entradas/salidas de las capas
        self.dphi = {} # Arreglo para la derivada de las salidas de las capas
        self.delta = {} # Arreglo para los errores de las salidas de las capas

        xl, xu = -1, 1;
        for l in range(1,self.L+1):
            self.w[l] = xl + (xu-xl)*np.random.rand(k[l-1][0], k[l][0]) # Se generan los pesos sinapticos para cada capa aleatoriamente
            self.b[l] = xl + (xu-xl)*np.random.rand(k[l][0],1) # Se generan los bias para cada capa aleatoriamente
            if k[l][1] in functions:
                self.f[l] = k[l][1] # Se generan las funciones de activacion para las capas
            else:
                print(Fore.RED + f"Function \"{k[l][1]}\" not available")
                exit(1)

    # Funcion para entrenar la red
    def fit(self, x, y, eta, epocas):
        loss = np.zeros(epocas) # Arreglo para la funcion de perdida de la red
        p = x.shape[1] # Numero de patrones de entrada
        self.phi[0] = x # Entrada de la red

        for epoca in range(epocas):
            # Etapa hacia adelante
            for l in range(1, self.L+1):
                v = np.matmul(self.w[l].T, self.phi[l-1]) + self.b[l]
                self.phi[l], self.dphi[l] = self.function(self.f[l], v)
                l += 1

            # Etapa hacia atras
            self.delta[self.L] = (y - self.phi[self.L])*self.dphi[self.L]
            loss[epoca] = np.dot(self.delta[self.L].flatten(), self.delta[self.L].flatten())
            l = self.L-1
            while l > 0:
                self.delta[l] = np.matmul(self.w[l+1], self.delta[l+1])*self.dphi[l]
                l -= 1

            # Ajuste de pesos y bias
            for l in range(1, self.L+1):
                self.w[l] += (eta/p)*np.matmul(self.phi[l-1], self.delta[l].T)
                self.b[l] += (eta/p)*np.sum(self.delta[l],1).reshape(-1,1)

        return loss

    # Funcion para regresar la prediccion de la red
    def predict(self, x):
        phi = np.array(x)
        for l in range(1, self.L+1):
            v = np.matmul(self.w[l].T, phi) + self.b[l]
            phi = self.function(self.f[l], v)[0]
        return phi

    # Funciones de activacion y su derivada
    def function(self, f, v, a=1, b=1):
        if f == 'step':
            y = 1*(v>=0)
            dy = np.ones(v.shape)
            return y, dy

        elif f == 'linear':
            y = v
            dy = np.ones(v.shape)
            return y, dy

        elif f == 'relu':
            y = v*(v>=0)
            dy = np.array(v>=0, dtype=np.float64)
            return y, dy

        elif f == 'tanh':
            y = a*np.tanh(b*v)
            dy = (b/a)*(1-y)*(1+y)
            return y, dy

        elif f == 'logistic':
            y = 1/(1 + np.exp(-a*v))
            dy = a*y*(1-y)
            return y, dy

        elif f == 'softmax':
            e = np.exp(v - np.max(v,axis=0))
            y = e/np.sum(e,axis=0)
            dy = np.ones(v.shape)
            return y, dy

        else:
            print(Fore.RED + f"Function \"{f}\" not available")

