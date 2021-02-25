#camera.py
# import the necessary packages
import cv2
import face_recognition
import numpy as np

# variables
reduction = 4
font = cv2.FONT_HERSHEY_COMPLEX
width,height = 800,600

class VideoCamera(object):
    def __init__(self,Lnames,encodings):
        self.video = cv2.VideoCapture(0)
        self.Lnames = Lnames
        self.encodings = encodings
    def __del__(self):
        self.video.release()

    def get_frame(self):
        #extracting frames
        ret, frame = self.video.read()
        if ret:
            frame_rgb = frame[:,:,::-1]
            frame_rgb = cv2.resize(frame_rgb,(0,0),fx=1.0/reduction,fy = 1.0/reduction)
            face_locations = face_recognition.face_locations(frame_rgb)
            for (top,right,bottom,left) in face_locations:
                top = top * reduction
                right = right* reduction
                bottom = bottom* reduction
                left = left * reduction
                color = (255,0,0)
                cv2.rectangle(frame,(left,top),(right,bottom),color,2)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

