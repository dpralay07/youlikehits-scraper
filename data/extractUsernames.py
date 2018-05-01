import os

with open('/home/hridoy/Work/youlikehits-scraper/data/customer7_id_user_score') as fr:
	content = fr.readlines()

	for lines in content:
		print lines.split(',')[0]