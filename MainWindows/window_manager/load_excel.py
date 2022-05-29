import xlrd
from PyQt5.QtWidgets import QFileDialog

from MainWindows.window_manager.message_window import create_message_window
from sqlite import cur, con
from sqlite.sqlite_manager import get_number_day


def load_excel_in_day(window, day):
    file_name = QFileDialog.getOpenFileName(window, 'Выберите таблицу', '', '(*.xlsx)')[0]
    workbook = xlrd.open_workbook(file_name)
    names = workbook.sheet_names()
    if len(names) != 1:
        create_message_window(window, 'Таблиц excel не валидна')
        return
    try:
        day_n = get_number_day(day)
        worksheet = workbook.sheet_by_name(names[0])
        data = get_data_in_worksheet(worksheet)
        window.clear_day()
        load_data_in_list_widget(data, day_n, window=window)
        create_message_window(window, 'Таблица создана')
    except xlrd.biffh.XLRDError:
        create_message_window(window, 'Таблиц excel не валидна')


def load_excel_in_week(window):
    file_name = QFileDialog.getOpenFileName(window, 'Выберите таблицу', '', '(*.xlsx)')[0]
    workbook = xlrd.open_workbook(file_name)
    days = workbook.sheet_names()
    for day in days:
        day_n = get_number_day(day)
        try:
            worksheet = workbook.sheet_by_name(day)
            data = get_data_in_worksheet(worksheet)
            cur.execute('''DELETE FROM events WHERE day = ?''', (day_n,))
            load_data_in_list_widget(data, day_n)
        except xlrd.biffh.XLRDError:
            pass
    create_message_window(window, 'Таблица создана')


def get_data_in_worksheet(worksheet: xlrd.sheet.Sheet):
    num_rows = worksheet.nrows - 1
    num_cells = worksheet.ncols - 1
    curr_row = -1
    data = []
    while curr_row < num_rows:
        row = []
        curr_row += 1
        curr_cell = -1
        while curr_cell < num_cells:
            curr_cell += 1
            cell_value = worksheet.cell_value(curr_row, curr_cell)
            row.append(cell_value)
        data.append(row)
    if data[0] != ['с', 'по', 'название', 'описание']:
        return []
    return data[1:]


def load_data_in_list_widget(data, day_n, window=False):
    for line in data:
        time = line[0].split(':') + line[1].split(':')
        name = line[2]
        event_text = line[-1]
        line = 'c {} по {} - {}'.format(*line)
        if window:
            window.EventView.addItem(line)
        cur.execute('''INSERT INTO events VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)''',
                    (day_n, *time, name, event_text))
    con.commit()
