from PyQt5.QtWidgets import QApplication,QWidget
from ui.edit import Ui_Form

class EditWin(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication([])
    win = EditWin()
    win.show()
    app.exec_()