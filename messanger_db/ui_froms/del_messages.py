# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'del_messages.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_del_messages(object):
    def setupUi(self, del_messages):
        del_messages.setObjectName("del_messages")
        del_messages.resize(340, 80)
        del_messages.setMinimumSize(QtCore.QSize(340, 80))
        del_messages.setMaximumSize(QtCore.QSize(340, 80))
        del_messages.setSizeIncrement(QtCore.QSize(227, 76))
        self.choose_time = QtWidgets.QLabel(del_messages)
        self.choose_time.setGeometry(QtCore.QRect(10, 10, 321, 21))
        self.choose_time.setMinimumSize(QtCore.QSize(321, 21))
        self.choose_time.setMaximumSize(QtCore.QSize(321, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.choose_time.setFont(font)
        self.choose_time.setAlignment(QtCore.Qt.AlignCenter)
        self.choose_time.setObjectName("choose_time")
        self.hours = QtWidgets.QLineEdit(del_messages)
        self.hours.setGeometry(QtCore.QRect(90, 40, 41, 20))
        self.hours.setObjectName("hours")
        self.minutes = QtWidgets.QLineEdit(del_messages)
        self.minutes.setGeometry(QtCore.QRect(150, 40, 41, 20))
        self.minutes.setObjectName("minutes")
        self.seconds = QtWidgets.QLineEdit(del_messages)
        self.seconds.setGeometry(QtCore.QRect(210, 40, 41, 20))
        self.seconds.setObjectName("seconds")
        self.delButton = QtWidgets.QPushButton(del_messages)
        self.delButton.setGeometry(QtCore.QRect(120, 62, 80, 18))
        self.delButton.setObjectName("delButton")
        self.first_two = QtWidgets.QLabel(del_messages)
        self.first_two.setGeometry(QtCore.QRect(138, 40, 7, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.first_two.setFont(font)
        self.first_two.setObjectName("first_two")
        self.second_two = QtWidgets.QLabel(del_messages)
        self.second_two.setGeometry(QtCore.QRect(198, 40, 7, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.second_two.setFont(font)
        self.second_two.setObjectName("second_two")

        self.retranslateUi(del_messages)
        QtCore.QMetaObject.connectSlotsByName(del_messages)

    def retranslateUi(self, del_messages):
        _translate = QtCore.QCoreApplication.translate
        del_messages.setWindowTitle(_translate("del_messages", "Dialog"))
        self.choose_time.setText(_translate("del_messages", "Время отправки"))
        self.first_two.setText(_translate("del_messages", ":"))
        self.second_two.setText(_translate("del_messages", ":"))
        self.delButton.setText(_translate("del_messages", "Отправить"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    del_messages = QtWidgets.QDialog()
    ui = Ui_del_messages()
    ui.setupUi(del_messages)
    del_messages.show()
    sys.exit(app.exec_())