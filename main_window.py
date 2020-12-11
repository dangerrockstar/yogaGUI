"""
somthing here type
"""

# import system module
import sys

# import some PyQt5 modules
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer

# import Opencv module
import cv2
import numpy as np 
from ui_main_window import *

class MainWindow(QWidget):
    # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
        #mask
        self.img2 = cv2.imread('./Clown_Mask.png')
        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        # set control_bt callback clicked  function
        self.ui.control_bt.clicked.connect(self.controlTimer)

    def basicImgProc(self , img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face = self.face_cascade.detectMultiScale(gray,1.3,5)
        for (x,y,w,h) in face:
            cv2.rectangle(img,(x,x),(x+w,y+h),(0,225,0),2)
            # img = np.concatenate((img, self.img2), axis=1)
            return img
        
    # view camera
    def viewCam(self):
        # read image in BGR format
        ret, image = self.cap.read()
        # rotate image 
        image = cv2.flip(image,1)
        # call function
        self.basicImgProc(image)
        # cv2.rectangle(image , (0,250) , (250,0) ,(0,255,0) , 5 )
        # get image infos
        height, width, channel = image.shape
        step = channel * width
        # create QImage from image
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label
        self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))

    # start/stop timer
    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture
            self.cap = cv2.VideoCapture(0)
            # start timer
            self.timer.start(20)
            # update control_bt text
            self.ui.control_bt.setText("Stop Camera")
        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update control_bt text
            self.ui.control_bt.setText("Start Camera")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())