# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tagpanel.ui'
#
# Created: Fri Feb  7 22:22:15 2014
#      by: pyside-uic 0.2.13 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_TagPanel(object):
    def setupUi(self, TagPanel):
        TagPanel.setObjectName("TagPanel")
        TagPanel.resize(222, 214)
        self.gridLayout = QtGui.QGridLayout(TagPanel)
        self.gridLayout.setObjectName("gridLayout")
        self.wgtTags = TagWidget(TagPanel)
        self.wgtTags.setObjectName("wgtTags")
        self.gridLayout.addWidget(self.wgtTags, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.edtTag = QtGui.QLineEdit(TagPanel)
        self.edtTag.setObjectName("edtTag")
        self.horizontalLayout.addWidget(self.edtTag)
        self.btnTag = QtGui.QPushButton(TagPanel)
        self.btnTag.setEnabled(False)
        self.btnTag.setObjectName("btnTag")
        self.horizontalLayout.addWidget(self.btnTag)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.wgtTagLib = TagWidget(TagPanel)
        self.wgtTagLib.setObjectName("wgtTagLib")
        self.gridLayout.addWidget(self.wgtTagLib, 2, 0, 1, 1)

        self.retranslateUi(TagPanel)
        QtCore.QMetaObject.connectSlotsByName(TagPanel)

    def retranslateUi(self, TagPanel):
        TagPanel.setWindowTitle(QtGui.QApplication.translate("TagPanel", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.btnTag.setText(QtGui.QApplication.translate("TagPanel", "贴标签", None, QtGui.QApplication.UnicodeUTF8))

from broom_tag import TagWidget
