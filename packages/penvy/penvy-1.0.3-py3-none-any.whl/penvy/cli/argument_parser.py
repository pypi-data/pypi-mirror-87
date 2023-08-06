from argparse import ArgumentParser
from penvy.cli.str2bool import str2bool


def create_argument_parser():
    argument_parser = ArgumentParser()
    argument_parser.add_argument(
        "-v", "--verbose", dest="verbose", type=str2bool, nargs="?", const=True, default=False, help="Enable verbose logging"
    )
    argument_parser.add_argument(
        "-y", "--yes", dest="skip_confirmation", type=str2bool, nargs="?", const=True, default=False, help="Skip confirmation"
    )

    return argument_parser
