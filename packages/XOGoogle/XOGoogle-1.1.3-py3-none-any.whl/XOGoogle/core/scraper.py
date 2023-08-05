#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import datetime
import requests
import trafilatura
import operator, itertools
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from typing import Optional, List
from typing import Dict, Any, List
from XOGoogle.core.settings import USER_AGENT


def scrape_google(cve: str, base_url="https://www.google.com/search?q=", start_page=1, page=1, crawl=False) -> Dict[str, Any]:
    start = (start_page - 1) * 10
    dorks = ["intext:exploit","intext:hacker","intext:attack","intext:patch", "inurl:blog", "inurl:article"]
    queries = [cve + dork for dork in dorks]
    search_results = []
    for query in queries:
        for page_no in range(start, start + (page * 10), 10):
            headers = {"user-agent": USER_AGENT}
            URL = base_url + '{}'.format(query) + '&start={}'.format(page_no)
            resp = requests.get(URL, headers=headers)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.content, "html.parser")
                for div in soup.findAll('div', {'class': 'g'}):
                    search_result = {}
                    try:
                        link = div.find(
                            'div', {'class': 'rc'}).find('a')['href']
                        if link:
                            search_result['link'] = link
                        title = div.find(
                            'div', {'class': 'rc'}).find('h3').text
                        if title:
                            search_result['title'] = title
                        breadcrumb = div.find('cite').text
                        if breadcrumb:
                            search_result['breadcrumb'] = breadcrumb
                        search_results.append(search_result)
                    except Exception:
                        continue
    key = operator.itemgetter('link')
    deduplicated_links = []
    for _, y in itertools.groupby(sorted(search_results, key=key), key=key):
        y = list(y)
        if y:
            deduplicated_links.append(y[0])
    if crawl:
        search_results = []
        for link in deduplicated_links:
            result = crawl_page(link)
            if result:
                search_results.append(result)
        results = {'ID': cve, 'gsearch_results': search_results}
    else:
        results = {'ID': cve, 'gsearch_results': deduplicated_links}
    return results


def crawl_page(search_result: Dict[str, Any], excluded_domains: List[str] = []):
    result = None
    try:
        domain = urlparse(search_result['link']).hostname
        if domain not in excluded_domains:
            html = trafilatura.fetch_url(search_result['link'])
            page_data = trafilatura.extract(html)
            meta = trafilatura.metadata.extract_metadata(html)
            date = meta.get('date', None)
            description = meta.get('description', None)
            search_result.update({'date': date, 'short_desc': description, 'page_data': page_data, 'new_article': True})
            result = search_result
    except Exception as err:
        print(err)
        print('Error in fetching link', search_result['link'])
    return result
