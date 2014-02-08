# coding: utf8
__author__ = 'loong'

import sys
reload(sys)
sys.setdefaultencoding("gbk")

from version import __version__
from PySide import QtGui, QtCore
from elib.pcs import PCS
from elib.registry import Registry
from elib.net.httpget import http_client
from elib.net.backends.qt import QtAsyncHTTPCore
from elib.upgrade import Upgrade
from elib.eqt.browser import DCookieJar
from login import LoginWin
from explorer import Explorer
from config import default_config
from player import Player
from elib.elog import log
import os


data_dir = os.path.expanduser('~/broom')


class Broom:
    def __init__(self):
        self.config = Registry(os.path.join(data_dir, 'config.json'),
                               default=default_config).get_root()
        self.marksdb = Registry(os.path.join(data_dir, 'marks.json'),
                                undefined_node='node').get_root()
        self.cookiejar = DCookieJar()
        self.cookiejar = DCookieJar(os.path.join(data_dir, 'cookies.txt'))
        self.login = LoginWin()
        self.login.brs.browser.setCookieJar(self.cookiejar)
        self.login.setWindowTitle(u'登陆 | Broom - %s' % __version__)
        self.pcs = PCS()
        self.root_explorer = ex = Explorer(self, self.marksdb.marks)
        ex.setWindowTitle(
            ex.windowTitle() + ' - %s' % __version__)
        self.player = Player(self, self.config.webkit.cache_location)
        self.player.set_cookiejar(self.cookiejar)
        self.init_signals()

    def init_signals(self):
        self.login.login_success.connect(self.on_login)
        self.pcs.play_required.connect(self.play)

    def on_login(self):
        self.pcs.set_cookie(self.login.cookie)
        self.root_explorer.show()
        self.root_explorer.start_iterfiles()

    def start(self):
        self.login.show()

    def play(self, url, meta):
        if self.config.video.use_embed:
            self.player.play(url, meta)
        else:
            QtGui.QDesktopServices.openUrl(url)


class FakePCS(PCS):
    def pan_request(self, meth, path, args=None, body_args=None, headers=None):
        return {'errno': 0}

    def iterfiles(self, path='/', progress_cb=None):
        import pickle
        self.cache = pickle.load(open('../wy721.dump', 'rb'))


app = QtGui.QApplication(sys.argv)
broom = Broom()


def setup_upgrade(broom):

    cfg = broom.config.upgrade
    broom.mod_up = up = Upgrade(__version__, cfg)
    up.timer = QtCore.QTimer()
    up.timer.setInterval(cfg.check_interval * 1000)
    up.timer.timeout.connect(up.try_check_update)
    up.timer.start()
    up.try_check_update()


def init():
    app.setStyleSheet('*{font-size: 12px;}')
    http_client.factory = QtAsyncHTTPCore


def main():
    init()
    setup_upgrade(broom)
    broom.start()
    app.exec_()


if __name__ == '__main__':
    main()
