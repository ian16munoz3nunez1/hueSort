import numpy as np
from robot import Robot
from graph import Graph

pi = np.pi

bot = Robot()
g = Graph()
g.clear()

t = 0.01
s = 20
n = int(s/t)

bot.connect('localhost', 9999)
k = np.diag([0.8, 0.8, 0.8])

bot.writeHome()
q = bot.readPose()

x_d = np.array([0.4, 0.3, pi], dtype=np.float64)
# q = bot.go2(t, s, n, q, k, x_d)

x_d = np.array([[0.1, 0.2, 0.3],
                [0.0, 0.1, 0.1],
                [0.0, pi/4, 0.0]], dtype=np.float64)
# q = bot.followTrajectory(t, n, q, k, x_d)

x_d = np.array([0.4, 0.3, 0.05], dtype=np.float64)
q = bot.ee2(t, n, q, k, x_d)

bot.disconnect()

g.drawBot(q, True)
g.q_plot()
g.qd_plot()
g.e_plot()
g.v_plot()
g.x_plot()
g.show()
