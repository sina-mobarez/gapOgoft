from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt


class ChannelDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.channel_name = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Add Channel")
        self.setFixedSize(300, 150)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Add New Channel")
        title.setObjectName("dialogTitle")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        self.channel_input = QLineEdit()
        self.channel_input.setPlaceholderText("Channel Name")
        self.channel_input.setObjectName("dialogInput")
        layout.addWidget(self.channel_input)

        add_btn = QPushButton("Add Channel")
        add_btn.setObjectName("dialogButton")
        add_btn.clicked.connect(self.add_channel)
        layout.addWidget(add_btn)

    def add_channel(self):
        channel_name = self.channel_input.text()
        if channel_name:
            self.channel_name = channel_name
            self.accept()
        else:
            error_label = QLabel("Please enter a channel name")
            error_label.setObjectName("errorLabel")
            self.layout().addWidget(error_label)
