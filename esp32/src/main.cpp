#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <time.h>

#include "Preferences.h"
#include "messages.h"
#include "secrets.h"

WiFiClient espClient;
PubSubClient mqttClient(espClient);
String deviceId;
String topic;
String uuid = "";

struct tm timeinfo;


#ifdef __cplusplus
extern "C" {
#endif
uint8_t temprature_sens_read();
#ifdef __cplusplus
}
#endif

void syncTime()
{
  configTime(0, 0, "pool.ntp.org", "time.nist.gov");
  while (!getLocalTime(&timeinfo))
  {
    Serial.println("Oczekiwanie na synchronizacje czasu...");
    delay(500);
  }

  Serial.println("Czas zsynchronizowany");
}

long long getTimeStampMs()
{
  struct timeval tv;
  gettimeofday(&tv, NULL);
  return (long long)tv.tv_sec * 1000LL + tv.tv_usec / 1000LL;
}


void saveUUID()
{
  Preferences uuidNamespace;
  uuidNamespace.begin("uuid",false);
  uuid = uuidNamespace.getString("uuid", "");

  if (uuid == "")
  {
    Serial.println("Saving new UUID");
    uuidNamespace.putString("uuid", UUID_GENERATED);
    uuid = UUID_GENERATED;
  }
  else Serial.print("UUID already exists!");
  Serial.print("UUID: ");
  Serial.println(uuid);
}

String generateDeviceIdFromEfuse()
{
  uint64_t chipId = ESP.getEfuseMac();
  char id[32];
  snprintf(id, sizeof(id), "esp32-%04X%08X",
           (uint16_t)(chipId >> 32),
           (uint32_t)chipId);
  return String(id);
}

void connectWiFi()
{
  Serial.print("Laczenie z Wi-Fi: ");
  Serial.println(WIFI_SSID);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("Polaczono z Wi-Fi");
  Serial.print("Adres IP: ");
  Serial.println(WiFi.localIP());
}

void connectMQTT()
{
  mqttClient.setServer(MQTT_HOST, MQTT_PORT);
  while (!mqttClient.connected())
  {
    Serial.print("Laczenie z MQTT...");
    if (mqttClient.connect(deviceId.c_str()))
    {
      Serial.println("OK");
    }
    else
    {
      Serial.print("blad, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" - ponowna proba za 2 s");
      delay(2000);
    }
  }
}



void publishSensorMeasurement(struct messages &msg)
{
  StaticJsonDocument<256> message;
  topic = "lab/" + String(MQTT_GROUP) + "/" + deviceId + "/sensors/" + msg.description;
  String unit = msg.unit;
  String description = msg.description;

  message["ts_ms"] = getTimeStampMs();
  message["device_name"] = msg.device_name;
  message["description"] = msg.description;
  message["value"] = msg.value;
  message["sensor"] = msg.device_name;
  message["unit"] = msg.unit;

  char payload[256];
  serializeJson(message, payload);
  mqttClient.publish(topic.c_str(), payload);

  Serial.print("Publikacja na topic: ");
  Serial.println(topic);
  Serial.println(payload);
}
void setup()
{
  Serial.begin(115200);
  delay(3000);
  saveUUID();
  deviceId = uuid;
  //deviceId = generateDeviceIdFromEfuse();
  Serial.print("Device ID: ");
  Serial.println(deviceId);
  connectWiFi();
  syncTime();
  connectMQTT();
}
void loop()
{
  if (WiFi.status() != WL_CONNECTED)
  {
    connectWiFi();
  }
  if (!mqttClient.connected())
  {
    connectMQTT();
  }
  mqttClient.loop();
  
  publishSensorMeasurement(tempSensorESP32);
  Serial.print("Temperature: ");
  
  // Convert raw temperature in F to Celsius degrees
  Serial.print((temprature_sens_read() - 32) / 1.8);
  Serial.println(" C");
  delay(5000);
}