# coding:utf8
__author__ = 'loong'
from common import QtGui, QtCore, QtNetwork, log
from elib.eqt.browser import SimpleBrowser
from elib.pcs import PCS


class LoginWin(QtGui.QWidget):
    login_success = QtCore.Signal()

    def __init__(self):
        super(LoginWin, self).__init__()
        self.cookie = None
        lo = QtGui.QVBoxLayout()
        self.brs = LoginBroswer()
        lo.addWidget(self.brs)
        self.setLayout(lo)
        self.brs.finished.connect(self.onFinished)

    def onFinished(self):
        self.cookie = self.brs.cookie
        self.login_success.emit()
        self.close()


class LoginBroswer(SimpleBrowser):
    finished = QtCore.Signal()

    def __init__(self):
        super(LoginBroswer, self).__init__()
        self.cookie = None
        self.browser.page().userAgent = 'Android'
        self.browser.setUrl('http://pan.baidu.com')
        self.browser.loadFinished.connect(self.onLoadFinished)
        self.myurl = QtGui.QLabel(u'联系作者: <a href="http://a.bit.so">http://a.bit.so</a>')
        self.myurl.setOpenExternalLinks(True)
        self.layout().addWidget(self.myurl)

    def onLoadFinished(self):
        if '/pan.baidu.com' in str(self.browser.url()):
            cookies = self.browser.cookieJar().cookiesForUrl(
                'http://pan.baidu.com')
            raw_cookie = ';'.join(
                [str(ck.toRawForm(QtNetwork.QNetworkCookie.NameAndValueOnly))
                 for ck in cookies])
            pcs = PCS(raw_cookie)
            d = pcs.listdir('/')

            @d.eb
            def eb(p):
                log.error(p)

            @d.cb
            def ok(p):
                self.cookie = raw_cookie
                self.finished.emit()
