import face_recognition
import cv2
import csv
import numpy as np
import os
from datetime import datetime

video_capture= cv2.VideoCapture(0)

avr_img= face_recognition.load_image_file("faces/avr.jpg")
avr_encoding= face_recognition.face_encodings(avr_img)[0]

ayush_img= face_recognition.load_image_file("faces/ayush.jpg")
ayush_encoding= face_recognition.face_encodings(ayush_img)[0]

krish_img= face_recognition.load_image_file("faces/krish.jpg")
krish_encoding= face_recognition.face_encodings(krish_img)[0]

known_face_encoding = [
avr_encoding,
ayush_encoding,
krish_encoding,
]

known_faces_names = [
"avr",
"ayush",
"krish"
]

students = known_faces_names.copy()

face_locations = []
face_encodings = []
face_names = []
s=True

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

f = open(current_date+'.csv','w+',newline = '')
lnwriter = csv.writer(f)

while True:
    _,frame = video_capture.read()
    small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
    rgb_small_frame = small_frame[:,:,::-1]
    if s:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, known_face_locations=face_locations, num_jitters=1)
        face_names = []
