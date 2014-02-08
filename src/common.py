# coding:utf8
__author__ = 'loong'
from PySide import QtGui, QtCore, QtNetwork
from elib.elog import log
from elib import eqt


FILE_MIME_TYPE = 'application/pcs-path'


def find_red(files):
    gmd5 = {}
    for f in files:
        if not f['isdir']:
            m = f['md5']
            if m not in gmd5:
                gmd5[m] = []
            gmd5[m].append(f)
    return [f for f in gmd5.itervalues() if len(f) > 1]


def get_size(groups):
    total_size = 0
    min_size = 0

    for g in groups:
        for f in g:
            total_size += f['size']
        min_size += g[0]['size']
    return total_size, total_size - min_size


def pcs_join(a):
    return '/'.join([i.rstrip('/') for i in a])


def prompt(text, parent=None):
    wgt = eqt.PromptWidget(parent, text)
    wgt.show()
    return wgt


def fmt_size(s):
    for i, unit in reversed(list(enumerate('\x00KMGTP'))):
        factor = 1024 ** i
        if s >= factor:
            return '%4.3f %sB' % (float(s) / factor, unit)
    return '%4s B' % s


class PromptableWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(PromptableWidget, self).__init__(parent)
        self._wait_wgt = None

    def prompt(self, text=None, defered=None):
        self._prompt(text)

        def _cb(p):
            self.hide_prompt()
            return p

        def _eb(p):
            self.hide_prompt()
            self.error(p)
            return p

        if defered:
            defered.cbs(_cb, _eb)

    def hide_prompt(self):
        self._prompt(show=False)

    def waitfor(self, defered):
        self.prompt(defered=defered)
        return defered

    def _prompt(self, text=None, show=True):
        if show and not self._wait_wgt:
            self._wait_wgt = prompt(text or u'请稍侯...', self)
        elif not show and self._wait_wgt:
            self._wait_wgt.finish()
            self._wait_wgt = None

    def error(self, p):
        log.error(p)
        eqt.alert("Error: %s" % p, self)


