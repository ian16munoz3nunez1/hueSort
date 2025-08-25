#include <WiFi.h>

NetworkServer server(9999);

void blink(int,int);
void bot(NetworkClient);

int mf1 = 19;
int mf2 = 5;
int mf3 = 16;
int mb1 = 33;
int mb2 = 26;
int mb3 = 14;

const char* ssid = "";
const char* password = "";

IPAddress ip(192,168,1,32);
IPAddress gateway(192,168,1,1);
IPAddress subnet(255,255,255,0);

void setup()
{
  pinMode(2, OUTPUT);
  pinMode(mf1, OUTPUT);
  pinMode(mf2, OUTPUT);
  pinMode(mf3, OUTPUT);
  pinMode(mb1, OUTPUT);
  pinMode(mb2, OUTPUT);
  pinMode(mb3, OUTPUT);
  
  WiFi.mode(WIFI_STA);
  WiFi.config(ip, gateway, subnet);
  WiFi.begin(ssid, password);
  blink(2, 200);

  while(WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
  }
  blink(3, 200);

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

      if(v1 >= 0)
      {
        analogWrite(mb1, 0);
        analogWrite(mf1, v1);
      }
      else
      {
        analogWrite(mf1, 0);
        analogWrite(mb1, abs(v1));
      }

      if(v2 >= 0)
      {
        analogWrite(mb2, 0);
        analogWrite(mf2, v2);
      }
      else
      {
        analogWrite(mf2, 0);
        analogWrite(mb2, abs(v2));
      }

      if(v3 >= 0)
      {
        analogWrite(mb3, 0);
        analogWrite(mf3, v3);
      }
      else
      {
        analogWrite(mf3, 0);
        analogWrite(mb3, abs(v3));
      }
    }
  }
  client.stop();
  // Serial.println("Client Disconnected");

  analogWrite(mf1, 0);
  analogWrite(mf2, 0);
  analogWrite(mf3, 0);
  analogWrite(mb1, 0);
  analogWrite(mb2, 0);
  analogWrite(mb3, 0);
  
  blink(4, 500);
}

void blink(int iter, int t)
{
  for(int i = 0; i < iter; i++)
  {
    digitalWrite(2, HIGH);
    delay(t);
    digitalWrite(2, LOW);
    delay(t);
  }
}

