import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.click)
        con = sqlite3.connect("BD")
        cur = con.cursor()
        self.result = cur.execute("SELECT * FROM Coffee").fetchall()
        self.tableWidget.setRowCount(len(self.result))
        self.tableWidget.setColumnCount(len(self.result[0]))
        for i, elem in enumerate(self.result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена', 'объем упаковки'])

    def click(self):
        self.ex = Dobav()
        self.ex.show()


class Dobav(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.initUI()

    def initUI(self):
        self.pushButton_2.clicked.connect(self.push)

    def push(self):
        con = sqlite3.connect("BD")
        cur = con.cursor()
        ids = [i[0] for i in cur.execute("SELECT ID FROM Coffee").fetchall()]
        if int(self.lineEdit.text()) in ids:
            cur.execute('''UPDATE Coffee
                        SET (name, step, mz, opis, price, V) = (?, ?, ?, ?, ?, ?)
                        WHERE ID = ?''', (
                self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_4.text(), self.lineEdit_5.text(),
                self.lineEdit_6.text(), self.lineEdit_7.text(), int(self.lineEdit.text())))
        else:
            cur.execute('''INSERT INTO Coffee VALUES(?,?,?,?,?,?,?)''',
                        (int(self.lineEdit.text()), self.lineEdit_2.text(), self.lineEdit_3.text(),
                         self.lineEdit_4.text(), self.lineEdit_5.text(), int(self.lineEdit_6.text()),
                         int(self.lineEdit_7.text())))
        con.commit()
        self.hide()
        ex.initUI()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
