from PyQt5.QtWidgets import QMainWindow
from MainWindows.window_manager.message_window import create_message_window
from sqlite import cur, con
from datetime import datetime
from .chart_day_window import ChartDayWindow
from MainWindows.template_window.main import Ui_MainWindow
from MainWindows.add_daily_note import AddNote
from .check_day_in_table import CheckDayDialog
from .window_manager.excel_table import create_excel
from .window_manager.load_excel import load_excel_in_week


class ChartWeekWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(ChartWeekWindow, self).__init__()
        self.setupUi(self)
        self.initUI()
        self.show()

    def initUI(self):
        self.MondayBt.clicked.connect(self.open_day)  # Понедельник
        self.TuesdayBt.clicked.connect(self.open_day)  # Вторник
        self.WednesdayBt.clicked.connect(self.open_day)  # Среда
        self.ThursdayBt.clicked.connect(self.open_day)  # Четверг
        self.FridayBt.clicked.connect(self.open_day)  # Пятница
        self.SaturdayBt.clicked.connect(self.open_day)  # Суббота
        self.SundayBt.clicked.connect(self.open_day)  # Воскресенье

        # Кнопка добавления заметки
        self.btn_add_note.clicked.connect(self.add_note)
        # Кнопка удаления всех заметок
        self.DeleteAllBt.clicked.connect(self.delete_all)
        # Кнопка удаления выбранного уведомления
        self.DeleteBt.clicked.connect(self.delete)
        # Кнопка создания таблицы
        self.bnt_create_week_table.clicked.connect(self.create_table)
        # Кнопка востановления графика недели из таблицы
        self.btn_load_week_table.clicked.connect(self.load_table)

        # Распарсим базу данных note и впишем все добавленные до этого заметки
        self.parse()

    def parse(self):
        all_notes = cur.execute('SELECT year, month, day, name FROM notes').fetchall()

        for i in range(len(all_notes)):
            year, month, day, name = all_notes[i]
            data = datetime(year=year, month=month, day=day)
            text = "{}.{}.{} - {}\n".format(data.strftime('%d'), data.strftime('%m'),
                                            data.strftime('%Y'), name, )
            self.listWidget.addItem(text)

    def open_day(self):
        """По нажатию на день недели открывается график этого дня"""
        s = self.sender().text()
        # Открываем окно графика выбранного дня
        self.window = ChartDayWindow(self, s)
        self.hide()

    def add_note(self):
        """По нажатию на кнопку добавления элемента открывается
        окно с выбором даты и его краткого описания"""
        self.window = AddNote(self)
        self.window.exec()

    def delete(self):
        """При удалении какого либо элемента, мы делаем
        проверку на то, выбран ли элемент"""
        if self.listWidget.currentRow() == -1:
            # Если элемент не выбран: мы выводим окно с надписью: 'Не выбран элемент'
            create_message_window(self, 'Не выбран элемент')
        else:
            # Если же элемент для удаления выбран:
            text = self.listWidget.currentItem().text()
            data, name = text[:10], text[13:].strip()
            day, month, year = list(map(int, data.split('.')))
            # Удаляем его из нашей базы данных
            cur.execute("DELETE FROM notes WHERE (year LIKE ? AND month LIKE ?"
                        " AND day LIKE ? AND name LIKE ?)", (int(year), int(month),
                                                             int(day), name,)).fetchall()
            con.commit()
            # А также из списка заметок
            self.listWidget.takeItem(self.listWidget.currentRow())

    def delete_all(self):
        """По нажатию на кнопку 'Очистить всё' мы опустошаем набор заметок,
        и удаляем все заметки из базы данных note"""
        self.listWidget.clear()
        cur.execute("DELETE FROM notes WHERE id > 0").fetchall()
        con.commit()

    def create_table(self):
        """Созадет график в таблице excel"""
        self.days_in_table = []
        dialog = CheckDayDialog(self)
        dialog.exec()
        create_excel(self, self.days_in_table)

    def load_table(self):
        """Востанавливает график недели из excel таблицы"""
        load_excel_in_week(self)
