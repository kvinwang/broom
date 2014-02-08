# coding:utf8
__author__ = 'loong'
import sys
import os

default_config = {
    'webkit': {
        'cache_location': os.path.expanduser('~/broom/cache')
    },
    'video': {
        'using_embed': False
    }
}

if 'linux' in sys.platform:
    default_config.update({
        'upgrade': {
            'url': 'http://broom.bit.so/check-update2',
            'check_interval': 600,
            }
    })
else:
    default_config.update({
        'upgrade': {
            'url': 'http://broom.bit.so/check-update',
            'check_interval': 600,
            }
    })


if __name__ == '__main__':
    import json
    json.dump(default_config, open('config.json', 'w'))

