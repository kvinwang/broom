# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'findred.ui'
#
# Created: Sat Feb  1 20:46:36 2014
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_FindRed(object):
    def setupUi(self, FindRed):
        FindRed.setObjectName("FindRed")
        FindRed.resize(597, 453)
        self.gridLayout = QtGui.QGridLayout(FindRed)
        self.gridLayout.setObjectName("gridLayout")
        self.treeDir = QtGui.QTreeWidget(FindRed)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeDir.sizePolicy().hasHeightForWidth())
        self.treeDir.setSizePolicy(sizePolicy)
        self.treeDir.setObjectName("treeDir")
        self.treeDir.header().setDefaultSectionSize(400)
        self.gridLayout.addWidget(self.treeDir, 0, 0, 1, 4)
        self.lblStatus = QtGui.QLabel(FindRed)
        self.lblStatus.setText("")
        self.lblStatus.setObjectName("lblStatus")
        self.gridLayout.addWidget(self.lblStatus, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(361, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        self.btnSmartCheck = QtGui.QPushButton(FindRed)
        self.btnSmartCheck.setObjectName("btnSmartCheck")
        self.gridLayout.addWidget(self.btnSmartCheck, 1, 2, 1, 1)
        self.btnDeleteChecked = QtGui.QPushButton(FindRed)
        self.btnDeleteChecked.setObjectName("btnDeleteChecked")
        self.gridLayout.addWidget(self.btnDeleteChecked, 1, 3, 1, 1)

        self.retranslateUi(FindRed)
        QtCore.QMetaObject.connectSlotsByName(FindRed)

    def retranslateUi(self, FindRed):
        FindRed.setWindowTitle(QtGui.QApplication.translate("FindRed", "文件查重", None, QtGui.QApplication.UnicodeUTF8))
        self.treeDir.headerItem().setText(0, QtGui.QApplication.translate("FindRed", "路径", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSmartCheck.setText(QtGui.QApplication.translate("FindRed", "智能勾选(慎用)", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDeleteChecked.setText(QtGui.QApplication.translate("FindRed", "删除勾选的文件", None, QtGui.QApplication.UnicodeUTF8))

