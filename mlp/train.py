import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colormaps
from mlp import MLP
pi = np.pi

df = pd.read_csv('color.csv')
r = np.array([df['r']])
g = np.array([df['g']])
b = np.array([df['b']])
label = np.array(df['color'])

clases = 4
p = 200
colors = [[1,0,0], [0,1,0], [0,0,1], [1,1,0]]

x = np.array([r.ravel(), g.ravel(), b.ravel()])
y = np.zeros((clases, clases*p))
for i in range(clases):
    y[i,i*p:(i+1)*p] = np.ones((1, p))

nn = MLP([(3,), (30, 'tanh'), (30, 'tanh'), (4,'softmax')]) # Objeto de tipo Multi-Layer Perceptron
loss = nn.fit(x, y, 1e-3, 50000) # Entrenamiento de la red
yp = nn.predict(x) # Prediccion de la red

fig = plt.figure(1)

ax1 = fig.add_subplot(121, projection='3d')
ax1.grid(True)

for i in range(clases*p):
    ax1.plot(r[:,i], g[:,i], b[:,i], 'o', c=colors[label[i]], markersize=8)

ax2 = fig.add_subplot(122, projection='3d')
ax2.grid(True)
yc = np.argmax(yp, axis=0)
for i in range(clases*p):
    ax2.plot(r[:,i], g[:,i], b[:,i], 'o', c=colors[yc[i]], markersize=8)

plt.figure(2)
plt.grid()

plt.plot(loss, 'g-', linewidth=2)
plt.title("Grafica del error", fontsize=20)
plt.xlabel('Epocas', fontsize=15)
plt.ylabel('Error', fontsize=15)

plt.show()

