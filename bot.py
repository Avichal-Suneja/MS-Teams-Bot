''' Bot to Auto attend Microsoft Teams class for Amity University Students
    Coded by - Avichal Suneja
'''

from selenium import webdriver
import pyautogui
from time import sleep
from datetime import datetime
import requests
import pickle
import subprocess


# These are all the user details we will be needing
UserInfo = {
	'ami_id':'',
	'ami_pw':'',
	'teams_add':'',
	'auth':'',
	'postUrl':''
}


# Function to keep looking for an image and return its coordinates 
def getCoordinates(subject, duration):
	sub = 'Images//' + subject + '.png'
	while True:
		try:
			x,y = pyautogui.locateCenterOnScreen(sub, confidence=0.8)
			break
		except:
			sleep(duration)
			continue

	return (x,y)


# Function to Join a class with it's Subject code 
def join(subject_code):
	x, y = getCoordinates(subject_code, 1)
	pyautogui.click(x,y, duration = 1)

	pyautogui.moveTo(688, 0)

	x, y = getCoordinates('join', 10)
	pyautogui.click(x,y, duration = 1)

	x,y = getCoordinates('joinNow', 1)
	pyautogui.click(x,y, duration = 1)


# Function to Leave the class and return to home page
def leave():
	pyautogui.hotkey('ctrl', 'shift', 'b')
	x, y = getCoordinates('back', 1)
	pyautogui.click(x,y, duration = 1)


# Function to Parse the time string and return a tuple of two datetime objects
def giveTime(time):
	try:
		start = str(time.text.strip()[0:5])
		end = str(time.text.strip()[9:14])

		start_obj = datetime.strptime(start, '%H:%M')
		end_obj = datetime.strptime(end, '%H:%M')

		return (start_obj, end_obj)

	except:
		return 'null'


# Custom Function to keep looking for an element after a fixed interval 
def getElement(type, interval, selector):
	while True:
		try:
			if type=='css':
				element = browser.find_element_by_css_selector(selector)
				break
			elif type=='class':
				element = browser.find_elements_by_class_name(selector)
				break
			elif type=='xpath':
				element = browser.find_element_by_xpath(selector)
				break
			elif type=='id':
				element = browser.find_element_by_id(selector)
				break
	
		except:
			sleep(interval)
			continue

	print("Element Found!")
	return element


# Custom click function to keep clicking after a fixed interval (Error Handling)
def myClick(element):
	while True:
		try:
			element.click()
			break
		except:
			sleep(1)
			print("Finding..")
			continue


def discordAlert(message):
	payload = {'content' : message}
	header = {
	'authorization' : UserInfo['auth']
	}

	r = requests.post(UserInfo['postUrl'], data = payload, headers = header)

'''The Main Code 
			Starts Here'''


# Taking all the user info we will be needing or loading it if it is already saved
try:
	UserInfo = pickle.load(open('userData.dat', 'rb'))
except:
	print("YOU ONLY NEED TO FILL THIS ONE TIME:")
	UserInfo['ami_id'] = input("Enter your Amizone Form Number: ")
	UserInfo['ami_pw'] = input("Enter your Amizone Password: ")
	UserInfo['teams_add'] = input("Paste your Teams App exe path: ")

	print("\nDISCORD API INFO:")
	UserInfo['auth'] = input("Enter your Discord authorization code: ")
	UserInfo['postUrl'] = input("Enter URL of your Discord Server: ")

	pickle.dump(UserInfo, open('userData.dat', 'wb'))


# Launching the Chrome WebBrowser
browser = webdriver.Chrome()


# Logging into Amizone with userid and password
browser.get('https://student.amizone.net/')
username = getElement('css', 2, '#loginform > div:nth-child(2) > input:nth-child(1)')
password = getElement('css', 2, 'div.validate-input:nth-child(3) > input:nth-child(1)')
username.send_keys(UserInfo['ami_id'])
password.send_keys(UserInfo['ami_pw'])
password.submit()


# Getting rid of the popup Modals blocking other elements
while True:
	try:
		# Going to the time table page and getting the subject codes and timings
		time_table = getElement('xpath', 2, '//*[@id="10"]')
		myClick(time_table)
		break
	except:
		try:
			cross_1 = getElement('css', 1, '#myModal > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > button:nth-child(1)')
			myClick(cross_1)
		except:
			try:
				cross_2 = getElement('css', 0.5, '#ModalPopTEDP > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > button:nth-child(1)')
				myClick(cross_2)
			except:
				try:
					cross_3 = getElement('css', 0.5, '#myModal > div > div > div.modal-header.modal-lg > button')
					myClick(cross_3)
				except:
					print("The Program will probably break now Fs in the chat")
					


sleep(2)
Time_list = getElement('class', 1, 'class-time')
Subject_list = getElement('class', 1, 'course-code')


# Timings - list of tuples of start and end datetime objects
# Subjects - list of all the subject Codes
timings = []
subjects = []


# Store all the datetime objects in timings list
for time in Time_list:
	time_obj = giveTime(time)
	if time_obj != 'null':
		timings.append(time_obj)


# Store all the Subject codes in subjects list
for course in Subject_list:
	if course.text.strip() != '':
		subjects.append(course.text.strip())


# Print statement for debugging
for i in range(len(timings)):
	print(subjects[i]+' class is from '+str(timings[i][0].strftime('%X')) + ' to ' +
			str(timings[i][1].strftime('%X')))


# Launching the Microsoft Teams app
subprocess.call(UserInfo['teams_add'])


# Main loop for all the Subjects
# It will join a class wait for it to get over and then leave
counter = 0

for sub in subjects:
	sleep(1)
	join(sub)

	while datetime.now().time() < timings[counter][1].time():

		time_left = timings[counter][1] - datetime.now()
		if(time_left.seconds <= 600):
			discordAlert("Time for " + sub + " Attendance!!")
			sleep(540)

		print("Waiting for " + sub + "to get over...")
		sleep(60)

	counter+=1
	leave()


discordAlert("All the classes for today are over GG")

'''                     END OF CODE                              '''
