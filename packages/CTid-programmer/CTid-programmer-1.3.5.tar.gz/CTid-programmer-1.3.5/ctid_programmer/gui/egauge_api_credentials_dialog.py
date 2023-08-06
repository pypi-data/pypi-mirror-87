# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'egauge_api_credentials_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Credentials_Dialog(object):
    def setupUi(self, Credentials_Dialog):
        if not Credentials_Dialog.objectName():
            Credentials_Dialog.setObjectName(u"Credentials_Dialog")
        Credentials_Dialog.resize(307, 174)
        self.gridLayout = QGridLayout(Credentials_Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.buttonBox = QDialogButtonBox(Credentials_Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)

        self.label = QLabel(Credentials_Dialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.label_3 = QLabel(Credentials_Dialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.username_lineEdit = QLineEdit(Credentials_Dialog)
        self.username_lineEdit.setObjectName(u"username_lineEdit")

        self.gridLayout.addWidget(self.username_lineEdit, 1, 1, 1, 1)

        self.password_lineEdit = QLineEdit(Credentials_Dialog)
        self.password_lineEdit.setObjectName(u"password_lineEdit")
        self.password_lineEdit.setInputMask(u"")
        self.password_lineEdit.setText(u"")
        self.password_lineEdit.setEchoMode(QLineEdit.Password)

        self.gridLayout.addWidget(self.password_lineEdit, 2, 1, 1, 1)

        self.prompt_label = QLabel(Credentials_Dialog)
        self.prompt_label.setObjectName(u"prompt_label")
        self.prompt_label.setWordWrap(True)

        self.gridLayout.addWidget(self.prompt_label, 0, 0, 1, 2)


        self.retranslateUi(Credentials_Dialog)
        self.buttonBox.accepted.connect(Credentials_Dialog.accept)
        self.buttonBox.rejected.connect(Credentials_Dialog.reject)

        QMetaObject.connectSlotsByName(Credentials_Dialog)
    # setupUi

    def retranslateUi(self, Credentials_Dialog):
        Credentials_Dialog.setWindowTitle(QCoreApplication.translate("Credentials_Dialog", u"eGauge API Login", None))
        self.label.setText(QCoreApplication.translate("Credentials_Dialog", u"Password", None))
        self.label_3.setText(QCoreApplication.translate("Credentials_Dialog", u"Username", None))
        self.prompt_label.setText(QCoreApplication.translate("Credentials_Dialog", u"Please enter your eGuard username and password.", None))
    # retranslateUi

