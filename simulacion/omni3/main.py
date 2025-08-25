import numpy as np
import matplotlib.pyplot as plt
from dibujarOmni3 import dibujarOmni3
pi = np.pi

t = 0.01
S = 10
N = int(S/t)

L = 8
x_i = np.array([0.0, 0.0, 0.0]).reshape(-1, 1)
x_dot = np.array([0.0, 0.0, 0.5]).reshape(-1, 1)

x_plot = np.array([[], [], []])
v_plot = np.array([[], [], []])

x_i = x_i.ravel()
m = np.array([[-np.sin(x_i[2]), np.cos(x_i[2]), L],
              [-np.sin(x_i[2]+2*pi/3), np.cos(x_i[2]+2*pi/3), L],
              [-np.sin(x_i[2]+4*pi/3), np.cos(x_i[2]+4*pi/3), L]])
x_i = x_i.reshape(-1, 1)

for _ in range(N):
    v = np.matmul(m, x_dot)
    x_dot = np.matmul(np.linalg.inv(m), v)
    x_i = x_i + x_dot*t

    x_plot = np.hstack((x_plot, x_i))
    v_plot = np.hstack((v_plot, v))

print(x_i)
print(v)

plt.figure(1)
dibujarOmni3(x_i.ravel(), L)
plt.plot(x_plot[0, :], x_plot[1, :], 'g-', linewidth=2)

plt.figure(2)
plt.grid()
plt.plot(x_plot[0, :], linewidth=2)
plt.plot(x_plot[1, :], linewidth=2)
plt.plot(x_plot[2, :], linewidth=2)
plt.legend(['x', 'y', '$\\theta$'])

plt.figure(3)
plt.grid()
plt.plot(v_plot[0, :], linewidth=2)
plt.plot(v_plot[1, :], linewidth=2)
plt.plot(v_plot[2, :], linewidth=2)
plt.legend(['$v_1$', '$v_2$', '$v_3$'])

plt.show()

