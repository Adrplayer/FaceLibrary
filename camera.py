############################
#  FaceLibrary
# this is a core prototype not abel to use
# only allowed for development use

import cv2
import sys
import face_recognition
import os

#face loads:

Adrian = face_recognition.load_image_file("faces/Adrian.jpg")

#face encodings:

Adrian_encodings = face_recognition.face_encodings(Adrian)

#encodings register: 

knowed_encodings = []
knowed_names = []

#names register:
with open("names.txt","r") as names:
    for name in names:
        name = name.rstrip()
        knowed_names.append(name)
        temp_file = "faces/"+name+".jpg"
        print(temp_file)
        if os.path.exists(temp_file):
            temp_image = face_recognition.load_image_file(temp_file)
            knowed_encodings.append(face_recognition.face_encodings(temp_image))
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
    faces_locations = []
    faces_encodings = []
    faces_names = []
    temp_name = []
    if ret:
        frame_rgb = frame[:,:,::-1]
        frame_rgb = cv2.resize(frame_rgb,(0,0),fx=1.0/reduction,fy=1.0/reduction)
        faces_locations = face_recognition.face_locations(frame_rgb)
        faces_encodings = face_recognition.face_encodings(frame_rgb,faces_locations)
        for encoding in faces_encodings:
            coincidencias = []
            for know in knowed_encodings:
                temp_coincidence = face_recognition.compare_faces(know,encoding)
                coincidencias.append(temp_coincidence)
            if coincidencias[0][0]:
                temp_name = knowed_names[0]
            else:
                temp_name = "????"
            print(coincidencias)
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

