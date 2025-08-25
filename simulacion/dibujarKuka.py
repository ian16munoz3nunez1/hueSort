import numpy as np
import matplotlib.pyplot as plt
pi = np.pi

def dibujar_kuka(p, q, p_plot=None, x_plot=None):
    alpha = np.array([pi/2, 0.0, 0.0, 0.0])
    a = np.array([0.0, 0.155, 0.135, 0.217])
    d = np.array([0.147, 0.0, 0.0, 0.0])

    #### Configuracion de la grafica
    fig = plt.figure(1)
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title("Kuka", fontsize=20)
    ax.set_xlabel('x', fontsize=15)
    ax.set_ylabel('y', fontsize=15)
    ax.set_zlabel('z', fontsize=15)
    ax.axis('equal')
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-3.5, 3.5)
    ax.set_zlim(0, 1)

    #### Matriz del eje global al de la plataforma
    wTp = np.array([[np.cos(p[2]), -np.sin(p[2]), 0.0, p[0]],
                    [np.sin(p[2]), np.cos(p[2]), 0.0, p[1]],
                    [0.0, 0.0, 1.0, 0.0],
                    [0.0, 0.0, 0.0, 1.0]])
    #### Matriz del eje de la plataforma a la base del manipulador
    pTb = np.array([[1.0, 0.0, 0.0, 0.170],
                    [0.0, 1.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0, 0.060],
                    [0.0, 0.0, 0.0, 1.0]])
    #### Matrices de transformacion
    t01 = np.array([[np.cos(q[0]), 0.0, np.sin(q[0]), 0.0],
                    [np.sin(q[0]), 0.0, -np.cos(q[0]), 0.0],
                    [0.0, 1.0, 0.0, d[0]],
                    [0.0, 0.0, 0.0, 1.0]])
    t12 = np.array([[np.cos(q[1]), -np.sin(q[1]), 0.0, a[1]*np.cos(q[1])],
                    [np.sin(q[1]), np.cos(q[1]), 0.0, a[1]*np.sin(q[1])],
                    [0.0, 0.0, 1.0, 0.0],
                    [0.0, 0.0, 0.0, 1.0]])
    t23 = np.array([[np.cos(q[2]), -np.sin(q[2]), 0.0, a[2]*np.cos(q[2])],
                    [np.sin(q[2]), np.cos(q[2]), 0.0, a[2]*np.sin(q[2])],
                    [0.0, 0.0, 1.0, 0.0],
                    [0.0, 0.0, 0.0, 1.0]])
    t34 = np.array([[np.cos(q[3]), -np.sin(q[3]), 0.0, a[3]*np.cos(q[3])],
                    [np.sin(q[3]), np.cos(q[3]), 0.0, a[3]*np.sin(q[3])],
                    [0.0, 0.0, 1.0, 0.0],
                    [0.0, 0.0, 0.0, 1.0]])

    t1 = wTp
    t2 = np.matmul(t1, pTb)
    t3 = np.matmul(t2, t01)
    t4 = np.matmul(t3, t12)
    t5 = np.matmul(t4, t23)
    t6 = np.matmul(t5, t34)

    #### Manipulador
    ax.plot(t2[0, 3], t2[1, 3], t2[2, 3], 'yo', linewidth=4, markersize=8)
    ax.plot(t3[0, 3], t3[1, 3], t3[2, 3], 'yo', linewidth=4, markersize=8)
    ax.plot(t4[0, 3], t4[1, 3], t4[2, 3], 'yo', linewidth=4, markersize=8)
    ax.plot(t5[0, 3], t5[1, 3], t5[2, 3], 'yo', linewidth=4, markersize=8)
    ax.plot([t2[0, 3], t3[0, 3]], [t2[1, 3], t3[1, 3]], [t2[2, 3], t3[2, 3]], 'y-', linewidth=4, markersize=8)
    ax.plot([t3[0, 3], t4[0, 3]], [t3[1, 3], t4[1, 3]], [t3[2, 3], t4[2, 3]], 'y-', linewidth=4, markersize=8)
    ax.plot([t4[0, 3], t5[0, 3]], [t4[1, 3], t5[1, 3]], [t4[2, 3], t5[2, 3]], 'y-', linewidth=4, markersize=8)
    ax.plot([t5[0, 3], t6[0, 3]], [t5[1, 3], t6[1, 3]], [t5[2, 3], t6[2, 3]], 'y-', linewidth=4, markersize=8)

    #### Trayectorias seguidas
    if p_plot is not None:
        ax.plot(p_plot[0, :], p_plot[1, :], 'r-', linewidth=2, markersize=8)
    if x_plot is not None:
        ax.plot(x_plot[0, :], x_plot[1, :], x_plot[2, :], 'g-', linewidth=2, markersize=8)

    #### Base del robot
    x = p[0]
    y = p[1]
    theta = p[2]
    L = 0.471/2
    l = 0.3/2

    Lo = L*0.3
    lo = L*0.2
    r_z = np.array([[np.cos(theta), -np.sin(theta), x],
                    [np.sin(theta), np.cos(theta), y],
                    [0.0, 0.0, 1.0]])
    lf = np.array([[1.0, 0.0, L], [0.0, 1.0, l], [0.0, 0.0, 1.0]])
    rf = np.array([[1.0, 0.0, L], [0.0, 1.0, -l], [0.0, 0.0, 1.0]])
    lb = np.array([[1.0, 0.0, -L], [0.0, 1.0, l], [0.0, 0.0, 1.0]])
    rb = np.array([[1.0, 0.0, -L], [0.0, 1.0, -l], [0.0, 0.0, 1.0]])

    rzlf = np.matmul(r_z, lf)
    rzrf = np.matmul(r_z, rf)
    rzlb = np.matmul(r_z, lb)
    rzrb = np.matmul(r_z, rb)

    p1 = np.matmul(r_z, np.array([+L+Lo, -l+lo, 1.0]).reshape(-1, 1))
    p2 = np.matmul(r_z, np.array([-L-Lo, -l+lo, 1.0]).reshape(-1, 1))
    p3 = np.matmul(r_z, np.array([+L+Lo, +l-lo, 1.0]).reshape(-1, 1))
    p4 = np.matmul(r_z, np.array([-L-Lo, +l-lo, 1.0]).reshape(-1, 1))
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'm-', linewidth=4, markersize=8)
    ax.plot([p1[0], p3[0]], [p1[1], p3[1]], 'm-', linewidth=4, markersize=8)
    ax.plot([p2[0], p4[0]], [p2[1], p4[1]], 'm-', linewidth=4, markersize=8)
    ax.plot([p3[0], p4[0]], [p3[1], p4[1]], 'm-', linewidth=4, markersize=8)

    #### Rueda izquierda delantera
    p1 = np.matmul(rzlf, np.array([+Lo, -lo, 1.0]))
    p2 = np.matmul(rzlf, np.array([-Lo, -lo, 1.0]))
    p3 = np.matmul(rzlf, np.array([+Lo, +lo, 1.0]))
    p4 = np.matmul(rzlf, np.array([-Lo, +lo, 1.0]))
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'c-', linewidth=4, markersize=8)
    ax.plot([p1[0], p3[0]], [p1[1], p3[1]], 'c-', linewidth=4, markersize=8)
    ax.plot([p2[0], p4[0]], [p2[1], p4[1]], 'c-', linewidth=4, markersize=8)
    ax.plot([p3[0], p4[0]], [p3[1], p4[1]], 'c-', linewidth=4, markersize=8)

    #### Rueda derecha delantera
    p1 = np.matmul(rzrf, np.array([+Lo, -lo, 1.0]))
    p2 = np.matmul(rzrf, np.array([-Lo, -lo, 1.0]))
    p3 = np.matmul(rzrf, np.array([+Lo, +lo, 1.0]))
    p4 = np.matmul(rzrf, np.array([-Lo, +lo, 1.0]))
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'c-', linewidth=4, markersize=8)
    ax.plot([p1[0], p3[0]], [p1[1], p3[1]], 'c-', linewidth=4, markersize=8)
    ax.plot([p2[0], p4[0]], [p2[1], p4[1]], 'c-', linewidth=4, markersize=8)
    ax.plot([p3[0], p4[0]], [p3[1], p4[1]], 'c-', linewidth=4, markersize=8)

    #### Rueda izquierda trasera
    p1 = np.matmul(rzlb, np.array([+Lo, -lo, 1.0]))
    p2 = np.matmul(rzlb, np.array([-Lo, -lo, 1.0]))
    p3 = np.matmul(rzlb, np.array([+Lo, +lo, 1.0]))
    p4 = np.matmul(rzlb, np.array([-Lo, +lo, 1.0]))
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'c-', linewidth=4, markersize=8)
    ax.plot([p1[0], p3[0]], [p1[1], p3[1]], 'c-', linewidth=4, markersize=8)
    ax.plot([p2[0], p4[0]], [p2[1], p4[1]], 'c-', linewidth=4, markersize=8)
    ax.plot([p3[0], p4[0]], [p3[1], p4[1]], 'c-', linewidth=4, markersize=8)

    #### Rueda derecha trasera
    p1 = np.matmul(rzrb, np.array([+Lo, -lo, 1.0]))
    p2 = np.matmul(rzrb, np.array([-Lo, -lo, 1.0]))
    p3 = np.matmul(rzrb, np.array([+Lo, +lo, 1.0]))
    p4 = np.matmul(rzrb, np.array([-Lo, +lo, 1.0]))
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'c-', linewidth=4, markersize=8)
    ax.plot([p1[0], p3[0]], [p1[1], p3[1]], 'c-', linewidth=4, markersize=8)
    ax.plot([p2[0], p4[0]], [p2[1], p4[1]], 'c-', linewidth=4, markersize=8)
    ax.plot([p3[0], p4[0]], [p3[1], p4[1]], 'c-', linewidth=4, markersize=8)

