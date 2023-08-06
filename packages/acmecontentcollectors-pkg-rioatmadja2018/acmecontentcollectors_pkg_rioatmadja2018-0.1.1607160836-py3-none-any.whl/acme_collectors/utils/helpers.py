#!/usr/bin/env python
import json

"""
Name: Rio Atmadja
Date: November 27, 2020 
Description: Helper utilities for ACME Collectors 
"""

def load_credentials(credential: str = "") -> bool:
    """
    Description
    -----------
    Helper function to load credential, if it's in JSON format return True, otherwise return False

    Parameters
    ----------
    :param credential: given a valid credential

    Returns
    -------
    :return: a boolean value
    """
    try:
        json.loads(open(credential, 'r').read())
        return True
    except:
        return False

def saved_log(log: str, message: str):
    """
    Description
    -----------
    Helper function to write message to the given path

    Parameters
    ----------
    :param log: given a valid path
    :param message: given a valid message

    Returns
    -------
    :return:
    """
    if not all([log, message]):
        raise AttributeError("You must provide the required parameters log and message.")

    with open(log, 'w') as f:
        f.write(message)
    f.close()

