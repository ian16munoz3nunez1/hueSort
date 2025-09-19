#include "led.h"

Led::Led(int pin)
{
    this->pin = pin;
    pinMode(this->pin, OUTPUT);
}

void Led::on()
{
    digitalWrite(pin, HIGH);
}

void Led::off()
{
    digitalWrite(pin, LOW);
}

void Led::blink(int times, int time)
{
    for(int i = 0; i < times; i++)
    {
        digitalWrite(pin, HIGH);
        delay(time);
        digitalWrite(pin, LOW);
        delay(time);
    }
}

