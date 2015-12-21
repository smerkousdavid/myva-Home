from SocketServer import TCPServer, BaseRequestHandler
from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM
from mraa import Gpio, DIR_OUT

coms = None
backPackLat = 0
backPackLong = 0
ifchocolate = False
ifpopcorn = False
currentTemp = 0
currentPress = 0


class Commands:
    def __init__(self):
        pass

    def Find(self, full, part1, part2="", part3=""):  # Make sure we get at least two
        # vars that we want so we look for keywords
        if str(part2) == "":
            return False if (str(part1) in str(full)) else True  # Look for one keyword
        elif str(part3) == "":
            return True if (str(part1) in str(full) and str(part2) in str(full)) else False  # Look for two key words
        else:
            return True if ((str(part1) in str(full)) and (str(part2)
                                                           in str(full)) and (
                            str(part3) in str(full))) else False  # Look for three key words

    # Don't mess with format, the phone looks very closely for these values

    def Flash(self, text):  # Show text at bottom of screen on phone
        return str("::FLASHING::" + str(text) + "::END:FLASHING::")  # Do not change format of any below

    def GoogleMaps(self, long1, lat1):
        return str("::MAPS::" + str(long1) + "::LAT::" + str(lat1) + "::END:MAPS::")

    def Speak(self, toSpeak):
        return str("::SPEAKS::" + str(toSpeak) + "::END:SPEAKS::")

    def Image(self, imageUrl):
        return str("::ICONS::" + str(imageUrl) + "::END:ICONS::")  # Currently only accepts URLs to images


class Handle(BaseRequestHandler):
    def handle(self):
        global backPackLong, backPackLat, ifpopcorn, ifchocolate, currentPress, currentTemp, relay  # pull global vals
        print "\nGot Client!"  # Debugging
        self.data = self.request.recv(1024).strip().lower()  # Pull values from phone
        print "Client command: ", self.data  # See original command for debugging
        command = Commands()  # Use above library
        result = command.Flash("Not a command!")  # Default value

        # All the commands (All photos here were from google search, so shapes might be a little off...)

        if command.Find(self.data, "light", "off"):  # If both keywords are here turn the lights off
            relay.write(1)  # Turn relay off
            result = command.Flash("Turning the lights off!") + command.Speak("Lights are off") + \
                command.Image("http://www.clker.com/cliparts/f/i/X/O/x/M/light-bulb-off-black-hi.png")
            # Make sure phone gets that
            print result

        elif command.Find(self.data, "light", "on"):  # Opposite of above
            relay.write(0)  # Turn relay on
            result = command.Flash("Turning the lights on!") + command.Speak("Lights are on") + \
                command.Image("http://www.clker.com/cliparts/R/b/I/7/2/u/light-bulb-off-hi.png")
            print result

        elif command.Find(self.data, "find", "backpack") or command.Find(self.data, "where", "backpack"):
            # Draw a map from phone to object
            if (backPackLat == 0) and (backPackLong == 0):
                result = command.Flash("Backpack not online") + command.Speak("Could not find GPS data from backpack")+\
                    command.Image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Question_Mark.svg/2000px-"
                                  "Question_Mark.svg.png")
            else:
                result = command.GoogleMaps(str(backPackLat + 0.0350000), str(backPackLong - 0.3091526)) \
                         + command.Speak("You're the white marker, red is the backpack")
            # Lat, Long (Adjust values as needed, my LinkitOne
            # Was a little offso I had to move values around a little (Try it first if not then use a more powerful GPS)
            print result

        elif command.Find(self.data, "hold", "on"):
            result = command.Speak("What do you mean?") + command.Flash("What!")  # Speak and show text
            print result

        elif command.Find(self.data, "have", "popcorn"):
            if ifpopcorn:
                result = command.Image("http://rack.0.mshcdn.com/media/ZgkyMDE0LzA0LzAzLzJhL1BvcGNvcm5fVGltLjc5N2RmLmp"
                                       "wZwpwCXRodW1iCTk1MHg1MzQjCmUJanBn/b790913b/80c/Popcorn_Time1.jpg") + \
                         command.Flash("Yea we do!") + command.Speak("We have popcorn Baby!")
            else:
                result = command.Image("https://teknoseyir.com/wp"
                                       "-content/uploads/2015/10/sad-popcorn-time-800x450.jpg") + \
                         command.Flash("OH NO! where'd it go?") + command.Speak("Sorry bud we don't have popcorn")
                # Accepts url and (some) base 64 images will display above resultText
            print result

        elif command.Find(self.data, "current", "temp"):  # Return in fahrenheit the current temp from NEO
            if currentTemp == 0 and currentPress == 0:  # Make sure you have values
                # It's almost impossible to get both values exactly 0 so this is our way of checking
                result = command.Flash("Couldn't get temp") + command.Speak("Temperature module not found") + \
                         command.Image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Question_Mark.svg/"
                                       "2000px-Question_Mark.svg.png")
            else:
                result = command.Flash("Temp (f): " + str(currentTemp)) + command.Speak("Current temperature is " +
                str(currentTemp) + "fahrenheit") + \
                         command.Image("http://static.bhphotovideo.com/explora/explora/sites/default/file"
                                                  "s/Color-Temperature.jpg")

        elif command.Find(self.data, "current", "press"):  # Return in kPa the current press from NEO
            if currentTemp == 0 and currentPress == 0:
                result = command.Flash("Couldn't get pressure") + command.Speak("Barometer module not found") + \
                         command.Image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Question_Mark.svg/"
                                       "2000px-Question_Mark.svg.png")
            else:
                result = command.Flash("Pressure (kPa): " + str(currentPress)) + command.Speak("Current pressure is " +
                str(currentPress) + "kPa") + \
                         command.Image("https://lh5.ggpht.com/tXTrF6QNXNA-NZwzbw9vlkqCr9uWTKv6_gk12dmwCvkxJt1IM7F9FSv"
                                       "7Hd1oY4vSCIVD=w300")

            print result

        elif command.Find(self.data, "where", "mammoth", "is"):  # Example of three keyword command search (also fun)
            result = command.Image("http://vkontakte.ru/images/gifts/256/44.jpg") \
                     + command.Speak("I'M A MAMMOTH MUAHAHAHA!") + command.Flash("MUAHAHAHA!")
            print result

        self.request.sendall(str(result + "\n"))  # Must return to phone the value


