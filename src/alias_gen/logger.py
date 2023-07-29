import argparse
import logging


def init_logger(args: argparse.Namespace):

    if args.debug:
        logging.basicConfig(format="%(levelname)s:\t%(message)s", level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


log = logging.getLogger("main")
debug = log.debug
