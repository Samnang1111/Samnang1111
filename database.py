
# database.py

from PyQt6.QtSql import QSqlDatabase, QSqlQuery

def init_db(db_name):
    """Initialize the SQLite database and create the expenses table if it doesn't exist."""
    database = QSqlDatabase.addDatabase('QSQLITE')
    database.setDatabaseName(db_name)

    if not database.open():
        return False
    
    # Create the expenses table
    query = QSqlQuery()
    query.exec("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL,
            description TEXT
        )
    """)
    
    return True

def fetch_expenses():
    """Fetch all expenses from the database."""
    query = QSqlQuery('SELECT * FROM expenses ORDER BY date DESC')
    expenses = []

    while query.next():
        row = [query.value(i) for i in range(5)]  # Assuming 5 columns in db
        expenses.append(row)
    return expenses

def add_expenses(date, category, amount, description):
    """Add a new expense to the database."""
    query = QSqlQuery()
    query.prepare("""
        INSERT INTO expenses (date, category, amount, description)
        VALUES (?, ?, ?, ?)
    """)
    query.addBindValue(date)
    query.addBindValue(category)
    query.addBindValue(amount)
    query.addBindValue(description)

    return query.exec()

def delete_expenses(expense_id):
    """Delete an expense from the database by its ID."""
    query = QSqlQuery()
    query.prepare('DELETE FROM expenses WHERE id = ?')
    query.addBindValue(expense_id)

    return query.exec()

def update_expenses(expense_id, date, category, amount, description):
    """Update an existing expense in the database."""
    query = QSqlQuery()
    query.prepare("""
        UPDATE expenses
        SET date = ?, category = ?, amount = ?, description = ?
        WHERE id = ?
    """)
    query.addBindValue(date)
    query.addBindValue(category)
    query.addBindValue(amount)
    query.addBindValue(description)
    query.addBindValue(expense_id)

    return query.exec()



# ___
def init_users_table():
    """Initialize the users table if it doesn't exist."""
    query = QSqlQuery()
    query.exec("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

def add_user(username, password):
    """Add a new user to the users table."""
    query = QSqlQuery()
    query.prepare("""
        INSERT INTO users (username, password)
        VALUES (?, ?)
    """)
    query.addBindValue(username)
    query.addBindValue(password)
    return query.exec()

def verify_user(username, password):
    """Verify a user's credentials."""
    query = QSqlQuery()
    query.prepare("""
        SELECT id FROM users WHERE username = ? AND password = ?
    """)
    query.addBindValue(username)
    query.addBindValue(password)
    query.exec()
    return query.next()  # Returns True if a match is found

from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from database import verify_user, init_db, init_users_table, add_user

class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 150)

        # Widgets
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.authenticate)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

    def authenticate(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return

        if verify_user(username, password):
            QMessageBox.information(self, "Success", "Login successful!")
            self.close()  # Close the login window
            self.open_expense_app()  # Open the main application
        else:
            QMessageBox.critical(self, "Error", "Invalid credentials. Try again.")

    def open_expense_app(self):
        from app import ExpenseApp
        self.expense_app = ExpenseApp()
        self.expense_app.show()
