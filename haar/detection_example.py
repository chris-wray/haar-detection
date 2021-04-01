import numpy as np
import cv2
import shutil
import os
import time
import zipfile
import datetime

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
# these arent my files but i need to make my own
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')
os.chdir(r'C:\Users\Chris Wray\Documents\Projects\haar\facefolder')
#initialize variables
cap = cv2.VideoCapture(0)
face_count = 0
show_smile = False

## !!! MAKE SURE THE PATH IS RIGHT!!!
def to_string(date):
        ret_string = ''
        i = 0
        while i<len(date)-1:
                if date[i] == (':' or ':' or ' '):
                        #print('switched '+date[i]+' with -')
                        ret_string +='-'
                else:
                        ret_string+=date[i]
                i+=1      
        return ret_string

cur_time = time.time()

while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    smiles = smile_cascade.detectMultiScale(gray, 1.3, 5)
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        face_count +=1
        dt = to_string(str(datetime.datetime.now()))
        filename= ('COUNT'+str(face_count)+'.png')
        if(face_count%10 == 0):
                #destroy the previous windows to manage memory
                cv2.destroyAllWindows()
                #write every 10th face, need to play with these values
                cv2.imwrite(filename, img)
        if(((face_count%100 == 0) or (time.time()-100 > cur_time)) and (cur_time < time.time()+15) ):
                cur_time = time.time()
                dt = to_string(str(datetime.datetime.now()))
                print(dt)
                move_zip = zipfile.ZipFile((dt+'.zip'), 'w')
                print('backing up to ' + dt + '.zip')
                for file_names in os.listdir():
                        if file_names.endswith('.png'):
                                print('writing ' + file_names + ' to ' +dt+'.zip')
                                move_zip.write(file_names, compress_type=zipfile.ZIP_DEFLATED)
                move_zip.close()

                for file_names in os.listdir():
                        if file_names.endswith('.png'):
                                print('deleting: '+file_names)
                                os.unlink(file_names)
        
        for(ex, ey, ew, eh) in eyes:
                cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

### DISPLAY AND CHECK FOR
### ESC - EXIT
### 'spacebar' - Toggles Smiles

    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break



cap.release()