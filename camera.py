#camera.py
# import the necessary packages
import cv2
import face_recognition
from face_recognition.api import face_distance
import numpy as np

# variables
reduction = 5
font = cv2.FONT_HERSHEY_COMPLEX
width,height = 800,600

class VideoCamera(object):
    def __init__(self,Lnames,encodings):
        self.video = cv2.VideoCapture(0)
        self.Lnames = Lnames
        self.knowed_encodings = encodings
        self.process_this_frame = True
        self.faces_names = []
    def __del__(self):
        self.video.release()

    def get_frame(self):
        #extracting frames
        ret, frame = self.video.read()
        
        if ret:
            frame_rgb = cv2.resize(frame,(0,0),fx=1.0/reduction,fy = 1.0/reduction)
            frame_rgb = frame_rgb[:,:,::-1]
            faces_locations = []
            faces_encodings = []
            faces_names = []

            if self.process_this_frame:
                faces_locations = face_recognition.face_locations(frame_rgb)
                faces_encodings = face_recognition.face_encodings(frame_rgb,faces_locations)


                for face_encoding in faces_encodings:
                    matches = face_recognition.compare_faces(self.knowed_encodings,face_encoding)
                    temp_name = "????"
                    if True in matches:
                        match_index = matches.index(True)
                        temp_name = self.Lnames[match_index]
                    faces_names.append(temp_name)
            self.process_this_frame = not self.process_this_frame

            for (top,right,bottom,left),name in zip(faces_locations,faces_names):
                top = top * reduction
                right = right* reduction
                bottom = bottom* reduction
                left = left * reduction
                if name != "????":
                    color = (0,255,0)
                else:
                    color = (0,0,255)
                cv2.rectangle(frame,(left,top),(right,bottom),color,2)
                cv2.rectangle(frame,(left,bottom-20),(right,bottom),color,cv2.FILLED)
                cv2.putText(frame,name,(left,bottom-6),font,0.6,(0,0,0),1)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

