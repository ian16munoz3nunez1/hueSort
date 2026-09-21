#include "arm.h"
#include <ESP32PWM.h>

Arm::Arm(int q1, int q2)
{
    ESP32PWM::allocateTimer(0);
    ESP32PWM::allocateTimer(1);

    q_1.setPeriodHertz(50);
    q_2.setPeriodHertz(50);

    q_1.attach(q1, 600, 2400);
    q_2.attach(q2, 600, 2400);
}

Arm::~Arm()
{
}

int* Arm::getPose()
{
    return currentPose;
}

void Arm::setPose(int theta_1, int theta_2)
{
    theta_1 = constrain(theta_1, 0, 120);
    theta_2 = constrain(theta_2, 0, 120);

    if(currentPose[0] < theta_1)
    {
        for(int i = currentPose[0]; i <= theta_1; i += 2)
        {
            q_1.write(i);
            delay(10);
        }
    }

    if(currentPose[0] > theta_1)
    {
        for(int i = currentPose[0]; i >= theta_1; i -= 2)
        {
            q_1.write(i);
            delay(10);
        }
    }

    if(currentPose[1] < theta_2)
    {
        for(int i = currentPose[1]; i <= theta_2; i += 2)
        {
            q_2.write(i);
            delay(10);
        }
    }

    if(currentPose[1] > theta_2)
    {
        for(int i = currentPose[1]; i >= theta_2; i -= 2)
        {
            q_2.write(i);
            delay(10);
        }
    }

    currentPose[0] = theta_1;
    currentPose[1] = theta_2;
}
