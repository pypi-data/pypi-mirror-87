import os
import re
import shutil

import dida


def _copytree(src, dst, ignore_patterns=None):
    names = os.listdir(src)
    os.makedirs(dst, exist_ok=True)

    def ignore(n):
        for pattern in ignore_patterns:
            if re.search(pattern, n):
                return True
        return False

    for name in names:
        if ignore(name):
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        if os.path.isdir(srcname):
            _copytree(srcname, dstname, ignore_patterns)
        else:
            shutil.copy2(srcname, dstname)
            print("Created: %s" % dstname)


def init(args):
    path = os.path.join(dida.__path__[0], 'templates', 'project')
    _copytree(path, os.getcwd(), ignore_patterns=[r'\.pyc$'])
    print('The project successfully initialized.')
