#!/usr/bin/python
"""
    This is the base file that takes care of the process of handling a
    connection with postgresql. User can create an object of this class
    and user this as an interface to interact with Postgres easily.
"""

# Library file required to setup Postgres.
import psycopg2
import traceback
import json

class PostgreSQL(object):
    """
        This is the base class that serves up the PostgreSQL functions
        to the end user with ease of access and handling.
    """
    def __init__(self, database="test", user="postgres",
                 password="password", host="127.0.0.1", port=4532):
        """
            This is the object Constructor function that processes the
            incoming items and creates a connection with Postgres.

            @:parameter
                database    -   Default Database to Connect to
                user        -   Postgres User name
                password    -   Postgres User password
                host        -   Postgres host name
                part        -   Connection port for Postgres
        """
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.error_found = False
        self.error = None
        self.postgres = None
        self.cursor = None
        self.connected = False
        self.__initialize()

    def __initialize(self):
        """
            This function is used as an initializer that actually sets-up a
            connection to the Postgres machine and creates a Cursor Object.
        """
        try:
            self.postgres = psycopg2.connect(
                database=self.database,
                user=self.user,
                password=self.password,
                host=self.host,
            )
            self.connected = True
            self.cursor = self.postgres.cursor()
            self.__setup_demo_database()
        except:
            self.error_found = True
            self.error = "Failed to Create a Connection with Postgres."

    def __setup_demo_database(self):
        """
            This function acts as a way to setup a Demo Database Table if one
            doesn't exist. This is a safety net that prevents the user from
            trying to insert data into the tables that doesn't exist.
        """
        create_string = '''CREATE TABLE IF NOT EXISTS DEMO
            (ID         SERIAL PRIMARY  KEY NOT NULL,
             USERNAME   TEXT                NOT NULL,
             EMAIL      TEXT                NOT NULL);
        '''
        try:
            self.cursor.execute(create_string)
            self.postgres.commit()
        except:
            self.error_found = True
            self.error = "Failed to Setup Demo Database Table. " + \
                         traceback.print_exc()

    def run_query_store(self, query_string, binding=None):
        """
            This function acts as a way to run a Query on the Postgres machine
            and this function is used for Persisting the Data to PostgreSQL
            system from the UI.
        """
        try:
            if self.connected and self.cursor is not None:
                if binding is not None:
                    self.cursor.execute(query_string, binding)
                else:
                    self.cursor.execute(query_string)
                self.postgres.commit()
                return ""
            else:
                return None
        except:
            self.__initialize()
            self.error_found = True
            self.error = "Failed to Execute the Query." + traceback.print_exc()
            return self.error

    def run_query(self, quert_string):
        """
            This function acts as a wat to read the Data from PostgreSQL machine.

            @:return
                postgres_data   -   JSON data of all items in PostgreSQL.
        """
        try:
            if self.connected and self.cursor is not None:
                self.cursor.execute(quert_string)
                rows = self.cursor.fetchall()
                return rows
            else:
                return "", "ERROR", "Failed to Obtain Data from PostgreSQL."
        except:
            return "", "", ""

    def check_status(self):
        """
            This function acts as a way to check and monitor the connection
            status for the Postgres Service.
        """
        if self.connected:
            return True, ""
        else:
            error = self.error
            if error is None :
                error = "Unable to Identify PostgreSQL connection Status."
            return False, error
