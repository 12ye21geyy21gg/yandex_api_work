import sys
from asdads import Ui_Form
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton


class cart(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.pushButton.clicked.connect(self.search)
        self.pushButton_2.clicked.connect()#твоя функция
        self.pushButton_3.clicked.connect(self.cheche)

    def search(self):
        self.S_O = self.lineEdit.text()
        self.textEdit.setText()#то что нужно ввест
    # to pygame :
    def cheche(self): #
        if QCheckBox


if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = Example()
        sys.exit(app.exec_())