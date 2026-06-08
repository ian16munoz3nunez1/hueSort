import numpy as np
from robot import Robot

pi = np.pi

bot = Robot()

t = 0.2
s = 70
n = int(s/t)

q = np.array([0, 0, 0, 0, pi/4, -pi/4], dtype=np.float64)
k = np.diag([0.4, 0.4, 0.4])

bot.connect('4.4.0.32', 9999)

x_d = np.array([-0.1, -0.1, 0.0], dtype=np.float64)
bot.go2(t, s, n, q, k, x_d)

# x_d = np.array([[0.1, 0.1, 0.0, 0.0],
#                 [0.0, 0.1, 0.1, 0.0],
#                 [0.0, pi/2, pi, 3*(pi/2)]])
# bot.followTrajectory(t, s, n, q, k, x_d)

bot.disconnect()
