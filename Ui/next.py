from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLineEdit, QVBoxLayout, QWidget, QPushButton, QProgressBar
from PyQt5.QtCore import QRect, QSize, QThread, pyqtSignal
from PyQt5 import QtGui
import sys
import time

from pynput import keyboard

from main_p import suggest

class MyThread(QThread):
   
    signal = pyqtSignal(object)
    def __init__(self):
        super().__init__()
        self.cnt=0
    def run(self):
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()
        while self.cnt<100:
            self.cnt+=1
            time.sleep(.05)
            self.signal.emit([self.cnt,"Fine"])
        listener.stop()
    
    def on_press(self, key):
        if key == keyboard.Key.esc:
            return False  # stop listener
        else:
            self.cnt=0
            self.signal.emit([0,"Ok"])
           
     # stop listener; remove this if want more keys

    
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.threadstatus=False
        self.setWindowTitle("Progress Qthread")
        self.setGeometry(1100,500,400,300)
        
        vbox = QVBoxLayout()
        self.progressBar = QProgressBar()
        hbox = QHBoxLayout()
        self.btn1 = QPushButton("Option 1",self)
        self.btn2 = QPushButton("Option 2",self)
        self.btn3 = QPushButton("Option 3",self)

        self.btn3.clicked.connect(self.threadStart)
        self.inputBox = QLineEdit()
        hbox.addWidget(self.btn1)
        hbox.addWidget(self.btn2)
        hbox.addWidget(self.btn3)

        vbox.addWidget(self.progressBar)
        vbox.addWidget(self.inputBox)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        
        self.btn1.clicked.connect(self.suggestWord)
        self.inputBox.textChanged[str].connect(self.suggestWord)
        
    
    def threadStart(self):
        if not self.threadstatus:
            self.threadstatus=True
            self.thread = MyThread()
            self.thread.signal.connect(self.setProgressValue)
            self.thread.start()
    
    def setProgressValue(self,val):
        if val[1]=="Ok":
            self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint) 
            self.show()

        self.progressBar.setValue(val[0])
        if val[0]==100: 
            self.threadstatus=False
    
    def suggestWord(self,val):
        suggestedWords=suggest(val)
        if len(suggestedWords[1])==0:
            self.btn1.setText(suggestedWords[0])
            self.btn2.setText("")
            self.btn3.setText("")
        else:
            self.btn1.setText(suggestedWords[1][0])
            self.btn2.setText(suggestedWords[1][1])
            if len(suggestedWords[1])>2:
                self.btn3.setText(suggestedWords[1][2])

if __name__ == "__main__":
    App = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(App.exec()) 

    