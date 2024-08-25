import tkinter as tk
from tkinter import scrolledtext
from backend import ChatBackend
import threading
import time


class ChatApp:
    def __init__(self, root, channel):
        self.backend = ChatBackend(channel)
        self.root = root
        self.root.title(f"Chat - Channel: {channel}")

        # Set up the GUI elements
        self.chat_display = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, state="disabled"
        )
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.entry_frame = tk.Frame(root)
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
    channel = input("Enter the channel name to join: ")
    app = ChatApp(root, channel)
    root.mainloop()
