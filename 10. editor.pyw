from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt5.QtCore import QStringListModel, Qt
from sympy import content

from ui.editor2 import Ui_Form

import os


class Editor(QWidget, Ui_Form):
    def __init__(self, file_path=None):
        self.is_top = False
        self.file_path = file_path
        super().__init__()
        self.setupUi(self)
        self.init()
        self.reload_file()

    def init(self):
        self.TopBtn.clicked.connect(self.set_top)
        self.LoadBtn.clicked.connect(self.load_file)
        self.ReloadBtn.clicked.connect(self.reload_file)
        self.SaveBtn.clicked.connect(self.save_file)
        self.SaveAsBtn.clicked.connect(self.save_as)
        self.OpenBtn.clicked.connect(self.open_file)

        self.LoadBtn.setShortcut('L')
        self.ReloadBtn.setShortcut('R')
        self.SaveBtn.setShortcut('S')
        self.SaveAsBtn.setShortcut('A')
        self.OpenBtn.setShortcut('O')

    def set_top(self):
        self.is_top = not self.is_top
        if self.is_top:
            self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
            self.TopBtn.setText("取消置顶")
        else:
            self.setWindowFlag(Qt.WindowStaysOnTopHint, False)
            self.TopBtn.setText("置顶窗口")
        self.show()

    def load_file(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "npc/heroes", "文本文件 (*.txt);;所有文件 (*)")
            if file_path == '': return
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.readlines()
            model = QStringListModel()
            model.setStringList(content)
            self.Lv.setModel(model)
            self.Status.setText(f'加载文件：{file_path}')
            self.setWindowTitle(file_path)
            self.file_path = file_path
        except Exception as e:
            self.Status.setText(f'加载失败：{e}')

    def reload_file(self):
        try:
            if self.file_path is None: return
            file_path = self.file_path
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.readlines()
            model = QStringListModel()
            model.setStringList(content)
            self.Lv.setModel(model)
            self.Status.setText(f'重载文件：{file_path}')
            self.setWindowTitle(file_path)
        except Exception as e:
            self.Status.setText(f'重载失败：{e}')

    def save_file(self):
        try:
            if self.file_path is None: return
            file_name = self.file_path.split('/')[-1]
            file_path = f'vpk/pak01_dir/scripts/npc/heroes/{file_name}'
            model = self.Lv.model()
            content = model.stringList()
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(content)
            self.Status.setText(f'保存文件：{file_path}')
            self.setWindowTitle(file_path)
            self.file_path = file_path
        except Exception as e:
            self.Status.setText(f'保存失败：{e}')

    def save_as(self):
        try:
            if self.file_path is None: return
            file_name = self.file_path.split('/')[-1]
            file_path, _ = QFileDialog.getSaveFileName(self, "保存文件", f"vpk/pak01_dir/scripts/npc/heroes/{file_name}", "文本文件 (*.txt);;所有文件 (*)")
            if file_path == '': return
            model = self.Lv.model()
            content = model.stringList()
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(content)
            self.Status.setText(f'另存文件：{file_path}')
            self.setWindowTitle(file_path)
            self.file_path = file_path
        except Exception as e:
            self.Status.setText(f'另存失败：{e}')

    def open_file(self):
        try:
            if self.file_path is None: return
            file_path = os.path.abspath(self.file_path)
            os.startfile(file_path)
            self.Status.setText(f'打开文件：{file_path}')
        except Exception as e:
            self.Status.setText(f'打开失败：{e}')

    def _read_select_line(self) -> str:
        model = self.Lv.model()
        index = self.Lv.selectionModel().currentIndex()
        line = model.stringList()[index.row()]
        return line

    def _write_select_line(self, line: str):
        model = self.Lv.model()
        index = self.Lv.selectionModel().currentIndex()
        model.setData(index, line)

if __name__ == '__main__':
    app = QApplication([])
    win = Editor('npc/heroes/npc_dota_hero_abaddon.txt')
    win.show()
    app.exec()
