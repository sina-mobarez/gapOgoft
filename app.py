import sys
import threading
import time
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QMessageBox,
)
from PyQt5.QtCore import Qt
from backend import ChatBackend


class ChatApp(QWidget):
    def __init__(self):
        super().__init__()
        self.backend = ChatBackend()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Chat Application")
        self.setGeometry(100, 100, 400, 300)
        self.showLoginScreen()

    def showLoginScreen(self):
        self.clearLayout()

        self.username_label = QLabel("Username:")
        self.username_entry = QLineEdit()

        self.password_label = QLabel("Password:")
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register)

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_entry)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_entry)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def showChannelSelectionScreen(self):
        self.clearLayout()

        self.channel_label = QLabel("Enter Channel Name:")
        self.channel_entry = QLineEdit()

        self.join_button = QPushButton("Join Channel")
        self.join_button.clicked.connect(self.startChat)

        layout = QVBoxLayout()
        layout.addWidget(self.channel_label)
        layout.addWidget(self.channel_entry)
        layout.addWidget(self.join_button)

        self.setLayout(layout)

    def showChatScreen(self):
        self.clearLayout()
        self.setGeometry(100, 100, 500, 400)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)

        self.message_entry = QLineEdit()
        self.message_entry.returnPressed.connect(self.sendMessage)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.sendMessage)

        layout = QVBoxLayout()
        layout.addWidget(self.chat_display)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.message_entry)
        h_layout.addWidget(self.send_button)

        layout.addLayout(h_layout)

        self.setLayout(layout)

        self.loadHistory()

        # Start a thread to listen for incoming messages
        threading.Thread(target=self.receiveMessages, daemon=True).start()

    def loadHistory(self):
        """Load the message history into the chat display."""
        history = self.backend.get_message_history()
        for msg in history:
            timestamp, message = msg.split(":", 1)
            self.chat_display.append(f"{time.ctime(int(timestamp))}: {message}")

    def sendMessage(self):
        """Send a message and update the chat display."""
        message = self.message_entry.text()
        if message:
            self.backend.publish_message(message)
            self.message_entry.clear()

    def receiveMessages(self):
        """Receive and display messages from the channel."""
        for message in self.backend.listen_messages():
            self.chat_display.append(f"Friend: {message}")

    def login(self):
        username = self.username_entry.text()
        password = self.password_entry.text()
        if self.backend.authenticate_user(username, password):
            self.showChannelSelectionScreen()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password!")

    def register(self):
        username = self.username_entry.text()
        password = self.password_entry.text()
        if self.backend.register_user(username, password):
            QMessageBox.information(
                self, "Success", "Registration successful! Please log in."
            )
        else:
            QMessageBox.warning(self, "Error", "Username already exists!")

    def startChat(self):
        channel = self.channel_entry.text()
        if channel:
            self.backend.set_channel(channel)
            self.showChatScreen()

    def clearLayout(self):
        """Clear the current layout."""
        if self.layout() is not None:
            # Clear all widgets from the layout
            while self.layout().count():
                child = self.layout().takeAt(0)
                if child.widget():
                    child.widget().setParent(None)

            # Delete the old layout
            layout = self.layout()
            del layout


if __name__ == "__main__":
    app = QApplication(sys.argv)
    chat_app = ChatApp()
    chat_app.show()
    sys.exit(app.exec_())
