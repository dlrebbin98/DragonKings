'''
Command-line interface for the application.

Usage:
    python run.py <command> [<args>...]

Options:
    -h --help       Show this screen.
    --version       Show version.
'''

from docopt import docopt
from . import __version__ as VERSION

def main():
    pass

if __name__ == '__main__':
    arguments = docopt(__doc__, version=VERSION)
    main()