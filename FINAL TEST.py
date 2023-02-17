import numpy as np
import cv2,os
from PIL import Image
import pickle
import sqlite3
import serial


port = serial.Serial('COM6', baudrate=9600, writeTimeout=0)
cam = cv2.VideoCapture(0)    
recognizer = cv2.face.LBPHFaceRecognizer_create() 
recognizer.read('trainner.yml')
cascadePath = 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascadePath);
path = 'dataSet'

def getProfile(id):
    conn=sqlite3.connect("FaceID.db")
    cmd="SELECT * FROM People WHERE ID="+str(id)
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile


while True:
    check, im = cam.read()
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
    for (x,y,w,h) in faces:
        id,conf=recognizer.predict(gray[y:y+h,x:x+w])
        print(id)
        cv2.rectangle(im,(x,y),(x+w,y+h),(255,0,0),2)
        profile=getProfile(id)
        if(profile!=None):
            cv2.putText(im,str(profile[1]),(x-10,y-10),cv2.FONT_HERSHEY_COMPLEX ,1, (18,5,255), 2, cv2.LINE_AA )
            cv2.putText(im,str(profile[2]),(x-10,y-50),cv2.FONT_HERSHEY_COMPLEX ,1, (18,5,255), 2, cv2.LINE_AA )
            cv2.putText(im,str(profile[3]),(x-10,y-90),cv2.FONT_HERSHEY_COMPLEX ,1, (18,5,255), 2, cv2.LINE_AA )
            cv2.putText(im,str(profile[4]),(x-10,y-130),cv2.FONT_HERSHEY_COMPLEX ,1, (18,5,255), 2, cv2.LINE_AA )
        im = cv2.rectangle(im, (x,y), (x+w,y+h),(0,255,255),4)
        # Checking the ID
        # Replace the "ID == 2" with your ID so that LED chaser can start
        # working
        if(id == 1):
            port.write(str.encode('1'))
            print("sent 1")

        # These are the ID other than your face.
        else:
            port.write(str.encode('0'))
            

            
    cv2.imshow('im',im)
    cv2.waitKey(10)

im.release()
cv2.destroyAllWindows()

