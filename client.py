import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
from login import *
from signup import *
from DoctorGUI import *
import socket 
import numpy as np
from scipy.signal import find_peaks
import json
from PyQt5.QtWidgets import QMessageBox


# HOST = 'localhost'
# PORT = 5000
# #Connect to server
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect((HOST, PORT))

emg_signals = [r'Datasets\EMG\emg_healthy.dat',r'Datasets\EMG\emg_myopathy.dat',r'Datasets\EMG\emg_neuropathy.dat']
emg_data = []
peaks = []
for emg in emg_signals:
    emg_data.append(np.fromfile(emg, dtype=int) / 10000000)
    peaks.append(len(find_peaks(emg_data[-1], height=0)[0]))

# def client_program():
#     host = 'localhost'  # as both code is running on same pc
#     port = 5000  # socket server port number

#     client_socket = socket.socket()  # instantiate
#     client_socket.connect((host, port))  # connect to the server

#     data = input(' -> ')
#     client_socket.send(data.encode())  # send data to the server
#     data = client_socket.recv(1024).decode()  # receive response

#     print('Received from server: ' + data)  # show response


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_layout = None
        self.setupUi("signup")
        # Create a socket object
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Define the server address and port
        HOST = 'localhost'
        PORT = 5000

        # Connect to the server
        self.client_socket.connect((HOST, PORT))

    def setupUi(self, layout_name):
        if layout_name == "signup":
            self.current_layout = SignUp()
        elif layout_name == "login":
            self.current_layout = LogIn()
        elif layout_name == "Doctor":
            self.current_layout = Ui_MainWindow()

        self.current_layout.setupUi(self)
        if layout_name == "signup":
            self.current_layout.loginButton.clicked.connect(lambda: self.switch_layout("login"))
            self.current_layout.signupButton.clicked.connect(self.register_user)
        elif layout_name == "login":
            self.current_layout.pushButton.clicked.connect(lambda: self.switch_layout("signup"))
            self.current_layout.Login_button.clicked.connect(lambda: self.switch_layout("Doctor"))
        elif layout_name == "Doctor":
            self.current_layout.logoutButton.clicked.connect(lambda: self.switch_layout("login"))
            

    def register_user(self):
        
        username = self.current_layout.textEdit_4.toPlainText()
        email = self.current_layout.textEdit_3.toPlainText()
        age = self.current_layout.ageText.toPlainText()
        gender =None
        if self.current_layout.radioButton_2.isChecked():
            gender = "Male"
        elif self.current_layout.radioButton_3.isChecked():
            gender = "Female"
        password = self.current_layout.textEdit_2.toPlainText()
        confirm = self.current_layout.textEdit.toPlainText()

        # Check if all required fields are filled
        if not all([username, email, age, gender, password, confirm]):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Please fill in all the required fields.")
            msg.setWindowTitle("Warning")
            msg.exec_()
            return

        user_data = {
            'username': username,
            'email': email,
            'age': age,
            'gender': gender,
            'password': password
        }
        # Encode data
        #TODO: hamza check sending json file to the server
        encoded_data = json.dumps(user_data).encode()

        # Send data to server
        self.client_socket.sendall(encoded_data)

        
        self.current_layout.signupButton.clicked.connect(lambda: self.switch_layout("Doctor"))
    
    def user_login(self):
        username = self.current_layout.textEdit_4.toPlainText()
        password = self.current_layout.textEdit_2.toPlainText()
        user_data = {
            'username': username,
            'password': password
        }
        # Encode data
        encoded_data = json.dumps(user_data).encode()

        # Send data to server
        self.client_socket.sendall(encoded_data)

        # Receive data from the server
        data = self.client_socket.recv(1024).decode()
        print('Received from server: ' + data)
       
    def switch_layout(self, layout_name):
        # Clear existing layout
        self.current_layout = None
        self.centralWidget().deleteLater()  # Clear existing widgets
        # Setup new layout
        
        self.setupUi(layout_name)
        self.adjustSize()
        
   


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    #client_program()
    sys.exit(app.exec_())