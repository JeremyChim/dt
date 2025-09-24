import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QListWidget, QFileDialog, QMessageBox)
from PyQt5.QtGui import QKeySequence

class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文本文件编辑器")
        self.setGeometry(100, 100, 1200, 800)
        self.lines = []
        self.clipboard = ""
        self.undoboard = ""

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
        self.btn_load = QPushButton("加载")
        self.btn_add = QPushButton("+")
        self.btn_sub = QPushButton("-")
        self.btn_cut = QPushButton("剪切")
        self.btn_paste = QPushButton("粘贴")
        self.btn_save = QPushButton("保存")
        self.btn_undo = QPushButton("撤销")  # 新增撤销按钮

        self.button_layout.addWidget(self.btn_load)
        self.button_layout.addWidget(self.btn_add)
        self.button_layout.addWidget(self.btn_sub)
        self.button_layout.addWidget(self.btn_cut)
        self.button_layout.addWidget(self.btn_paste)
        self.button_layout.addWidget(self.btn_save)
        self.button_layout.addWidget(self.btn_undo)  # 添加到按钮布局

        # 设置快捷键
        self.btn_load.setShortcut('L')  # L键绑定“加载”
        self.btn_add.setShortcut(' ')   # 空格键绑定“+”
        self.btn_sub.setShortcut('C')   # C键绑定“-”
        self.btn_cut.setShortcut('X')   # X键绑定“剪切”
        self.btn_paste.setShortcut('V')  # V键绑定“粘贴”
        self.btn_save.setShortcut('S')   # S键绑定“保存”
        self.btn_undo.setShortcut('Z')   # Z键绑定“撤销”

        # 连接按钮到功能
        self.btn_load.clicked.connect(self.load_file)
        self.btn_add.clicked.connect(self.add)
        self.btn_sub.clicked.connect(self.sub)
        self.btn_cut.clicked.connect(self.cut)
        self.btn_paste.clicked.connect(self.paste)
        self.btn_save.clicked.connect(self.save_file)
        self.btn_undo.clicked.connect(self.undo)  # 连接撤销功能

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

    def add(self):
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            index = self.list_widget.row(selected_items[0])
            old_text = selected_items[0].text()
            print(old_text.split('"'))
            tab = old_text.split('"')[0]
            ab_name = old_text.split('"')[1]
            ab_value = old_text.split('"')[3]
            if 'Cooldown' in ab_name or 'ManaCost' in ab_name or 'CastPoint' in ab_name:
                val = '-25%'
            else:
                val = '+50%'
            if ab_name == "value":
                sa = f'{tab}"special_bonus_shard"\t\t"{val}"\n'
                sp = f'{tab}"special_bonus_scepter"\t\t"{val}"\n'
                new_text = old_text + sa + sp
            else:
                o = f'{tab}"{ab_name}"\n'
                s = tab + '{\n'
                va = f'{tab}\t"value"\t\t"{ab_value}"\n'
                sa = f'{tab}\t"special_bonus_shard"\t\t"{val}"\n'
                sp = f'{tab}\t"special_bonus_scepter"\t\t"{val}"\n'
                e = tab + '}\n'
                new_text = o + s + va + sa + sp + e
            self.lines[index] = new_text
            self.list_widget.takeItem(index)
            self.list_widget.insertItem(index, new_text)
            self.undoboard = old_text
        else:
            QMessageBox.warning(self, "警告", "未选中任何行！")

    def sub(self):
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            index = self.list_widget.row(selected_items[0])
            old_text = selected_items[0].text()
            print(old_text.split('"'))
            tab = old_text.split('"')[0]
            ab_name = old_text.split('"')[1]
            ab_value = old_text.split('"')[3]
            val = '-25%'
            if ab_name == "value":
                sa = f'{tab}"special_bonus_shard"\t\t"{val}"\n'
                sp = f'{tab}"special_bonus_scepter"\t\t"{val}"\n'
                new_text = old_text + sa + sp
            else:
                o = f'{tab}"{ab_name}"\n'
                s = tab + '{\n'
                va = f'{tab}\t"value"\t\t"{ab_value}"\n'
                sa = f'{tab}\t"special_bonus_shard"\t\t"{val}"\n'
                sp = f'{tab}\t"special_bonus_scepter"\t\t"{val}"\n'
                e = tab + '}\n'
                new_text = o + s + va + sa + sp + e
            self.lines[index] = new_text
            self.list_widget.takeItem(index)
            self.list_widget.insertItem(index, new_text)
            self.undoboard = old_text
        else:
            QMessageBox.warning(self, "警告", "未选中任何行！")

    def cut(self):
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            index = self.list_widget.row(selected_items[0])
            self.clipboard = self.lines[index]
            self.lines.pop(index)
            self.list_widget.takeItem(index)
        else:
            QMessageBox.warning(self, "警告", "未选中任何行！")

    def paste(self):
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

    def undo(self):
        if self.undoboard:
            selected_items = self.list_widget.selectedItems()
            if selected_items:
                index = self.list_widget.row(selected_items[0])
                self.lines[index] = self.undoboard
                self.list_widget.takeItem(index)
                self.list_widget.insertItem(index, self.undoboard)
            else:
                QMessageBox.warning(self, "警告", "未选中任何行！")
        else:
            QMessageBox.warning(self, "警告", "无撤销内容！")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec_())