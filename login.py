from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QMessageBox
from PyQt6.QtCore import Qt
import sys

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(0, 0, 550, 550)
        self.setWindowTitle('Expense Tracker App')

        layout = QGridLayout()
        layout.setSpacing(5)
        self.setLayout(layout)

        title = QLabel('Login Form')
        layout.addWidget(title, 0, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)

        self.un_label = QLabel('Username: ')
        layout.addWidget(self.un_label, 1, 0)

        self.un_input = QLineEdit()
        layout.addWidget(self.un_input, 1, 1)
        
        self.pw_label = QLabel('Password: ')
        
        layout.addWidget(self.pw_label, 2, 0)

        self.pw_input = QLineEdit()
        self.pw_input.setEchoMode(QLineEdit.EchoMode.Password) # Hide the password
        layout.addWidget(self.pw_input, 2, 1)

        rem_label = QCheckBox('Remember me!')
        layout.addWidget(rem_label, 3, 0, Qt.AlignmentFlag.AlignLeft)

        fgPw = QPushButton('Forgot password?')
        layout.addWidget(fgPw, 3, 1, Qt.AlignmentFlag.AlignRight)

        lg_btn = QPushButton('Login')
        layout.addWidget(lg_btn, 4, 0, 1, 3, Qt.AlignmentFlag.AlignHCenter)

        rs_btn = QPushButton("Don't have an account? Register")
        layout.addWidget(rs_btn, 5, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)

        lg_btn.clicked.connect(self.login)
        
    def login(self):
        # print(self.un_input.text())
        # print(self.pw_input.text())
        if self.un_input.text() == 'Nang' and self.pw_input.text() == '1234':
            print('Password is correct.')
        else:
            print('Password is incorrect.')  

    def register(self):
        layout = QGridLayout()
        title = QLabel('Login Form')
        layout.addWidget(title, 0, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)
        self.un_label = QLabel('Username: ')
        layout.addWidget(self.un_label, 1, 0)
        

app = QApplication(sys.argv)

window = Window()
window.show()
app.exit(app.exec())



