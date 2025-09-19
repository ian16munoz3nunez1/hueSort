#include <WiFi.h>
#include "led.h"
#include "motor.h"

NetworkServer server(9999);

void bot(NetworkClient);

Led led0(2);
Motor motor1(19, 33);
Motor motor2(5, 26);
Motor motor3(16, 14);

const char* ssid = "";
const char* password = "";

IPAddress ip(192,168,1,32);
IPAddress gateway(192,168,1,1);
IPAddress subnet(255,255,255,0);

void setup()
{
  WiFi.mode(WIFI_STA);
  WiFi.config(ip, gateway, subnet);
  WiFi.begin(ssid, password);
  led0.blink(2, 200);

  while(WiFi.status() != WL_CONNECTED) { delay(1000); }
  led0.blink(3, 200);

  // Serial.begin(115200);
  // Serial.println("");
  // Serial.println("WiFi connected!!");
  // Serial.print("IP Address: ");
  // Serial.println(WiFi.localIP());

  server.begin();
}

void loop()
{
  NetworkClient client = server.accept();

  if(client)
  {
    // Serial.println("New Client Connected");
    bot(client);
  }

  led0.blink(1, 500);
}

void bot(NetworkClient client)
{
  String velocidad1, velocidad2, velocidad3;
  int v1, v2, v3;
  
  while(client.connected())
  {
    if(client.available())
    {
      String msg = client.readStringUntil('\n');

      if(msg == "q") break;

      velocidad1 = msg.substring(0,4);
      velocidad2 = msg.substring(4,8);
      velocidad3 = msg.substring(8,12);

      v1 = velocidad1.toInt();
      v2 = velocidad2.toInt();
      v3 = velocidad3.toInt();

      motor1.setVelocity(v1);
      motor2.setVelocity(v2);
      motor3.setVelocity(v3);
    }
  }
  client.stop();
  // Serial.println("Client Disconnected");

  motor1.stop();
  motor2.stop();
  motor3.stop();

  led0.blink(4, 500);
}

