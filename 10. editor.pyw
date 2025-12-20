from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt5.QtCore import QStringListModel, Qt

from ui.editor2 import Ui_Form

import os


class Editor(QWidget, Ui_Form):
    def __init__(self, file_path=None):
        self.is_top = False
        self.file_path = file_path
        self.cut_board = []
        self.undo_board = None
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
        self.AutoBtn.clicked.connect(self.style_auto)
        self.Style1Btn.clicked.connect(self.style_1)
        self.Style2Btn.clicked.connect(self.style_2)
        self.Style3Btn.clicked.connect(self.style_3)
        self.Style4Btn.clicked.connect(self.style_4)
        self.Style5Btn.clicked.connect(self.style_5)
        self.CutBtn.clicked.connect(self.cut)
        self.PasteBtn.clicked.connect(self.paste)
        self.UndoBtn.clicked.connect(self.undo)
        self.TabBtn.clicked.connect(self.tab)
        self.BackBtn.clicked.connect(self.back)
        self.SaBtn.clicked.connect(self.sa_init)
        self.SpBtn.clicked.connect(self.sp_init)
        self.Sa2Btn.clicked.connect(self.sa2_init)
        self.Sp2Btn.clicked.connect(self.sp2_init)

        self.Style1Btn.setText('冷却(D)')
        self.Style2Btn.setText('=1(1)')
        self.Style3Btn.setText('""(2)')
        self.Style4Btn.setText('天赋(3)')
        self.Style5Btn.setText('=0(0)')

        self.LoadBtn.setShortcut('L')
        self.ReloadBtn.setShortcut('R')
        self.SaveBtn.setShortcut('S')
        self.SaveAsBtn.setShortcut('A')
        self.OpenBtn.setShortcut('O')
        self.AutoBtn.setShortcut(' ')
        self.Style1Btn.setShortcut('D')
        self.Style2Btn.setShortcut('1')
        self.Style3Btn.setShortcut('2')
        self.Style4Btn.setShortcut('3')
        self.Style5Btn.setShortcut('0')
        self.CutBtn.setShortcut('X')
        self.PasteBtn.setShortcut('V')
        self.UndoBtn.setShortcut('Z')
        self.TabBtn.setShortcut('Tab')
        self.BackBtn.setShortcut('Backspace')

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

    def style_auto(self):
        try:
            line = self._read_select_line()
            if line == "": return
            if 'Cooldown' in line or 'ManaCost' in line or 'CastPoint' in line:
                self._modify_line_4()
            elif "value" in line:
                self._modify_line_1()
            else:
                self._modify_line_2()
            self.undo_board = line
        except Exception as e:
            self.Status.setText(f'转换失败：{e}')

    def style_1(self):
        try:
            line = self._read_select_line()
            if line == "": return
            if "value" in line:
                self._modify_line_3()
            else:
                self._modify_line_4()
            self.undo_board = line
        except Exception as e:
            self.Status.setText(f'转换失败：{e}')

    def style_2(self):
        try:
            line = self._read_select_line()
            if line == "": return
            if "value" in line:
                self._modify_line_5('=1', '=1')
            else:
                self._modify_line_6('=1', '=1')
            self.undo_board = line
        except Exception as e:
            self.Status.setText(f'转换失败：{e}')

    def style_3(self):
        try:
            line = self._read_select_line()
            self._modify_line_1()
            self.undo_board = line
        except Exception as e:
            self.Status.setText(f'转换失败：{e}')

    def style_4(self):
        try:
            line = self._read_select_line()
            self._modify_line_7()
            self.undo_board = line
        except Exception as e:
            self.Status.setText(f'转换失败：{e}')

    def style_5(self):
        try:
            line = self._read_select_line()
            if line == "": return
            if "value" in line:
                self._modify_line_5('=0', '=0')
            else:
                self._modify_line_6('=0', '=0')
            self.undo_board = line
        except Exception as e:
            self.Status.setText(f'转换失败：{e}')

    def cut(self):
        try:
            line = self._read_select_line()
            self.cut_board.append(line)
            self._write_select_line('')
            self.Status.setText(f'剪切：{len(self.cut_board)}')
        except Exception as e:
            self.Status.setText(f'剪切失败：{e}')

    def paste(self):
        try:
            if len(self.cut_board) == 0: return
            old_line = self._read_select_line()
            all_line = ''
            for line in self.cut_board:
                all_line = all_line + line
            new_line = old_line + self._tab_lines(all_line)
            self._write_select_line(new_line)
            self.Status.setText(f'粘贴：{len(self.cut_board)}')
            self.cut_board = []
        except Exception as e:
            self.Status.setText(f'粘贴失败：{e}')

    def undo(self):
        try:
            if self.undo_board is None: return
            self._write_select_line(self.undo_board)
            self.Status.setText(f'撤回：{self.undo_board}')
            self.undo_board = None
        except Exception as e:
            self.Status.setText(f'撤回失败：{e}')

    def tab(self):
        try:
            line = self._read_select_line()
            new_line = self._tab_lines(line)
            self._write_select_line(new_line)
        except Exception as e:
            self.Status.setText(f'缩进失败：{e}')

    def back(self):
        try:
            line = self._read_select_line()
            new_line = self._back_lines(line)
            self._write_select_line(new_line)
        except Exception as e:
            self.Status.setText(f'反缩进失败：{e}')

    def sa_init(self):
        self.SaLe.setText('+25%')

    def sp_init(self):
        self.SpLe.setText('+50%')

    def sa2_init(self):
        self.Sa2Le.setText('-12.5%')

    def sp2_init(self):
        self.Sp2Le.setText('-25%')

    def _read_select_line(self) -> str:
        model = self.Lv.model()
        index = self.Lv.selectionModel().currentIndex()
        line = model.stringList()[index.row()]
        return line

    def _write_select_line(self, line: str):
        model = self.Lv.model()
        index = self.Lv.selectionModel().currentIndex()
        model.setData(index, line)

    def _modify_line_1(self):
        old_line = self._read_select_line()
        old_split = old_line.split('"')
        tab = old_split[0]
        sa_val = self.SaLe.text()
        sp_val = self.SpLe.text()
        sa_line = f'{tab}"special_bonus_shard"\t\t"{sa_val}"\n'
        sp_line = f'{tab}"special_bonus_scepter"\t\t"{sp_val}"\n'
        new_line = old_line + sa_line + sp_line
        self._write_select_line(new_line)

    def _modify_line_2(self):
        old_line = self._read_select_line()
        old_split = old_line.split('"')
        tab = old_split[0]
        name = old_split[1]
        value = old_split[3]
        sa_val = self.SaLe.text()
        sp_val = self.SpLe.text()
        name_line = f'{tab}"{name}"\n'
        head_line = tab + '{\n'
        value_line = f'{tab}\t"value"\t\t\t\t\t\t"{value}"\n'
        sa_line = f'{tab}\t"special_bonus_shard"\t\t"{sa_val}"\n'
        sp_line = f'{tab}\t"special_bonus_scepter"\t\t"{sp_val}"\n'
        end_line = tab + '}\n'
        new_line = name_line + head_line + value_line + sa_line + sp_line + end_line
        self._write_select_line(new_line)

    def _modify_line_3(self):
        old_line = self._read_select_line()
        old_split = old_line.split('"')
        tab = old_split[0]
        sa_val = self.Sa2Le.text()
        sp_val = self.Sp2Le.text()
        sa_line = f'{tab}"special_bonus_shard"\t\t"{sa_val}"\n'
        sp_line = f'{tab}"special_bonus_scepter"\t\t"{sp_val}"\n'
        new_line = old_line + sa_line + sp_line
        self._write_select_line(new_line)

    def _modify_line_4(self):
        old_line = self._read_select_line()
        old_split = old_line.split('"')
        tab = old_split[0]
        name = old_split[1]
        value = old_split[3]
        sa_val = self.Sa2Le.text()
        sp_val = self.Sp2Le.text()
        name_line = f'{tab}"{name}"\n'
        head_line = tab + '{\n'
        value_line = f'{tab}\t"value"\t\t\t\t\t\t"{value}"\n'
        sa_line = f'{tab}\t"special_bonus_shard"\t\t"{sa_val}"\n'
        sp_line = f'{tab}\t"special_bonus_scepter"\t\t"{sp_val}"\n'
        end_line = tab + '}\n'
        new_line = name_line + head_line + value_line + sa_line + sp_line + end_line
        self._write_select_line(new_line)

    def _modify_line_5(self, sa_val, sp_val):
        old_line = self._read_select_line()
        old_split = old_line.split('"')
        tab = old_split[0]
        sa_line = f'{tab}"special_bonus_shard"\t\t"{sa_val}"\n'
        sp_line = f'{tab}"special_bonus_scepter"\t\t"{sp_val}"\n'
        new_line = old_line + sa_line + sp_line
        self._write_select_line(new_line)

    def _modify_line_6(self, sa_val, sp_val):
        old_line = self._read_select_line()
        old_split = old_line.split('"')
        tab = old_split[0]
        name = old_split[1]
        value = old_split[3]
        name_line = f'{tab}"{name}"\n'
        head_line = tab + '{\n'
        value_line = f'{tab}\t"value"\t\t\t\t\t\t"{value}"\n'
        sa_line = f'{tab}\t"special_bonus_shard"\t\t"{sa_val}"\n'
        sp_line = f'{tab}\t"special_bonus_scepter"\t\t"{sp_val}"\n'
        end_line = tab + '}\n'
        new_line = name_line + head_line + value_line + sa_line + sp_line + end_line
        self._write_select_line(new_line)

    def _modify_line_7(self):
        old_line = self._read_select_line()
        old_split = old_line.split('"')
        tab = old_split[0]
        name = old_split[1]
        value = old_split[3]
        if value == '1':
            value2 = '=1'
        elif '=' in value:
            value2 = value
            value = value.replace('=','')
        else:
            value2 = f'+{value}'
        value_line = f'{tab}"value"\t\t\t\t\t\t"{value}"\n'
        sa_line = f'{tab}"special_bonus_shard"\t\t"{value2}"\n'
        sp_line = f'{tab}"special_bonus_scepter"\t\t"{value2}"\n'
        old_line = f'{tab}"{name}"\t\t\t\t\t\t"{value2}"\n'
        new_line = value_line + sa_line + sp_line + old_line
        self._write_select_line(new_line)

    @staticmethod
    def _tab_lines(line) -> str:
        lines = line.split('\n')
        new_line = '\n'.join([f'\t{line}' for line in lines])
        return new_line

    @staticmethod
    def _back_lines(line) -> str:
        lines = line.split('\n')
        new_line = '\n'.join([line[1:] if line.startswith('\t') else line for line in lines])
        return new_line


if __name__ == '__main__':
    app = QApplication([])
    win = Editor()
    win.show()
    app.exec()
