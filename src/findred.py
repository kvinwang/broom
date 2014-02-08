# coding:utf8
__author__ = 'loong'
from common import PromptableWidget, QtCore, find_red, get_size, fmt_size
from ui.findred import Ui_FindRed
from elib import eqt


class FindRed(PromptableWidget):
    selected_changed = QtCore.Signal(str)

    def __init__(self, pcs):
        """

        :type pcs: PCS
        """
        super(FindRed, self).__init__()
        self.pcs = pcs
        self.ui = Ui_FindRed()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.path_d = {}
        self.groups = []
        self.load_pcs_nodes(pcs.cache.itervalues())
        self.lazy_reload = eqt.LazyDo(
            500, lambda: self.load_pcs_nodes(self.pcs.cache.itervalues()))
        self.init_menu()
        self.init_signals()

    def init_signals(self):
        self.pcs.path_deleted.connect(self.reload_from_pcs)
        self.pcs.path_moved.connect(self.reload_from_pcs)
        self.pcs.path_changed.connect(self.reload_from_pcs)
        self.ui.btnDeleteChecked.clicked.connect(self.delete_checked)
        self.ui.btnSmartCheck.clicked.connect(self.smart_check)
        self.ui.treeDir.itemSelectionChanged.connect(self.on_selection_changed)

    def deinit_signals(self):
        self.pcs.path_deleted.disconnect(self.reload_from_pcs)
        self.pcs.path_moved.disconnect(self.reload_from_pcs)
        self.pcs.path_changed.disconnect(self.reload_from_pcs)

    def closeEvent(self, e):
        #self.deinit_signals()
        return super(FindRed, self).closeEvent(e)

    def reload_from_pcs(self):
        self.lazy_reload()

    def on_selection_changed(self):
        items = self.ui.treeDir.selectedItems()
        path = ''
        if items:
            meta = items[0].userData()
            if meta:
                path = meta['path']
        self.selected_changed.emit(path)

    def load_pcs_nodes(self, nodes):
        groups = find_red(nodes)
        total, red = get_size(groups)
        self.ui.lblStatus.setText(
            u'共%s重复文件，去重可节省%s' % (fmt_size(total), fmt_size(red)))
        sizesum = lambda g: sum([f['size'] for f in g])
        groups.sort(lambda a, b: cmp(sizesum(a), sizesum(b)), reverse=True)
        self.ui.treeDir.clear()
        self.path_d = {}
        self.groups = []
        for g in groups:
            f = g[0]
            diritem = eqt.SortableTreeItem([self.pcs.basename(f['path'])])
            grp = []
            self.groups.append(grp)
            for f in g:
                item = eqt.SortableTreeItem([f['path']], f)
                item.setCheckState(0, QtCore.Qt.Unchecked)
                self.path_d[f['path']] = item
                diritem.addChild(item)
                grp.append((f, item))
            self.ui.treeDir.addTopLevelItem(diritem)
            diritem.setExpanded(True)

    def init_menu(self):
        from elib.eqt.menu import TreeMenu, TreeActionWrapper

        class ActionDelete(TreeActionWrapper):
            text = u'删除'

            def test(self, f):
                if f:
                    return True

            def treeAction(self0, tree):
                filelist = [item.userData().get('path', '/')
                            for item in tree.selectedItems()]
                if filelist:
                    self.waitfor(self.pcs.delete(filelist))

        self._menu = TreeMenu([ActionDelete()])
        self._menu.attach(self.ui.treeDir)

    def delete_checked(self):
        checked_items = []
        for group in self.groups:
            for f, item in group:
                if item.checkState(0) == QtCore.Qt.Checked:
                    checked_items.append(f)
        if checked_items:
            if eqt.confirm(u'确定要删除勾选的文件吗？', self):
                files = [f['path'] for f in checked_items]
                d = self.pcs.delete(files)
                d.progress.connect(
                    lambda s, t: self.set_status(u'正在删除 %s/%s ' % (s, t)))
                d.cbs(lambda a: eqt.alert(u'删除完成!', self),
                      lambda p:
                      eqt.alert(u'<a style="color:red">错误！</a>', self))
        else:
            eqt.alert(u'没有勾选文件!', self)

    def set_status(self, text):
        self.ui.lblStatus.setText(text)

    def smart_check(self):
        for group in self.groups:
            to_reserve_item = None
            to_delete_items = []
            for f, item in group:
                if not to_reserve_item:
                    to_reserve_item = (f, item)
                    continue
                if (len(self.pcs.basename(f['path'])) <
                        len(self.pcs.basename(to_reserve_item[0]['path']))):
                    to_delete_items.append(to_reserve_item)
                    to_reserve_item = (f, item)
                else:
                    to_delete_items.append((f, item))
            to_reserve_item[1].setCheckState(0, QtCore.Qt.Unchecked)
            for f, item in to_delete_items:
                item.setCheckState(0, QtCore.Qt.Checked)


