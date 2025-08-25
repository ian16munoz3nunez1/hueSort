import numpy as np
import matplotlib.pyplot as plt
pi = np.pi

def dibujarOmni3(p, L):
    x = p[0]
    y = p[1]
    theta = p[2]

    plt.axis('equal')
    plt.grid()
    plt.xlabel('x', fontsize=15)
    plt.ylabel('y', fontsize=15)
    # plt.plot(x, y, 'yo', fillstyle='none', linewidth=12, markersize=12)
    plt.plot(x, y, 'yo', markersize=12)

    Lo = L*0.2
    lo = L*0.4
    rz1 = np.array([[np.cos(theta), -np.sin(theta), x],
                     [np.sin(theta), np.cos(theta), y],
                     [0, 0, 1]])
    rz2 = np.array([[np.cos(theta+2*pi/3), -np.sin(theta+2*pi/3), x],
                     [np.sin(theta+2*pi/3), np.cos(theta+2*pi/3), y],
                     [0, 0, 1]])
    rz3 = np.array([[np.cos(theta+4*pi/3), -np.sin(theta+4*pi/3), x],
                     [np.sin(theta+4*pi/3), np.cos(theta+4*pi/3), y],
                     [0, 0, 1]])
    m1 = np.array([[1, 0, L],
                   [0, 1, 0],
                   [0, 0, 1]])
    m2 = np.array([[1, 0, L],
                   [0, 1, 0],
                   [0, 0, 1]])
    m3 = np.array([[1, 0, L],
                   [0, 1, 0],
                   [0, 0, 1]])
    r_z1 = np.matmul(rz1, m1)
    r_z2 = np.matmul(rz2, m2)
    r_z3 = np.matmul(rz3, m3)

    ## Ruedas
    p1 = np.matmul(r_z1, np.array([[+Lo], [-lo], [1]]))
    p2 = np.matmul(r_z1, np.array([[-Lo], [-lo], [1]]))
    p3 = np.matmul(r_z1, np.array([[+Lo], [+lo], [1]]))
    p4 = np.matmul(r_z1, np.array([[-Lo], [+lo], [1]]))
    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'b-', linewidth=4)
    plt.plot([p1[0], p3[0]], [p1[1], p3[1]], 'b-', linewidth=4)
    plt.plot([p2[0], p4[0]], [p2[1], p4[1]], 'b-', linewidth=4)
    plt.plot([p3[0], p4[0]], [p3[1], p4[1]], 'b-', linewidth=4)

    p1 = np.matmul(r_z2, np.array([[+Lo], [-lo], [1]]))
    p2 = np.matmul(r_z2, np.array([[-Lo], [-lo], [1]]))
    p3 = np.matmul(r_z2, np.array([[+Lo], [+lo], [1]]))
    p4 = np.matmul(r_z2, np.array([[-Lo], [+lo], [1]]))
    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'b-', linewidth=4)
    plt.plot([p1[0], p3[0]], [p1[1], p3[1]], 'b-', linewidth=4)
    plt.plot([p2[0], p4[0]], [p2[1], p4[1]], 'b-', linewidth=4)
    plt.plot([p3[0], p4[0]], [p3[1], p4[1]], 'b-', linewidth=4)

    p1 = np.matmul(r_z3, np.array([[+Lo], [-lo], [1]]))
    p2 = np.matmul(r_z3, np.array([[-Lo], [-lo], [1]]))
    p3 = np.matmul(r_z3, np.array([[+Lo], [+lo], [1]]))
    p4 = np.matmul(r_z3, np.array([[-Lo], [+lo], [1]]))
    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'b-', linewidth=4)
    plt.plot([p1[0], p3[0]], [p1[1], p3[1]], 'b-', linewidth=4)
    plt.plot([p2[0], p4[0]], [p2[1], p4[1]], 'b-', linewidth=4)
    plt.plot([p3[0], p4[0]], [p3[1], p4[1]], 'b-', linewidth=4)

    ## Base
    phi = np.linspace(0, 2*pi, 50)

    cx = x + (L-Lo) * np.cos(phi)
    cy = y + (L-Lo) * np.sin(phi)
    plt.plot(cx, cy, 'c', linewidth=4)

    pc = np.matmul(rz1, np.array([[L*0.4], [0], [1]]))
    cx = pc[0] + L*0.15 * np.cos(phi)
    cy = pc[1] + L*0.15 * np.sin(phi)
    plt.plot(cx, cy, 'r-', linewidth=4)

