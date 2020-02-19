import sys
from pyui import Ui_Form
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton


class cart(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        # self.pushButton.clicked.connect(self.search)
        # self.pushButton_2.clicked.connect(self.rest)
        # self.pushButton_3.clicked.connect(self.cheche)
        self.isRest = False
        self.postal = False
        self.adress = False

    def rest(self):
        self.isRest = True

    def search(self):
        self.S_O = self.lineEdit.text()
        self.textEdit.setText()#то что нужно ввест
    # to pygame :
    def cheche(self): #
        if self.checkBox.isChecked():
            self.postal = True
        else:
            self.postal = False
        if self.checkBox_2.isChecked():
            self.adress = True
        else:
            self.adress = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = cart()
    ex.show()
    sys.exit(app.exec_())
