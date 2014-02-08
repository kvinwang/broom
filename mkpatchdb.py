# coding:utf8
__author__ = 'loong'
import json

base_url = 'http://git.oschina.net/loongw/broom-patches/raw/master/'


def make_patchdb(files, version):
    db = {}
    for filename in files:
        ov = filename.split('-', 1)[0]
        nv = version
        db[ov] = {
            'version': nv,
            'url': base_url + filename,
            'description': ''
        }
    return json.dump(db, open('broom_patches.json', 'w'))
