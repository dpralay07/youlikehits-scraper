import requests
from bs4 import BeautifulSoup
import re
import datetime
import ConfigParser
import contextlib
import requests

# Read username and password from config file
settings_file = "configs/config.txt"
config = ConfigParser.ConfigParser()
config.readfp(open(settings_file))

# Fill in your details here to be posted to the login form.
payload = {
    'username': config.get('Credentials', 'username'),
    'pass': config.get('Credentials', 'password')
}

print("****** YOULIKEHITS PARSER ******")

# Use 'with' to ensure the session context is closed after use.
fw =  open('followers/followers_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.csv','a+')

print('Using Credentials:' + str(payload))

pageCounter = 0

session = requests.session()
r = session.post('https://www.youlikehits.com/login.php', data=payload)

while pageCounter <= 99:
	followerPageContent = session.get("https://youlikehits.com/twitter2.php?show=" + str(pageCounter)).content

	userPoints = re.findall('<b>Points.*<br>', followerPageContent)
	userPoints = [x[15:-4] for x in userPoints]
	

	# Find all followers data
	soup = BeautifulSoup(followerPageContent, 'html.parser')
	followersDiv = soup.find("div", {"id": "getpoints"})

	soup = BeautifulSoup(str(followersDiv), 'html.parser')
	followersLinks = soup.find_all('a')

	for vals in zip(followersLinks,userPoints):
		if 'screen_name' in str(vals[0]):
			screen_name = re.search("screen_name=(.*)','Twitter", str(vals)).group(1)
			
			fw.write(screen_name + ',' + vals[1] + '\n')

	
	pageCounter += 12
