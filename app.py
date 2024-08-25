import tkinter as tk
from tkinter import scrolledtext, messagebox
from backend import ChatBackend
import threading
import time


class ChatApp:
    def __init__(self, root):
        self.backend = ChatBackend()
        self.root = root
        self.root.title("Chat Application")

        self.login_screen()

    def login_screen(self):
        """Display the login screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("300x200")

        self.username_label = tk.Label(self.root, text="Username:")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.root, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self.root, text="Login", command=self.login)
        self.login_button.pack(pady=5)

        self.register_button = tk.Button(
            self.root, text="Register", command=self.register
        )
        self.register_button.pack(pady=5)

    def register(self):
        """Register a new user."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.backend.register_user(username, password):
            messagebox.showinfo("Success", "Registration successful! Please log in.")
        else:
            messagebox.showerror("Error", "Username already exists!")

    def login(self):
        """Authenticate and log in the user."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.backend.authenticate_user(username, password):
            self.choose_channel_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    def choose_channel_screen(self):
        """Display the channel selection screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("300x150")

        self.channel_label = tk.Label(self.root, text="Enter Channel Name:")
        self.channel_label.pack(pady=10)
        self.channel_entry = tk.Entry(self.root)
        self.channel_entry.pack(pady=5)

        self.join_button = tk.Button(
            self.root, text="Join Channel", command=self.start_chat
        )
        self.join_button.pack(pady=10)

    def start_chat(self):
        """Start the chat after selecting a channel."""
        channel = self.channel_entry.get()
        if channel:
            self.backend.set_channel(channel)
            self.chat_screen()

    def chat_screen(self):
        """Display the chat screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("500x400")

        self.chat_display = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, state="disabled"
        )
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.pack(padx=10, pady=10, fill=tk.X, expand=False)

        self.message_entry = tk.Entry(self.entry_frame)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(
            self.entry_frame, text="Send", command=self.send_message
        )
        self.send_button.pack(side=tk.RIGHT)

        self.load_history()

        # Start a thread to listen for incoming messages
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def load_history(self):
        """Load the message history into the chat display."""
        history = self.backend.get_message_history()
        self.chat_display.config(state="normal")
        for msg in history:
            timestamp, message = msg.split(":", 1)
            self.chat_display.insert(
                tk.END, f"{time.ctime(int(timestamp))}: {message}\n"
            )
        self.chat_display.config(state="disabled")
        self.chat_display.yview(tk.END)

    def send_message(self, event=None):
        """Send a message and update the chat display."""
        message = self.message_entry.get()
        if message:
            self.backend.publish_message(message)
            self.message_entry.delete(0, tk.END)

    def receive_messages(self):
        """Receive and display messages from the channel."""
        for message in self.backend.listen_messages():
            self.chat_display.config(state="normal")
            self.chat_display.insert(tk.END, f"Friend: {message}\n")
            self.chat_display.config(state="disabled")
            self.chat_display.yview(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
