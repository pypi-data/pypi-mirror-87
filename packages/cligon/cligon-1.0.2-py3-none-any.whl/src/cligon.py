#!/usr/bin/env python3
"""
C.L.I.G.O.N
Check if Link Is Good Or Not
Written in Python 3.8.2
"""

import sys
import argparse

try:
    from src import url_checker
except ModuleNotFoundError:
    import url_checker

UrlChecker = url_checker.UrlChecker

VERSION = "1.0.0"


def main():
    """cligon main function"""

    try:
        args = process_arguments(sys.argv[1:])

        time_out = 2.5
        checker = UrlChecker()
        urls = checker.parse_urls_from_file(args.filename)
        urls_status_list = checker.check_urls_thread(urls, time_out)
        checker.output_urls_and_status(urls_status_list, args)
        del urls_status_list
    except FileNotFoundError as e:
        print(e)

    return sys.exit(0)


def process_arguments(args):
    """Process the system arguments using argparser"""

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="input file to check URL links")
    parser.add_argument(
        "-v",
        "--version",
        help="display program name and version number",
        action="version",
        version="C.L.I.G.O.N (Check if Link Is Good Or Not) - CLIGON - " + str(VERSION),
    )
    parser.add_argument(
        "-j",
        "--json",
        action="store_true",
        help="output program results into JSON format",
    )
    parser.add_argument(
        "--all", action="store_true", help="default, output all url types"
    )
    parser.add_argument("--good", action="store_true", help="only display good urls")
    parser.add_argument("--bad", action="store_true", help="only display bad urls")

    return parser.parse_args(args)


if __name__ == "__main__":
    main()
