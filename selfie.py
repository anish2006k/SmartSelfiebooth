from tkinter import *
from PIL import ImageTk, Image
import cv2
from playsound import playsound
import os
import webbrowser

root = Tk()
root.title("Smart Selfie Booth")
root.configure(bg='dark slate gray')

lbl = Label(root, text="My selfie Corner", font=('Forte', 24), bg='dark slate gray', fg='gold2')
lbl.grid()

vdo = Label(root)
vdo.grid(padx=50)

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')

def detect(frame):
    global face_cascade
    global smile_cascade

    frame = cv2.copyMakeBorder(frame, 30, 30, 30, 30, cv2.BORDER_CONSTANT)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 20)
        for (sx, sy, sw, sh) in smiles:
            image = str(x)+"_"+str(y)+"smiles.jpg"
            cv2.imwrite(image, frame)

            playsound("camera.mp3")
            cv2.imshow("Selfiee", cv2.imread(image))
    return frame

def video_stream():
    _, frame = cap.read()
    canvas = detect(frame)
    cv2image = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    vdo.imgtk = imgtk
    vdo.configure(image=imgtk)
    vdo.after(1, video_stream)

video_stream()

def openDir():
    webbrowser.open(os.getcwd())

btn = Button(root, text="Gallery", width=50, bg="gold2", command=openDir)
btn.grid(pady=25)

root.mainloop()
