#!/usr/bin/env python
import pytest 
import os 
from unittest import TestCase 
from acme_collectors.engines.ibm_watson_nlp import WatsonNLP
"""
Name: Rio Atmadja
Date: December 05, 2020
Description: Test case for Watson Tone Analyzer 
"""
CREDENTIAL_PATH: str = os.path.join(os.path.expanduser("~/"), "credentials.json") 
class TestWatsonToneAnalyzer(TestCase): 

    @pytest.mark.skipif(os.getenv("BITBUCKET_BRANCH") == "master" or os.getenv("BITBUCKET_BRANCH") == "develop",  
                      reason="Local Test Only.") 
    def test_tone_analyzer(self): 
        article: str = """
        In a statement, United Nations Secretary-General Antonio Guterres’s spokesman urged for “restraint and the need to avoid any actions that could lead to an escalation of tensions in the region”.
        But Iran’s Supreme Leader Ali Hosseini Khamenei called for the killers to be brought to justice, and a sense of discomfort has settled over some Iraqis.
        The killing of one of Iran’s towering figures felt reminiscent of the assassination of top Iranian General Qassem Soleimani in January.
        The killing of Soleimani by a US air strike paved the path towards an uptick in violence between American troops and Iran-backed armed groups, like Kataib Hezbollah.
        The group released a statement following the killing of Fakhrizadeh calling for revenge against the “Zionist-American-Saudi axis’ criminal record. The cost of their crimes must be high.”
        """ 
        tone_analyzer = WatsonNLP(cred_path=CREDENTIAL_PATH)
        return self.assertEqual(len(tone_analyzer.get_tone(sentence=article)), 3 )
