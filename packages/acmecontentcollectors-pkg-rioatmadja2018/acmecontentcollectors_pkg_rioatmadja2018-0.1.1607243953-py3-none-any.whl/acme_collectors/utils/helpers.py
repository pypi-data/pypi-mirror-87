#!/usr/bin/env python
import json
import os 

"""
Name: Rio Atmadja
Date: November 27, 2020 
Description: Helper utilities for ACME Collectors 
"""

def load_credentials(credential_path: str = ""):
    """
    Description
    -----------
    Decorator to load credential_paths to the system environment 

    Parameters
    ----------
    :param credential_path: given a valid credential_path

    Returns
    -------
    :return: 
    """
    def wrap(function): 

        def wrap_function(*args, **kwargs): 
            
            # check if the credential_path exists 
            if not os.path.exists(credential_path):
                raise FileNotFoundError(f"Please provide the right credential_paths. Please check the following credential {credential_path}")
            
            # read the credential to the memory  
            creds: str = open(credential_path, 'r').read().strip("\n") 
            
            # before loading make sure that the string representation is in dictionary format 
            if not creds.index('{') == 0 and not creds.index('}') == len(creds) - 1: 
                raise TypeError(f"Please provide the right JSON format for the following file: {credential_path}") 

            # load the credential_paths to the system environments 
            for key,value in json.loads(creds).items(): 
                os.environ[key] = value # load all the credentials to the system variables (Credit: Google Cloud API behavior)  

            return function(*args, **kwargs) 

        return wrap_function 

    return wrap 
        

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

def get_current_credential_paths(credential_path: str = "" , credential_file_name: str = "credentials.json") -> str :
    """
    Description
    -----------
    Helper function to return the credentials path. 
    Note: Temporary Work around to the static credential path and this version might be deprecated in the future. 
    
    Parameters
    ----------
    :credential_path: given an optional parameter with default of empty string
    :credential_file_name: given an optional parameter with default of credentials.json 
    
    Return
    -------
    :return: a path to the credentials
    """
    
    # if the user supply the credential path, then we're good
    if credential_path:
        return credential_path
    
    # Support Linux and Mac OSX Only at this version
    if not hasattr(os, 'uname'):
        raise NotImplementedError(f"This library supports only Mac OSX and Linux Only")
        
    passwd_file: str = "/etc/passwd"
    if not os.path.exists(passwd_file):
        raise FileNotFoundError(f"Unable to find {passwd_file}. That's odd, Are you running *.nix Operating System?")
        
    current_user: str = [attr.split(":")[0] for attr in open(passwd_file,'r').read().strip().split("\n") if str(os.getuid()) in str(attr.split(":")[2]) ][0] # Mapped the current user 

    return os.path.join(os.path.expanduser(f"~{current_user}"), credential_file_name)
