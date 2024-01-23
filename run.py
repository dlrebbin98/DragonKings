'''
Command-line interface for the application.

Usage:
    python run.py <command> [<args>...]

Options:
    -h --help       Show this screen.
    --version       Show version.
'''
from docopt import docopt

from dragon_king import Simulation


def main():
    sim = Simulation(n_nodes=10, n_edges=50)
    sim.iterate(tot_timesteps=10, mechanism='IN', epsilon=0.6)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    main()