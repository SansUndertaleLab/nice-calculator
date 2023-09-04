import tkinter as tk
from tkinter import Entry, Button, StringVar, Label
import calculator  

def on_button_click(event):
    text = event

    if text == "=":
        expression = entry.get()
        result = calculator.calculate(expression)
        entry.delete(0, tk.END)  
        entry.insert(tk.END, str(result))
    elif text == "C":
        entry.delete(0, tk.END)
    elif text == "bksp":
        current_input = entry.get()
        new_input = current_input[:-1]  
        entry.delete(0, tk.END)
        entry.insert(tk.END, new_input)
    else:
        entry.insert(tk.END, text)


root = tk.Tk()
root.title("Calculator")


entry = Entry(root, font=("Helvetica", 16), bd=10, width=30, justify="right")
entry.grid(row = 0, column = 0, columnspan = 4)


button_texts = [
    "C", "(", ")", "bksp",
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "0", ".", "pi", "+",
    "gr", "^", "=",
]

row, col = 1, 0
buttons = {}

for text in button_texts:
    if text == "=":
        column_span = 2
    else:
        column_span = 1
    button = Button(root, text=text, padx=30, pady=20, font=("Helvetica", 16))
    button.grid(row=row, column=col, columnspan = column_span, sticky="nsew")
    buttons[text] = button  
    col += 1
    if col > 3:
        col = 0
        row += 1

for button_text, button in buttons.items():
    button.configure(command = lambda button_text = button_text: on_button_click(button_text))

root.mainloop()
