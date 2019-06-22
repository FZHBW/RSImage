from PyQt5 import QtCore, QtGui, QtWidgets
import sys
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(640, 480)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(370, 80, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(140, 80, 113, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(180, 200, 256, 192))
        self.textBrowser.setObjectName("textBrowser")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 80, 111, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 220, 141, 16))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "PushButton"))
        self.label.setText(_translate("Dialog", "这是Line Edit ->"))
        self.label_2.setText(_translate("Dialog", "这是Text Browser ->"))

def main():
    """
    主函数，用于运行程序
    :return: None
    """
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(dialog)
    dialog.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()