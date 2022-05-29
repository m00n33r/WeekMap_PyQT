import sys
from PyQt5.QtWidgets import QApplication
from MainWindows import ChartWeekWindow
from MainWindows.window_manager.message_window import create_message_window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChartWeekWindow()
    try:
        sys.exit(app.exec())
    except Exception as e:
        create_message_window(window, 'Программа завершилась некорректно')
