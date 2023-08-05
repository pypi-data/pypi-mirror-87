# !/usr/bin/env python
# -*- coding: utf-8 -*-
from argparse import ArgumentParser, Namespace
from typing import Tuple, List


def parse_args() -> Tuple[Namespace, List[str]]:
    """ Parses the args from command line
    Returns:
        Tuple[Namespace, List[str]]: Returns known parsed
        arguments and a list of unknown args
    """
    parser = ArgumentParser()

    parser.add_argument(
        "-k",
        dest='keyword',
        type=str,
        help="Give keyword to fetch results")

    parser.add_argument(
        "-f",
        dest="format",
        required=False,
        default="json",
        help="Output format")

    parser.add_argument(
        "-p",
        dest="pages",
        required=False,
        default=1,
        type=int,
        help="no of google search result pages to be scraped")

    parser.add_argument(
        "-t",
        dest="threads",
        required=False,
        default=5,
        type=int,
        help="Number of threads")

    parser.add_argument(
        "-c",
        dest="crawl",
        required=False,
        default=False,
        type=bool,
        help="Crawl the scraped links")

    parser.add_argument(
        "-url",
        dest="base_url",
        required=False,
        default="https://www.google.com/search?q=",
        type=str,
        help="Enter the base url to be used for search")

    args, unknown = parser.parse_known_args()

    return args, unknown
