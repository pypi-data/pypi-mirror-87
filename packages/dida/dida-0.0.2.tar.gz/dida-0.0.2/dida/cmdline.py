import argparse

from dida.commands.init import init
from dida.commands.run import run

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(title='commands')

parser_init = subparsers.add_parser('init')
parser_init.set_defaults(func=init)

parser_run = subparsers.add_parser('run')
parser_run.set_defaults(func=run)
parser_run.add_argument('--port', type=int)


def main(args=None):
    args = parser.parse_args(args)
    if 'func' in args:
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main(['run'])
