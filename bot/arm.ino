#include <WiFi.h>
#include "arm.h"

WiFiServer server(9999);

const char* ssid = "IZZI-BC36";
const char* password = "vm5sstg3";

IPAddress ip(192,168,1,32);
IPAddress gateway(192,168,1,1);
IPAddress mask(255,255,255,0);

int q_1, q_2;
int current1, current2;
String msg;
Arm arm = Arm(25, 26);

int i = 0;
void setup()
{
  WiFi.mode(WIFI_STA);
  WiFi.config(ip, gateway, mask);
  WiFi.begin(ssid, password);

  while(WiFi.status() != WL_CONNECTED) {}
  // Serial.begin(115200);
  // Serial.setTimeout(10);

  server.begin();
}

void loop()
{
  // while(!Serial){}

  // if(Serial.available() > 0)
  // {
  //   q_1 = Serial.read();
  //   q_2 = Serial.read();

  //   arm.setPose(q_1, q_2);
  // }

  WiFiClient client = server.accept();

  if(client)
  {
    while(client.connected())
    {
      if(client.available())
      {
        msg = client.readStringUntil('\n');

        if(msg == "q") break;

        q_1 = msg.charAt(0);
        q_2 = msg.charAt(1);

        arm.setPose(q_1, q_2);
      }
    }
    client.stop();
  }
}
