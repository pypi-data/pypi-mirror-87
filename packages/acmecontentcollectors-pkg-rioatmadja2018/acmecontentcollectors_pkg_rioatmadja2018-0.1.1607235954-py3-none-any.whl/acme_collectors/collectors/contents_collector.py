#!/usr/bin/env python
from bs4 import BeautifulSoup
from urllib import request
import time
import re
"""
Name: Rio Atmadja
Date: November 25, 2020
Description: Content collectors to retrieve data from different streams such as website, and Apis
"""

# Alias
from typing import Dict, List

class ContentsCollector(object):
    """
    NAME
        ContentsCollectors

    DESCRIPTION
        Parse contents from the following sources:
            - Google
            - Just Paste it
            - Twitter
            - Aljazeera

    PACKAGE CONTENTS
        search_contents_from_google
        justpasteit_contents
    """

    def __init__(self):
        self.headers: Dict = {
            'user-agent': 'Mozilla/3.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/137.36 (KHTML, like Gecko) Chrome/56.0.4240.183 Safari/137.36',
            'accept': '*/*'
        }

    def search_contents_from_google(self, keyword: str, wait_time: int = 5) -> List[str]:
        """
        Description
        -----------
        This function uses Google search to find the contents from https://justpaste.it and return the links

        Parameters
        ----------
        :param keyword: given the valid keyword
        :param wait_time: given the optional parameter with the default value of 5 seconds

        Return
        ------
        :return: a list of links from https://justpaste.it
        """

        if not keyword:
            raise AttributeError("Please provide a keyword")

        try:
            google_url: str = f"https://www.google.com/search?num=100&start=10&hl=en&meta=&q=site%3Ajustpaste.it%20intext%3A({keyword})"
            response = request.urlopen(request.Request(url=google_url, headers=self.headers)).read()

            soup = BeautifulSoup(response, 'html.parser')
            results: List[str] = list(set(list(map(lambda tag: re.sub(".*.?q=|&sa=.*.", "", tag),
                                                   filter(lambda tag: 'https://justpaste.it' in str(tag),
                                                          [tag.find('a').get('href') for tag in soup.find_all('div') if
                                                           tag.find('a')])))))

            time.sleep(wait_time)
            return list(filter(lambda url: 'https://justpaste.it' in url, results))

        except ConnectionError as e:
            raise ConnectionError("Unable to make query to https://www.google.com. Please try again") from e

    def justpasteit_contents(self, url: str) -> Dict:
        """
        Description
        -----------
        Helper function to grab the website content from https://justpaste.it

        Parameters
        ----------
        :param url: given a valid url

        Returns
        -------
        :return:
        """
        try:
            response = request.urlopen(request.Request(url=url, headers=self.headers)).read()
            soup = BeautifulSoup(response, 'html.parser')
            if not soup:
                return {'date_created': None,
                        'post_modified': None,
                        'number_views': None,
                        'url': None,
                        'image_url': None,
                        'language': None,
                        'posts': None
                        }

            javascript_elements: List = soup.find('head').find_all('script')
            for script in javascript_elements:
                if isinstance(script.string, str):
                    metadata: Dict = eval(
                        re.sub(r".*.window\.barOptions =", "", script.string.strip(' ').replace('true', 'True').replace('false','False').replace('null', 'None').split('\n')[-2]).strip(
                            ";").lstrip(' '))

            return {'date_created': metadata.get('createdText', None),
                    'post_modified': metadata.get('modifiedText', None),
                    'number_views': metadata.get('viewsText', None),
                    'url': url,
                    'image_url': [img.get('src') for img in soup.find('body').find_all('img') if 'justpaste' in img.get('src') and '/img/r/' in img.get('src')],
                    'language': metadata.get('contentLang', None),
                    'posts': soup.find('body').text
                   }

        except ConnectionError as e:
            raise ConnectionError(f"Unable to make request to {url}. Please Try Again Later.")