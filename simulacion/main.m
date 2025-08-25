close all
clear
clc

syms x_p y_p theta a_4 a_3 a_2 d_1 theta1 theta2 theta3 theta4

%% YouBot
% tx = cos(theta1) * (a_4*cos(theta2+theta3+theta4) + a_3*cos(theta2+theta3) + a_2*cos(theta2));
% ty = sin(theta1) * (a_4*cos(theta2+theta3+theta4) + a_3*cos(theta2+theta3) + a_2*cos(theta2));
% tz = a_4*sin(theta2+theta3+theta4) + a_3*sin(theta2+theta3) + a_2*sin(theta2) + d_1;

%% Kuka-YouBot
tx = cos(theta+theta1) * ( a_4*cos(theta2+theta3+theta4) + a_3*cos(theta2+theta3) + a_2*cos(theta2) ) + 0.145*cos(theta) + x_p;
ty = sin(theta+theta1) * ( a_4*cos(theta2+theta3+theta4) + a_3*cos(theta2+theta3) + a_2*cos(theta2) ) + 0.145*sin(theta) + y_p;
tz = a_4*sin(theta2+theta3+theta4) + a_3*sin(theta2+theta3) + a_2*sin(theta2) + d_1 + 0.140;

disp('----tx----')
diff(tx, x_p)
diff(tx, y_p)
diff(tx, theta)
diff(tx, theta1)
diff(tx, theta2)
diff(tx, theta3)
diff(tx, theta4)

disp('----ty----')
diff(ty, x_p)
diff(ty, y_p)
diff(ty, theta)
diff(ty, theta1)
diff(ty, theta2)
diff(ty, theta3)
diff(ty, theta4)

disp('----tz----')
diff(tz, x_p)
diff(tz, y_p)
diff(tz, theta)
diff(tz, theta1)
diff(tz, theta2)
diff(tz, theta3)
diff(tz, theta4)

