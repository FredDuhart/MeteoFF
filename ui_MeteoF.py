# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitledAkwOBf.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFormLayout,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(600, 600)
        Dialog.setMinimumSize(QSize(600, 400))
        Dialog.setMaximumSize(QSize(600, 700))
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.listFav = QListWidget(Dialog)
        self.listFav.setObjectName(u"listFav")

        self.verticalLayout.addWidget(self.listFav)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer_4 = QSpacerItem(20, 15, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.spnDuree = QSpinBox(Dialog)
        self.spnDuree.setObjectName(u"spnDuree")
        self.spnDuree.setMinimum(2)
        self.spnDuree.setMaximum(15)
        self.spnDuree.setValue(7)

        self.horizontalLayout.addWidget(self.spnDuree)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_4)

        self.lineLoc = QLineEdit(Dialog)
        self.lineLoc.setObjectName(u"lineLoc")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.lineLoc)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.btnSearch = QPushButton(Dialog)
        self.btnSearch.setObjectName(u"btnSearch")

        self.verticalLayout_2.addWidget(self.btnSearch)

        self.comboSearch = QComboBox(Dialog)
        self.comboSearch.setObjectName(u"comboSearch")

        self.verticalLayout_2.addWidget(self.comboSearch)

        self.btnOkSearch = QPushButton(Dialog)
        self.btnOkSearch.setObjectName(u"btnOkSearch")

        self.verticalLayout_2.addWidget(self.btnOkSearch)

        self.verticalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        self.btnAddFav = QPushButton(Dialog)
        self.btnAddFav.setObjectName(u"btnAddFav")

        self.verticalLayout_2.addWidget(self.btnAddFav)

        self.btnRemoveFav = QPushButton(Dialog)
        self.btnRemoveFav.setObjectName(u"btnRemoveFav")

        self.verticalLayout_2.addWidget(self.btnRemoveFav)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.btnClose = QPushButton(Dialog)
        self.btnClose.setObjectName(u"btnClose")

        self.verticalLayout_2.addWidget(self.btnClose)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)


        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Favoris", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Dur\u00e9e", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"jours", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Recherche", None))
        self.btnSearch.setText(QCoreApplication.translate("Dialog", u"Chercher", None))
        self.btnOkSearch.setText(QCoreApplication.translate("Dialog", u"Pr\u00e9visions", None))
        self.btnAddFav.setText(QCoreApplication.translate("Dialog", u"Ajouter aux favoris", None))
        self.btnRemoveFav.setText(QCoreApplication.translate("Dialog", u"Retirer des favoris", None))
        self.btnClose.setText(QCoreApplication.translate("Dialog", u"Fermer", None))
    # retranslateUi

