# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'explorer.ui'
#
# Created: Sat Feb  8 16:46:03 2014
#      by: pyside-uic 0.2.13 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Explorer(object):
    def setupUi(self, Explorer):
        Explorer.setObjectName("Explorer")
        Explorer.resize(836, 579)
        self.gridLayout = QtGui.QGridLayout(Explorer)
        self.gridLayout.setObjectName("gridLayout")
        self.lblStatus = QtGui.QLabel(Explorer)
        self.lblStatus.setObjectName("lblStatus")
        self.gridLayout.addWidget(self.lblStatus, 3, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 507, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 5, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(497, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 1, 1, 1)
        self.btnFindRed = QtGui.QPushButton(Explorer)
        self.btnFindRed.setObjectName("btnFindRed")
        self.gridLayout.addWidget(self.btnFindRed, 3, 6, 1, 1)
        self.btnShowMarked = QtGui.QPushButton(Explorer)
        self.btnShowMarked.setObjectName("btnShowMarked")
        self.gridLayout.addWidget(self.btnShowMarked, 3, 5, 1, 1)
        self.btnReload = QtGui.QPushButton(Explorer)
        self.btnReload.setObjectName("btnReload")
        self.gridLayout.addWidget(self.btnReload, 3, 3, 1, 2)
        self.ckbUsingEmbedPlayer = QtGui.QCheckBox(Explorer)
        self.ckbUsingEmbedPlayer.setObjectName("ckbUsingEmbedPlayer")
        self.gridLayout.addWidget(self.ckbUsingEmbedPlayer, 3, 2, 1, 1)
        self.wgtTagPanel = TagPanel(Explorer)
        self.wgtTagPanel.setObjectName("wgtTagPanel")
        self.gridLayout.addWidget(self.wgtTagPanel, 0, 4, 1, 3)
        self.splitter = QtGui.QSplitter(Explorer)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.treeDir = QtGui.QTreeWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeDir.sizePolicy().hasHeightForWidth())
        self.treeDir.setSizePolicy(sizePolicy)
        self.treeDir.setDragEnabled(True)
        self.treeDir.setDragDropOverwriteMode(True)
        self.treeDir.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.treeDir.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.treeDir.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.treeDir.setObjectName("treeDir")
        self.treeDir.header().setDefaultSectionSize(400)
        self.treeDir2 = QtGui.QTreeWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeDir2.sizePolicy().hasHeightForWidth())
        self.treeDir2.setSizePolicy(sizePolicy)
        self.treeDir2.setDragEnabled(True)
        self.treeDir2.setDragDropOverwriteMode(True)
        self.treeDir2.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.treeDir2.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.treeDir2.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.treeDir2.setObjectName("treeDir2")
        self.treeDir2.header().setDefaultSectionSize(400)
        self.gridLayout.addWidget(self.splitter, 0, 0, 3, 4)
        self.label = QtGui.QLabel(Explorer)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 4, 1, 3)

        self.retranslateUi(Explorer)
        QtCore.QMetaObject.connectSlotsByName(Explorer)

    def retranslateUi(self, Explorer):
        Explorer.setWindowTitle(QtGui.QApplication.translate("Explorer", "Broom - 百度网盘文件整理", None, QtGui.QApplication.UnicodeUTF8))
        self.lblStatus.setText(QtGui.QApplication.translate("Explorer", "Status", None, QtGui.QApplication.UnicodeUTF8))
        self.btnFindRed.setText(QtGui.QApplication.translate("Explorer", "文件查重", None, QtGui.QApplication.UnicodeUTF8))
        self.btnShowMarked.setText(QtGui.QApplication.translate("Explorer", "标签", None, QtGui.QApplication.UnicodeUTF8))
        self.btnReload.setText(QtGui.QApplication.translate("Explorer", "reload", None, QtGui.QApplication.UnicodeUTF8))
        self.ckbUsingEmbedPlayer.setText(QtGui.QApplication.translate("Explorer", "内置播放器", None, QtGui.QApplication.UnicodeUTF8))
        self.treeDir.headerItem().setText(0, QtGui.QApplication.translate("Explorer", "名称", None, QtGui.QApplication.UnicodeUTF8))
        self.treeDir.headerItem().setText(1, QtGui.QApplication.translate("Explorer", "大小", None, QtGui.QApplication.UnicodeUTF8))
        self.treeDir2.headerItem().setText(0, QtGui.QApplication.translate("Explorer", "名称", None, QtGui.QApplication.UnicodeUTF8))
        self.treeDir2.headerItem().setText(1, QtGui.QApplication.translate("Explorer", "大小", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Explorer", "<a href=\'http://a.bit.so\'>http://a.bit.so</a>", None, QtGui.QApplication.UnicodeUTF8))

from broom_tag import TagPanel
