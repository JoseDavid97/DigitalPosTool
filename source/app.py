import configparser
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QIntValidator
from PyQt5.QtCore import QDate, QTime
from functools import partial
from source.utils import showAlert
from datetime import datetime
from source.dbLibrary import PDO
from source.printer import Printer

class MainApp(QMainWindow):
    value = ""
    lastDaTim = ""
    lastValue = 0
    editList = []

    def __init__(self):
        super(MainApp, self).__init__()

        config = configparser.ConfigParser()
        config.read('source/settings.ini')
        self.settings = config['App']
        
        self.ui = loadUi('source/GUI.ui', self)
        self.pdo = PDO()

        self.pr = Printer()

        self.modelList1 = QStandardItemModel()
        self.ui.listView.setModel(self.modelList1)

        self.modelList2 = QStandardItemModel()
        self.ui.listViewSum.setModel(self.modelList2)

        self.ui.lineEdit.setValidator(QIntValidator())

        self.setWindowTitle(f"Panaderia La Quinta")
        self.initKeyboard()
        self.goTo(0)

    def adminMode(self, txt):
        if txt.text() == "OK":
            self.goTo(1)

    def checkValue(self):
        value = int(self.value) if self.value != "" else 0
        if (value >= 50 and value%50 == 0):
            msgbox = showAlert(type_msg="Question", title="Alerta", msg=f"¿Seguro que desea ingresar venta por {value} COP?")
            msgbox.buttonClicked.connect(self.checkValue2)
            msgbox.exec()
        elif value == int(self.settings['adminPwd']): 
            msgbox = showAlert(type_msg="Question", title="Modo administrador", msg=f"¿Desea ingresar al modo administrador?")
            msgbox.buttonClicked.connect(self.adminMode)
            msgbox.exec()
            self.value = ""
            self.labelLastTranVal.setText(self.value)
        else:
            showAlert(type_msg="Critical", title="Valor incorrecto", msg=f"El valor {value} COP es inválido")
            self.value = ""
            self.labelLastTranVal.setText(self.value)

    def checkValue2(self, txt):
        if txt.text() == "OK":
            rNow = datetime.now()
            
            self.pdo.saveBill(self.value, rNow)
            self.putHistory(self.value, rNow)
            self.makeBill(self.value, rNow)

        self.value = ""
        self.labelLastTranVal.setText(self.value)

    def getNumber(self, value=None):
        if ((value == 0 and len(self.value)) or value != 0):
            self.value += str(value)
            self.labelLastTranVal.setText(self.value)

    def putHistory(self, price, date):
        text = f"{date.strftime('%d/%B/%Y %I:%M %p')} - Total: {price} COP"
        item = QStandardItem(text)
        self.modelList1.appendRow(item)

    def makeBill(self, price, date):
        file = open("source/lastBill.txt", 'w')
        file.write(f"{self.settings['bName']}\n")
        file.write(f"Fecha: {date.strftime('%d / %B / %Y  %I:%M  %p')}\n")
        file.write(f'Total: {price} COP')
        file.close()

    def setTotalBill(self, range, total):
        file = open("source/totalBill.txt", 'w')
        file.write(f"{self.settings['bName']}\n")
        file.write(f"Desde: {range['from']}\n")
        file.write(f"Hasta: {range['to']}\n")
        file.write(f'Total: {total} COP')
        file.close()
        
    def delDigit(self):
        self.value = self.value[0:-1]
        self.labelLastTranVal.setText(self.value)

    def goTo(self, index):
        self.ui.stackedWidget.setCurrentIndex(index)

    def makeSummary(self):

        self.modelList2.clear()

        fromD = self.ui.calendarWidgetFrom.selectedDate()
        toD = self.ui.calendarWidgetTo.selectedDate()

        fromT = self.ui.comboBoxFrom.currentIndex()
        toT = self.ui.comboBoxTo.currentIndex() + 1

        if toT == 24: 
            toD = toD.addDays(1)
            toT = 0

        fromTS = f"0{fromT}" if fromT<10 else f"{fromT}"
        toTS = f"0{toT}" if toT<10 else f"{toT}"

        fromStr = fromD.toString("yyyy-MM-dd")+f"T{fromTS}:00:00"
        toStr = toD.toString("yyyy-MM-dd")+f"T{toTS}:00:00"

        data = self.pdo.getRecords(fromStr, toStr)
        self.editList = data

        total = 0
        for item in data:
            text = f"{item[1].strftime('%d / %B / %Y  %I:%M %p')} - Total: {int(item[2])} COP"
            qitem = QStandardItem(text)
            self.modelList2.appendRow(qitem)
            total += item[2]

        fromStr = fromD.toString("dd / MM / yyyy")+f" {fromTS}:00:00"
        toStr = toD.toString("dd / MM / yyyy")+f" {toTS}:00:00"
        self.setTotalBill(range = {'from':fromStr, 'to':toStr}, total = round(total))

        self.ui.labelTotalValue.setText(f"{int(total)} COP")

    def makeSummaryH(self):
        self.modelList2.clear()

        fromD = self.ui.calendarWidgetFrom.selectedDate()
        toD = self.ui.calendarWidgetTo.selectedDate()

        fromT = self.ui.comboBoxFrom.currentIndex()
        toT = self.ui.comboBoxTo.currentIndex() + 1

        if toT == 24: 
            toD = toD.addDays(1)
            toT = 0

        fromTS = f"0{fromT}" if fromT<10 else f"{fromT}"
        toTS = f"0{toT}" if toT<10 else f"{toT}"

        fromStr = fromD.toString("yyyy-MM-dd")+f"T{fromTS}:00:00"
        toStr = toD.toString("yyyy-MM-dd")+f"T{toTS}:00:00"

        data = self.pdo.getGroupedRecords(fromStr, toStr)
        self.editList = False
        
        total = 0
        for item in data:
            text = f"{item[1]} - Total: {int(item[0])} COP"
            qitem = QStandardItem(text)
            self.modelList2.appendRow(qitem)
            total += item[0]

        fromStr = fromD.toString("dd / MM / yyyy")+f" {fromTS}:00:00"
        toStr = toD.toString("dd / MM / yyyy")+f" {toTS}:00:00"
        self.setTotalBill(range = {'from':fromStr, 'to':toStr}, total = round(total))

        self.ui.labelTotalValue.setText(f"{int(total)} COP")

    def editRecord(self):
        tInd = self.ui.listViewSum.currentIndex()
        if tInd.isValid() and self.editList:
            self.editRec = self.editList[tInd.row()]
            self.editRecord2()
            
    def editRecord2(self):
        self.goTo(2)

        cuDT = self.editRec[1]
        qdate = QDate(cuDT.year, cuDT.month, cuDT.day)
        qtime = QTime(cuDT.hour, cuDT.minute, cuDT.second)

        self.ui.calendarWidgetEdit.setSelectedDate(qdate)
        self.ui.timeEdit.setTime(qtime)
        self.ui.lineEdit.setText(str(int(self.editRec[2])))

    def editRecord3(self):
        self.newValue = int(self.ui.lineEdit.text())

        if (self.newValue >= 50 and self.newValue%50 == 0):
            msgbox = showAlert(type_msg="Question", title="Alerta", msg=f"¿Seguro que desea modificar venta por {self.newValue} COP?")
            msgbox.buttonClicked.connect(self.editRecord4)
            msgbox.exec()
        else:
            showAlert(type_msg="Critical", title="Valor incorrecto", msg=f"El valor {self.newValue} COP es inválido")

    def editRecord4(self, txt):
        if txt.text() == "OK":
            self.pdo.editRecord(self.editRec[0], self.newValue)
        self.goTo(1)
        self.makeSummary()

    def deleteRecord(self):
        tInd = self.ui.listViewSum.currentIndex()
        if tInd.isValid() and self.editList:
            self.delPK = self.editList[tInd.row()][0]
            value = int(self.editList[tInd.row()][2])
            msgbox = showAlert(type_msg="Question", title="Alerta", msg=f"¿Seguro que desea eliminar venta por {value} COP?")
            msgbox.buttonClicked.connect(self.deleteRecord2)
            msgbox.exec()      

    def deleteRecord2(self, txt):
        if txt.text() == "OK":  
            self.pdo.delRecord(self.delPK)
            self.makeSummary()
        
    def initKeyboard(self):

        self.pushButtonOk.clicked.connect(self.checkValue)
        self.pushButtonDel.clicked.connect(self.delDigit)
        self.pushButtonOpen.clicked.connect(self.pr.openCashDrawer)
        self.pushButtonPrint.clicked.connect(self.pr.printBill)
        self.pushButtonGoRec.clicked.connect(partial(self.goTo, 0))
        self.pushButtonSum.clicked.connect(self.makeSummary)
        self.pushButtonEdRec.clicked.connect(self.editRecord)
        self.pushButtonEdRec2.clicked.connect(self.editRecord3)
        self.pushButtonGoAdmin.clicked.connect(partial(self.goTo, 1))
        self.pushButtonDelRec.clicked.connect(self.deleteRecord)
        self.pushButtonPrintSum.clicked.connect(self.pr.printSummary)
        self.pushButtonSumH.clicked.connect(self.makeSummaryH)

        for i in range(10):
            exec(f"self.pushButton{i}.clicked.connect(partial(self.getNumber, i))")

        