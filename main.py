try:
	from PySide2.QtUiTools import QUiLoader
	from PySide2.QtWidgets import QApplication , QMessageBox , QPushButton , QDialog 
	from PySide2.QtCore import QFile, QTimer
	from PySide2 import QtCore
	from PySide2.QtWidgets import QWidget
	from PySide2 import QtGui 
	import pics.pics
except:
	from PySide.QtUiTools import QUiLoader
	from PySide.QtGui import QApplication, QMessageBox, QPushButton, QDialog
	from PySide.QtCore import QFile, QTimer
	from PySide import QtCore
	import pics.pics2

import time
import sys
from datetime import datetime

TEST_STATUS = True

class MyGUI():

	def __init__(self, useFullscreen=True):
		self.files = [ "VideoPlay.ui"
                    ]
						
		self.windows = []
		self.frontScreen = None
		self.timer = None
		self.timeCnt = 0
		self.imageIndex = 0
		self.fullscreen = useFullscreen
		self.images = []
		self.small_text = []
		self.mode = None
		self.jobPickStatus = bool
		
		for file in self.files:
			uiFile = QFile(file)
			uiFile.open(QFile.ReadOnly)
			
			window = QUiLoader().load(uiFile)
			self.windows.append(window)
			
			if file == "VideoPlay.ui":
				window.pushButtonBig.clicked.connect(lambda:self.buttonPressed("splash"))
				
		self.timer = QTimer()
		self.timer.setInterval(1000)
		self.timer.setSingleShot(False)
		self.timer.timeout.connect(self.timerCB)
		
	def timerCB(self):
		print("Timer callback is called!")
		
		self.timeCnt += 1
		
		# this is for toggling screen for replenish mode
		if self.frontScreen == self.getScreen(2) and self.timeCnt >= 5:
		
			self.imageIndex += 1
			if self.imageIndex >= len(self.images):
				self.imageIndex = 0
		
			if(len(self.images) > 0):
				info = "image:url(:/" + self.images[self.imageIndex] + ");\n border:none"
				self.frontScreen.bTimage.setStyleSheet(info)
				
			self.timeCnt = 0
				
	def start(self):
		'''
		This is the function to call the first screen of display.
		This function should be called once only. 
		'''
 
		self.frontScreen = self.getScreen(0)
		if not self.fullscreen:
			self.frontScreen.show()
		else:
			self.frontScreen.showFullScreen()
		
	def getScreen(self, index):
		if index >= len(self.windows):
			print("Wrong value....")
			return None
			
		return self.windows[index]
			
	def buttonPressed(self, file, info=None):
		print("Pressed: " + file)
		
		newScreen = None
		
		if self.timer is not None:
			self.timer.stop()

		if file == "opencv":
            pass

if __name__ == "__main__":
    
	app = QApplication(sys.argv)
	
	ui = MyGUI(False)
	
	ui.start()
	
	sys.exit(app.exec_())
