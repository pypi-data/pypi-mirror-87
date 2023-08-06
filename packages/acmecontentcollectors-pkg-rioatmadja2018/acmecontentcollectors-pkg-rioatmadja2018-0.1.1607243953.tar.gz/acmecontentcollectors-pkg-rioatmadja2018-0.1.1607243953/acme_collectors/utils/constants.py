#!/usr/bin/env python
from acme_collectors.utils.helpers import get_current_credential_paths
"""
Name: Rio Atmadja
Date: November 25, 2020
Description: Constant script
"""

# Create justpasteit_posts 
CREATE_TABLE: str = """
    CREATE TABLE `justpasteit_posts` (
        `post_id` INT(11) NOT NULL AUTO_INCREMENT, 
        `date_created` TEXT, 
        `post_modified` TEXT, 
        `number_views` VARCHAR(255), 
        `url` VARCHAR(255),
        `image_url` TEXT, 
        `language` VARCHAR(255), 
        `posts` LONGTEXT , 
        PRIMARY KEY (post_id) 
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""

# Notification template
NOTIFICATION_TEMPLATE: str = """
To: %s
From: dscnotifier@gmail.com  
Subject: %s

NOTIFICATION 
--------------------------------
Server Name: %s
Server Address: %s
LOG Reference: %s
--------------------------------

MESSAGE
--------------------------------
%s
"""

# Create translated_posts 
TRANSLATED_TBL: str = """
    CREATE TABLE `translated_posts` (
        `post_id` INT(11) NOT NULL AUTO_INCREMENT,
        `original_post` LONGTEXT,
        `translated_post` LONGTEXT,
        `url` VARCHAR(255),
        `image_url` TEXT,
        `language` VARCHAR(255),
        `translated` BOOLEAN, 
        PRIMARY KEY (post_id) 
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8; 
"""
# NOTE: Location to your credentials
CREDENTIAL_PATH: str = get_current_credential_paths() 
