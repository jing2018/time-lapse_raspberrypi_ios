from time import sleep
from time import time
from datetime import datetime
from sh import gphoto2 as gp
import sys
import pyrebase
import signal, os, subprocess

#Firebase configuration
config = {
    "apiKey": "apiKey",
    "authDomain": "testproject-fec80.firebaseapp.com",
    "databaseURL": "https://testproject-fec80.firebaseio.com",
    "storageBucket": "testproject-fec80.appspot.com",
}

firebase = pyrebase.initialize_app(config)

#Firebase Database Initialization
db = firebase.database()
#auth = firebase.auth()
#user = auth.sign_in_with_email_and_password("", "")

#get the current time
shot_date =datetime.now().strftime("%Y-%m-%d ")
shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
picName = db.child('picName').get().val()
picID = picName
folderName=db.child('folderName').get().val()
sleepTime2=db.child('intervalTime').get().val()

#insitial this program running time
#when time's up, stop running
hours=db.child('hours').get().val()
minutes=db.child('minutes').get().val()

clearCommand = ["--folder","/store_00020001/DCIM/100CANON", "-R", "--delete-all-files"]
triggerCommand = ["--trigger-capture"]
downloadCommand =["--get-all-files"]
folder_name = shot_date + folderName
save_location = "/home/pi/Desktop/gphoto/images/" +folder_name


#kill gphoto2 process that
#starts whenever we connect the camera
def killgphoto2Process():
    p= subprocess.Popen(['ps','-A'],stdout=subprocess.PIPE)
    out, err =p.communicate()
    #search for the line that has the process
    #we want to kill
    for line in out.splitlines():
        if b'gvfsd-gphoto2' in line:
            #kill the process
            pid = int(line.split(None,1)[0])
            os.kill(pid,signal.SIGKILL)
            
def createSaveFolder():
    try:
        os.makedirs(save_location)
    except:
        print("Failed to create the new directory")
    os.chdir(save_location)

def captureImages():
    gp(triggerCommand)
    sleep(1)
    gp(downloadCommand)
    gp(clearCommand)
    
    
def renameFiles(ID):
    for filename in os.listdir("."):
        if len(filename) < 13:
            if filename.endswith(".JPG"):
                os.rename(filename, (shot_time + ID +" .JPG"))
                print("Renamed the JPG")
           # elif filename.endswith(".CR2"):
               # os.rename(filename, (shot_time + ID + ".CR2"))
              #  print("Rename the CR2")

#define running time
#def minutesTimer(n):
 #   for i in range(n):
 #       sleep(60*n)
#def hoursTimer(n):
  #  for i in range(n):
  #      sleep(60*60*n)
    
#hoursTimer(hours)
#minutesTimer(minutes)

killgphoto2Process()
gp(clearCommand)

timestart=time()
timeend=timestart+10*60

while(True):
    if time()>timeend:
        sys.exit()
    
    #Get value of trigger
    trigger = db.child('trigger').child("state").get().val()
    #while loop to run untill user kills programs
    if(trigger == "ON"):
        #timeon=time()
        #timeoff=timeon+minutes*60+hours*3600
        #if time()>timeoff:
            #trigger = db.child('trigger').child("state").set('OFF')
        #while (True):
        shot_date =datetime.now().strftime("%Y-%m-%d")
        shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        createSaveFolder()
        captureImages()        
        renameFiles(picID)
        sleep(sleepTime2)
    
#sleep(0.1)

    
