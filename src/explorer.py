# coding:utf8
__author__ = 'loong'
from elib import eqt
from elib.tree import Tree
from elib.misc import Signal
from elib.eqt.bind import Remember
from findred import FindRed
from itertools import count
from ui.explorer import Ui_Explorer
from common import PromptableWidget, QtCore, log, pcs_join, fmt_size
import json
from common import FILE_MIME_TYPE


class FileTree(object):
    def __init__(self, pcs, tree, marks):
        self.path_d = {}
        self.marks = marks
        self.waitsig = Signal()
        self.pcs = pcs
        self.tree = tree
        self.init_signal()
        self.init_dragdrop()
        self.init_menu()

    def waitfor(self, d):
        self.waitsig.emit(d)
        return d

    def init_signal(self):
        def on_double_clicked():
            for item in self.tree.selectedItems()[:1]:
                meta = item.userData().meta
                if meta.get('category') == 1:
                    self.pcs.play(meta.get('path'))

        self.tree.doubleClicked.connect(on_double_clicked)

    def init_menu(self):
        from elib.eqt.menu import TreeMenu, TreeActionWrapper

        class ActionDelete(TreeActionWrapper):
            text = u'删除'

            def testSelection(self, selection):
                return True

            def itemsAction(self0, items):
                filelist = [item.userData().meta.get('path', '/')
                            for item in items]
                if filelist:
                    self.waitfor(self.pcs.delete(filelist))

        class ActionRename(TreeActionWrapper):
            text = u'重命名'

            def test(self, data):
                return True

            def itemAction(self0, item):
                old_name = item.userData().meta.get('path')
                parent, name = old_name.rsplit('/', 1)
                dlg = eqt.AutoUI(self.tree, u'重命名',
                                 [('name', u'输入新文件名', str, name)])
                dlg.resize(400, dlg.height())
                if dlg.exec_():
                    new_name = dlg.value('name')
                    if new_name != name:
                        self.is_moving = True
                        new_pathname = pcs_join((parent, new_name))
                        self.pcs.rename(old_name, new_pathname).cb(
                            lambda p: self.focus_path(new_pathname))
                        self.is_moving = False

        class ActionMkdir(TreeActionWrapper):
            text = u'新建文件夹'

            def test(self, node):
                if node.meta['isdir']:
                    return True

            def itemAction(self0, item):
                def mkdir(path):
                    dlg = eqt.AutoUI(self.tree, u'新建文件夹',
                                     [('name', u'输入名称', str, '')])
                    dlg.resize(300, dlg.height())
                    if dlg.exec_():
                        name = dlg.value('name')
                        if name:
                            path = pcs_join((path, name))
                            self.waitfor(self.pcs.create(path)).cb(
                                lambda p: self.focus_path(path))

                path = item.userData().meta.get('path') or ''
                mkdir(path)

        class ActionPlay(TreeActionWrapper):
            text = u'播放'
            #autoHide = True

            def test(self, node):
                return not node.meta['isdir'] and node.meta.get('category') == 1

            def itemAction(self0, item):
                node = item.userData()
                self.pcs.play(node.meta['path'])

        self._menu = menu = TreeMenu([ActionPlay(),
                                      ActionDelete(),
                                      ActionRename(),
                                      ActionMkdir()])
        menu.attach(self.tree)

    def current_path_stack(self):
        stack = []
        cur_item = self.tree.currentItem()
        while cur_item:
            stack.append(cur_item._path)
            cur_item = cur_item.parent()
        return stack

    def focus_path_stack(self, stack):
        while stack:
            path = stack.pop(0)
            if self.focus_path(path):
                break

    def focus_path(self, path, expand=None):
        if expand is None:
            expand = True
        item = None
        while path:
            item = self.path_d.get(path)
            if item:
                break
            path, _ = path.rsplit('/', 1)
        if item:
            self.tree.clearSelection()
            item.setSelected(True)
            self.tree.setCurrentItem(item)
            if expand is not None:
                item.setExpanded(expand)
            return True
        return False

    def load(self, vfs, path=None):
        self.path_d = {}
        old_path = path and [path] or self.current_path_stack()

        self.tree.clear()
        root_item = eqt.SortableTreeItem([u'网盘', fmt_size(vfs.root.size)],
                                         vfs.root)
        root_item._path = '/'
        self.path_d['/'] = root_item

        def fillin_nodes(wgtitem, fsnode):
            for f in fsnode.sorted_subnodes:
                if not f.meta['isdir'] and self.marks.get(f.meta['md5']):
                    fname = u'[★]' + f.name
                else:
                    fname = f.name
                item = eqt.SortableTreeItem([fname, fmt_size(f.size)],
                                            f)
                item._path = f.meta.get('path')
                self.path_d[item._path] = item
                wgtitem.addChild(item)
                if vfs.isdir(f):
                    fillin_nodes(item, f)

        fillin_nodes(root_item, vfs.root)
        self.tree.addTopLevelItem(root_item)
        self.focus_path_stack(old_path)

    def init_dragdrop(self):
        _mimeData = self.tree.mimeData

        def get_path(item):
            return item.userData().meta.get('path')

        def mimeData(items):
            #mime = QtCore.QMimeData()
            mime = _mimeData(items)
            text = json.dumps([get_path(item) for item in items])
            mime.setData(FILE_MIME_TYPE, text)
            return mime

        self.tree.mimeData = mimeData

        def dropMimeData(item, flag, mime, action):
            path_json = mime.data(FILE_MIME_TYPE)
            if path_json:
                try:
                    lst_path = json.loads(unicode(path_json))
                    meta = item.userData().meta
                    dst = meta.get('path')
                    if not meta.get('isdir'):
                        dst, ignore = dst.rsplit('/', 1)
                    self.move(lst_path, dst)
                except Exception as e:
                    log.E()
                    eqt.alert(u'移动文件失败:%s' % e, self.tree)
            return True

        self.tree.dropMimeData = dropMimeData

    def move(self, filelist, dest):
        def _cb(p):
            if len(filelist) == 1:
                self.focus_path(pcs_join((dest, filelist[0])))
            else:
                self.focus_path(dest)
        self.waitfor(self.pcs.move(filelist, dest)).cb(_cb).ignore()


