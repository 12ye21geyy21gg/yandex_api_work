import sys, os
from pyui import Ui_Form
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from PyQt5.QtCore import QTimer


class cart(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.search)
        self.pushButton_2.clicked.connect(self.rest)
        self.pushButton_3.clicked.connect(self.cheche)
        self.pushButton_4.clicked.connect(self.move)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(300)


    def rest(self):
        self.isRest = True
        with open('taxi1', mode='w', encoding='utf8') as f:
            f.write('reset:lol')

    def update(self):
        if os.path.isfile('taxi2'):
            with open('taxi2', mode='r', encoding='utf8') as f:
                t = f.read()
                print(t != self.textEdit.toPlainText(),t,self.textEdit.toPlainText())
                if t != self.textEdit.toPlainText():
                    self.textEdit.setText(t)
            os.remove('taxi2')

    def search(self):
        self.S_O = self.lineEdit.text()
        with open('taxi1', mode='w', encoding='utf8') as f:
            f.write('search:' + self.S_O)

    def cheche(self):
        s = ''
        if self.checkBox.isChecked():
            s = s + '1'
        else:
            s = s + '0'
        if self.checkBox_2.isChecked():
            s = s + '1'
        else:
            s = s + '0'
        with open('taxi1', mode='w', encoding='utf8') as f:
            f.write('check:' + s)

    def move(self):
        with open('taxi1', mode='w', encoding='utf8') as f:
            f.write(f'move:{self.lineEdit_2.text()},{self.lineEdit_3.text()},{self.lineEdit_4.text()}')


app = QApplication([])

main = cart()
main.show()
sys.exit(app.exec_())
