#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from XOGoogle.core.input import parse_args
from XOGoogle.core.scraper import scrape_google


def main() -> json:
    arguments, _ = parse_args()
    base_url = arguments.base_url
    results = scrape_google(
        arguments.keyword, base_url, crawl=arguments.crawl, page=arguments.pages)
    return results


if __name__ == "__main__":
    main()
