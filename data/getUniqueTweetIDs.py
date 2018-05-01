import os
import csv
import tweepy
from tweepy import OAuthHandler

allFiles = os.listdir(".")
CONSUMER_KEY = "WjVn46MubIf8bcHYc3e9dlpr4"
CONSUMER_SECRET = "ZRiGULmrsrtgcRGpERH1MAqb53ufl2TKLlqo1sBj9F2BDMT9Cy"
OAUTH_TOKEN = "170995068-luaKH0btNMAm7SbUo8uVARcNOXCyObb61KrioDAo"
OAUTH_TOKEN_SECRET = "Ccjjbp4T5RfOz5mqiIIXJgWSEG7Wqk7dIIOdvaiq4NjAB"
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True)


uniqueTweetIDs = set()

for files in allFiles:
	if files == "customer10_tweetID_points.csv":
		file=open(files, "r")
		reader = csv.reader(file)
		for line in reader:
			uniqueTweetIDs.add((line[0],line[1]))

with open('customer10_id_user_score','a+') as fw:
	for unqTwts in uniqueTweetIDs:
		print "Working for tweet id: %s", unqTwts[0]
		try:
			tweet = api.get_status(unqTwts[0])
			fw.write(str(tweet.user.screen_name) + "," + str(unqTwts[0]) + "," + str(unqTwts[1]) + "\n")
		except tweepy.error.TweepError as e:
			with open('tweetId_deleted','a+') as fn:
				fn.write(str(unqTwts[0]) + "\n")
			print("\nTwitter error: %s" %e)
			continue