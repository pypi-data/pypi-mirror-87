#!/usr/bin/python 
from ibm_watson import ToneAnalyzerV3 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from acme_collectors.utils.constants import IBM_TONE_ANALYZER_ENDPOINT
from acme_collectors.utils.helpers import load_credentials
import os 
import json

from typing import Dict, List, Union

"""
                         ___ ____  __  __  __        ___  _____ ____   ___  _   _ 
                        |_ _| __ )|  \/  | \ \      / / \|_   _/ ___| / _ \| \ | |
                         | ||  _ \| |\/| |  \ \ /\ / / _ \ | | \___ \| | | |  \| |
                         | || |_) | |  | |   \ V  V / ___ \| |  ___) | |_| | |\  |
                        |___|____/|_|  |_|    \_/\_/_/   \_\_| |____/ \___/|_| \_|

                                                                                                                            
                                                 `-:.                                               
                                               -:++++/.                                             
                                             ./++///+++-`                                           
                                           ./+///+o+///++-`                                         
                                         .:+////+oys++//++/.                                        
                                       .:++//+++oyhyso+////+/.                                      
                                     .:+///+++ooyhhhyyso++////:.                                    
                                   .://///++ooyhhhhyhhyyo++////+:.                                  
                                 .://///++osyhhhhhhhhhhhyyso++///+:`                                
                               `-////++osyyhhhhhhhhhhhhhhhhyyso+////:.                              
                             `-/////+osyhhhhhhhhhhhhhhhhyhhhhyyyo+//++:`                            
                           `.////++++oosyyhhyyhhyhhhhhhyhhyhhyso+o+/////.                           
                          .://///o++++++oshhyhyhhhyhyhyyhhhys++ooo+o++///:`                         
                        `://////+o++o+o+o+yyyyyssyhhssysyhhy+++o++oo+++////-`                       
                      `-////++++ooo+o++oo+osoos++shyoo++osso++oo++ooooo+/////:`                     
                    `.////ooo++++o++oo+++++o++s++ohys+++o++o++oooooo+o+++o+////-`                   
                  `-:///+oyhs+++oo+ooo+oo++o++o++ohyso++oo+oo+++o+oo+oo+osys+////-`                 
                `-/////+oyyhhso+oo+oooooooooooo++shyso++oo+oo+ooo+oo+o++syhys++///+-`               
              .:/+///++oyyhhhhyysso+o+ooo+oo++o++syhsoo+oo+o++++++o++oyyhhhhyyo++//++:`             
           `.//++//++osyyhhhhhhhhysoo+oooooooosooyhhyyo+oo+oooooo++syhhhhhhhhyyso+///+/-`           
          -+++///+++syyhhhhhhhhhyy+oooooo+oo+oyyyhyyhyyyyo+oo++o++++yhhhhdhhhhhyys+o+////-`         
        -/++///++ssyyhhhhhhhhhhyyo+ooooooooosyhyooo+oosyys+o+ooo+++++yhhhdhhhhhhyyys++///+/-`       
      `/+///++osyhhyhhhhhhhdhhhyhyhhhyyhyyyhhhy++ooo+o+shhyyyyyyyyyyyyhhhhhhdhhhhhhyyyso+///+:`     
       -/+/+/++osyhhhhhhhhhdhhhyyyyyyyhhyyyhhhy++ooo+o+shhyyyyyyyyyyyyhhhhhhhhhhhhhhyyso++/+//.     
        `-/++//+oosyyhhhhhhhhhdhyo+oooooo++oshys+ooo+ooyhy+oooooooo++yhhhhhhhhhhhhyysso++++/:.      
          `-/+///++ooyyhhhhhhhhhhs++o+oooo+o+oyyyyyyyhyyho++oo+oo+o+ohhhhhhhhhhhyyoo+++//+/.        
            `:/+///+++oyhhhhhhhhhhs+o+o+o+oo++osyyyyhyssoo+ooooo+++oyhhhhhhhhhyyo+++/////.          
              `:+++/+o+osyhhhhyysso+o+oooo+so+oo+ohhyoooooo+ooooo++sysyyhhhhhysoo+++//:.            
                `:/+//+++syhyyo+oooooooooo+soooo+oyhyoo+oo++o+oo+ooo+o+osyyhyo++++++:.`             
                  `:////++yysoo+ooooooooo++oo+oo+oyhyoo+o++oooooo+o++++++yyho++/++/.`               
                    `://+/+o+oooooooooo+oo+so+oo+oyhys++ooooooooo+o++o+++oso+/+//-`                 
                      `:+///+ooo+ooooo+oo++ysooo+oyhyooooossoo+oo+oo++++++++++/-`                   
                        .:////oo+o+ooo++o+ohhyyssshhyssyyyyyo++o++oo++o+/+++/-`                     
                          .:/+/++++ooo++osyhhhhyyyyhyyyhhhhhyo+o+++o+++//+/-`                       
                           `./++//+++oossyhhhyyyyyyhyyyhhhhhhysoo+oo++/+/-`                         
                             `-//+//+osyyhhhyyyhhhyyyhhhhhyhhhyyy++/+//-`                           
                               `.:++/++osyyhhhyyhyyyyyhhhhhhyysoo//+/:`                             
                                  ./+//++oosyyhhhyhhyyhhhhysso+////:.                               
                                   `-////+ooosyhhhyhyhhyyyoo+//+//.                                 
                                     `-////+o++syhyhhyysoo+///+/-`                                  
                                       `-+/+/+oooyhhhyo++/+/+/-`                                    
                                         `:/+//+++yyso++//++:`                                      
                                           `:/+//+oo+/+/++:`                                        
                                             .:+//++//++/`                                          
                                               ./////+/-                                            
                                                 -///-`                                             
 `                                                 `                                                
                                                             
Name: Rio Atmadja
Date: December 04, 2020 
Description: IBM Watson Engine class to analyze a given tone from a sentence. 
                                                          
"""
class WatsonNLP(object):   

    def __init__(self, cred_path: str):
        """
        NAME 
            WatsonNLP 

        DESCRIPTION
            Python module for ACME project to analyze tone from a post or news paper article. 

        PACKAGE CONTENTS 
            get_tone
        """
        self.response: List = [] 
        self.cred_path: str = cred_path 
        if not self.cred_path and not load_credentials(credential=cred_path): 
            raise FileNotFoundError(f"[X] Please provide the right credentials.")
        
        self.creds = json.loads(open(self.cred_path, 'r').read()) 
        if not self.creds.get('IBM_TOKEN_API'):
            raise AttributeError("Please provide the right IBM_TOKEN_API")


    def get_tone(self, sentence:str, version: str = "2017-09-21") -> Union[List,Dict]:
        """
        Description
        -----------
        Helper function to extract tone from the given sentence 

        Parameters
        ----------
        :param sentence: given a non-empty string 
        :param version: an optional args with default of 2017-09-21 (Please reffer to the documentation https://cloud.ibm.com/apidocs/tone-analyzer?code=python) 

        Return
        ------
        :return: a list of dictionary that contains text, score, and tone name. 
        """
        if not sentence:
            raise ValueError("Please provide a valid sentence.")
        try:
            tone_analyzer = ToneAnalyzerV3(version=version, authenticator=IAMAuthenticator(self.creds.get('IBM_TOKEN_API')) ) 
            tone_analyzer.set_service_url(IBM_TONE_ANALYZER_ENDPOINT) 
            tones: Union[List, Dict] = tone_analyzer.tone(sentence).get_result().get('sentences_tone')

            if not tones:
                return [] 

            for sentence in tones: 
                sentence_tones: List = sentence.get('tones')
                if sentence_tones: 

                    score: float = sentence_tones[0].get('score') 
                    tone_name: str = sentence_tones[0].get('tone_name') 

                    self.response.append({'text': sentence.get('text'),
                                          'score': score,
                                          'tone_name': tone_name 
                                         })
                
            return self.response

        except ConnectionError as e:
            raise ConnectionError(f"Unable to connect to the following endpoint {IBM_TONE_ANALYZER_ENDPOINT}. Please try again later.") from e 
