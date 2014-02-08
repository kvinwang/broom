# coding:utf8
__author__ = 'loong'
from PySide import QtGui
from ui.broom_tag import TagWidget
from elib import eqt
from elib.eqt.menu import TreeActionWrapper, TreeMenu
from common import fmt_size, FILE_MIME_TYPE
import json


class Ui_CategoryPanel:
    def setupUi(self, panel):
        layout = QtGui.QVBoxLayout()
        self.tree = QtGui.QTreeWidget()
        layout.addWidget(self.tree)
        self.tree.headerItem().setText(0, u"路径")
        self.tree.headerItem().setText(1, u"大小")
        self.tree.setColumnWidth(0, 500)
        self.tree.setSortingEnabled(True)
        self.tree.setDragDropMode(self.tree.DragOnly)
        self.tagwgt = TagWidget()
        self.tagwgt.setCheckable(True)
        layout.addWidget(self.tagwgt)
        panel.setLayout(layout)


class CategoryPanel(QtGui.QWidget):
    def __init__(self, broom, markdb):
        super(CategoryPanel, self).__init__()
        self.setWindowTitle(u'标记的文件')
        self.broom = broom
        self.items = []
        self.pcs = broom.pcs
        self.markdb = markdb
        self.ui = Ui_CategoryPanel()
        self.ui.setupUi(self)
        self.ui.tagwgt.tagToggled.connect(self.reload)
        self.ui.tree.doubleClicked.connect(self.play_selectedItem)
        self.init_menu()
        self.resize(600, 600)
        self.reload()
        self.markdb.listen(self.cleanup)
        self.markdb.listen(self.load_tags)
        self.match_md5s = set()
        self.init_dragdrop()
        self.load_tags()

    def load_tags(self):
        self.ui.tagwgt.load_tags(self.broom.root_explorer.taglib)

    def init_dragdrop(self):
        _mimeData = self.ui.tree.mimeData

        def mimeData(items):
            mime = _mimeData(items)
            text = json.dumps([item.userData()['path'] for item in items])
            mime.setData(FILE_MIME_TYPE, text)
            return mime

        self.ui.tree.mimeData = mimeData

    def closeEvent(self, e):
        #self.markdb.remove_cb(self.cleanup)
        return super(CategoryPanel, self).closeEvent(e)

    def play_selectedItem(self):
        for item in self.ui.tree.selectedItems()[:1]:
            meta = item.userData()
            if meta['category'] == 1:
                self.pcs.play(meta['path'])

    def init_menu(self):
        class ActionPlay(TreeActionWrapper):
            text = u'播放'
            #autoHide = True

            def test(self, meta):
                return not meta['isdir'] and meta.get('category') == 1

            def itemAction(self0, item):
                meta = item.userData()
                self.pcs.play(meta['path'])

        self._menu = menu = TreeMenu([ActionPlay()])
        menu.attach(self.ui.tree)

    def update_count(self):
        self.setWindowTitle(u'%s个' % len(self.items))

    def cleanup(self):
        if not self.isVisible():
            return

        items = []
        for item in self.items[:]:
            if not self.match(item.userData()):
                md5 = item.userData()['md5']
                if md5 in self.match_md5s:
                    self.match_md5s.remove(md5)
                ind = self.ui.tree.indexOfTopLevelItem(item)
                self.ui.tree.takeTopLevelItem(ind)
            else:
                items.append(item)
        self.items = items
        items = []

        for meta in self.pcs.cache.itervalues():
            if (not meta['isdir']
                    and self.match(meta)
                    and meta['md5'] not in self.match_md5s):

                item = eqt.SortableTreeItem(
                    [self.pcs.basename(meta['path']),
                     eqt.Cell(meta['size'], fmt_size(meta['size']))], meta)
                self.match_md5s.add(meta['md5'])
                items.append(item)
        self.items.extend(items)
        self.ui.tree.addTopLevelItems(items)
        self.update_count()

    def match(self, meta):
        marks = set(self.ui.tagwgt.checked_tags)
        marks_ = self.markdb.get(meta['md5'])
        if marks:
            return marks.intersection(marks_ or [])
        else:
            return meta['category'] == 1 and not marks_

    def reload(self):
        self.ui.tree.clear()
        self.match_md5s = set()
        items = []

        for meta in self.pcs.cache.itervalues():
            if not meta['isdir'] and self.match(meta):
                item = eqt.SortableTreeItem(
                    [self.pcs.basename(meta['path']),
                     eqt.Cell(meta['size'], fmt_size(meta['size']))],
                    meta)
                self.match_md5s.add(meta['md5'])
                items.append(item)
        self.items = items
        self.ui.tree.addTopLevelItems(items)
        self.update_count()
