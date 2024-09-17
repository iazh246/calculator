import customtkinter, pyperclip, json
from customtkinter import *

with open('data.json', 'r') as file:
    data = json.load(file)

fonts = data['fonts']
color_palate = data['color_palate']
buttons = data['buttons']
row = data['row']
col = data['col']

button_to_command = {}
evaluation_history = []

n_undo = 0

replacements = {
    '^': '**', 
    'x': '*', '÷': '/', 
    'multiplied by': '*', 'times': '*', 
    'divided by': '/', 'plus': '+', 'minus': '-',
    'add': '+', 'subtract': '-',
    'into': '*', 'over': '/', 'equals': '=',
    'power of': '**', 'raised to': '^', 'to the power of': '**',
    
    
    # Swedish terms
    'multiplicerat med': '*', 'gånger': '*', 
    'dividerat med': '/', 'delat på': '/',
    'addera': '+', 'adderat med': '+','subtrahera': '-', 'subtraherat med': '-','minus': '-',
    'delat med': '/', 'gånger med': '*',
    
    
    # Mathematical symbols as words
    'plus sign': '+', 'minus sign': '-',
    'multiply sign': '*', 'times sign': '*', 'divide sign': '/',
    'power': '**',
    
    # Additional math terms
    'modulus': '%', 'mod': '%', 'sqrt': 'sqrt',
    'factorial': '!', 'logarithm': 'log'
}


def evaluate(): 
    if calculator_textbox.get() == '':
            calculator_textbox.delete(0, customtkinter.END)
            calculator_textbox.insert(0, ":)")
    else:   
        try:
            expression = calculator_textbox.get().strip().lower()

            # Loop through the dictionary and replace each occurrence
            for key, value in replacements.items():
                expression = expression.replace(key, value)

            if not evaluation_history or expression != evaluation_history[-1]:
                evaluation_history.append(expression)

            result = eval(expression)

            calculator_textbox.delete(0, customtkinter.END)
            calculator_textbox.insert(0, str(result))
        except:
            calculator_textbox.delete(0, customtkinter.END)
            calculator_textbox.insert(0, "Syntax Error")

def button_pressed(button): 
    if button == '=':
        evaluate()
    else:
        current_text = calculator_textbox.get()
        calculator_textbox.delete(0, customtkinter.END)
        calculator_textbox.insert(0, current_text + button)

def undo():
    global n_undo

    undo_len = len(evaluation_history)

    # Ensure n_undo stays within bounds
    if n_undo < undo_len:
        # Delete the current text
        calculator_textbox.delete(0, customtkinter.END)
        
        # Insert the previous evaluation from history
        calculator_textbox.insert(customtkinter.END, evaluation_history[undo_len - n_undo - 1])

        # Increment n_undo for the next undo
        n_undo += 1
    else:
        # If we exceed history, reset to the most recent evaluation
        n_undo = 0
        calculator_textbox.delete(0, customtkinter.END)
        calculator_textbox.insert(customtkinter.END, evaluation_history[-1])
    
    

for i in range(10):
    button_to_command[str(i)] = lambda i=i: button_pressed(str(i))

for operator in ['+', '-', '*', '/']:
    button_to_command[operator] = lambda operator=operator: button_pressed(operator)

button_to_command['.'] = lambda: button_pressed('.')
button_to_command['='] = evaluate



root = customtkinter.CTk()
root.geometry(f"360x540")
root.title("Calculator")

calculator_bar = customtkinter.CTkFrame(root, height=60, corner_radius=0,
                                        bg_color=color_palate['dark'], 
                                        fg_color=color_palate['dark'])
calculator_bar.pack(fill='x', side='top')

calculator_textbox = customtkinter.CTkEntry(calculator_bar, 
                                            height=75, corner_radius=10,
                                            font=tuple(fonts['textbox']), 
                                            fg_color=color_palate['dark'])
calculator_textbox.pack(fill='x', padx=5, pady=5)
calculator_textbox.bind("<Return>", lambda event: evaluate())

calc_bar_copy = customtkinter.CTkButton(calculator_bar, text='Copy', 
                                        width=80, height=80, corner_radius=10,
                                        fg_color=color_palate['secondary'], 
                                        hover_color=color_palate['highlight'], 
                                        command=lambda: pyperclip.copy(calculator_textbox.get()))
calc_bar_copy.pack(side='left', padx=5, pady=5)

calc_bar_paste = customtkinter.CTkButton(calculator_bar, text='Paste', 
                                         width=80, height=80, corner_radius=10,
                                         fg_color=color_palate['secondary'], 
                                         hover_color=color_palate['highlight'], 
                                         command=lambda: calculator_textbox.insert(customtkinter.END, pyperclip.paste()))
calc_bar_paste.pack(side='left', padx=5, pady=5)

calc_bar_undo = customtkinter.CTkButton(calculator_bar, text='Undo', 
                                        width=80, height=80, corner_radius=10, 
                                        fg_color=color_palate['secondary'], 
                                        hover_color=color_palate['highlight'], 
                                        command=undo)
calc_bar_undo.pack(side='left', padx=5, pady=5)

calc_bar_clear = customtkinter.CTkButton(calculator_bar, text='C', 
                                         width=80, height=80, corner_radius=10, 
                                         fg_color=color_palate['secondary'], 
                                         hover_color=color_palate['highlight'], 
                                         command=lambda: calculator_textbox.delete(0, customtkinter.END))
calc_bar_clear.pack(side='left', padx=5, pady=5)

calc_bar_reset_window_size = customtkinter.CTkButton(calculator_bar, text='Reset\nWindow\nSize', 
                                                     width=80, height=80, corner_radius=10,
                                                     fg_color=color_palate['secondary'],
                                                     hover_color=color_palate['highlight'],
                                                     command=lambda: root.geometry(f"360x540"))
calc_bar_reset_window_size.pack(side='left', padx=5, pady=5)

calc_bar_print_eval_history = customtkinter.CTkButton(calculator_bar, text='Print\nHistory', 
                                                      width=80, height=80, corner_radius=10,
                                                      fg_color=color_palate['secondary'],
                                                      hover_color=color_palate['highlight'],
                                                      command=lambda: print(evaluation_history))
calc_bar_print_eval_history.pack(side='left', padx=5, pady=5)

button_frame = customtkinter.CTkFrame(root, corner_radius=0, bg_color=color_palate['main'])
button_frame.pack(side='top', fill='both', expand=True)

for i, button in enumerate(buttons):
    button_command = button_to_command[button]
    
    ctk_button = customtkinter.CTkButton(button_frame, text=button, 
                                         width=80, height=80, corner_radius=10,
                                         fg_color=color_palate['secondary'], 
                                         hover_color=color_palate['highlight'], 
                                         font=tuple(fonts['button_big']),
                                         command=button_command)
    ctk_button.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
    
    col += 1
    
    if (i + 1) % 4 == 0:
        row += 1
        col = 0
        
    if button in ['.', '=', '+', '-', '*', '/']:
        ctk_button.configure(fg_color=color_palate['dark'])
        
root.mainloop()