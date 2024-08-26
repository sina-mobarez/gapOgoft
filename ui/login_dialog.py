from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)
from PyQt6.QtCore import Qt


class LoginDialog(QDialog):
    def __init__(self, database):
        super().__init__()
        self.database = database
        self.username = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Login")
        self.setFixedSize(300, 200)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Chat App Login")
        title.setObjectName("loginTitle")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setObjectName("loginInput")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setObjectName("loginInput")
        layout.addWidget(self.password_input)

        button_layout = QHBoxLayout()
        login_btn = QPushButton("Login")
        login_btn.setObjectName("loginButton")
        login_btn.clicked.connect(self.login)
        button_layout.addWidget(login_btn)

        register_btn = QPushButton("Register")
        register_btn.setObjectName("registerButton")
        register_btn.clicked.connect(self.register)
        button_layout.addWidget(register_btn)

        layout.addLayout(button_layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if self.database.verify_user(username, password):
            self.username = username
            self.accept()
        else:
            self.show_error("Invalid credentials")

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username and password:
            try:
                self.database.add_user(username, password)
                self.username = username
                self.accept()
            except:
                self.show_error("Username already exists")
        else:
            self.show_error("Please enter username and password")

    def show_error(self, message):
        error_label = QLabel(message)
        error_label.setObjectName("errorLabel")
        self.layout().addWidget(error_label)
