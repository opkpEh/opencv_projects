import cv2
import os
from datetime import date
from datetime import datetime
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import joblib
from PIL import Image

def capture_and_recognize():
    cap = cv2.VideoCapture(0)
    
    taking_attendance = False

    while True:
        ret, frame = cap.read()
        faces = extract_faces(frame)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            face = cv2.resize(frame[y:y+h, x:x+w], (50, 50))
            identified_person = identify_face(face.reshape(1, -1))[0]
            cv2.putText(frame, f'{identified_person}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

            if taking_attendance:
                # Add the attendance for the identified person
                add_attendance(identified_person)

        cv2.imshow('Face Recognition', frame)

        key = cv2.waitKey(1) & 0xFF

        if key == 27:  # Press 'Esc' to exit
            break
        elif key == ord('t'):  # Press 't' to start taking attendance
            taking_attendance = not taking_attendance
            print("Taking attendance:", taking_attendance)
        elif key == ord('g'):  # Press 'g' to add a new student
            add_new_student()

    cap.release()
    cv2.destroyAllWindows()

def add_new_student():
    newusername = input("Enter the new student's name: ")
    newuserid = input("Enter the new student's ID: ")

    userimagefolder = 'static/faces/' + newusername + '_' + str(newuserid)
    if not os.path.isdir(userimagefolder):
        os.makedirs(userimagefolder)

    i, j = 0, 0
    cap = cv2.VideoCapture(0)

    while 1:
        _, frame = cap.read()
        faces = extract_faces(frame)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 20), 2)
            cv2.putText(frame, f'Images Captured: {i}/{nimgs}', (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 20), 2, cv2.LINE_AA)

            if j % 5 == 0:
                name = newusername + '_' + str(i) + '.jpg'
                cv2.imwrite(userimagefolder + '/' + name, frame[y:y+h, x:x+w])
                i += 1

            j += 1

        if j == nimgs * 5:
            break

        cv2.imshow('Adding new User', frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    print('Training Model')
    train_model()

image = Image.new('RGB', (1920, 1080), color='white')

image.save('background.png')
image.save('capture.png')

nimgs = 10

imgBackground = cv2.imread("background.png")

datetoday = date.today().strftime("%m_%d_%y")
datetoday2 = date.today().strftime("%d-%B-%Y")

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

if not os.path.isdir('Attendance'):
    os.makedirs('Attendance')
if not os.path.isdir('static'):
    os.makedirs('static')
if not os.path.isdir('static/faces'):
    os.makedirs('static/faces')
if f'Attendance-{datetoday}.csv' not in os.listdir('Attendance'):
    with open(f'Attendance/Attendance-{datetoday}.csv', 'w') as f:
        f.write('Name,Roll,Time')

def totalreg():
    return len(os.listdir('static/faces'))

def extract_faces(img):
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_points = face_detector.detectMultiScale(gray, 1.2, 5, minSize=(20, 20))
        return face_points
    except:
        return []

def identify_face(facearray):
    model = joblib.load('static/face_recognition_model.pkl')
    return model.predict(facearray)

def train_model():
    faces = []
    labels = []
    userlist = os.listdir('static/faces')
    for user in userlist:
        for imgname in os.listdir(f'static/faces/{user}'):
            img = cv2.imread(f'static/faces/{user}/{imgname}')
            resized_face = cv2.resize(img, (50, 50))
            faces.append(resized_face.ravel())
            labels.append(user)
    faces = np.array(faces)
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(faces, labels)
    joblib.dump(knn, 'static/face_recognition_model.pkl')

def extract_attendance():
    df = pd.read_csv(f'Attendance/Attendance-{datetoday}.csv')
    names = df['Name']
    rolls = df['Roll']
    times = df['Time']
    l = len(df)
    return names, rolls, times, l

def add_attendance(name):
    username = name.split('_')[0]
    userid = name.split('_')[1]
    current_time = datetime.now().strftime("%H:%M:%S")

    df = pd.read_csv(f'Attendance/Attendance-{datetoday}.csv')
    if int(userid) not in list(df['Roll']):
        with open(f'Attendance/Attendance-{datetoday}.csv', 'a') as f:
            f.write(f'\n{username},{userid},{current_time}')

def getallusers():
    userlist = os.listdir('static/faces')
    names = []
    rolls = []
    l = len(userlist)

    for i in userlist:
        name, roll = i.split('_')
        names.append(name)
        rolls.append(roll)

    return userlist, names, rolls, l

def capture_and_recognize():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        faces = extract_faces(frame)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            face = cv2.resize(frame[y:y+h, x:x+w], (50, 50))
            identified_person = identify_face(face.reshape(1, -1))[0]
            cv2.putText(frame, f'{identified_person}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

            # Add the attendance for the identified person
            add_attendance(identified_person)

        cv2.imshow('Face Recognition', frame)

        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    while True:
        command = input("Press 't' to take attendance, 'g' to add a new student, or 'q' to quit: ")
        if command == 't':
            capture_and_recognize()
        elif command == 'g':
            add_new_student()
        elif command == 'q':
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == '__main__':
    main()
