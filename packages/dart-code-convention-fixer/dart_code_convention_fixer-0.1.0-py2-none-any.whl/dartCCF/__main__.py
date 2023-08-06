# __main__.py

from .cmd_parser import parse_command
import dartCCF


def main():
    """ Dart source code analyzer"""
    print("Dart source code analyzer v. %s." % dartCCF.__version__)
    analyzer = parse_command()
    analyzer.run()


if __name__ == '__main__':
    main()
