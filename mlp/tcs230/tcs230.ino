// TCS230

#define S0 32
#define S1 33
#define S2 25
#define S3 26
#define out 27

int freqR = 0;
int freqG = 0;
int freqB = 0;

void setup()
{
    pinMode(S0, OUTPUT);
    pinMode(S1, OUTPUT);
    pinMode(S2, OUTPUT);
    pinMode(S3, OUTPUT);
    pinMode(out, INPUT);

    digitalWrite(S0, HIGH);
    digitalWrite(S1, LOW);

    Serial.begin(115200);
    // Serial.setTimeout(10);
    // while(!Serial){}
}

void loop()
{
    String rgb;

    // Filtro rojo de lectura
    digitalWrite(S2, LOW);
    digitalWrite(S3, LOW);
    delay(100);
    freqR = pulseIn(out, LOW);
    delay(100);

    // Filtro verde de lectura
    digitalWrite(S2, HIGH);
    digitalWrite(S3, HIGH);
    delay(100);
    freqG = pulseIn(out, LOW);
    delay(100);

    // Filtro azul de lectura
    digitalWrite(S2, LOW);
    digitalWrite(S3, HIGH);
    delay(100);
    freqB = pulseIn(out, LOW);
    delay(100);

    rgb = String(freqR) + "-" + String(freqG) + "-" + String(freqB);
    Serial.println(rgb);
}
