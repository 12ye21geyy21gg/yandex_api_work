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
        postal = False
        adress = False
        if self.checkBox.isChecked():
            postal = True
        else:
            postal = False
        if self.checkBox_2.isChecked():
            adress = True
        else:
            adress = False

            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = cart()
    ex.show()
    sys.exit(app.exec_())
