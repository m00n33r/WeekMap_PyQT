from PyQt5.QtWidgets import QDialog
from MainWindows.template_window.calendar import Ui_Dialog
from datetime import datetime
from MainWindows.window_manager.message_window import create_message_window
from sqlite import cur, con


class AddNote(Ui_Dialog, QDialog):
    def __init__(self, main_window):
        super(AddNote, self).__init__()
        self.setupUi(self)
        self.mainWindow = main_window
        # Кнопка добавления заметки
        self.NoteSaveBt.clicked.connect(self.write)

    def write(self):
        """Заносим выбранную пользователем дату в переменную data,
         и записываем дату и название заметки в главное окно"""
        data = self.calendarWidget.selectedDate()
        day = data.day()
        month = data.month()
        year = data.year()
        data = datetime(year=year, month=month, day=day)
        text = self.NoteText.text().strip()
        # Добавляем эту заметку в базу данных notes
        try:
            cur.execute("INSERT INTO notes VALUES(NULL, ?, ?, ?, ?)",
                        (data.strftime('%Y'), data.strftime('%m'),
                         data.strftime('%d'), text,)).fetchall()
            con.commit()
            # Добавляем заметку в главное окно
            self.mainWindow.listWidget.addItem(data.strftime('%d.%m.%Y')
                                               + ' - ' + text + '\n')
            self.close()
        except Exception:
            create_message_window(self, 'Заметка под таким названием уже существует')
            self.close()
