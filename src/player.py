# coding:utf8
__author__ = 'loong'
from ui.broom_tag import TagWidget
from elib.eqt.browser import SimpleBrowser
from PySide.QtWebKit import QWebSettings
from PySide import QtCore, QtGui
from elib.elog import log


QWebSettings.globalSettings().setAttribute(QWebSettings.PluginsEnabled, True)


def derive_cls(cls):
    cls_str = '''class Klass(Parent):
    _pp = Parent'''

    tpl = r'''

    def {0}(self, *a, **ka):
        v = self._pp.{0}(self, *a, **ka)
        tpl = '\n'.join(['attr  : %s',
                         'args  : %s',
                         'kargs : %s',
                         'rv    : %s'])
        log.error__(tpl % ('{0}', a, ka, v))
        return v
'''

    for attr in dir(cls):
        if not attr.startswith('_') and attr != 'invalidate':
            if type(getattr(cls, 'tr')) == type(getattr(cls, attr)):
                cls_str += tpl.format(attr)

    env = {'Parent': cls}
    glb = env.copy()
    glb.update(globals())
    exec cls_str in glb, env
    return env.get('Klass')


if __name__ == '__main__':
    derive_cls(QtGui.QHBoxLayout)


class Player(SimpleBrowser):
    def __init__(self, broom, data_path=None):
        super(Player, self).__init__(data_path=data_path, save_cookie=False)
        self.updating = False
        self.broom = broom
        self.cfg = broom.marksdb
        #self.browser.page().userAgent = 'Mozilla/4.0 Broom'
        self.browser.page().userAgent = None
        self.meta = None
        self.init_ui()

    def init_ui(self):
        self.mark_panel = TagWidget()
        self.mark_panel.setCheckable(True)
        self.mark_panel.tagToggled.connect(self.save_marks)
        self.layout().addWidget(self.mark_panel)
        self.load_tags()
        self.cfg.listen(self.load_tags)

    def load_tags(self):
        self.mark_panel.load_tags(self.broom.root_explorer.taglib)

    def set_cookiejar(self, cj):
        self.browser.setCookieJar(cj)

    def closeEvent(self, e):
        self.browser.setUrl('')
        return super(Player, self).closeEvent(e)

    def play(self, url, meta=None):
        log.info('Play url:', url)
        self.meta = meta
        url = QtCore.QUrl.fromEncoded(url)
        self.browser.load(url)
        self.show()
        self.update_marks()

    def update_marks(self):
        self.updating += 1
        md5 = self.meta.get('md5')
        marks = self.cfg.marks.get(md5) or []
        self.mark_panel.check_tags(marks)
        self.updating -= 1

    def save_marks(self):
        if self.updating:
            return
        md5 = self.meta.get('md5')
        marks = list(self.mark_panel.checked_tags)
        self.cfg.marks.set(md5, marks)
