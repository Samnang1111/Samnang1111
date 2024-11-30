import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

# Define the main window class
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Button Example")
        
        # Set up the layout
        layout = QVBoxLayout()

        # Create buttons
        button1 = QPushButton("Button 1")
        button1.clicked.connect(lambda: print("Button 1 clicked"))
        
        button2 = QPushButton("Button 2")
        button2.clicked.connect(lambda: print("Button 2 clicked"))

        # Add buttons to layout
        layout.addWidget(button1)
        layout.addWidget(button2)
        
        # Create additional buttons dynamically
        for i in range(3, 6):
            button = QPushButton(f"Button {i}")
            button.clicked.connect(lambda checked, i=i: print(f"Button {i} clicked"))
            layout.addWidget(button)

        # Set the layout for the main window
        self.setLayout(layout)

# Main application code
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
