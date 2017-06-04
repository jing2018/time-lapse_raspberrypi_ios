from time import sleep
from datetime import datetime
from sh import gphoto2 as gp

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

def killgphoto2Process():
    p= subprocess.Popen(['ps','-A'],stdout=subprocess.PIPE)
    out, err =p.communicate()

    for line in out.splitlines():
        if b'gvfsd-gphoto2' in line:
            pid = int(line.split(None,1)[0])
            os.kill(pid,signal.SIGKILL)



shot_date =datetime.now().strftime("%Y-%m-%d")
shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
picID ="PiShots"

clearCommand = ["--folder","/store_00020001/DCIM/100CANON", "-R", "--delete-all-files"]
triggerCommand = ["--trigger-capture"]
downloadCommand =["--get-all-files"]


folder_name = shot_date + picID
save_location = "/home/pi/Desktop/gphoto/images/" +folder_name

def createSaveFolder():
    try:
        os.makedirs(save_location)
    except:
        print("Failed to create the new directory")
    os.chdir(save_location)

def captureImages():
    gp(triggerCommand)
    sleep(3)
    gp(downloadCommand)
    gp(clearCommand)
    
def renameFiles(ID):
    for filename in os.listdir("."):
        if len(filename) < 13:
            if filename.endswith(".JPG"):
                os.rename(filename, (shot_time + ID +" .JPG"))
                print("Renamed the JPG")
            elif filename.endswith(".CR2"):
                os.rename(filename, (shot_time + ID + ".CR2"))
                print("Rename the CR2")


killgphoto2Process()
gp(clearCommand)



while(True):
#Get value of trigger
    trigger = db.child('trigger').child("state").get().val()
#while loop to run untill user kills programs
    if(trigger == "ON"):
        #while (True):
        createSaveFolder()
        captureImages()
        renameFiles(picID)
        sleep(5)
    
#sleep(0.1)

    
