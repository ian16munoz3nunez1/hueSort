#!python3

# Ian Mu;oz Nu;ez - Omnidireccional de 3 ruedas

import numpy as np
import matplotlib.pyplot as plt


def dibujarMovil(L, q: [float], p_b: [float], a: [float], d: [float]):
    x = q[0]
    y = q[1]
    theta = q[2]
    x_t, y_t, z_t = p_b
    pi = np.pi

    ax = plt.axes(projection='3d')
    ax.axis('equal')
    ax.grid(True)
    lim = 0.3
    ax.set_xlim([-lim, lim])
    ax.set_ylim([-lim, lim])
    ax.set_zlim([-lim, lim])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.plot(x, y, 'yo', linewidth=3, markersize=5)

    Lo = L*0.1
    lo = L*0.2
    r_z1 = np.array([[np.cos(theta), -np.sin(theta), x],
                    [np.sin(theta), np.cos(theta), y],
                    [0, 0, 1]])
    r_z2 = np.array([[np.cos(theta+2*(pi/3)), -np.sin(theta+2*(pi/3)), x],
                    [np.sin(theta+2*(pi/3)), np.cos(theta+2*(pi/3)), y],
                    [0, 0, 1]])
    r_z3 = np.array([[np.cos(theta+4*(pi/3)), -np.sin(theta+4*(pi/3)), x],
                    [np.sin(theta+4*(pi/3)), np.cos(theta+4*(pi/3)), y],
                    [0, 0, 1]])
    w1 = np.array([[1, 0, L],
                   [0, 1, 0],
                   [0, 0, 1]])
    w2 = np.array([[1, 0, L],
                   [0, 1, 0],
                   [0, 0, 1]])
    w3 = np.array([[1, 0, L],
                   [0, 1, 0],
                   [0, 0, 1]])
    w1 = np.matmul(r_z1, w1)
    w2 = np.matmul(r_z2, w2)
    w3 = np.matmul(r_z3, w3)

    # Base
    phi = np.linspace(0, 2*pi, 50)

    cx = x + (L-Lo)*np.cos(phi)
    cy = y + (L-Lo)*np.sin(phi)
    ax.plot(cx, cy, 'c', linewidth=4)

    # pc = np.dot(r_z1, np.array([L*0.4, 0, 1]).reshape(-1, 1))
    # cx = pc[0] + L*0.15*np.cos(phi)
    # cy = pc[1] + L*0.15*np.sin(phi)
    # ax.plot(cx, cy, 'r', linewidth=4)

    # Ruedas
    p1 = np.dot(w1, np.array([+Lo, -lo, 1]).reshape(-1, 1))
    p2 = np.dot(w1, np.array([-Lo, -lo, 1]).reshape(-1, 1))
    p3 = np.dot(w1, np.array([+Lo, +lo, 1]).reshape(-1, 1))
    p4 = np.dot(w1, np.array([-Lo, +lo, 1]).reshape(-1, 1))
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'b-', linewidth=4)
    ax.plot([p1[0], p3[0]], [p1[1], p3[1]], 'b-', linewidth=4)
    ax.plot([p2[0], p4[0]], [p2[1], p4[1]], 'b-', linewidth=4)
    ax.plot([p3[0], p4[0]], [p3[1], p4[1]], 'b-', linewidth=4)

    p1 = np.dot(w2, np.array([+Lo, -lo, 1]).reshape(-1, 1))
    p2 = np.dot(w2, np.array([-Lo, -lo, 1]).reshape(-1, 1))
    p3 = np.dot(w2, np.array([+Lo, +lo, 1]).reshape(-1, 1))
    p4 = np.dot(w2, np.array([-Lo, +lo, 1]).reshape(-1, 1))
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'b-', linewidth=4)
    ax.plot([p1[0], p3[0]], [p1[1], p3[1]], 'b-', linewidth=4)
    ax.plot([p2[0], p4[0]], [p2[1], p4[1]], 'b-', linewidth=4)
    ax.plot([p3[0], p4[0]], [p3[1], p4[1]], 'b-', linewidth=4)

    p1 = np.dot(w3, np.array([+Lo, -lo, 1]).reshape(-1, 1))
    p2 = np.dot(w3, np.array([-Lo, -lo, 1]).reshape(-1, 1))
    p3 = np.dot(w3, np.array([+Lo, +lo, 1]).reshape(-1, 1))
    p4 = np.dot(w3, np.array([-Lo, +lo, 1]).reshape(-1, 1))
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'b-', linewidth=4)
    ax.plot([p1[0], p3[0]], [p1[1], p3[1]], 'b-', linewidth=4)
    ax.plot([p2[0], p4[0]], [p2[1], p4[1]], 'b-', linewidth=4)
    ax.plot([p3[0], p4[0]], [p3[1], p4[1]], 'b-', linewidth=4)

    # Manipulador
    wt1 = np.array([[np.cos(theta), 0, -np.sin(theta), x_t*np.cos(theta) - y_t*np.sin(theta) + x],
                    [np.sin(theta), 0, np.cos(theta), x_t*np.sin(theta) + y_t*np.cos(theta) + y],
                    [0, 1, 0, z_t + d[0]],
                    [0, 0, 0, 1]], dtype=np.float64)
    ax.plot3D(wt1[0, 3], wt1[1, 3], wt1[2, 3], 'ko')

    wt2 = np.array([[np.cos(theta)*np.cos(q[4]), -np.cos(theta)*np.sin(q[4]), -np.sin(theta), x + x_t*np.cos(theta) - y_t*np.sin(theta) + a[1]*np.cos(theta)*np.cos(q[4])],
                    [np.sin(theta)*np.cos(q[4]), -np.sin(theta)*np.sin(q[4]), np.cos(theta), y + x_t*np.sin(theta) + y_t*np.cos(theta) + a[1]*np.sin(theta)*np.cos(q[4])],
                    [np.sin(q[4]), np.cos(q[4]), 0, z_t + d[0] + a[1]*np.sin(q[4])],
                    [0, 0, 0, 1]], dtype=np.float64)
    ax.plot3D(wt2[0, 3], wt2[1, 3], wt2[2, 3], 'ko')
    ax.plot3D([wt1[0, 3], wt2[0, 3]], [wt1[1, 3], wt2[1, 3]], [wt1[2, 3], wt2[2, 3]], 'k-', linewidth=2)

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

    t14 = x + x_t*np.cos(q[2]) - y_t*np.sin(q[2]) + np.cos(q[2])*(a[1]*np.cos(q[4]) + a[2]*np.cos(q[4]+q[5]))
    t24 = y + x_t*np.sin(q[2]) + y_t*np.cos(q[2]) + np.sin(q[2])*(a[1]*np.cos(q[4]) + a[2]*np.cos(q[4]+q[5]))
    t34 = z_t + d[0] + a[1]*np.sin(q[4]) + a[2]*np.sin(q[4]+q[5])
    t44 = 1

    wte = np.array([[t11, t12, t13, t14],
                    [t21, t22, t23, t24],
                    [t31, t32, t33, t34],
                    [t41, t42, t43, t44]], dtype=np.float64)
    ax.plot3D([wt2[0, 3], wte[0, 3]], [wt2[1, 3], wte[1, 3]], [wt2[2, 3], wte[2, 3]], 'k-', linewidth=2)
