import sys
from PyQt6.QtWidgets import QApplication
from database import Database
from redis_manager import RedisManager
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    # Load stylesheet
    with open("assets/styles.qss", "r") as f:
        app.setStyleSheet(f.read())

    database = Database()
    redis_manager = RedisManager()

    window = MainWindow(database, redis_manager)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
