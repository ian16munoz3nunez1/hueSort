#include "esp_camera.h"
#include <WiFi.h>
#include <WiFiClient.h>
#include <WiFiServer.h>

// WiFi credentials
const char* ssid = "esp32net";
const char* password = "ciNNam0n2412";

// TCP server on port 8080
WiFiServer server(10001);

// IP address configuration
IPAddress ip(192,168,4,101);
IPAddress gateway(192,168,4,1);
IPAddress subnet(255,255,255,0);

// Camera configuration for AI-Thinker ESP32-CAM
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

void setup() {
  // Serial.begin(115200);
  // Serial.setDebugOutput(true);

  // Initialize camera
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  
  // Lower resolution for better streaming performance
  config.frame_size = FRAMESIZE_VGA;  // 640x480
  config.jpeg_quality = 12;
  config.fb_count = 1;

  // Initialize camera
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    // Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  // Connect to WiFi
  WiFi.mode(WIFI_STA);
  WiFi.config(ip, gateway, subnet);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { delay(500); }

  // Start TCP server
  server.begin();
}

void loop() {
  WiFiClient client = server.available();
  
  if (client) {
    while (client.connected()) {
      // Take a picture
      camera_fb_t * fb = esp_camera_fb_get();
      if (!fb) { break; }

      // Send the image size
      uint32_t frame_size = fb->len;
      client.write((uint8_t*)&frame_size, 4);
      
      // Send the image data
      size_t sent = 0;
      while (sent < fb->len) {
        size_t chunk_size = min((size_t)1024, fb->len - sent);
        size_t bytes_written = client.write(fb->buf + sent, chunk_size);
        if (bytes_written == 0) { break; }
        sent += bytes_written;
      }
      
      // Free space to reuse memory address
      esp_camera_fb_return(fb);
      delay(100);
    }
    
    client.stop();
  }
}