class Explorer(PromptableWidget):
    iterFinished = QtCore.Signal()
    explorers = {}
    id_gen = count()

    def __init__(self, broom, marks):
        """

            :type pcs: PCS
        """
        super(Explorer, self).__init__()
        self.current_meta = None
        self.remember = Remember()
        self.taglib = set()
        self.broom = broom
        self.pcs = broom.pcs
        self.marks = marks
        self.findred_win = None
        self.category_win = None
        self.is_moving = False
        self.eid = self.id_gen.next()
        self.explorers[self.eid] = self
        self.ui = ui = Ui_Explorer()
        ui.setupUi(self)
        ui.treeDir.setColumnWidth(0, 400)
        self.ltree = FileTree(self.pcs, self.ui.treeDir, marks)
        self.rtree = FileTree(self.pcs, self.ui.treeDir2, marks)
        self.init_config()
        self.init_signals()
        self.reload_ui()

    def init_config(self):
        for m in self.marks.value.itervalues():
            for n in m:
                self.taglib.add(n)

        self.ui.wgtTagPanel.load_taglib(self.taglib)

        self.remember.bind(self.broom.config, [
            ('video.use_embed', self.ui.ckbUsingEmbedPlayer)
        ])

    def closeEvent(self, e):
        self.explorers.pop(self.eid)
        self.deinit_signals()
        return super(Explorer, self).closeEvent(e)

    def init_signals(self):
        self.pcs.path_deleted.connect(self.on_path_deleted)
        self.pcs.path_moved.connect(self.on_path_moved)
        self.pcs.path_created.connect(self.on_path_created)
        self.pcs.path_changed.connect(self.reload_ui)
        self.pcs.iter_progress.connect(self.upgrade_progress)
        self.iterFinished.connect(self.on_iter_finished)
        self.ui.btnFindRed.clicked.connect(self.show_findred)
        self.ui.btnShowMarked.clicked.connect(self.show_marked)
        self.ui.btnReload.clicked.connect(self.reload_ui)
        self.ltree.waitsig.connect(self.waitfor)
        self.rtree.waitsig.connect(self.waitfor)

        @self.ui.wgtTagPanel.tagChanged.connect
        def _changetag():
            if self.current_meta:
                tags = list(self.ui.wgtTagPanel.tags)
                self.marks.set(self.current_meta['md5'], tags)

        @self.ui.wgtTagPanel.tagAdded.connect
        def _addtag(tag):
            self.taglib.add(tag)

        def dec(tree):
            @tree.itemSelectionChanged.connect
            def _():
                self.chnode(tree)

        dec(self.ui.treeDir)
        dec(self.ui.treeDir2)

    def chnode(self, tree):
        items = tree.selectedItems()
        if len(items) == 1:
            meta = items[0].userData().meta
            if not meta['isdir']:
                marks = self.marks.get(meta['md5'])
                self.ui.wgtTagPanel.set_tags(marks or [])
                self.current_meta = meta
                self.ui.wgtTagPanel.setEnabled(True)
                return

        self.ui.wgtTagPanel.setEnabled(False)
        self.ui.wgtTagPanel.set_tags([])
        self.current_meta = None

    def deinit_signals(self):
        self.pcs.path_deleted.disconnect(self.on_path_deleted)
        self.pcs.path_moved.disconnect(self.on_path_moved)
        self.pcs.path_created.disconnect(self.on_path_created)
        self.pcs.path_changed.disconnect(self.reload_ui)
        self.pcs.iter_progress.disconnect(self.upgrade_progress)

    def on_path_created(self, path):
        self.reload_ui(path)

    def on_path_deleted(self, path):
        self.reload_ui(path[0])

    def on_path_moved(self, src, dst):
        if self.is_moving:
            cur_path = dst.rstrip('/')
            if len(src) == 1 and dst.endswith('/'):
                cur_path = pcs_join((cur_path, src[0].rsplit('/', 1)[1]))
        else:
            cur_path = None
        self.reload_ui(cur_path)

    def show_marked(self):
        from category import CategoryPanel

        if not self.category_win:
            self.category_win = CategoryPanel(self.broom, self.marks)
        self.category_win.show()

    def upgrade_progress(self, prog):
        self.ui.lblStatus.setText(u'正在获取文件列表... %s' % prog)

    def start_iterfiles(self):
        self.prompt(u'正在获取文件列表...',
                    self.pcs.iterfiles())

    def show_findred(self):
        if not self.findred_win:
            self.findred_win = win = FindRed(self.pcs)
            win.selected_changed.connect(self.focus_path)
        self.findred_win.show()

    def on_iter_finished(self):
        self.reload_ui()

    def reload_ui(self, current_path=None):
        vfs = Tree()
        vfs.load_from_pcs_nodes(self.pcs.cache.values())
        vfs.stats_size()
        self.ltree.load(vfs, current_path)
        self.rtree.load(vfs)
        self.ui.lblStatus.setText(u'一共%s个目录或文件' % len(self.pcs.cache))

    def focus_path(self, path, expand=None):
        self.ltree.focus_path(path, expand)
