#include <LGPS.h>
#include <LTask.h>
#include <LWiFi.h>
#include <LWiFiClient.h>

#define SSID "PLACE ROUTER SSID HERE"
#define PASS "PLACE ROUTER PASSWORD HERE"
#define IP "192.168.1.17"
#define PORT 9292

LWiFiClient client;
gpsSentenceInfoStruct info;
char buff[256];


static unsigned char getComma(unsigned char num,const char *str)
{
  unsigned char i,j = 0;
  int len=strlen(str);
  for(i = 0;i < len;i ++)
  {
     if(str[i] == ',')
      j++;
     if(j == num)
      return i + 1; 
  }
  return 0; 
}

static double getDouble(const char *s)
{
  char buf[13];
  unsigned char i;
  double rev;
  
  i=getComma(1, s);
  i = i - 1;
  strncpy(buf, s, i);
  buf[i] = 0;
  rev=atof(buf);
  return rev; 
}

void parser(const char* data)
{
  double latitude;
  double longitude;
  int tmp;
  if(data[0] == '$')
  {
    tmp = getComma(2, data);
    latitude = getDouble(&data[tmp]);
    tmp = getComma(4, data);
    longitude = getDouble(&data[tmp]);
    tmp = getComma(7, data);
    while (!(client.connect(IP, PORT))) delay(5);
    sprintf(buff, "GPS1:LAT:%10.4f:LONG:-%10.4f:END:GPS1:", latitude, longitude);
    client.println(buff);
    delay(2);
    client.stop();
    delay(10);
  }
}

void setup() {
  LWiFi.begin();
  LGPS.powerOn();
  while (!(LWiFi.connect(SSID, LWiFiLoginInfo(LWIFI_WPA, PASS)))) delay(1);
  delay(1000);
}

void loop() {
  LGPS.getData(&info);
  parser((const char*)info.GPGGA);
  delay(8000);
}
