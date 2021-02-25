from flask import Flask, render_template,Response, request, redirect
from flask.helpers import url_for
from pymongo import MongoClient
import os
import face_recognition
import sys
import numpy as np
import cv2

#ALLOWED:
ALLOWED_EXTENSIONS = {'png','jpg','jpeg'}

#Mongo client
client = MongoClient('localhost',27017,username="root",password="Adriano28") #Client constructor
db = client['face_db'] #client collection
faces=db.face #faces 

#Check file:
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

#CV variables:
reduction = 4
font = cv2.FONT_HERSHEY_COMPLEX
width,height = 800,600

cap = cv2.VideoCapture(0)


def gen(camera):
    while(True):
        ret, frame = camera.read()
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
gen(cap)
cap.release()
cv2.destroyAllWindows()
