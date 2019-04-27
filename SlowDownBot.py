import praw
import os
from handlers.imageHandler import saveImage
import urllib.request
from gfycat.client import GfycatClient
import requests
import time
from requests_toolbelt import MultipartEncoder
from upload import upload
import youtube_dl
from creds import *

reddit = praw.Reddit(client_id=reddit_id,
                     client_secret=reddit_secret,
                     username=reddit_username,
                     password=reddit_password,
                     user_agent= 'Slows down gifs by /u/PeskyPotato')


blacklistSubs = []
WAIT = 10

'''
Check if message in inbox was mention and calls checkComments
and marks the message as read.
'''
def scanInbox():
    for message in reddit.inbox.unread(mark_read=False):
        if message.was_comment and '/u/slowdownbot' in reddit.comment(message.id).body.lower():
            # print(message.was_comment)
            checkComments(reddit.comment(message.id))
            reddit.inbox.mark_read([message])

'''
If comment in subreddit not blacklisted take the speed and calls
generateReply and comments if reply not blank.
'''
def checkComments(comment):
    print("Checking comment")
    commentText = comment.body.lower()
    if checkBlacklistSub(comment.subreddit):
        commentText = commentText[16:].strip()
        speed = commentText.lower().split('x')[0]
        if speed[0] == " ":
            speed = speed.split(" ")[1]
        try:
            speed = float(speed)
        except ValueError:
            print("invalid speed", speed)
            return 1
        print("comment seed", speed)
        text = generateReply(speed, comment)
        print(text)
        try:
            if text is not None:
                comment.reply(text) 
                # pass # for testing
        except praw.exceptions.APIException as e:
            print(e)
            print("Commenting too much, trying again in 15 minutes")
            time.sleep(900)
            comment.reply(text)

def checkBlacklistSub(sub):
    if sub not in blacklistSubs:
        return True
    else:
        return False

'''
Calls downloadGif and slowDown, and creates the comment body 
for the reply. If any of the calls fail returns None.
'''
def generateReply(speed, comment):
    comment = reddit.comment(id=comment) 
    submission  = comment.submission

    if downloadGif(comment, submission) == 0:
        if slowDown(submission.id, speed) == 0:
            gfyname = upload(submission.id)
            # gfyname = "done" # for testing

    if gfyname is not None:
        slow_link = "https://gfycat.com/{}".format(gfyname)
        reply = "[Slowed down {}x]({})\n\n----\n\n^[Code](https://github.com/lamelmon) ^| ^[Bugs](https://github.com/lamelemon)".format(speed, slow_link)

        return reply
    return None

'''
gets the downloaded mp4 from temp/ and slowed it down using ffmpeg
and returns 1 is failed, 0 if successful.
'''
def slowDown(sub_id, speed = 0.5):
    print("slowing down")
    try:
        speed = float(speed)
    except ValueError:
        print("invalid speed", speed)
        return 1
    if isinstance(speed, float):
        speed = 1/speed
        os.system('ffmpeg -loglevel panic -hide_banner -y -i temp/{}.mp4 -filter:v "setpts={}*PTS" temp/slow-{}.mp4'.format(str(sub_id), speed, str(sub_id)))
        # os.system('rm temp/{}.mp4'.format(str(sub_id)))
        return 0

'''
Downloads the file in mp4 saves to temp/ returns 1 is failed
0 if successful.
'''
def downloadGif(comment, submission):
    # print("downloading gif")
    # Get posted gif link
    link = submission.url
    title = submission.title 

    print('Downloading post:', title.encode('utf-8'), link)
    if '.gifv' in link:
        link = link.replace('gifv', 'mp4')
        try:
            saveImage(link, submission.id, '.mp4')
        except urllib.error.HTTPError:
            with open('error.txt', 'a+') as logFile:
                logFile.write('HTTPError (timeout): '+ link + '\n')
                logFile.close()

    else:
        ydl_opts = {
            'videoformat': 'mp4',
            'outtmpl': 'temp/{}.mp4'.format(submission.id)
        }
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
        except youtube_dl.utils.DownloadError:
            print("somethings wrong", link)
            return 1
    return 0


def main():
    while(True):
        scanInbox()
        time.sleep(WAIT)

if __name__ == '__main__':
    main()

# #'0.5', 'eiyefnn'
# scanInbox()
