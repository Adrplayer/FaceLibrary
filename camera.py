############################
#  FaceLibrary
# this is a core prototype not abel to use
# only allowed for development use

import cv2
import sys
import face_recognition
import os
import numpy as np


# knowed arrays
knowed_encodings = []
knowed_names = []

#names/encodings register:
with open("names.txt","r") as names:
    for name in names:
        name = name.rstrip()
        knowed_names.append(name)
        temp_file = "faces/"+name+".jpg"
        print(temp_file)
        if os.path.exists(temp_file):
            temp_image = face_recognition.load_image_file(temp_file)
            knowed_encodings.append(face_recognition.face_encodings(temp_image)[0])
        else:
            print(temp_file + " not exists,"+ name +" encodings not register"+"\n")
print (knowed_names)

#check existences:
if (not len(knowed_encodings)):
    sys.exit("the encodings list is empty, add images and names to use the system")

#CV variables:

reduction = 4 #factor to reduce the cal time, 5 by default

font = cv2.FONT_HERSHEY_COMPLEX #font to show the names in the render system

width, height = 800, 600 # frame dimensions

cap = cv2.VideoCapture(0) # Video Capture (camera)


#function to use face reconition
while (cap.isOpened()) :
    ret,frame = cap.read() #read from camera
    faces_locations = [] #location of the faces 
    faces_encodings = []
    faces_names = []
    if ret:
        frame_rgb = frame[:,:,::-1]
        frame_rgb = cv2.resize(frame_rgb,(0,0),fx=1.0/reduction,fy=1.0/reduction)
        faces_locations = face_recognition.face_locations(frame_rgb)
        faces_encodings = face_recognition.face_encodings(frame_rgb,faces_locations)
        faces_names = []
        for encoding in faces_encodings:
            matches = face_recognition.compare_faces(knowed_encodings,encoding)
            temp_name = "????"
            print(matches)
            face_distances = face_recognition.face_distance(knowed_encodings,encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                temp_name = knowed_names[best_match_index]
            faces_names.append(temp_name)
        for (top,right,bottom,left), temp_name in zip(faces_locations,faces_names):
            top = top * reduction
            right = right * reduction
            bottom = bottom * reduction
            left = left * reduction
            if temp_name != "????":
                color = (0,255,0)
            else:
                color = (0,0,255)
            cv2.rectangle(frame,(left,top),(right,bottom),color,2)
            cv2.rectangle(frame,(left,bottom-20),(right,bottom),color,-1)
            cv2.putText(frame,temp_name,(left,bottom-6),font,0.6,(0,0,0),1) 
        cv2.imshow("My Face",frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    else:
        print("No camera Conection")
        break


#close program
cap.release() #clear memory
cv2.destroyAllWindows() #close the opened windows

