from socket import socket, AF_INET, SOCK_STREAM
from neo import Temp
from neo import Barometer
from time import sleep

temp = Temp()
baro = Barometer()

IP = "192.168.1.17"
PORT = 9292

while True:
	tempVal = temp.getTemp("f")  # Get temp from temperature sensor
	baroTemp = baro.getTemp("f")  # Get temp from barometer sensor
	averageTemp = (tempVal + baroTemp) / 2   # Get average from both sensors
	pressure = baro.getPressure()  # Get kPa from barometer

	print "Average temp: "+str(averageTemp)+" f\nPressure: "+str(pressure)+" kPa\n"

	sock = socket(AF_INET, SOCK_STREAM)
	sock.connect((IP, PORT))
	sock.send("::TEMP::"+str(averageTemp)+"::BARO::"+str(pressure)+"::END:TEMP::")
	sock.close()

	sleep(30)
