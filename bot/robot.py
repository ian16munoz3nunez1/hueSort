import socket
import errno
import numpy as np
import os

pi = np.pi
L = 0.08
p_b = [0.07, 0.0, 0.085]
a = [0, 0.05, 0.05]
d = [0, 0, 0]
x_t, y_t, z_t = p_b


class Robot:
    def __init__(self):
        if not os.path.isdir("./data/"):
            os.mkdir("./data/")

        q_file = "./data/q.csv"
        qd_file = "./data/q_dot.csv"
        xd_file = "./data/x_d.csv"
        e_file = "./data/e.csv"
        v_file = "./data/v.csv"
        x_file = "./data/x.csv"

        self.q_plot = open(q_file, 'a')
        self.qd_plot = open(qd_file, 'a')
        self.xd_plot = open(xd_file, 'a')
        self.e_plot = open(e_file, 'a')
        self.v_plot = open(v_file, 'a')
        self.x_plot = open(x_file, 'a')

        if os.path.getsize(q_file) == 0:
            self.q_plot.write("t,x_b,y_b,theta_b,theta_2,theta_3\n")
        if os.path.getsize(qd_file) == 0:
            self.qd_plot.write("t,x_b,y_b,theta_b,theta_2,theta_3\n")
        if os.path.getsize(xd_file) == 0:
            self.xd_plot.write("t,x_b,y_b,theta_b,x,y,z\n")
        if os.path.getsize(e_file) == 0:
            self.e_plot.write("t,x_b,y_b,theta_b,x,y,z\n")
        if os.path.getsize(v_file) == 0:
            self.v_plot.write("t,v_1,v_2,v_3\n")
        if os.path.getsize(x_file) == 0:
            self.x_plot.write("t,x,y,z\n")

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

    def disconnect(self):
        self.sock.close()
        print("Robot disconnected")

        self.q_plot.close()
        print("File q.csv closed")
        self.qd_plot.close()
        print("File q_dot.csv closed")
        self.xd_plot.close()
        print("File x_d.csv closed")
        self.e_plot.close()
        print("File e.csv closed")
        self.v_plot.close()
        print("File v.csv closed")
        self.x_plot.close()
        print("File x.csv closed")

    def writeHome(self):
        q = np.array([0, 0, 0, pi/4, -pi/4])

        with open("./data/pose.dat", 'w') as pose:
            for i in range(5):
                pose.write(f"{q[i]}\n")
        pose.close()

    def writePose(self, q):
        with open("./data/pose.dat", 'w') as pose:
            for i in range(5):
                pose.write(f"{q[i]}\n")
        pose.close()

    def readPose(self):
        try:
            q = np.ndarray((5,), dtype=np.float64)
            with open("./data/pose.dat", 'r') as pose:
                for i in range(5):
                    q[i] = np.float64(pose.readline())
            pose.close()

        except Exception as e:
            print(f"Unable to read pose from file: {e}")
            q = np.array([0, 0, 0, pi/4, -pi/4])

        print("==== Pose ==== ")
        print(f"x: {q[0]}")
        print(f"y: {q[1]}")
        print(f"theta: {q[2]}")
        print(f"theta_2: {q[3]}")
        print(f"theta_3: {q[4]}")
        print("==== Pose ==== ")

        return q

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
        t11 = np.cos(q[2])*np.cos(q[3] + q[4])
        t21 = np.sin(q[2])*np.cos(q[3] + q[4])
        t31 = np.sin(q[3] + q[4])
        t41 = 0

        t12 = -np.cos(q[2])*np.sin(q[3] + q[4])
        t22 = -np.sin(q[2])*np.sin(q[3] + q[4])
        t32 = np.cos(q[3] + q[4])
        t42 = 0

        t13 = -np.sin(q[2])
        t23 = np.cos(q[2])
        t33 = 0
        t43 = 0

        t14 = q[0] + x_t*np.cos(q[2]) - y_t*np.sin(q[2]) + np.cos(q[2])*(a[1]*np.cos(q[3]) + a[2]*np.cos(q[3] + q[4]))
        t24 = q[1] + x_t*np.sin(q[2]) + y_t*np.cos(q[2]) + np.sin(q[2])*(a[1]*np.cos(q[3]) + a[2]*np.cos(q[3] + q[4]))
        t34 = z_t + d[0] + a[1]*np.sin(q[3]) + a[2]*np.sin(q[3]+q[4])
        t44 = 1

        wte = np.array([[t11, t12, t13, t14],
                        [t21, t22, t23, t24],
                        [t31, t32, t33, t34],
                        [t41, t42, t43, t44]], dtype=np.float64)
        return wte

    def j_v(self, q: np.ndarray) -> np.ndarray:
        t11, t21, t31 = 1, 0, 0
        t12, t22, t32 = 0, 1, 0

        t13 = -x_t*np.sin(q[2]) - y_t*np.cos(q[2]) - np.sin(q[2])*(a[1]*np.cos(q[3])+a[2]*np.cos(q[3]+q[4]))
        t23 = x_t*np.cos(q[2]) - y_t*np.sin(q[2]) + np.cos(q[2])*(a[1]*np.cos(q[3])+a[2]*np.cos(q[3]+q[4]))
        t33 = 0

        t14 = -a[1]*np.cos(q[2])*np.sin(q[3]) - a[2]*np.cos(q[2])*np.sin(q[3]+q[4])
        t24 = -a[1]*np.sin(q[2])*np.sin(q[3]) - a[2]*np.sin(q[2])*np.sin(q[3]+q[4])
        t34 = a[1]*np.cos(q[3]) + a[2]*np.cos(q[3]+q[4])

        t15 = -a[2]*np.cos(q[2])*np.sin(q[3]+q[4])
        t25 = -a[2]*np.sin(q[2])*np.sin(q[3]+q[4])
        t35 = a[2]*np.cos(q[3]+q[4])

        jacob = np.array([[t11, t12, t13, t14, t15],
                          [t21, t22, t23, t24, t25],
                          [t31, t32, t33, t34, t35]], dtype=np.float64)
        return jacob

    def go2(self, t: float, n: int, q: np.ndarray((5,), dtype=np.float64),
            k: np.ndarray((3, 3), dtype=np.float64),
            x_d: np.ndarray((3,), dtype=np.float64)):
        q_dot = np.array([0, 0, 0, 0, 0], dtype=np.float64)

        try:
            with open("./data/last_time.dat", 'r') as file:
                last = np.float64(file.readline())
            file.close()

        except Exception:
            last = 0

        i = 0
        while i < n:
            try:
                e = x_d - q[:3]
                self.e_plot.write(f"{last + (i*t)},{e[0]},{e[1]},{e[2]},0,0,0\n")
                if np.abs(np.mean(e)) < 1e-4:
                    break

                self.q_plot.write(f"{last + (i*t)},{q[0]},{q[1]},{q[2]},{q[3]},{q[4]}\n")
                self.qd_plot.write(f"{last + (i*t)},{q_dot[0]},{q_dot[1]},{q_dot[2]},{q_dot[3]},{q_dot[4]}\n")
                self.xd_plot.write(f"{last + (i*t)},{x_d[0]},{x_d[1]},{x_d[2]},0,0,0\n")

                m = self.matrix(q)
                v = np.matmul(m, np.matmul(k, e))
                self.v_plot.write(f"{last + (i*t)},{v[0]},{v[1]},{v[2]}\n")

                q_dot[:3] = np.matmul(np.linalg.inv(m), v)
                q[:3] = q[:3] + q_dot[:3].ravel()*t

                i += 1

            except KeyboardInterrupt:
                break

        with open("./data/last_time.dat", 'w') as file:
            file.write(f"{last + (i*t)}")
        file.close()

        return q

    def followTrajectory(self, t: float, n: int,
                         q: np.ndarray((5,), dtype=np.float64),
                         k: np.ndarray((3, 3), dtype=np.float64),
                         x_d: np.ndarray((3,), dtype=np.float64),
                         loop: bool = False):
        q_dot = np.array([0, 0, 0, 0, 0], dtype=np.float64)

        try:
            with open("./data/last_time.dat", 'r') as file:
                last = np.float64(file.readline())
            file.close()

        except Exception:
            last = 0

        length = x_d.shape[1]

        i = 0
        j = 0
        while i < n:
            try:
                e = x_d[:, j] - q[:3]
                self.e_plot.write(f"{last + (i*t)},{e[0]},{e[1]},{e[2]},0,0,0\n")
                if np.abs(np.mean(e)) < 1e-4:
                    j += 1
                    if j == length and not loop:
                        break
                    elif j == length and loop:
                        j = j % length

                self.q_plot.write(f"{last + (i*t)},{q[0]},{q[1]},{q[2]},{q[3]},{q[4]}\n")
                self.qd_plot.write(f"{last + (i*t)},{q_dot[0]},{q_dot[1]},{q_dot[2]},{q_dot[3]},{q_dot[4]}\n")
                self.xd_plot.write(f"{last + (i*t)},{x_d[0, j]},{x_d[1, j]},{x_d[2, j]},0,0,0\n")

                m = self.matrix(q)
                v = np.matmul(m, np.matmul(k, e))
                self.v_plot.write(f"{last + (i*t)},{v[0]},{v[1]},{v[2]}\n")

                q_dot[:3] = np.matmul(np.linalg.inv(m), v)
                q[:3] = q[:3] + q_dot[:3].ravel()*t

                i += 1

            except KeyboardInterrupt:
                break

        with open("./data/last_time.dat", 'w') as file:
            file.write(f"{last + (i*t)}")
        file.close()

        return q

    def ee2(self, t: float, n: int,
            q: np.ndarray((5,), dtype=np.float64),
            k: np.ndarray((3, 3), dtype=np.float64),
            x_d: np.ndarray((3,), dtype=np.float64)):
        q_dot = np.array([0, 0, 0, 0, 0])

        try:
            with open("./data/last_time.dat", 'r') as file:
                last = np.float64(file.readline())
            file.close()

        except Exception:
            last = 0

        i = 0
        while i < n:
            try:
                x_i = self.wTe(q)[:3, 3]
                self.x_plot.write(f"{last + (i*t)},{x_i[0]},{x_i[1]},{x_i[2]}\n")

                e = x_d - x_i
                self.e_plot.write(f"{last + (i*t)},0,0,0,{e[0]},{e[1]},{e[2]}\n")

                self.q_plot.write(f"{last + (i*t)},{q[0]},{q[1]},{q[2]},{q[3]},{q[4]}\n")
                self.qd_plot.write(f"{last + (i*t)},{q_dot[0]},{q_dot[1]},{q_dot[2]},{q_dot[3]},{q_dot[4]}\n")
                self.xd_plot.write(f"{last + (i*t)},0,0,0,{x_d[0]},{x_d[1]},{x_d[2]}\n")

                v = np.matmul(self.matrix(q), q_dot[:3])
                self.v_plot.write(f"{last + (i*t)},{v[0]},{v[1]},{v[2]}\n")

                if np.abs(np.mean(e)) < 1e-4:
                    break

                j = np.linalg.pinv(self.j_v(q))
                q_dot = np.matmul(j, np.matmul(k, e))
                q = q + q_dot*t

                i += 1

            except KeyboardInterrupt:
                break

        with open("./data/last_time.dat", 'w') as file:
            file.write(f"{last + (i*t)}")
        file.close()

        return q
