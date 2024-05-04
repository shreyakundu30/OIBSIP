import tkinter as tk
from tkinter import ttk, messagebox
import string
import random
import pyperclip

class PasswordGeneratorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Random Password Generator")

        self.label_length = ttk.Label(master, text="Password Length:")
        self.label_length.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_length = ttk.Entry(master)
        self.entry_length.grid(row=0, column=1, padx=10, pady=10)

        self.label_complexity = ttk.Label(master, text="Complexity:")
        self.label_complexity.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.complexity_var = tk.StringVar()
        self.complexity_combobox = ttk.Combobox(master, textvariable=self.complexity_var,
                                                 values=["Low", "Medium", "High"])
        self.complexity_combobox.current(1)
        self.complexity_combobox.grid(row=1, column=1, padx=10, pady=10)

        self.label_characters = ttk.Label(master, text="Characters:")
        self.label_characters.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.lower_case_var = tk.IntVar()
        self.lower_case_check = ttk.Checkbutton(master, text="Lowercase", variable=self.lower_case_var)
        self.lower_case_check.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.upper_case_var = tk.IntVar()
        self.upper_case_check = ttk.Checkbutton(master, text="Uppercase", variable=self.upper_case_var)
        self.upper_case_check.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.digits_var = tk.IntVar()
        self.digits_check = ttk.Checkbutton(master, text="Digits", variable=self.digits_var)
        self.digits_check.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        self.symbols_var = tk.IntVar()
        self.symbols_check = ttk.Checkbutton(master, text="Symbols", variable=self.symbols_var)
        self.symbols_check.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        self.generate_button = ttk.Button(master, text="Generate Password", command=self.generate_password)
        self.generate_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.copy_button = ttk.Button(master, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(master, textvariable=self.password_var, state='readonly')
        self.password_entry.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

    def generate_password(self):
        length = self.get_password_length()
        complexity = self.complexity_var.get()
        characters = self.get_selected_characters()

        if not length:
            messagebox.showerror("Error", "Please enter a valid password length.")
            return

        if not any((self.lower_case_var.get(), self.upper_case_var.get(), self.digits_var.get(), self.symbols_var.get())):
            messagebox.showerror("Error", "Please select at least one character type.")
            return

        password = self.generate_random_password(length, characters)
        self.password_var.set(password)

    def get_password_length(self):
        try:
            length = int(self.entry_length.get())
            return length
        except ValueError:
            return None

    def get_selected_characters(self):
        characters = ""
        if self.lower_case_var.get():
            characters += string.ascii_lowercase
        if self.upper_case_var.get():
            characters += string.ascii_uppercase
        if self.digits_var.get():
            characters += string.digits
        if self.symbols_var.get():
            characters += string.punctuation
        return characters

    def generate_random_password(self, length, characters):
        if self.complexity_var.get() == "Low":
            return ''.join(random.choices(characters, k=length))
        elif self.complexity_var.get() == "Medium":
            return ''.join(random.choices(characters, k=length))
        elif self.complexity_var.get() == "High":
            if len(characters) < 8:
                messagebox.showwarning("Warning", "High complexity requires at least 8 characters.")
                return None
            else:
                return ''.join(random.sample(characters, k=length))

    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Success", "Password copied to clipboard.")
        else:
            messagebox.showerror("Error", "No password generated.")

def main():
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
