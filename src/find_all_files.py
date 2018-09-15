import os
import sys
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QLabel, QPushButton

class documentSearch(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Find a document")
        self.initUI()
        
    def initUI(self):
        self.label = QLabel( "Find a document")
        self.search_document_field = QLineEdit(self)
    
    def run(self):
        
        self.show()
        
    def find_all_files(self, file):
        operating_sys = sys.platform
        if operating_sys == "win32":
            thing = "\\"
        elif operating_sys == "linux":
            thing = '/'   
    # print(os.getcwd())
    # print(os.listdir())
   #  print(sys.platform)
    # os.chdir("../")
    # print(os.getcwd())
  
        for i in os.walk('/'):
        
            for j in i:
                if file in j or j == file:
                    print("File found!")
                    return "Path to file: " + str(i[0]) + thing + str(file)
                 # print("File name: " + str(file))
                else:
                    pass
    