#ifndef MOTOR_H
#define MOTOR_H

#include <Arduino.h>

class Motor
{
private:
    int forward_pin;
    int backward_pin;

public:
    Motor(int, int);

    void setVelocity(int);
    void stop();
};

#endif//MOTOR_H
