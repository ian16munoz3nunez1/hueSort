#ifndef ARM_H
#define ARM_H

#include <Arduino.h>
#include <ESP32Servo.h>

class Arm
{
private:
    Servo q_1;
    Servo q_2;
    int currentPose[2] = {0, 0};

public:
    Arm(int, int);
    ~Arm();

    int* getPose();
    void setPose(int, int);
};

#endif//ARM_H
