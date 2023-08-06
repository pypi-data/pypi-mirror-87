#!/usr/bin/env python
from unittest import TestCase
from acme_collectors.engines.google_nlp import GoogleNLP
import pytest
import os
from typing import Dict, List
"""
Name: Rio Atmadja
Date: November 27,2020
Description: Google NLP Unit Test
"""
TEST_WORD: str = "ﺎﻟﺩﻮﻟﺓ ﺍﻺﺳﻼﻤﻳﺓ"
TEMP_CREDS_PATH: str = '/home/rioatmadja/Downloads/playground-s-11-9cec1422-152af8754a95.json'


class TestGoogleNLP(TestCase):

    @pytest.mark.skipif(not os.path.exists(TEMP_CREDS_PATH) or os.getenv("BITBUCKET_BRANCH", "") == 'master' or os.getenv("BITBUCKET_BRANCH", "") == 'develop',
                        reason="Local unit test")
    def test_detect_language(self):

        google_translate = GoogleNLP(creds_path=TEMP_CREDS_PATH)
        response: Dict = google_translate.detect_original_language(sentence=TEST_WORD)
        self.assertEqual(response.get('language'), 'ar')

    @pytest.mark.skipif(not os.path.exists(TEMP_CREDS_PATH) or os.getenv("BITBUCKET_BRANCH", "") == 'master' or os.getenv("BITBUCKET_BRANCH", "") == 'develop',
                        reason="Local unit test")
    def test_translate_language(self):

        google_translate = GoogleNLP(creds_path=TEMP_CREDS_PATH)
        response: Dict = google_translate.translate_to_language(sentence=TEST_WORD)
        self.assertEqual(response.get('translatedText'), 'The Islamic State')

    @pytest.mark.skipif(not os.path.exists(TEMP_CREDS_PATH) or os.getenv("BITBUCKET_BRANCH", "") == 'master' or os.getenv("BITBUCKET_BRANCH", "") == 'develop',
                        reason="Local unit test")
    def test_extract_text_from_image(self):
        image_url: str = "https://www.python.org/static/community_logos/python-logo-inkscape.svg"
        google_translate = GoogleNLP(creds_path=TEMP_CREDS_PATH)
        response: List = google_translate.extract_text_from_image(image_url=image_url)
        self.assertListEqual(response, ['2 python\nTM\n', '2', 'python', 'TM'])
