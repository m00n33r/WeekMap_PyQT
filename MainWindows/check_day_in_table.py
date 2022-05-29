from PyQt5.QtWidgets import QDialog, QCheckBox, QGroupBox

from MainWindows.template_window.check_days import Ui_Dialog


class CheckDayDialog(Ui_Dialog, QDialog):
    def __init__(self, mainwindow):
        super(CheckDayDialog, self).__init__()
        self.mainwindow = mainwindow
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        self.btn_group_days.buttons()
        self.buttonBox.accepted.connect(self.get_days)
        self.buttonBox.rejected.connect(self.dialog_close)

    def dialog_close(self):
        self.close()

    def get_days(self):
        btns = map(lambda x: x.text(),
                   filter(lambda x: x.isChecked(), self.btn_group_days.buttons()))
        self.mainwindow.days_in_table = list(btns)
        self.close()
