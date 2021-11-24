"""
MIT License

Copyright (c) 2021 Devansh Singh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import mysql.connector as mc

class Database:
    """Class for maintaining and authenticating user, database
    and table credentials

    Attributes
    ----------
    username: str
        Local MySQL server username
    password: str
        Local MySQL server password
    """

    def __init__(self, username: str, password: str) -> None:
        """
        Parameters
        ----------
        username: str
            Local MySQL server username
        password: str
            Local MySQL server password
        """

        self.uname = username
        self.passw = password
        Database.connection = None
        Database.cursor = None

    def authenticate(self) -> bool:
        """Connect to the MySQL server on the local machine
        with the initialized credentials

        Returns
        -------
        bool
            True if connection with the localhost can be made,
            else False
        """

        try:
            # initialize connection with MySQL
            Database.connection = mc.connect(
                host = "localhost",
                user = self.uname,
                password = self.passw,
                autocommit = True
            )

            if Database.connection.is_connected():
                # initialize cursor object for execution of commands
                Database.cursor = Database.connection.cursor(buffered = True)
                return True

            else:
                return False

        except:
            return False

    def auth_db(self, database: str) -> bool:
        """
        Check whether the provided database exists
        or not in the local MySQL server 

        Parameters
        ----------
        database: str
            name of the database to authenticate
        
        Returns
        -------
        bool
            True if database exists else False
        """
        authenticate = self.authenticate()

        try:
            if authenticate is True:
                Database.cursor.execute("show databases")
                # list of all databases of user
                result = Database.cursor.fetchall()

                for db in result:
                    if db[0] == database:
                        return True

                return False

            else:
                return False

        except:
            return False

    def auth_table(self, db: str, table: str) -> bool:
        """
        Check whether the provided table exists
        or not in the selected database

        Parameters
        ----------
        db: str
            name of database to use
        table: str
            name of table to authenticate

        Returns
        -------
        bool
            True if table exists else False
        """
        authenticate = self.authenticate().authenticate()

        try:
            if authenticate is True:
                Database.cursor.execute(f"use {db}")
                Database.cursor.execute("show tables")
                # list of all tables in selected database
                result = Database.cursor.fetchall()

                for data in result:
                    if data[0] == table:
                        return True

                return False

            else:
                return False

        except:
            return False

    def auth_table_columns(self, db: str, table: str, query: str) -> bool:
        """
        Check whether the provided table has the given column 
        as a parameter

        Parameters
        ----------
        db: str
            name of database to use
        table: str
            name of table to use
        query: str
            name of column to authenticate

        Returns
        -------
        bool
            True if column matches else False
        """
        authenticate = self.authenticate()

        try:
            if (authenticate is True):
                # split column name and type of column
                query = query.split(' ')
                Database.cursor.execute(f"use {db}")
                Database.cursor.execute(f"select * from {table}")
                # contains description of all columns in the table
                result = Database.cursor.description

                for column in result:
                    if column[0].lower() == query[0].lower():
                        return True

                return False

            else:
                return False

        except:
            return False
