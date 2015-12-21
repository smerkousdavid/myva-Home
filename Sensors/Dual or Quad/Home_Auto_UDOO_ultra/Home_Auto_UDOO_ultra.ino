#include <Udoo.h>

#define IP "192.168.1.17" //Server IP
#define PORT 9292 //Server PORT

#define trigPin 13
#define echoPin 12
#define thereDistance 10

Udoo udoo;
TcpClient client;
boolean last = true;

boolean there()
{
  long duration, distance;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = (duration/2) /26.1;
  if(distance < thereDistance)
    return true;
  return false;
}

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  udoo.init(); //Must call this before any other udoo commands
  client.connect(IP, PORT); //Set Ip and port for TcpClient
}

void loop() {
  boolean current;
  while((current = there()) == last) delay(1500);
  last = current;
  client.send("::POPCORN::"+String(current)+"::END:POPCORN::"); //Send to Server
  client.close(); //Close the socket
  delay(10);
}
