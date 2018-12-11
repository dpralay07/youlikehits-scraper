
# coding: utf-8

# In[132]:


import requests
from bs4 import BeautifulSoup
import urllib
import re
import ConfigParser
import datetime
import sys

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Read username and password from config file
settings_file = "config.txt"

# Using ConfigParser you can access the configuration files
config = ConfigParser.ConfigParser()
config.readfp(open(settings_file))

# Get the usernames and password
payload = {
    'username': config.get('Credentials', 'username'),
    'pass': config.get('Credentials', 'password')
}

content = None

# print twtIDs

print "****** YOULIKEHITS PARSER WORKING ******"
# Use 'with' to ensure the session context is closed after use.
fw =  open('datas/allFiles_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.csv','a+')
collusiveFollowers = []
# requests.session() means all the codes written inside it will work till the session
with requests.Session() as s:
    # login to youlikehits using payload parameters
    p = s.post('https://youlikehits.com/login.php', data=payload, verify=False)
    count = 0
    while count < 999:
        print count
        followPageContent = s.get("https://youlikehits.com/twitter2.php?show=" + str(count)).content

        # Find all tweet points    
        # allTweetPoints = re.findall('<b>Points.*<br>',retweetPageContent)
        # allTweetPoints = [x[15:-4] for x in allTweetPoints]
        
        # Find all iframes in the web page
        soup = BeautifulSoup(followPageContent, 'html.parser')

        tag = soup.find_all('img')

        

        for imgLinks in tag:
            # print imgLinks
            try:
                soup = BeautifulSoup(str(imgLinks), 'html.parser')
                if soup.find('img')['alt']:
                    followerScreenname = soup.find('img')['alt']
                    if followerScreenname[0] == '@':
                        collusiveFollowers.append(followerScreenname[1:])
            except:
                pass
        count += 9

for item in collusiveFollowers:
    print item  
    try:
        fw.write(str(item).encode('utf-8') + '\n')   
    except:
        pass

