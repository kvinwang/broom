# coding:utf8
__author__ = 'loong'
from elib.eqt.layout import FlowLayout
from PySide import QtGui, QtCore


class TagWidget(QtGui.QWidget):
    tagClicked = QtCore.Signal(str)
    tagToggled = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(TagWidget, self).__init__(parent=parent)
        self.checkable = False
        self.setLayout(FlowLayout())
        self.tag_wgts_d = {}
        self.checked_tags = set()

    def setCheckable(self, yes):
        self.checkable = yes
        if yes:
            css = 'QPushButton:checked { background-color: red;}'
            self.setStyleSheet(css)

    def add_tag(self, tag):
        if tag in self.tag_wgts_d:
            return

        tagwgt = QtGui.QPushButton(unicode(tag))
        if self.checkable:
            tagwgt.setCheckable(True)

        self.layout().addWidget(tagwgt)
        self.tag_wgts_d[tag] = tagwgt

        @tagwgt.clicked.connect
        def emit():
            self.tagClicked.emit(tag)

        @tagwgt.toggled.connect
        def emit():
            if tagwgt.isChecked():
                self.checked_tags.add(tag)
            else:
                self.checked_tags.remove(tag)
            self.tagToggled.emit(tag)

    def load_tags(self, tags):
        self.clear()
        for tag in tags or []:
            self.add_tag(tag)

    def clear(self):
        for tag in self.tag_wgts_d.keys():
            self.remove_tag(tag)

    def remove_tag(self, tag):
        tagwgt = self.tag_wgts_d.pop(tag)
        self.layout().removeWidget(tagwgt)

    def check_tags(self, tags):
        self.checked_tags = set(tags)
        for tag, btn in self.tag_wgts_d.items():
            if tag in self.checked_tags:
                btn.setChecked(QtCore.Qt.Checked)
            else:
                btn.setChecked(QtCore.Qt.Unchecked)


class TagPanel(QtGui.QWidget):
    tagChanged = QtCore.Signal()
    tagAdded = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(TagPanel, self).__init__(parent=parent)
        self.tags = set()
        self.taglib = set()
        self.ui = Ui_TagPanel()
        self.ui.setupUi(self)
        self._init_signals()

    def _init_signals(self):
        self.ui.btnTag.clicked.connect(self._add_tag)
        self.ui.edtTag.textChanged.connect(self.check_state)
        self.ui.edtTag.returnPressed.connect(
            self.ui.btnTag.click)

        self.tagChanged.connect(self.update_ui)

        @self.ui.wgtTags.tagClicked.connect
        def rm_tag(tag):
            self.tags.remove(tag)
            self.tagChanged.emit()

        @self.ui.wgtTagLib.tagClicked.connect
        def add_tag(tag):
            self.tags.add(tag)
            self.tagChanged.emit()

    def check_state(self):
        self.ui.btnTag.setEnabled(bool(self.ui.edtTag.text()))

    def _add_tag(self):
        tag = self.ui.edtTag.text()
        self.tags.add(tag)
        self.tagAdded.emit(tag)
        self.tagChanged.emit()
        self.ui.edtTag.setText(u'')

    def update_ui(self):
        self.ui.wgtTags.load_tags(self.tags)
        self.load_taglib()

    def load_taglib(self, taglib=None):
        if taglib is not None:
            self.taglib = taglib
        tags = [t for t in self.taglib if t not in self.tags]
        self.ui.wgtTagLib.load_tags(tags)

    def set_tags(self, tags):
        self.tags = set(tags or [])
        self.update_ui()

from tagpanel import Ui_TagPanel
