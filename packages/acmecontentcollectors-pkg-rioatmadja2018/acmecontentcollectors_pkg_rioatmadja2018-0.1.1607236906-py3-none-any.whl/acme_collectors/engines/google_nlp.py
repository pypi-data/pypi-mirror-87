#!/usr/bin/env python
from google.cloud import translate_v2 as translate
from google.cloud import vision
from acme_collectors.utils.helpers import load_credentials
import os

# Alias
from typing import Dict, List, Union

"""
Name: Rio Atmadja
Date: November 27, 2020 
Description: Google helper for natural language processing 
"""
class GoogleNLP(object):

    def __init__(self, creds_path: str):
        """
        NAME
            GoogleNLP

        DESCRIPTION
            Python module for ACME project for dealing with the natural language processing

        PACKAGE CONTENTS
            detect_original_language
            translate_to_language
            extract_text_from_image
        """

        if not os.path.exists(creds_path):
            raise FileNotFoundError("Please provide the right Google credentials")

        if not load_credentials(credential=creds_path):
            raise TypeError(f"The following file {creds_path} must be in JSON format.")

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds_path
        self.cred_path: str = creds_path
        self.translate_client = translate.Client()
        self.image_client = vision.ImageAnnotatorClient()
        self.image_vision = vision.Image()


    def detect_original_language(self, sentence: str) -> Dict:
        """
        Description
        ------------
        Helper function to detect the given language of the given sentence

        Parameters
        ----------
        :params sentence: given a non-empty sentence

        Returns
        -------
        :return: a dictionary with language, confidence, and input attributes
        """

        if not sentence:
            raise AttributeError("Please provide the required parameter: sentence.")

        return self.translate_client.detect_language(sentence)

    def translate_to_language(self, sentence: str, language: str = 'en') -> Union[str, list]:
        """
        Description
        -----------
        Helper function to translate the given sentence to English, unless specified.

        Parameters
        ----------
        :params sentence: given a non-empty sentence
        :params language: optional parameters with default as English

        Returns
        --------
        :return: a dictionary with translated text, detected source language, and the input attributes
        """

        if not sentence:
            raise AttributeError("Please provide the required parameter: sentence.")

        return self.translate_client.translate(sentence, target_language=language)

    def extract_text_from_image(self, image_url: str) -> List:
        """
        Description
        -----------
        Helper function to extract words from the given image

        Parameters
        ----------
        :param image_url: given a valid image_url

        Returns
        -------
        :return: a list of words
        """

        self.image_vision.source.image_uri = image_url
        response = self.image_client.text_detection(image=self.image_vision)
        texts = response.text_annotations

        if not texts:
            return []

        return [text.description for text in texts]

