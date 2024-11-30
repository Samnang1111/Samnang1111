# main.py
import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from database import init_db
from app import ExpenseApp

def main():
    
    
    app = QApplication(sys.argv) # ''sys.argv'' to ensure it runs smootly

    if not init_db('expense.db'):
        QMessageBox.critical(None, 'Error', 'Could not load your database...')
        sys.exit(1)

    window = ExpenseApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

