import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import QStringListModel, Qt
from PyQt5.QtGui import QFont

from script.ability_script import update_charge_restore, update_value_more, update_value, expand_per
from script.tab_script import tab_up, tab_down
from ui.editor import Ui_MainWindow


class Editor(QMainWindow, Ui_MainWindow):
    def __init__(self, url=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Edited')
        self.__init()
        self.__url = url
        self.__file_name = ''
        self.__undo_board = ''
        self.__clip_board = []
        if self.__url:
            self.__load_the_file(reload=True)

    def __init(self):
        # font = QFont("Consolas", 10)
        font = QFont("JetBrains Mono", 9)
        font.setBold(True)  # 设置为粗体
        # font.setItalic(True)  # 设置为斜体
        self.listView.setFont(font)
        # act
        self.actionopen.triggered.connect(self.__load_the_file)
        self.actionopen_now.triggered.connect(self.__open_the_file)
        self.actionsave.triggered.connect(self.__save)
        self.actionsave_as.triggered.connect(lambda: self.__save(save_as=True))
        # btn
        self.pushButton_2.clicked.connect(lambda: self.__load_the_file(reload=True))
        self.pushButton.clicked.connect(self.__write_select_line)
        self.pushButton_3.clicked.connect(lambda: self.__write_select_line(cd=1))
        self.pushButton_10.clicked.connect(lambda: self.__write_select_line(ch=1))
        self.pushButton_8.clicked.connect(self.__save)
        self.pushButton_7.clicked.connect(self.__tab_up)
        self.pushButton_9.clicked.connect(self.__tab_down)
        self.pushButton_6.clicked.connect(self.__undo)
        self.pushButton_5.clicked.connect(self.__cut)
        self.pushButton_4.clicked.connect(self.__paste)
        self.pushButton_12.clicked.connect(lambda: self.__write_select_line(va=1))
        self.pushButton_15.clicked.connect(lambda: self.__write_select_line(va=2))
        self.pushButton_14.clicked.connect(lambda: self.__write_select_line(va=3))
        self.pushButton_16.clicked.connect(lambda: self.__write_select_line(va=4))
        self.pushButton_13.clicked.connect(lambda: self.__write_select_line(va=5))
        self.pushButton_17.clicked.connect(lambda: self.__write_select_line(va=6))
        self.pushButton_19.clicked.connect(lambda: self.__write_select_line(va=7))
        self.pushButton_18.clicked.connect(lambda: self.__write_select_line(va=9))
        self.pushButton_11.clicked.connect(lambda: self.__write_select_line(va=0))
        self.pushButton_20.clicked.connect(lambda: self.__write_select_line(va=11))
        self.pushButton_21.clicked.connect(lambda: self.__write_select_line(va=12))

        # 快捷键
        self.actionopen.setShortcut('l')
        self.actionopen_now.setShortcut('o')
        self.actionsave.setShortcut('s')
        self.actionsave_as.setShortcut('ctrl+s')

        self.pushButton_7.setShortcut('tab')
        self.pushButton_9.setShortcut('backspace')
        self.pushButton.setShortcut('space')
        self.pushButton_3.setShortcut('d')
        self.pushButton_6.setShortcut('z')
        self.pushButton_5.setShortcut('x')
        self.pushButton_4.setShortcut('v')
        self.pushButton_2.setShortcut('r')
        self.pushButton_10.setShortcut('c')
        self.pushButton_12.setShortcut('1')
        self.pushButton_15.setShortcut('2')
        self.pushButton_14.setShortcut('3')
        self.pushButton_16.setShortcut('4')
        self.pushButton_13.setShortcut('5')
        self.pushButton_17.setShortcut('6')
        self.pushButton_19.setShortcut('7')
        self.pushButton_18.setShortcut('9')
        self.pushButton_11.setShortcut('0')
        self.pushButton_20.setShortcut('-')
        self.pushButton_21.setShortcut('=')

    def __open_the_file(self):
        # url = self.url
        url = os.path.abspath(self.__url)
        try:
            os.startfile(url)
            self.statusbar.showMessage(f"已成功打开文件: {url}")
        except FileNotFoundError:
            self.statusbar.showMessage(f"文件未找到: {url}")
        except Exception as e:
            self.statusbar.showMessage(f"打开文件时出现错误: {e}")

    def __load_the_file(self, reload=False):
        if reload:
            url = self.__url
        else:
            url, _ = QFileDialog.getOpenFileName(self, "选择文件", "npc/heroes", "文本文件 (*.txt);;所有文件 (*)")  # 打开文件管理器

        if url:
            with open(url, 'r', encoding='utf-8', errors='ignore') as f:
                ls = f.readlines()
            m = QStringListModel()  # 建立模型
            m.setStringList(ls)  # 写入内容至模型
            self.listView.setModel(m)  # lv绑定模型
            self.__file_name = url.split('/')[-1]  # 记忆文件名
            self.__url = url  # 记忆路径
            self.statusbar.showMessage(f'操作：载入数据成功，路径：{url}')
        else:
            self.statusbar.showMessage(f'操作：载入数据路径为空！')

    def dragEnterEvent(self, event):
        """允许拖拽文件"""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """处理拖放事件"""
        url = [u.toLocalFile() for u in event.mimeData().urls()][0]
        if url:
            with open(url, 'r', encoding='utf-8', errors='ignore') as f:
                ls = f.readlines()
            m = QStringListModel()  # 建立模型
            m.setStringList(ls)  # 写入内容至模型
            self.listView.setModel(m)  # lv绑定模型
            self.listView.setStyleSheet("font-family: Consolas; font-size: 12px; font-weight: bold;")
            self.__file_name = url.split('/')[-1]  # 记忆文件名
            self.__url = url  # 记忆路径
            self.statusbar.showMessage(f'操作：载入数据成功，路径：{url}')

    def __read_select_line(self):
        """
        读取选中行
        :return: 模型，行索引，行内容
        """
        # try:
        #     m = self.listView.model()  # 读模型，QStringListModel
        #     ls = self.listView.selectionModel().selectedIndexes()  # [<PyQt6.QtCore.QModelIndex>]
        #     i = ls[0]  # <PyQt6.QtCore.QModelIndex>
        #     t = m.data(i)  # 读
        #     return m, i, t
        # except Exception as e:
        #     self.statusbar.showMessage(f'操作：读取模型失败，错误：{e}')
        #     return None, None, None

        try:
            m = self.listView.model()  # 读模型，QStringListModel
            ls = self.listView.selectionModel().selectedIndexes()  # [<PyQt5.QtCore.QModelIndex>]
            i = ls[0]  # <PyQt5.QtCore.QModelIndex>
            t = m.data(i, Qt.DisplayRole)  # 读，PyQt5 需要显式指定角色
            return m, i, t
        except Exception as e:
            self.statusbar.showMessage(f'操作：读取模型失败，错误：{e}')
            return None, None, None

    def __write_select_line(self, cd=0, ch=0, va=-1):
        """
        写入选中行
        :param cd: -25%
        :param ch: AbilityChargeRestoreTime
        :param va: =0, +1, +25%, +33%, +5, +50, +500, +75%, +100%
        :return:
        """
        m, i, t = self.__read_select_line()  # 模型，行索引，行内容
        if not t:
            self.statusbar.showMessage(f'操作：写入模型失败，错误：内容为空')
        else:
            x = t
            try:
                if ch == 1:
                    x = update_charge_restore(x)
                else:
                    if 'value' in x:
                        x = update_value(x)
                    else:
                        x = update_value_more(x)

                    if cd == 1 or 'Cooldown' in x or 'ManaCost' in x or 'CastPoint' in x or 'RestoreTime' in x:
                        x = x.replace(expand_per, '-25%')
                    elif va == 1:
                        x = x.replace(expand_per, '+1')
                    elif va == 2:
                        x = x.replace(expand_per, '+25%')
                    elif va == 3:
                        x = x.replace(expand_per, '+50%')
                    elif va == 4:
                        x = x.replace(expand_per, '+5')
                    elif va == 5:
                        x = x.replace(expand_per, '+50')
                    elif va == 6:
                        x = x.replace(expand_per, '+500')
                    elif va == 7:
                        x = x.replace(expand_per, '+1000')
                    elif va == 9:
                        x = x.replace(expand_per, '+100%')
                    elif va == 0:
                        x = x.replace(expand_per, '=0')
                    elif va == 11:
                        x = x.replace(expand_per, '-1')
                    elif va == 12:
                        x = x.replace(expand_per, '=1')

                # 开始写入
                m.setData(i, x)  # 写
                self.__undo_board = f'{t}'  # 备份原字段
            except Exception as e:
                self.statusbar.showMessage(f'操作：写入模型失败，错误：{e}')

    def __save(self, save_as=False):
        """保存文件"""
        if save_as:
            url, _ = QFileDialog.getSaveFileName(self, "保存文件", rf"vpk\pak01_dir\scripts\npc\heroes\{self.__file_name}", "文本文件 (*.txt);;所有文件 (*)")
        else:
            url = self.__url

        try:
            if url:
                file_name = url.split('/')[-1]
                url = rf'vpk/pak01_dir/scripts/npc/heroes/{file_name}'
                with open(url, 'w') as f:
                    m = self.listView.model()  # 读模型，QStringListModel
                    row = m.rowCount()  # 共多少行
                    ls = []
                    for r in range(row):
                        i = m.index(r, 0)  # r行0列
                        # tx = m.data(i)  # 内容 QT6
                        tx = m.data(i, Qt.DisplayRole)  # 内容，显式指定角色 QT5
                        ls.append(tx)  # 写入列表
                    f.writelines(ls)  # 写
                self.__url = url
                self.statusbar.showMessage(f'操作：保存数据成功，路径：{url}')
        except Exception as e:
            print(e)
            self.statusbar.showMessage(f'操作：保存数据失败，错误：{e}')

    def __tab_up(self):
        m, i, t = self.__read_select_line()  # 模型，行索引，行内容
        if t:
            x = tab_up(t)
            m.setData(i, x)  # 写

    def __tab_down(self):
        m, i, t = self.__read_select_line()  # 模型，行索引，行内容
        if t:
            x = tab_down(t)
            m.setData(i, x)  # 写

    def __undo(self):
        """撤回"""
        m, i, t = self.__read_select_line()
        if self.__undo_board:
            m.setData(i, self.__undo_board)  # 写
            self.statusbar.showMessage(f'操作：撤回成功')

    def __cut(self):
        """剪切"""
        m, i, t = self.__read_select_line()
        if not t:
            self.statusbar.showMessage(f'操作：剪切失败，错误：内容为空')
        else:
            self.__clip_board.append(tab_up(t))  # 剪切
            m.setData(i, '')  # 删
            self.statusbar.showMessage(f'操作：剪切成功，剪切板次数：{len(self.__clip_board)}')

    def __paste(self):
        """粘贴"""
        if not self.__clip_board:
            self.statusbar.showMessage(f'操作：粘贴失败，剪切板为空')
        else:
            m, i, t = self.__read_select_line()
            if not i:
                self.statusbar.showMessage(f'操作：粘贴失败，错误：索引值为空')
            else:
                m.setData(i, t + '\n'.join(self.__clip_board))  # 写
                self.__clip_board = []  # 清空剪切板
                self.statusbar.showMessage(f'操作：粘贴成功')


if __name__ == '__main__':
    app = QApplication([])
    win = Editor(r'')
    win.show()
    app.exec()
