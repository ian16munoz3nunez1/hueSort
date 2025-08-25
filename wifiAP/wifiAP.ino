#include <WiFi.h>
#include <WiFiAP.h>

#define LED 2

const char *ssid = "esp32net";
const char *password = "ciNNam0n2412";
IPAddress ip(192,168,4,1);
IPAddress gateway(192,168,4,1);
IPAddress subnet(255,255,255,0);

void blink(int);

void setup()
{
  Serial.begin(115200);
  pinMode(LED, OUTPUT);
  WiFi.mode(WIFI_AP);
  WiFi.softAPConfig(ip, gateway, subnet);
  blink(1);

  if(!WiFi.softAP(ssid, password))
  {
    log_e("Soft AP creation failed");
    while(1);
  }
  else
  {
    blink(2);
    // IPAddress myIP = WiFi.softAPIP();
    // Serial.print("AP IP: ");
    // Serial.println(myIP);
  }

}

void loop()
{
}

void blink(int x)
{
  for(int i = 0; i < x; i++)
  {
    digitalWrite(LED, HIGH);
    delay(500);
    digitalWrite(LED, LOW);
    delay(500);
  }
}
