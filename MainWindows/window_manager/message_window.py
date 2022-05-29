from PyQt5.QtWidgets import QMessageBox


def create_message_window(window, text):
    QMessageBox.information(window, 'Уведомление', text)
