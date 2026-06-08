import socket
import errno
import numpy as np
import matplotlib.pyplot as plt
from time import sleep

from dibujarMovil import dibujarMovil

pi = np.pi
L = 0.08
p_b = [0.05, 0.0, 0.015]
a = [0, 0.05, 0.05]
d = [0, 0, 0]
x_t, y_t, z_t = p_b


class Robot:
    def connect(self, host: str, port: int):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        status = self.sock.connect_ex((host, port))

        if status > 0:
            if status == errno.ECONNREFUSED:
                raise ValueError("Connection refused")

            elif status == errno.ETIMEDOUT:
                raise ValueError("Connection timeout")

            else:
                raise ValueError(f"Error connecting - errno: {status}")
        print("Successfully connected")

    def setJointVelocity(self, v: [float]):
        l, h = -10000, 10000
        lim = 100
        v = (l + (h - l)) * v
        v = np.minimum(v, np.array([lim, lim, lim]))
        v = np.maximum(v, np.array([-lim, -lim, -lim]))
        v = ''.join([str(int(x)).zfill(4) for x in v])
        self.sock.send(v.encode('utf-8'))

    def setVelocity(self, v: [float]):
        v = ''.join([str(x).zfill(4) for x in v])

        try:
            self.sock.send(v.encode('utf-8'))
            return True

        except Exception:
            return False

    def matrix(self, q: [float]):
        m = np.array([[-np.sin(q[2]), np.cos(q[2]), L],
                      [-np.sin(q[2] + (2*pi)/3), np.cos(q[2] + (2*pi)/3), L],
                      [-np.sin(q[2] + (4*pi)/3), np.cos(q[2] + (4*pi)/3), L]])

        return m

    def wTe(self, q: np.ndarray) -> np.ndarray:
        t11 = np.cos(q[2])*np.cos(q[4]+q[5])
        t21 = np.sin(q[2])*np.cos(q[4]+q[5])
        t31 = np.sin(q[4]+q[5])
        t41 = 0

        t12 = -np.cos(q[2])*np.sin(q[4]+q[5])
        t22 = -np.sin(q[2])*np.sin(q[4]+q[5])
        t32 = np.cos(q[4]+q[5])
        t42 = 0

        t13 = -np.sin(q[2])
        t23 = np.cos(q[2])
        t33 = 0
        t43 = 0

        t14 = q[0] + x_t*np.cos(q[2]) - y_t*np.sin(q[2]) + np.cos(q[2])*(a[1]*np.cos(q[4]) + a[2]*np.cos(q[4]+q[5]))
        t24 = q[1] + x_t*np.sin(q[2]) + y_t*np.cos(q[2]) + np.sin(q[2])*(a[1]*np.cos(q[4]) + a[2]*np.cos(q[4]+q[5]))
        t34 = z_t + d[0] + a[1]*np.sin(q[4]) + a[2]*np.sin(q[4]+q[5])
        t44 = 1

        wte = np.array([[t11, t12, t13, t14],
                        [t21, t22, t23, t24],
                        [t31, t32, t33, t34],
                        [t41, t42, t43, t44]], dtype=np.float64)
        return wte

    def j_v(self, q: np.ndarray) -> np.ndarray:
        t11, t21, t31 = 1, 0, 0
        t12, t22, t32 = 0, 1, 0

        t13 = -x_t*np.sin(q[2]) - y_t*np.cos(q[2]) - np.sin(q[2])*(a[1]*np.cos(q[4])+a[2]*np.cos(q[4]+q[5]))
        t23 = x_t*np.cos(q[2]) - y_t*np.sin(q[2]) + np.cos(q[2])*(a[1]*np.cos(q[4])+a[2]*np.cos(q[4]+q[5]))
        t33 = 0

        t14, t24, t34 = 0, 0, 0

        t15 = -a[1]*np.cos(q[2])*np.sin(q[4]) - a[2]*np.cos(q[2])*np.sin(q[4]+q[5])
        t25 = -a[1]*np.sin(q[2])*np.sin(q[4]) - a[2]*np.sin(q[2])*np.sin(q[4]+q[5])
        t35 = a[1]*np.cos(q[4]) + a[2]*np.cos(q[4]+q[5])

        t16 = -a[2]*np.cos(q[2])*np.sin(q[4]+q[5])
        t26 = -a[2]*np.sin(q[2])*np.sin(q[4]+q[5])
        t36 = a[2]*np.cos(q[4]+q[5])

        jacob = np.array([[t11, t12, t13, t14, t15, t16],
                          [t21, t22, t23, t24, t25, t26],
                          [t31, t32, t33, t34, t35, t36]], dtype=np.float64)
        return jacob

    def disconnect(self):
        self.sock.close()
        print("Robot disconnected")

    def go2(self, t: float, s: int, n: int, q: [np.float64],
            k: [np.float64], x_d: [np.float64]):
        q_dot = np.array([0, 0, 0, 0, 0, 0], dtype=np.float64)

        q_plot = np.zeros((3, n))
        qd_plot = np.zeros((3, n))
        xd_plot = np.zeros((3, n))
        e_plot = np.zeros((3, n))
        v_plot = np.zeros((3, n))
        t_plot = np.arange(0, s, t)

        i = 0
        while i < n:
            try:
                e = x_d - q[:3]
                e_plot[:, i] = e
                if np.abs(np.mean(e)) < 1e-4:
                    break

                q_plot[:, i] = q[:3]
                qd_plot[:, i] = q_dot[:3]
                xd_plot[:, i] = x_d

                m = self.matrix(q)
                v = np.matmul(m, np.matmul(k, e))
                v_plot[:, i] = v

                q_dot[:3] = np.matmul(np.linalg.inv(m), v)
                q[:3] = q[:3] + q_dot[:3].ravel()*t

                i += 1

            except KeyboardInterrupt:
                break

        self.showGraphics(q, q_plot, qd_plot, xd_plot, e_plot,
                          v_plot, t_plot)

    def followTrajectory(self, t: float, s: int, n: int, q: [np.float64],
                         k: [np.float64], x_d: [np.float64],
                         loop: bool = False):
        q_dot = np.array([0, 0, 0, 0, 0, 0], dtype=np.float64)

        q_plot = np.zeros((3, n))
        qd_plot = np.zeros((3, n))
        xd_plot = np.zeros((3, n))
        e_plot = np.zeros((3, n))
        v_plot = np.zeros((3, n))
        t_plot = np.arange(0, s, t)

        length = x_d.shape[1]

        i = 0
        j = 0
        while i < n:
            try:
                e = x_d[:, j] - q[:3]
                e_plot[:, i] = e
                if np.abs(np.mean(e)) < 1e-4:
                    j += 1
                    if j == length and not loop:
                        break
                    elif j == length and loop:
                        j = j % length

                q_plot[:, i] = q[:3]
                qd_plot[:, i] = q_dot[:3]
                xd_plot[:, i] = x_d[:, j]

                m = self.matrix(q)
                v = np.matmul(m, np.matmul(k, e))
                v_plot[:, i] = v

                q_dot[:3] = np.matmul(np.linalg.inv(m), v)
                q[:3] = q[:3] + q_dot[:3].ravel()*t

                i += 1

            except KeyboardInterrupt:
                break

        self.showGraphics(q, q_plot, qd_plot, xd_plot, e_plot, v_plot, t_plot)

    def showGraphics(self, q: [np.float64],
                     q_plot: [np.float64],
                     qd_plot: [np.float64],
                     xd_plot: [np.float64],
                     e_plot: [np.float64],
                     v_plot: [np.float64],
                     t_plot: [np.float64]):
        plt.figure(1)
        dibujarMovil(L, q, p_b, a, d)
        plt.plot(q_plot[0, :], q_plot[1, :], 'y-', linewidth=2)

        plt.figure(2)
        plt.grid()

        plt.plot(t_plot, q_plot[0, :], '-', linewidth=2)
        plt.plot(t_plot, q_plot[1, :], '-', linewidth=2)
        plt.plot(t_plot, q_plot[2, :], '-', linewidth=2)
        plt.plot(t_plot, xd_plot[0, :], '-', linewidth=2)
        plt.plot(t_plot, xd_plot[1, :], '-', linewidth=2)
        plt.plot(t_plot, xd_plot[2, :], '-', linewidth=2)

        plt.title("Trajectory", fontsize=20)
        plt.xlabel('t', fontsize=15)
        plt.ylabel('q', fontsize=15)
        plt.legend(['x', 'y', '$\\theta$', '$x_d$', '$y_d$', '$\\theta_d$'])

        plt.figure(3)
        plt.grid()

        plt.plot(t_plot, qd_plot[0, :], '-', linewidth=2)
        plt.plot(t_plot, qd_plot[1, :], '-', linewidth=2)
        plt.plot(t_plot, qd_plot[2, :], '-', linewidth=2)

        plt.title("Control", fontsize=20)
        plt.xlabel('t', fontsize=15)
        plt.ylabel('$\\dot{q}$', fontsize=15)
        plt.legend(['x', 'y', '$\\theta$'])

        plt.figure(4)
        plt.grid()

        plt.plot(t_plot, e_plot[0, :], '-', linewidth=2)
        plt.plot(t_plot, e_plot[1, :], '-', linewidth=2)
        plt.plot(t_plot, e_plot[2, :], '-', linewidth=2)

        plt.title("Error", fontsize=20)
        plt.xlabel('t', fontsize=15)
        plt.ylabel('e', fontsize=15)
        plt.legend(['$e_x$', '$e_y$', '$e_\\theta$'])

        plt.figure(5)
        plt.grid()

        plt.plot(t_plot, v_plot[0, :], '-', linewidth=2)
        plt.plot(t_plot, v_plot[1, :], '-', linewidth=2)
        plt.plot(t_plot, v_plot[2, :], '-', linewidth=2)

        plt.title("Velocities", fontsize=20)
        plt.xlabel('t', fontsize=15)
        plt.ylabel('v', fontsize=15)
        plt.legend(['0', '1', '2'])

        plt.show()
