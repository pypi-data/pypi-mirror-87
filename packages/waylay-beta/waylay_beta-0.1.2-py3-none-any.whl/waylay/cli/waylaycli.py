import argparse
import logging


def main():
    logging.basicConfig()
    parser = argparse.ArgumentParser(
        prog='waylaycli', description='Command line interface to the Waylay Python SDK'
    )
    args = parser.parse_args()
    parser.print_help()
