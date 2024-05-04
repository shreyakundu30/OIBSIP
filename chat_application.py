import tkinter as tk
from tkinter import messagebox, scrolledtext
import socket
import threading
import time
import os
import base64

class ChatClient:
    def __init__(self, host, port, username):
        self.host = host
        self.port = port
        self.username = username
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.running = True
        self.thread = threading.Thread(target=self.receive_messages)
        self.thread.start()

    def receive_messages(self):
        while self.running:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if message.startswith("###"):
                    self.handle_command(message)
                else:
                    app.receive_message(message)
            except Exception as e:
                print(e)
                break

    def send_message(self, message):
        self.socket.sendall(message.encode('utf-8'))

    def handle_command(self, command):
        if command == "###exit":
            self.running = False
            self.socket.close()
            os._exit(0)

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Application")

        self.chat_label = tk.Label(root, text="Chat")
        self.chat_label.grid(row=0, column=0, padx=10, pady=10)

        self.users_label = tk.Label(root, text="Users")
        self.users_label.grid(row=0, column=1, padx=10, pady=10)

        self.chat_history = scrolledtext.ScrolledText(root, width=50, height=20)
        self.chat_history.grid(row=1, column=0, padx=10, pady=10, rowspan=2)

        self.users_list = tk.Listbox(root, width=20, height=20)
        self.users_list.grid(row=1, column=1, padx=10, pady=10, rowspan=2)

        self.message_entry = tk.Entry(root, width=50)
        self.message_entry.grid(row=3, column=0, padx=10, pady=10)

        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.grid(row=3, column=1, padx=10, pady=10)

        self.chat_client = None

        self.username = None
        self.password = None

        self.login_window()

    def login_window(self):
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Login")

        self.username_label = tk.Label(self.login_window, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=10)

        self.username_entry = tk.Entry(self.login_window)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        self.password_label = tk.Label(self.login_window, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=10)

        self.password_entry = tk.Entry(self.login_window, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        self.login_button = tk.Button(self.login_window, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def login(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()

        if not self.username or not self.password:
            messagebox.showerror("Error", "Please enter username and password.")
            return

        self.chat_client = ChatClient('127.0.0.1', 12345, self.username)

        self.root.title(f"Chat Application - Logged in as {self.username}")
        self.login_window.destroy()

    def receive_message(self, message):
        self.chat_history.insert(tk.END, message + '\n')

    def send_message(self):
        message = self.message_entry.get()
        if not message:
            return
        if message.startswith("/"):
            command = message.split()[0][1:]
            if command == "exit":
                self.chat_client.send_message("###exit")
                self.root.destroy()
                os._exit(0)
            else:
                messagebox.showerror("Error", "Invalid command")
        else:
            encrypted_message = self.encrypt_message(message)
            self.chat_client.send_message(encrypted_message)
            self.message_entry.delete(0, tk.END)

    def encrypt_message(self, message):
        key = 7
        encoded_chars = []
        for char in message:
            encoded_char = chr(ord(char) + key)
            encoded_chars.append(encoded_char)
        encoded_message = ''.join(encoded_chars)
        return encoded_message

def main():
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
