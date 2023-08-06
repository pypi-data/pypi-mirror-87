#!/usr/bin/env python
import os
import requests
from uuid import uuid4
from subprocess import Popen, PIPE
from acme_collectors.utils.constants import NOTIFICATION_TEMPLATE
from acme_collectors.utils.helpers import saved_log

"""
Name: Rio Atmadja
Date: November 26, 2020
Description: Notification class to alert the user about the given events
"""

class Notifications(object):
    """
    NAME
        Notifications

    DESCRIPTION
        Python class to alert the users about the given event.

    PACKAGE CONTENTS
        send_notification
    """
    def __init__(self):
        self.ssmtp_path: str = "/usr/sbin/ssmtp"
        self.server_info = os.uname()
        self.server_address = requests.get('https://ifconfig.me').text
        self.log_path: str = os.path.join(os.path.expanduser("~/"), ".acme_log")

        if not os.path.exists(self.ssmtp_path):
            raise FileNotFoundError(
                f"Make sure to properly setup ssmtp on your {self.server_info.sysname} - {self.server_info.machine} - {self.server_info.release}")

    def send_notification(self, email_address: str, notification_subject: str, notification_msg: str):
        """
        Description
        -----------
        Helper function to send notification to the user about specific server events

        Parameters
        ----------
        :param email_address: given a valid email address
        :param notification_subject: given a valid notifaction subject
        :param notification_msg: given a valid notification message

        Returns
        -------
        :return:
        """
        if not all([email_address, notification_subject, notification_msg]):
            raise AttributeError("Please provide the following required parameters: email_address, "
                                 "notification_subject, and notification_msg")

        current_log: str = f"{str(uuid4())}.log"
        notification = NOTIFICATION_TEMPLATE % (email_address,
               notification_subject,
               self.server_info.nodename,
               self.server_address,
               current_log,
               notification_msg)

        if not os.path.exists(self.log_path):
            os.mkdir(self.log_path)

        # Saved the log to the given path
        log: str = os.path.join(self.log_path, current_log)
        saved_log(log=log, message=notification)

        try:
            Popen(f"{self.ssmtp_path} {email_address} < {log}", stderr=PIPE, stdout=PIPE, shell=True)

        except ConnectionError as e:
            saved_log(log=log, message="Something went wrong ...")
            raise ConnectionError(f"Unable to send notifiaction to {email_address}. Please try again later.")
