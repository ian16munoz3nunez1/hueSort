#ifndef LED_H
#define LED_H

#include <Arduino.h>

class Led
{
private:
    int pin;

public:
    Led(int);

    void on();
    void off();
    void blink(int, int);
};

#endif//LED_H
