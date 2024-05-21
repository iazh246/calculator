import customtkinter as ctk
from customtkinter import *

import tkinter as tk
import threading, time

from vars import *

def equals():
    print("Equals button pressed")
    
    try:
        result = eval(calculator_textbox.get())
        calculator_textbox.delete(0, tk.END)
        calculator_textbox.insert(0, str(result))
    except:
        calculator_textbox.delete(0, tk.END)
        calculator_textbox.insert(0, "Syntax Error")

def button_pressed(button):
    if button == '=':
        equals()
    else:
        current_text = calculator_textbox.get()
        calculator_textbox.delete(0, tk.END)
        calculator_textbox.insert(0, current_text + button)
        
button_to_command = {
    '7': lambda: button_pressed('7'), '8': lambda: button_pressed('8'), '9': lambda: button_pressed('9'), '/': lambda: button_pressed('/'), 
    '4': lambda: button_pressed('4'), '5': lambda: button_pressed('5'), '6': lambda: button_pressed('6'), '*': lambda: button_pressed('*'), 
    '1': lambda: button_pressed('1'), '2': lambda: button_pressed('2'), '3': lambda: button_pressed('3'), '-': lambda: button_pressed('-'), 
    '.': lambda: button_pressed('.'), '0': lambda: button_pressed('0'), '=': equals, '+': lambda: button_pressed('+')
}

# Function to generate suggestions
def generate_suggestions(expression):
    suggestions = []

    # Add simple typo corrections
    if '+' in expression:
        suggestions.append(expression.replace('+', '-'))
    if '-' in expression:
        suggestions.append(expression.replace('-', '+'))
    
    # Add more sophisticated suggestions as needed

    return suggestions[:5]  # Limit to 5 suggestions

# Function to update suggestions
def update_suggestions():
    while True:
        global calculator_textbox
        
        expression = calculator_textbox.get()
        suggestions = generate_suggestions(expression)
        for widget in suggestions_bar.winfo_children():
            widget.destroy()
        for suggestion in suggestions:
            suggestion_button = ctk.CTkButton(suggestions_bar, text=suggestion, width=150, height=40, fg_color=color_palate['secondary'], hover_color=color_palate['highlight'], corner_radius=5, command=lambda s=suggestion: calculator_textbox.insert(tk.END, s))
            suggestion_button.pack(side='left', padx=5, pady=5)
        time.sleep(1)  # Update suggestions every second

update_thread = threading.Thread(target=update_suggestions)
update_thread.start()

root = ctk.CTk()
root.geometry(f"{bheight//3}x{bwidth//4}+0+0")

calculator_bar = ctk.CTkFrame(root, height=60, bg_color=color_palate['dark'], fg_color=color_palate['dark'], corner_radius=0)
calculator_bar.pack(fill='x', side='top')

calculator_textbox = ctk.CTkEntry(calculator_bar, font=fonts['textbox'], fg_color=color_palate['dark'], height=75, corner_radius=0)
calculator_textbox.pack(fill='x')

button_frame = ctk.CTkFrame(root, corner_radius=0, bg_color=color_palate['main'])
button_frame.pack(side='top', fill='both', expand=True)

for i, button in enumerate(buttons):
    button_command = button_to_command[button]
    
    ctk_button = ctk.CTkButton(button_frame, text=button, width=80, height=80, fg_color=color_palate['secondary'], bg_color=color_palate['main'], hover_color=color_palate['highlight'], corner_radius=0, command=button_command)
    ctk_button.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
    
    col += 1
    
    if (i + 1) % 4 == 0:
        row += 1
        col = 0

suggestions_bar = ctk.CTkFrame(root, bg_color=color_palate['dark'], fg_color=color_palate['dark'], corner_radius=0)
suggestions_bar.pack(fill='both', side='bottom')

root.mainloop()