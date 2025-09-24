import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QListWidget, QFileDialog, QMessageBox, QShortcut, QListWidgetItem)
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtCore import Qt
import os

class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文本文件编辑器")
        self.setGeometry(100, 100, 1200, 800)
        self.lines = []
        self.file_name = ""
        self.clipboard = []
        self.undoboard = ""

        # 主窗口部件和布局
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        # 列表控件用于显示文本行
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.ExtendedSelection)
        # 设置默认字体为 JetBrains Mono，大小为 9
        font = QFont("JetBrains Mono", 9)
        self.list_widget.setFont(font)
        # 启用双击编辑
        self.list_widget.setEditTriggers(QListWidget.DoubleClicked)
        # 连接 itemChanged 信号以捕获编辑完成
        self.list_widget.itemChanged.connect(self.on_item_changed)
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
        self.btn_undo = QPushButton("撤销")

        self.button_layout.addWidget(self.btn_load)
        self.button_layout.addWidget(self.btn_add)
        self.button_layout.addWidget(self.btn_sub)
        self.button_layout.addWidget(self.btn_cut)
        self.button_layout.addWidget(self.btn_paste)
        self.button_layout.addWidget(self.btn_save)
        self.button_layout.addWidget(self.btn_undo)

        # 设置快捷键
        self.btn_load.setShortcut('L')
        self.btn_sub.setShortcut('C')
        self.btn_paste.setShortcut('V')
        self.btn_save.setShortcut('S')
        self.btn_undo.setShortcut('Z')

        # 使用 QShortcut 绑定空格键和 X 键
        QShortcut(QKeySequence(' '), self, self.add)
        QShortcut(QKeySequence('X'), self, self.cut)

        # 连接按钮到功能
        self.btn_load.clicked.connect(self.load_file)
        self.btn_add.clicked.connect(self.add)
        self.btn_sub.clicked.connect(self.sub)
        self.btn_cut.clicked.connect(self.cut)
        self.btn_paste.clicked.connect(self.paste)
        self.btn_save.clicked.connect(self.save_file)
        self.btn_undo.clicked.connect(self.undo)

    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "打开文本文件", "npc/heroes", "文本文件 (*.txt)")
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    self.lines = [line for line in file.readlines()]
                self.list_widget.clear()
                for line in self.lines:
                    item = QListWidgetItem(line.rstrip('\n'))
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                    self.list_widget.addItem(item)
                self.file_name = file_name
            except Exception as e:
                QMessageBox.critical(self, "错误", f"无法加载文件：{str(e)}")

    def add(self):
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            index = self.list_widget.row(selected_items[0])
            old_text = self.lines[index]
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
            item = QListWidgetItem(new_text.rstrip('\n'))
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.list_widget.takeItem(index)
            self.list_widget.insertItem(index, item)
            self.undoboard = old_text
            # 恢复焦点和选中状态
            self.list_widget.setCurrentRow(index)
        else:
            QMessageBox.warning(self, "警告", "未选中任何行！")

    def sub(self):
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            index = self.list_widget.row(selected_items[0])
            old_text = self.lines[index]
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
            item = QListWidgetItem(new_text.rstrip('\n'))
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.list_widget.takeItem(index)
            self.list_widget.insertItem(index, item)
            self.undoboard = old_text
            # 恢复焦点和选中状态
            self.list_widget.setCurrentRow(index)
        else:
            QMessageBox.warning(self, "警告", "未选中任何行！")

    def cut(self):
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            # 收集所有选中行的索引（从大到小排序以避免删除时的索引偏移）
            indices = sorted([self.list_widget.row(item) for item in selected_items], reverse=True)
            self.clipboard = [self.lines[i] for i in indices]
            # 从后向前删除行
            for index in indices:
                self.lines.pop(index)
                self.list_widget.takeItem(index)
            # 恢复焦点到接近原位置的行（如果可能）
            new_index = min(indices[-1], len(self.lines) - 1) if self.lines else -1
            if new_index >= 0:
                self.list_widget.setCurrentRow(new_index)
        else:
            QMessageBox.warning(self, "警告", "未选中任何行！")

    def paste(self):
        if self.clipboard:
            selected_items = self.list_widget.selectedItems()
            index = self.list_widget.row(selected_items[0]) + 1 if selected_items else len(self.lines)
            # 为每行添加制表符 \t
            indented_lines = ['\t' + line.rstrip('\n') + '\n' for line in self.clipboard]
            # 插入所有行
            for line in indented_lines:
                self.lines.insert(index, line)
                item = QListWidgetItem(line.rstrip('\n'))
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                self.list_widget.insertItem(index, item)
                index += 1
            self.clipboard = []  # 清空 clipboard
            # 恢复焦点到第一行插入的位置
            self.list_widget.setCurrentRow(index - len(indented_lines))
        else:
            QMessageBox.warning(self, "警告", "剪贴板为空！")

    def save_file(self):
        default_path = "vpk/pak01_dir/scripts/npc/heroes"
        default_file = self.file_name if self.file_name else ""
        file_name, _ = QFileDialog.getSaveFileName(self, "保存文本文件", os.path.join(default_path, os.path.basename(default_file)), "文本文件 (*.txt)")
        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write('\n'.join(self.lines) + '\n')
                self.file_name = file_name
                QMessageBox.information(self, "成功", "文件保存成功！")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"无法保存文件：{str(e)}")

    def undo(self):
        if self.undoboard:
            selected_items = self.list_widget.selectedItems()
            if selected_items:
                index = self.list_widget.row(selected_items[0])
                self.lines[index] = self.undoboard
                item = QListWidgetItem(self.undoboard.rstrip('\n'))
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                self.list_widget.takeItem(index)
                self.list_widget.insertItem(index, item)
                # 恢复焦点和选中状态
                self.list_widget.setCurrentRow(index)
            else:
                QMessageBox.warning(self, "警告", "未选中任何行！")
        else:
            QMessageBox.warning(self, "警告", "无撤销内容！")

    def on_item_changed(self, item):
        index = self.list_widget.row(item)
        old_text = self.lines[index]
        new_text = item.text() + '\n'
        self.undoboard = old_text
        self.lines[index] = new_text
        # 恢复焦点和选中状态
        self.list_widget.setCurrentRow(index)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec_())