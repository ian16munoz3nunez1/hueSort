import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dibujarMovil import dibujarMovil

pi = np.pi
L = 0.08
p_b = [0.07, 0.0, 0.085]
a = [0, 0.05, 0.05]
d = [0, 0, 0]
x_t, y_t, z_t = p_b


class Graph:
    def drawBot(self, q: np.ndarray, plot_x: np.ndarray = False):
        q_df = pd.read_csv("./data/q.csv")

        x_b = np.array(q_df['x_b'])
        y_b = np.array(q_df['y_b'])

        plt.figure(1)
        if plot_x:
            x_df = pd.read_csv("./data/x.csv")
            x = np.array(x_df['x'])
            y = np.array(x_df['y'])
            z = np.array(x_df['z'])
            x_plot = np.vstack((x, y, z))

            dibujarMovil(L, q, p_b, a, d, x_plot)
            plt.plot(x_b, y_b, 'g-', linewidth=2)

        else:
            dibujarMovil(L, q, p_b, a, d)
            plt.plot(x, y, 'y-', linewidth=2)

    def q_plot(self):
        q_df = pd.read_csv("./data/q.csv")
        xd_df = pd.read_csv("./data/x_d.csv")

        t = np.array(q_df['t'])
        x_b = np.array(q_df['x_b'])
        y_b = np.array(q_df['y_b'])
        theta_b = np.array(q_df['theta_b'])
        theta_2 = np.array(q_df['theta_2'])
        theta_3 = np.array(q_df['theta_3'])

        x_d = np.array(xd_df['x_b'])
        y_d = np.array(xd_df['y_b'])
        thetab_d = np.array(xd_df['theta_b'])

        plt.figure(2)
        plt.grid()

        plt.plot(t, x_b, '-', linewidth=2)
        plt.plot(t, y_b, '-', linewidth=2)
        plt.plot(t, theta_b, '-', linewidth=2)
        plt.plot(t, x_d, '-', linewidth=2)
        plt.plot(t, y_d, '-', linewidth=2)
        plt.plot(t, thetab_d, '-', linewidth=2)
        plt.plot(t, theta_2, '-', linewidth=2)
        plt.plot(t, theta_3, '-', linewidth=2)

        plt.title("Trajectory", fontsize=20)
        plt.xlabel('t', fontsize=15)
        plt.ylabel('q', fontsize=15)
        plt.legend(['$x_b$', '$y_b$', '$\\theta_b$', '$x_d$', '$y_d$', '$\\theta_d$', '$\\theta_2$', '$\\theta_3$'])

    def qd_plot(self):
        df = pd.read_csv("./data/q_dot.csv")

        t = np.array(df['t'])
        x = np.array(df['x_b'])
        y = np.array(df['y_b'])
        theta = np.array(df['theta_b'])
        theta_2 = np.array(df['theta_2'])
        theta_3 = np.array(df['theta_3'])

        plt.figure(3)
        plt.grid()

        plt.plot(t, x, '-', linewidth=2)
        plt.plot(t, y, '-', linewidth=2)
        plt.plot(t, theta, '-', linewidth=2)
        plt.plot(t, theta_2, '-', linewidth=2)
        plt.plot(t, theta_3, '-', linewidth=2)

        plt.title("Control", fontsize=20)
        plt.xlabel('t', fontsize=15)
        plt.ylabel('q', fontsize=15)
        plt.legend(['x', 'y', '$\\theta$', '$\\theta_2$', '$\\theta_3$'])

    def e_plot(self):
        df = pd.read_csv("./data/e.csv")

        t = np.array(df['t'])
        x_b = np.array(df['x_b'])
        y_b = np.array(df['y_b'])
        theta_b = np.array(df['theta_b'])
        x = np.array(df['x'])
        y = np.array(df['y'])
        z = np.array(df['z'])

        plt.figure(4)
        plt.grid()

        plt.plot(t, x_b, '-', linewidth=2)
        plt.plot(t, y_b, '-', linewidth=2)
        plt.plot(t, theta_b, '-', linewidth=2)
        plt.plot(t, x, '-', linewidth=2)
        plt.plot(t, y, '-', linewidth=2)
        plt.plot(t, z, '-', linewidth=2)

        plt.title("Error", fontsize=20)
        plt.xlabel('t', fontsize=15)
        plt.ylabel('e', fontsize=15)
        plt.legend(['$e_{x_b}$', '$e_{y_b}$', '$e_{\\theta_b}$', '$e_x$', '$e_y$', '$e_z$'])

    def v_plot(self):
        df = pd.read_csv("./data/v.csv")

        t = np.array(df['t'])
        v_1 = np.array(df['v_1'])
        v_2 = np.array(df['v_2'])
        v_3 = np.array(df['v_3'])

        plt.figure(5)
        plt.grid()

        plt.plot(t, v_1, '-', linewidth=2)
        plt.plot(t, v_2, '-', linewidth=2)
        plt.plot(t, v_3, '-', linewidth=2)

        plt.title("Velocities", fontsize=20)
        plt.xlabel('t', fontsize=15)
        plt.ylabel('v', fontsize=15)
        plt.legend(['$v_1$', '$v_2$', '$v_3$'])

    def x_plot(self):
        x_df = pd.read_csv("./data/x.csv")
        xd_df = pd.read_csv("./data/x_d.csv")

        t = np.array(x_df['t'])
        x = np.array(x_df['x'])
        y = np.array(x_df['y'])
        z = np.array(x_df['z'])

        x_d = np.array(xd_df['x'])
        y_d = np.array(xd_df['y'])
        z_d = np.array(xd_df['z'])

        plt.figure(6)
        plt.grid()

        plt.plot(t, x, '-', linewidth=2)
        plt.plot(t, y, '-', linewidth=2)
        plt.plot(t, z, '-', linewidth=2)
        plt.plot(t, x_d, '-', linewidth=2)
        plt.plot(t, y_d, '-', linewidth=2)
        plt.plot(t, z_d, '-', linewidth=2)

        plt.title("End Effector", fontsize=20)
        plt.xlabel('t', fontsize=15)
        plt.ylabel('x', fontsize=15)
        plt.legend(['x', 'y', 'z', '$x_d$', '$y_d$', '$z_d$'])

    def show(self):
        plt.show()

    def clear(self):
        with open("./data/q.csv", 'w') as file:
            file.write("t,x_b,y_b,theta_b,theta_2,theta_3\n")
        file.close()

        with open("./data/q_dot.csv", 'w') as file:
            file.write("t,x_b,y_b,theta_b,theta_2,theta_3\n")
        file.close()

        with open("./data/x_d.csv", 'w') as file:
            file.write("t,x_b,y_b,theta_b,x,y,z\n")
        file.close()

        with open("./data/e.csv", 'w') as file:
            file.write("t,x_b,y_b,theta_b,x,y,z\n")
        file.close()

        with open("./data/v.csv", 'w') as file:
            file.write("t,v_1,v_2,v_3\n")
        file.close()

        with open("./data/x.csv", 'w') as file:
            file.write("t,x,y,z\n")
        file.close()

        with open("./data/last_time.dat", 'w') as file:
            file.write("0.0")
        file.close()


if __name__ == '__main__':
    mode = sys.argv[1]
    g = Graph()

    if mode.lower() == 'plot':
        g.q_plot()
        g.qd_plot()
        g.e_plot()
        g.v_plot()
        g.show()

    elif mode.lower() == 'clear':
        g.clear()
