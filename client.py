import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
from login import *
from signup import *
from DoctorGUI import *
from socket import *
import numpy as np
from scipy.signal import find_peaks


HOST = '127.0.0.1'
PORT = 5000
#Connect to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

emg_signals = [r'Datasets\EMG\emg_healthy.dat',r'Datasets\EMG\emg_myopathy.dat',r'Datasets\EMG\emg_neuropathy.dat']
emg_data = []
peaks = []
for emg in emg_signals:
    emg_data.append(np.fromfile(emg, dtype=int) / 10000000)
    peaks.append(len(find_peaks(emg_data[-1], height=0)[0]))

def client_program():
    host = 'localhost'  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    data = input(' -> ')
    client_socket.send(data.encode())  # send data to the server
    data = client_socket.recv(1024).decode()  # receive response

    print('Received from server: ' + data)  # show response


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_layout = None
        self.setupUi("signup")
        

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
            self.current_layout.signupButton.clicked.connect(lambda: self.switch_layout("Doctor"))
        elif layout_name == "login":
            self.current_layout.pushButton.clicked.connect(lambda: self.switch_layout("signup"))
            self.current_layout.Login_button.clicked.connect(lambda: self.switch_layout("Doctor"))
        elif layout_name == "Doctor":
            self.current_layout.logoutButton.clicked.connect(lambda: self.switch_layout("login"))

       
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
    client_program()
    sys.exit(app.exec_())