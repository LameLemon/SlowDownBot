import urllib.request
import time

def saveImage(link, name, ext):
    try:
        urllib.request.urlretrieve(link, 'temp/' + str(name) + ext)
    except urllib.error.URLError:
        time.sleep(20)
        try:
            urllib.request.urlretrieve(link, 'temp/'+ str(name) + ext)
        except:
            with open('error.txt', 'a+') as logFile:
                logFile.write('Error: '+ link + '\n')
                logFile.close()
    
