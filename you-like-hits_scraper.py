
# coding: utf-8

# In[132]:


import requests
from bs4 import BeautifulSoup
import urllib
import re
import ConfigParser

# Read username and password from config file
settings_file = "config.txt"
config = ConfigParser.ConfigParser()
config.readfp(open(settings_file))

# Fill in your details here to be posted to the login form.
payload = {
    'username': config.get('Credentials', 'username'),
    'pass': config.get('Credentials', 'password')
}


# Use 'with' to ensure the session context is closed after use.
with requests.Session() as s:
    # login to youlikehits using payload parameters
    p = s.post('https://youlikehits.com/login.php', data=payload)
    count = 0
    while count < 9999:
        retweetPageContent = s.get("https://youlikehits.com/retweets.php?show=" + str(count)).content

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
        import re

        with open('customer11_tweetID_points.csv','a+') as fw:
            for i, urls in enumerate(rtURLs):
                iframecontent = s.get("https://youlikehits.com/" + urls).content
                soup = BeautifulSoup(iframecontent, 'html.parser')

                # Regex for twitter id
                fw.write(str(re.search("(?P<url>https?://[^\s]+)", iframecontent).group("url").split(",")[0][43:-1]) + "," + str(allTweetPoints[i]) + "\n")

        count += 9