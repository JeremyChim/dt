import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QListWidget, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文本文件编辑器")
        self.setGeometry(100, 100, 600, 400)
        self.lines = []
        self.clipboard = ""

        # 主窗口部件和布局
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        # 列表控件用于显示文本行
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.SingleSelection)
        self.layout.addWidget(self.list_widget)

        # 按钮布局
        self.button_layout = QHBoxLayout()
        self.layout.addLayout(self.button_layout)

        # 按钮
        self.btn_load = QPushButton("加载文件")
        self.btn_print = QPushButton("打印选中行")
        self.btn_replace = QPushButton("替换选中行")
        self.btn_cut = QPushButton("剪切选中行")
        self.btn_paste = QPushButton("粘贴")
        self.btn_save = QPushButton("保存文件")

        self.button_layout.addWidget(self.btn_load)
        self.button_layout.addWidget(self.btn_print)
        self.button_layout.addWidget(self.btn_replace)
        self.button_layout.addWidget(self.btn_cut)
        self.button_layout.addWidget(self.btn_paste)
        self.button_layout.addWidget(self.btn_save)

        # 连接按钮到功能
        self.btn_load.clicked.connect(self.load_file)
        self.btn_print.clicked.connect(self.print_selected)
        self.btn_replace.clicked.connect(self.replace_selected)
        self.btn_cut.clicked.connect(self.cut_selected)
        self.btn_paste.clicked.connect(self.paste_line)
        self.btn_save.clicked.connect(self.save_file)

    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "打开文本文件", "", "文本文件 (*.txt)")
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    # 直接读取每行，保留原始内容（包括缩进）
                    self.lines = [line for line in file.readlines()]
                self.list_widget.clear()
                self.list_widget.addItems(self.lines)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"无法加载文件：{str(e)}")

    def print_selected(self):
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            print(selected_items[0].text())
        else:
            QMessageBox.warning(self, "警告", "未选中任何行！")

    def replace_selected(self):
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            index = self.list_widget.row(selected_items[0])
            new_text = selected_items[0].text() + "_替换"
            self.lines[index] = new_text
            self.list_widget.takeItem(index)
            self.list_widget.insertItem(index, new_text)
        else:
            QMessageBox.warning(self, "警告", "未选中任何行！")

    def cut_selected(self):
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            index = self.list_widget.row(selected_items[0])
            self.clipboard = self.lines[index]
            self.lines.pop(index)
            self.list_widget.takeItem(index)
        else:
            QMessageBox.warning(self, "警告", "未选中任何行！")

    def paste_line(self):
        if self.clipboard:
            selected_items = self.list_widget.selectedItems()
            index = self.list_widget.row(selected_items[0]) + 1 if selected_items else len(self.lines)
            self.lines.insert(index, self.clipboard)
            self.list_widget.insertItem(index, self.clipboard)
        else:
            QMessageBox.warning(self, "警告", "剪贴板为空！")

    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "保存文本文件", "", "文本文件 (*.txt)")
        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as file:
                    # 保存时每行添加换行符
                    file.write('\n'.join(self.lines) + '\n')
                QMessageBox.information(self, "成功", "文件保存成功！")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"无法保存文件：{str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec_())