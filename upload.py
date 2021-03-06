import requests
import time
from requests_toolbelt import MultipartEncoder
from creds import *

client_id = gfycat_id
client_secret = gfycat_secret

def get_token():
    payload = {
    'grant_type':'client_credentials',
    'client_id':client_id,
    'client_secret':client_secret
    }

    url = "https://api.gfycat.com/v1/oauth/token"
    r = requests.post(url, data=str(payload), headers={'User-Agent': "Slow down bot"})
    
    response = r.json()

    access_token = response["access_token"]
    print(response)
    # print(access_token)
    return access_token
    
def upload(sub_id):
    print("uploading")
    title = "please work..."

    # get gfyname
    url = "https://api.gfycat.com/v1/gfycats"
    headers = {"Authorization": "Bearer " + get_token(), 'User-Agent': "Slow down bot",
                'Content-Type': 'application/json'}

    params = {}

    if title:
        params["title"] = sub_id

    r = requests.post(url, headers=headers, data=str(params))
    # print(r.text)

    metadata = r.json()

    url = "https://filedrop.gfycat.com"
    with open("temp/slow-{}.mp4".format(sub_id), 'rb') as f:
        files = {"key": metadata["gfyname"], "file": (metadata["gfyname"], f, "video/mp4")}

        m = MultipartEncoder(fields=files)

        r = requests.post(url, data=m, headers={'Content-Type': m.content_type, 'User-Agent': "Slowing down gifs"})
        print("Metadata", metadata)
        time.sleep(10)
        url = "https://api.gfycat.com/v1/gfycats/fetch/status/" + metadata["gfyname"]
        headers = {'User-Agent': "Slowing down gifs"}
        print("waiting for encode...", end=" ")
        r = requests.get(url, headers=headers)
        ticket = r.json()
        print("before", ticket)
        time.sleep(15)

        # if still encoding
        percentage = 0
        for i in range(457):
            if ticket["task"] == "encoding":
                time.sleep(15)
                r = requests.get(url, headers=headers)
                ticket = r.json()
                print(ticket)
                if float(ticket.get('progress', 0)) > percentage:
                    percentage = float(ticket['progress'])
                    print(percentage, end=" ")
                else:
                    break
        # sometimes takes time for the task to start
        if ticket["task"] == "NotFoundo":
            time.sleep(20)
        if ticket["task"] == "error":
            print("Something wrong", ticket)
            return None
        if ticket["task"] == "complete":
            print(ticket["gfyname"])
            return ticket["gfyname"]

        print("something wrong", ticket)
        return None

'''
Called for testing purposes to check if file uploaded
'''
def info(gfyname):

        url = "https://api.gfycat.com/v1/gfycats/fetch/status/" + gfyname
        headers = {'User-Agent': "Slowing down gifs"}

        r = requests.get(url, headers=headers)
        ticket = r.json()
        print(ticket)



# info('InexperiencedMatureGoitered')
