import tkinter as tk
import math

class Calculator:
    def __init__(self):
        self.expression = ''  # Initialize the expression attribute
        self.pi = math.pi
        self.exp = math.e
        
        # Initialize the GUI
        self.root = tk.Tk()
        self.root.title("Modern Calculator")
        self.root.configure(bg="#2E2E2E")
        self.root.geometry('400x500')
        
        # Display area setup
        self.display_text = tk.Text(self.root, height=2, width=19, font=('Helvetica', 28), bg='#1C1C1C', fg='#FFFFFF', bd=0, padx=10, pady=10)
        self.display_text.grid(columnspan=5, row=0, pady=20, padx=20)
        
        # Create calculator buttons
        self.create_buttons()
        
        # Bind keypresses to handle_keypress method
        self.root.bind('<Key>', self.handle_keypress)
        
        # Run the main event loop
        self.root.mainloop()

    def add_to_expression(self, symbol):
        self.expression += str(symbol)
        self.update_display(self.expression)

    def delete_last_character(self):
        self.expression = self.expression[:-1]
        self.update_display(self.expression)

    def evaluate_expression(self):
        try:
            # Replace % with '/100' for percentage calculations
            if '%' in self.expression:
                self.expression = self.expression.replace('%', '/100')
            result = str(eval(self.expression))
            self.update_display(result)
            self.expression = result
        except ZeroDivisionError:
            self.clear_expression()
            self.update_display('Error: Div by 0')
        except Exception:
            self.clear_expression()
            self.update_display('Undefined')

    def clear_expression(self):
        self.expression = ''
        self.update_display('')

    def calculate_log(self):
        try:
            result = str(math.log10(float(self.expression)))
            self.update_display(result)
            self.expression = result
        except ValueError:
            self.clear_expression()
            self.update_display('Error: Log')

    def calculate_sqrt(self):
        try:
            result = str(math.sqrt(float(self.expression)))
            self.update_display(result)
            self.expression = result
        except ValueError:
            self.clear_expression()
            self.update_display('Error: Sqrt')

    def handle_keypress(self, event):
        key = event.char
        if key.isdigit() or key in '+-*/()%':
            self.add_to_expression(key)
        elif key == '=' or key == '\r':
            self.evaluate_expression()
        elif key.lower() == 'l':
            self.calculate_log()
        elif key.lower() == 's':
            self.calculate_sqrt()
        elif key == '\x08':
            self.delete_last_character()
        elif key.lower() == 'c':
            self.clear_expression()

    def update_display(self, text):
        self.display_text.delete(1.0, 'end')
        self.display_text.insert(1.0, text)

    def create_button(self, text, row, col, command, bg_color, fg_color, width=4, height=2, font=('Helvetica', 18, 'bold')):
        button = tk.Button(self.root, text=text, width=width, height=height, font=font,
                           command=command, bg=bg_color, fg=fg_color, bd=0, relief='ridge')
        button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        return button

    def create_buttons(self):
        # Configure rows and columns for flexible spacing
        for i in range(1, 6):
            self.root.grid_rowconfigure(i, weight=1)
        for j in range(5):
            self.root.grid_columnconfigure(j, weight=1)
        
        # Define colors for buttons
        button_bg = "#4E4E4E"
        number_bg = "#3A3A3A"
        operator_bg = "#FF9500"
        text_color = "#FFFFFF"

        # Numeric and basic operation buttons
        self.create_button('1', 3, 1, lambda: self.add_to_expression('1'), number_bg, text_color)
        self.create_button('2', 3, 2, lambda: self.add_to_expression('2'), number_bg, text_color)
        self.create_button('3', 3, 3, lambda: self.add_to_expression('3'), number_bg, text_color)
        self.create_button('4', 4, 1, lambda: self.add_to_expression('4'), number_bg, text_color)
        self.create_button('5', 4, 2, lambda: self.add_to_expression('5'), number_bg, text_color)
        self.create_button('6', 4, 3, lambda: self.add_to_expression('6'), number_bg, text_color)
        self.create_button('7', 5, 1, lambda: self.add_to_expression('7'), number_bg, text_color)
        self.create_button('8', 5, 2, lambda: self.add_to_expression('8'), number_bg, text_color)
        self.create_button('9', 5, 3, lambda: self.add_to_expression('9'), number_bg, text_color)
        self.create_button('0', 6, 2, lambda: self.add_to_expression('0'), number_bg, text_color)
        self.create_button('C', 2, 1, self.clear_expression, button_bg, text_color)
        self.create_button('⌫', 2, 2, self.delete_last_character, button_bg, text_color)
        self.create_button('+', 3, 4, lambda: self.add_to_expression('+'), operator_bg, text_color)
        self.create_button('-', 4, 4, lambda: self.add_to_expression('-'), operator_bg, text_color)
        self.create_button('*', 5, 4, lambda: self.add_to_expression('*'), operator_bg, text_color)
        self.create_button('/', 6, 4, lambda: self.add_to_expression('/'), operator_bg, text_color)
        self.create_button('.', 6, 3, lambda: self.add_to_expression('.'), number_bg, text_color)
        self.create_button('%', 2, 3, lambda: self.add_to_expression('%'), button_bg, text_color)
        self.create_button('(', 6, 1, lambda: self.add_to_expression('('), button_bg, text_color)
        self.create_button(')', 6, 0, lambda: self.add_to_expression(')'), button_bg, text_color)
        self.create_button('=', 6, 4, self.evaluate_expression, operator_bg, text_color)
        self.create_button('π', 3, 0, lambda: self.add_to_expression(self.pi), button_bg, text_color)
        self.create_button('e', 4, 0, lambda: self.add_to_expression(self.exp), button_bg, text_color)
        self.create_button('log', 5, 0, self.calculate_log, button_bg, text_color)
        self.create_button('√', 2, 0, self.calculate_sqrt, button_bg, text_color)

# Run the Calculator
if __name__ == "__main__":
    Calculator()
