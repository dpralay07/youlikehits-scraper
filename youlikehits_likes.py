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
fw =  open('likes/likes_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.csv','a+')

print('Using Credentials:' + str(payload))

pageCounter = 0

session = requests.session()
r = session.post('https://www.youlikehits.com/login.php', data=payload)

while pageCounter <= 99:
	likesPageContent = session.get("https://youlikehits.com/favtweets.php?show=" + str(pageCounter)).content

	tweetPoints = re.findall('<b>Points.*<br>', likesPageContent)
	tweetPoints = [x[15:-4] for x in tweetPoints]
	# Find all iframes in the web page
	soup = BeautifulSoup(likesPageContent, 'html.parser')
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

	    tweetId = str(re.search("(?P<url>https?://[^\s]+)", iframecontent).group("url").split(",")[0])
	    
	    fw.write(tweetId + ',' + tweetPoints[i] + '\n')
        

	pageCounter += 9