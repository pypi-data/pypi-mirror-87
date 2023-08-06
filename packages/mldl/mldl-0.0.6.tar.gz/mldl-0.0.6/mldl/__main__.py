"""
MLDL module entry point
"""
import sys
from .cli.cli_main import main as _main


def main():
    """module entry point function
    """
    _main(sys.argv[1:])


if __name__ == '__main__':
    main()
