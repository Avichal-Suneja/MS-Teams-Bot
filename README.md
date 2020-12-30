# MS-Teams-Bot
This is a Program which uses Selenium and Pyautogui modules to automate attending classes from MS-Teams.
It logs into your college account (Amizone in my case) fetches the time table from there and parses that data into a usable format of datetime object. 
Then it launches MS teams on your desktop and uses image recognition to find the classes of the respective subjects, join them and leave them in accordance with the time table it fetched earlier. 
Ten minutes before every class ends, it also notifies you on your discord server through the post API of the request module for attendance. 
This Project is just for Educational Purpose and does not support missing your classes in any way.

PS: For this to work on your computer you need to have Python on your machine and pip install all the modules mentioned in the code and a geckodriver for Selenium Module to run Chrome browser remotely
