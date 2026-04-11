#include "motor.h"

Motor::Motor(int forward, int backward)
{
    this->forward_pin = forward;
    this->backward_pin = backward;

    pinMode(this->forward_pin, OUTPUT);
    pinMode(this->backward_pin, OUTPUT);
}

void Motor::setVelocity(int velocity)
{
    if(velocity == 0)
    {
        analogWrite(forward_pin, 0);
        analogWrite(backward_pin, 0);
    }

    if(velocity > 0)
    {
        int v = map(velocity, 0, 100, 0, 255);
        analogWrite(backward_pin, 0);
        analogWrite(forward_pin, v);
    }

    if(velocity < 0)
    {
        int v = map(abs(velocity), 0, 100, 0, 255);
        analogWrite(forward_pin, 0);
        analogWrite(backward_pin, v);
    }
}

void Motor::stop()
{
    analogWrite(forward_pin, 0);
    analogWrite(backward_pin, 0);
}
