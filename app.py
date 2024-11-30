#app.py

from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QDateEdit, QLineEdit, QComboBox, QTableWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import QDate, Qt
from database import fetch_expenses, add_expenses, delete_expenses, update_expenses  # Assuming `update_expenses` is defined in `database.py`

class ExpenseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.load_table_data()

    def settings(self):
        self.setGeometry(0, 0, 550, 550)
        self.setWindowTitle('Expense Tracker App')

    def initUI(self):
        # Create all objects
        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.dropdown = QComboBox()
        self.amount = QLineEdit()
        self.description = QLineEdit()

        self.btn_add = QPushButton('Add Expense')
        self.btn_delete = QPushButton('Delete Expense')
        self.btn_edit = QPushButton('Edit Expense')  # New button to edit

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(['ID', 'Date', 'Category', 'Amount', 'Description'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.total_label = QLabel("Total Expenses: $0")  # Label for showing the total expenses
        
        self.populate_dropdown()

        self.btn_add.clicked.connect(self.add_expense)
        self.btn_delete.clicked.connect(self.delete_expense)
        self.btn_edit.clicked.connect(self.edit_expense)  # Connect the edit button to edit function
        
        # Set up layout
        self.setup_layout()
        self.apply_style()

    def setup_layout(self):
        master = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()

        # Row1
        row1.addWidget(QLabel('Date'))
        row1.addWidget(self.date_box)
        row1.addWidget(QLabel('Category'))
        row1.addWidget(self.dropdown)

        # Row2
        row2.addWidget(QLabel('Amount'))
        row2.addWidget(self.amount)
        row2.addWidget(QLabel('Description'))
        row2.addWidget(self.description)

        # Row3
        row3.addWidget(self.btn_add)
        row3.addWidget(self.btn_edit)
        row3.addWidget(self.btn_delete)

        master.addLayout(row1)
        master.addLayout(row2)
        master.addLayout(row3)
        master.addWidget(self.table)
        master.addWidget(self.total_label)  # Add total label to layout

        self.setLayout(master)

    def apply_style(self):
        self.btn_add.setObjectName("btn_add")
        self.btn_delete.setObjectName("btn_delete")
        self.btn_edit.setObjectName("btn_edit")

        self.setStyleSheet("""
            QWidget { background-color: #e3e9f2; font-family: Arial, sans-serif; font-size: 14px; color: #333; }
                           
            QLabel { font-size: 16px; color: #2c3e50; font-weight: bold; padding: 5px; }
                              
            QLineEdit, QComboBox, QDateEdit { background-color: #fff; font-size: 14px; color: #333; border: 1px solid #b0bfc6; border-radius: 8px; padding: 5px; hover:  }
            
            QLineEdit:hover {background-color: #ecf0f1}
            QDateEdit:hover {background-color: #ecf0f1} 
            QComboBox:hover {background-color: #ecf0f1} 
             
                       
            QPushButton { background-color: #d3e0ea; font-size: 14px; color: #333; border: 1px solid #b0bfc6; border-radius: 10px; padding: 6px 12px; }
                           
            QTableWidget { background-color: #fff; alternate-background-color: #f2f7fb; gridline-color: #c0c9d0; selection-background-color: #4caf50; selection-color: white; font-size: 14px; border: 1px solid #cfd9e1; padding: 5px; }
                           
            QHeaderView::section { background-color: #e3e9f2; font-weight: bold; font-size: 14px; color: #2c3e50; padding: 5px; border: 1px solid #cfd9e1; }
            
            #btn_add { background-color: green; color: white; border-radius: 8px; padding: 8px 16px; font-size: 14px; }
            #btn_add:hover {background-color: #218838}
            
            #btn_delete { background-color:#f70707 ; color: white; border-radius: 8px; padding: 8px 16px; font-size: 14px; }
            #btn_delete:hover {background-color: #c82333}
            
            #btn_edit { background-color: #ff9800; color: white; border-radius: 8px; padding: 8px 16px; font-size: 14px; }
            #btn_edit:hover {background-color: #e69500}
                           
            """)

    def populate_dropdown(self):
        categories = ['Food', 'Rent', 'Entertainment', 'Shopping', 'Other']
        self.dropdown.addItems(categories)

    def load_table_data(self):
        expenses = fetch_expenses()
        self.table.setRowCount(0)
        total_expense = 0

        for row_idx, expense in enumerate(expenses):
            self.table.insertRow(row_idx)
            for col_idx, data in enumerate(expense):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
            total_expense += float(expense[3])  # Sum up the amounts

        self.update_total_label(total_expense)  # Update total expense label

    def update_total_label(self, total):
        self.total_label.setText(f"Total Expenses: ${total:.2f}")

    def clear_inputs(self):
        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()

    def add_expense(self):
        date = self.date_box.date().toString('yyyy-MM-dd')
        category = self.dropdown.currentText()
        amount = self.amount.text()
        description = self.description.text()

        if not amount or not description:
            QMessageBox.warning(self, 'Input Error', 'Amount and Description cannot be empty!')
            return

        if add_expenses(date, category, amount, description):
            self.load_table_data()  # Refresh table data
            self.clear_inputs()
        else:
            QMessageBox.critical(self, 'Error', 'Failed to add expense!')

    def delete_expense(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, 'Uh oh', 'You need to choose a row to delete.')
            return

        expense_id = int(self.table.item(selected_row, 0).text())
        confirm = QMessageBox.question(self, 'Confirm', 'Are you sure you want to delete?', 
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm == QMessageBox.StandardButton.Yes:
            if delete_expenses(expense_id):
                self.load_table_data()  # Refresh table data
                QMessageBox.information(self, 'Success', 'Expense deleted successfully!')
            else:
                QMessageBox.critical(self, 'Error', 'Failed to delete expense!')

    def edit_expense(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, 'Selection Error', 'Please select a row to edit.')
            return

        # Fetch the existing data
        expense_id = int(self.table.item(selected_row, 0).text())
        date = self.date_box.date().toString('yyyy-MM-dd')
        category = self.dropdown.currentText()
        amount = self.amount.text()
        description = self.description.text()

        if not amount or not description:
            QMessageBox.warning(self, 'Input Error', 'Amount and Description cannot be empty!')
            return

        # Update the record in the database
        if update_expenses(expense_id, date, category, amount, description):
            self.load_table_data()  # Refresh table data to update total and display new values
            QMessageBox.information(self, 'Success', 'Expense updated successfully!')
            self.clear_inputs()
        else:
            QMessageBox.critical(self, 'Error', 'Failed to update expense!')
