import os
import socket
import sys

from tornado.ioloop import IOLoop

from dida.app import make_app
from dida.settings import Setting
from dida.utils import walk_module

sys.path.insert(0, os.getcwd())


def run(args):
    setting = Setting()

    mods = setting.get('JOB_MODULES')
    if mods:
        for mod in mods:
            walk_module(mod)

    port = args.port or 6060

    app = make_app()
    app.listen(port)
    print(
        "Running on:",
        "- Local:   http://localhost:%s" % port,
        "- Network: http://%s:%s" % (socket.gethostbyname(socket.gethostname()), port),
        sep=os.linesep,
        file=sys.stderr
    )
    try:
        IOLoop.current().start()
    except KeyboardInterrupt:
        pass
