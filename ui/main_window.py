from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QLineEdit,
    QPushButton,
    QLabel,
)
from PyQt6.QtCore import pyqtSlot
from ui.login_dialog import LoginDialog
from ui.channel_dialog import ChannelDialog


class MainWindow(QMainWindow):
    def __init__(self, database, redis_manager):
        super().__init__()
        self.database = database
        self.redis_manager = redis_manager
        self.username = None
        self.current_channel = None
        self.redis_manager.message_received.connect(self.receive_message)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Chat Application")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)

        # Channel list
        channel_layout = QVBoxLayout()
        self.channel_list = QListWidget()
        self.channel_list.itemClicked.connect(self.change_channel)
        channel_layout.addWidget(QLabel("Channels"))
        channel_layout.addWidget(self.channel_list)
        self.add_channel_btn = QPushButton("Add Channel")
        self.add_channel_btn.clicked.connect(self.add_channel)
        channel_layout.addWidget(self.add_channel_btn)

        # Chat area
        chat_layout = QVBoxLayout()
        self.chat_history = QListWidget()
        self.message_input = QLineEdit()
        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.send_message)

        chat_layout.addWidget(QLabel("Chat"))
        chat_layout.addWidget(self.chat_history)
        chat_layout.addWidget(self.message_input)
        chat_layout.addWidget(self.send_btn)

        layout.addLayout(channel_layout, 1)
        layout.addLayout(chat_layout, 3)

        self.show_login_dialog()

    def show_login_dialog(self):
        dialog = LoginDialog(self.database)
        if dialog.exec():
            self.username = dialog.username
            self.setWindowTitle(f"Chat Application - {self.username}")
            self.load_channels()

    def load_channels(self):
        # In a real app, you'd load channels from the database or server
        self.channel_list.addItems(["General", "Random", "Tech"])

    def add_channel(self):
        dialog = ChannelDialog()
        if dialog.exec():
            new_channel = dialog.channel_name
            self.channel_list.addItem(new_channel)

    def change_channel(self, item):
        if self.current_channel:
            self.redis_manager.unsubscribe(self.current_channel)

        self.current_channel = item.text()
        self.chat_history.clear()
        # Load recent messages for the channel
        messages = self.database.get_messages(self.current_channel)
        for msg in messages:
            self.chat_history.addItem(f"{msg[2]}: {msg[3]}")

        # Subscribe to the new channel
        self.redis_manager.subscribe(self.current_channel)

    @pyqtSlot(str, str)
    def receive_message(self, channel, message):
        if channel == self.current_channel:
            self.chat_history.addItem(message)

    def send_message(self):
        if not self.current_channel:
            return
        message = self.message_input.text()
        if message:
            full_message = f"{self.username}: {message}"
            self.redis_manager.publish(self.current_channel, full_message)
            self.database.add_message(self.current_channel, self.username, message)
            self.message_input.clear()
