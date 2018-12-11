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
fw =  open('retweeters/retweeters_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.csv','a+')

print('Using Credentials:' + str(payload))

pageCounter = 0

session = requests.session()
r = session.post('https://www.youlikehits.com/login.php', data=payload)

while pageCounter <= 9:
	retweetPageContent = session.get("https://youlikehits.com/retweets.php?show=" + str(pageCounter)).content

	# Find all tweet points    
	allTweetPoints = re.findall('<b>Points.*<br>',retweetPageContent)
	allTweetPoints = [x[15:-4] for x in allTweetPoints]

	# Find all iframes in the web page
	soup = BeautifulSoup(retweetPageContent, 'html.parser')
	tag = soup.find_all('iframe')

	# Get URLs of retweets
	rtURLs = []
	for items in tag:
	    soup = BeautifulSoup(str(items), 'html.parser')
	    tag1 = soup.find_all('iframe')[0]
	    rtURLs.append(tag1['src'])

	# Get BlackMarket Tweet-IDs
	for i, urls in enumerate(rtURLs):
	    iframecontent = session.get("https://youlikehits.com/" + urls).content
	    soup = BeautifulSoup(iframecontent, 'html.parser')

	    fw.write(str(re.search("(?P<url>https?://[^\s]+)", iframecontent).group("url").split(",")[0][43:-1]) + "," + str(allTweetPoints[i]) + "\n")

	pageCounter += 9
