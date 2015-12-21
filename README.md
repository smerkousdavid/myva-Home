# myva-Home
Voice controlled home automation system, with easy to use examples and libraries<br>
Created by David Smerkous<br><br>

What?
------------------
This is a prebuilt application to easily allow you to modify and experiment<br>
With the appliances in your home, all running on a microprocessor (Linkit_Smart)<br>
<br>
EXAMPLE VIDEO:<br>
Link coming soon<br><br>

Install
------------------
Before moving on make sure that you installed<br>
1. Udoo library https://github.com/smerkousdavid/Udoo-Library (Install on Udoo)<br>
2. Neo library https://github.com/smerkousdavid/Neo.GPIO (Install on Neo)<br>
3. Rfid library https://github.com/miguelbalboa/rfid (Install on Either above)<br>
Libraries 1 and 2 need to be installed for the Udoo quad/dual and Neo to work!<br>
Make sure you checked out the Wiring_Info to properly wire the sensors<br>

Here are all the steps needed to get all sensors workig<br>
1. Install the zip<br>
2. Unpack it on desktop<br>
3. Navigate to 'Android_App'<br>
4. Plug in android device<br>
5. Copy apk to phone using explorer<br>
6. Open phones file explorer<br>
7. Navigate to where apk was placed<br>
8. Click on apk and it'll install like all other apps<br>
9. Make sure WinSCP and puTTy are installed<br>
  https://winscp.net/eng/index.php<br>
  http://www.putty.org/<br>
10. Open WinSCP<br>
11. Get the Ip of SMART by connecting through station mode or by router admin<br>
12. Connect to SMART using that IP (Default login = root, Pass = what you used before)<br>
13. (Left side) Navigate to 'Server' <br>
14. Copy 'Linkit_Smart_Server.py' to the SMART's /root folder<br>
15. puTTY open up SMART ssh connection<br>
16. cd into '/root'<br>
17. run command 'python Server.py'<br>
18. DON'T close the window<br>
19. On computer navigate to 'Sensors' (Not using WinSCP)<br>
20. Under each folder where there is a arduino sketch, modify it for your network<br>
   The Ip's, SSID and PASSWORD values then flash to each device<br>
21. If on Udoo quad/dual copy modified arduino sketch over on flash drive<br>
22. Flash the Due on the Udoo with the new sketch<br>
23. One file in Sensors -> Neo is a python file called Home_Auto_Neo<br>
24. Copy on flash drive to Neo and run the python script as root NOT sudo example below<br>
    echo udooer | sudo -S su -c 'Auto_Home_Neo.py'<br>
25. Open up the app and try the example commands<br>


Other
-----------
Have any questions or would like to contribute. Just contact me at smerkousdavid@gmail.com<br>

