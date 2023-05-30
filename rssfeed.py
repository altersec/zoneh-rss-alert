#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import feedparser
import hashlib
import pymsteams

current_dir = os.getcwd()

#Read parameters from .env file
load_dotenv()
feed = os.getenv("FEED")
webhook = os.getenv("WEBHOOK")
terms = os.getenv("TERMS").split(',')

#Create a new MSTeams object
myTeamsMessage = pymsteams.connectorcard(webhook)

f = feedparser.parse(feed)


#Create a temp file and an old file
temp_file = os.path.join(current_dir, 'temp')
old_file = os.path.join(current_dir, 'old')

#Write the current feed to a temp file
tempfile = open(temp_file, "w")
for element in f.entries:
    tempfile.write(str(element))
    tempfile.write('\n')
tempfile.close()

digests = []

#Calculate the md5 hash of the current and old feed
for filename in [temp_file, old_file]:
    hasher = hashlib.md5()
    with open(filename, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
        a = hasher.hexdigest()
        digests.append(a)

#If the hashes are different, send a message to teams and update the old file
if digests[0] != digests[1]:
    f = feedparser.parse(feed)
    oldfile = open(old_file, "w")
    for element in f.entries:
        oldfile.write(str(element))
        oldfile.write('\n')
    oldfile.close()
    
    myTeamsMessage.summary("Warning")
    myMessageSection = pymsteams.cardsection()
    myMessageSection.title(f.feed.updated)

    content=[]
    temptuple=()

#Search for entries that contain terms and add to a teams message
    for i in range(len(f.entries)):
        for j in range(len(terms)):
            if terms[j] in f.entries[i].title:
                myMessageSection.addFact(f.entries[i].title,f.entries[i].link)
                temptuple=(f.entries[i].title,f.entries[i].link)
                print(temptuple)
                content.append(temptuple)
    if not content:
        #print("no data")
        quit()

    myTeamsMessage.addSection(myMessageSection)            
    myTeamsMessage.send()
