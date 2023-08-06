#!/usr/bin/env python
import pymysql
from pymysql import MySQLError
from pymysql.err import DatabaseError
from acme_collectors.utils.constants import CREDENTIAL_PATH
from acme_collectors.utils.helpers import load_credentials
import os
import json

# Alias
from typing import Dict, List
from pymysql.connections import Connection

"""
Name: Rio Atmadja
Date: November 25, 2020
Description: MySQL engine class 
"""
class MySQLEngine(object):

    @load_credentials(CREDENTIAL_PATH) 
    def __init__(self, host: str = "127.0.0.1", user: str = "root", passwd: str = "", port: int = 3306, db: str = ""):
        """
        NAME
            MySQLEngine 

        DESCRIPTION
            MySQL Engine to provide functionality to read, update, delete, and write to the MYSQL database

        PACKAGE CONTENTS 
            mysql_connection
            bulk_insert
            create_table

        """
        
        # if parameters are left to their default values, then proceed to read from the system variables. 
        self.host: str = os.getenv('MYSQL_SERVER') if not host else host 
        self.user: str = os.getenv('MYSQL_ROOT_USER') if user == 'root' else os.getenv('MYSQL_USER') if user == 'default' else user 
        self.passwd: str = os.getenv('MYSQL_PASSWD') if not passwd else passwd 
        self.port: str = os.getenv('MYSQL_PORT') if not port else port 
        self.db: str = os.getenv('MYSQL_DB') if not db else db 

        self.conn = self.mysql_connection()
        self.cursor = self.conn.cursor()

    def mysql_connection(self) -> Connection:
        """
        Description
        -----------
        Helper function that returns MySQL Connection object

        Returns
        -------
        :return: a MySQL Connection object
        """

        try:
            conn = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db)
            return conn

        except MySQLError as e:
            raise MySQLError(f"Unable to connect to host {self.host}")

    def bulk_insert(self, insert_query: str, args: List[tuple]):
        """
        Description
        -----------
        Helper functions to do bulk insert into the MySQL database

        Parameters
        ----------
        :param insert_query: given a valid INSERT query
        :param args: given a non-empty list of tuples

        Return
        ------
        :return:
        """
        if not all([insert_query, args]):
            raise AttributeError("Both insert_query and args are required parameters.")

        if "insert into" not in insert_query.lower():
            raise ValueError("Please check your INSERT query.")

        if not isinstance(args, List) and not isinstance(args, tuple):
            raise TypeError("Must be type of List of tuple.")

        try:
            self.cursor.executemany(insert_query, args)
            self.conn.commit()
            self.conn.close()

        except MySQLError as e:
            raise MySQLError("MySQL has encountered the following errors. Please check your insert query") from e

    def create_table(self, create_tbl_query: str, table_name: str) :
        """
        Description
        -----------
        Helper function to create MySQL table

        Parameters
        ----------
        :param create_tbl_query: given a valid sql query
        :param table_name: given a valid table_name

        Returns
        -------
        :return:
        """
        if not all([create_tbl_query, table_name]):
            raise AttributeError("Both create_tbl_query and table_name are required parameters.")

        # Check if the given table exists
        self.cursor.execute("SHOW TABLES")
        current_tables = list(map(lambda tbl: tbl[0], self.cursor.fetchall()))

        if create_tbl_query in current_tables:
            raise DatabaseError(f"The given database {table_name} has already been created.")

        self.cursor.execute(create_tbl_query)
        self.conn.commit()