def truFal(message):  # Since arduino bool to string is 0 or 1 we need to change it so python can read it
    if "1" in str(message):
        return True
    return False


def SensorCut(full, first, end, second=""):  # We need a end before a second value
    toRet = ["", ""]
    toRet[0] = full[int(full.index(first) + len(first)):int(full.index(end))]
    if second != "":  # This will auto replace the first substring
        toRet[0] = full[int(full.index(first) + len(first)):int(full.index(second))]
        toRet[1] = full[int(full.index(second) + len(second)):int(full.index(end))]
    return toRet


# Example formatting
# GPS1:LAT: 4005.2603:LONG: 6006.3773:END:GPS1:
# ::CARD::(RANDOM HEX CODE)::END:CARD::
# ::CARD::(RANDOM HEX CODE)::CARD:RELEASE::::END:CARD::
# ::POPCORN::1::END:POPCORN::
# ::TEMP::77.0::BARO::98.8::END:TEMP::


def Sensors(values):  # Called when client sensor sends data
    global coms, backPackLat, backPackLong, ifchocolate, ifpopcorn, currentTemp, currentPress
    values = values.replace(" ", "")
    if coms.Find(values, "GPS1", "LONG", "END"):
        vals = SensorCut(values, "GPS1:LAT:", ":END:GPS1:", ":LONG:")
        backPackLat = float(vals[0]) / 100  # Must divide by 100, or LatLng on phone flips out
        backPackLong = float(vals[1]) / 100  # Old val = 200.0  new val = 2.00
        print "New GPS values LAT: " + str(backPackLat) + " LONG: " + str(backPackLong)
    elif coms.Find(values, ":CARD:", ":END:CARD:"):
        vals = SensorCut(values, "::CARD::", "::END:CARD::")
        if len(vals[0]) > 5:  # Replace this to check if code matches a card for other items like icecream
            ifchocolate = True
    elif coms.Find(values, ":CARD:", ":END:CARD:", "CARD:RELEASE"):
        vals = SensorCut(values, "::CARD::", "::END:CARD::")
        if len(vals[0]) > 5:  # Replace this to check if code matches a card for other items like icecream
            ifchocolate = False
    elif coms.Find(values, ":POPCORN:", ":END:POPCORN:"):
        ifpopcorn = truFal(SensorCut(values, "::POPCORN::", "::END:POPCORN::")[0])
        print "POPCORN: " + str(ifpopcorn)

    elif coms.Find(values, ":TEMP:", ":END:TEMP:", ":BARO:"):
        vals = SensorCut(values, "::TEMP::", "::END:TEMP::", "::BARO::")
        currentTemp = round(float(vals[0]), 1)
        currentPress = round(float(vals[1]), 1)
        print "TEMP: " + str(currentTemp) + "\nPressure: " + str(currentPress)


def SensorStart():  # This runs on separate thread
    global coms
    coms = Commands()
    serv = socket(AF_INET, SOCK_STREAM)
    serv.bind(("", 9292))  # SENSOR PORT 9292
    serv.listen(1)

    while True:  # Loop forever
        conn, addr = serv.accept()
        data = conn.recv(1024)
        Sensors(data)
        conn.close()


if __name__ == "__main__":
    global relay
    print "Welcome to David's home automation!!!\nStarting light controller"
    relay = Gpio(43)  # p2 on Linkit Smart
    relay.dir(DIR_OUT)  # Relay must be output
    relay.write(1)  # Start the relay off (Inversed)
    print "light controller started\nStarting Server"
    PORT = 9191  # PHONE PORT 9191
    Thread(target=SensorStart).start()  # Start sensor server in new thread
    TCPServer(("", PORT), Handle).serve_forever()  # Start main phone server in main thread
