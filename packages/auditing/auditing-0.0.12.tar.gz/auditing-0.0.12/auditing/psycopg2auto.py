import datetime
import logging
import re
from threading import Semaphore
from uuid import UUID

import psycopg2
import psycopg2.errors
from numpy import long
from psycopg2 import sql
from psycopg2._psycopg import OperationalError
from psycopg2.pool import ThreadedConnectionPool


# Inspired by: https://stackoverflow.com/questions/48532301/python-postgres-psycopg2-threadedconnectionpool-exhausted
class AutoThreadedConnectionPool(ThreadedConnectionPool):
    def __init__(self, minconn, maxconn, *args, **kwargs):
        self._semaphore = Semaphore(maxconn)
        super().__init__(minconn, maxconn, *args, **kwargs)

    def getconn(self, *args, **kwargs):
        self._semaphore.acquire()
        return super().getconn(*args, **kwargs)

    def putconn(self, *args, **kwargs):
        super().putconn(*args, **kwargs)
        self._semaphore.release()

    # Change THIS method to use the connection logic below (with auto-stuff)
    def _connect(self, key=None):
        """Create a new connection and assign it to 'key' if not None."""
        conn = connect(*self._args, **self._kwargs)
        if key is not None:
            self._used[key] = conn
            self._rused[id(conn)] = key
        else:
            self._pool.append(conn)
        return conn


class AutoConnection:
    def __init__(self, connection):
        self.connection = connection

    def cursor(self):
        return AutoCursor(self.connection)

    # Just delegate everything else.
    def __getattr__(self, name):
        return getattr(self.connection, name)


class AutoCursor:
    def __init__(self, connection):
        self.cursor = connection.cursor()
        self.connection = connection

    def execute(self, *args, **kwargs):
        try:
            self.cursor.execute(*args, **kwargs)
        # If the table does not exist, create it.
        except psycopg2.errors.lookup("42P01") as e:
            self.connection.rollback()
            if re.match(r'^relation ".*" does not exist\n', e.args[0]):
                # Figure out which table is missing.
                match = re.findall("INSERT INTO (.*) \((.*)\) VALUES", args[0])[0]
                table_name, columns, values = match[0], match[1].split(","), args[1]
                columns = [c.strip() for c in columns]
                # Figure out the types.
                types = [map_type(value) for value in values]
                table_definition = ",".join(["{} {}".format(column, types[i]) for i, column in enumerate(columns)])
                # Create the table.
                command = sql.SQL("CREATE TABLE {} ({})").format(sql.Identifier(table_name), sql.SQL(table_definition))
                self.cursor.execute(command)
                self.connection.commit()
                logging.log(logging.INFO, "AUTO: CREATE TABLE {} ({})".format(table_name, table_definition))
                # Do recursion.
                return self.execute(*args, **kwargs)
            # If no special case handling was found, just raise the error as usual.
            raise e
        # If a column is missing, add it.
        except psycopg2.errors.lookup("42703") as e:
            self.connection.rollback()
            if re.match(r'^column ".*" of relation ".*" does not exist\n', e.args[0]):
                # Figure out which column is missing.
                column = re.findall(r'^column "(.*)" of relation "(.*)" does not exist\n', e.args[0])[0][0].strip()
                # Figure out the type.
                match = re.findall("INSERT INTO (.*) \((.*)\) VALUES", args[0])[0]
                table_name, columns, values = match[0], match[1].split(","), args[1]
                columns = [c.strip().lower() for c in columns]
                column_definition = "{} {}".format(column, map_type(values[columns.index(column.lower())]))
                # Modify the table.
                command = sql.SQL("ALTER TABLE {} ADD COLUMN {}").format(sql.SQL(table_name),
                                                                         sql.SQL(column_definition))
                self.cursor.execute(command)
                self.connection.commit()
                logging.log(logging.INFO, "AUTO: ALTER TABLE {} ADD COLUMN {}".format(table_name, column_definition))
                # Do recursion.
                return self.execute(*args, **kwargs)
            # If no special case handling was found, just raise the error as usual.
            raise e

    # Just delegate everything else.
    def __getattr__(self, name):
        return getattr(self.cursor, name)


def connect(*args, **kwargs):
    try:
        return AutoConnection(psycopg2.connect(*args, **kwargs))
    except OperationalError as e:
        # If the database does not exist, create it.
        if e.args[0] == 'FATAL:  database "{}" does not exist\n'.format(kwargs["database"]):
            db = kwargs["database"]
            kwargs["database"] = "postgres"
            connection = psycopg2.connect(**kwargs)
            connection.autocommit = True
            cursor = connection.cursor()
            command = sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db))
            cursor.execute(command)
            connection.close()
            logging.log(logging.INFO, "AUTO: CREATE DATABASE {}".format(db))
            # Do recursion.
            kwargs["database"] = db
            return AutoConnection(psycopg2.connect(**kwargs))
        # If no special case handling was found, just raise the error as usual.
        raise e


# region Type mappings

def map_type(obj):
    if type(obj) in default_type_mappings:
        return default_type_mappings[type(obj)]
    raise ValueError("Unsupported type {}".format(type(obj)))


# TODO: Should be customizable
default_type_mappings = {
    None: "NULL",
    bool: "bool",
    str: "text",
    float: "double precision",
    int: "int",
    long: "bigint",
    UUID: "uuid",
    dict: "hstore",
    list: "array",
    datetime.datetime: "timestamp",
    datetime.timedelta: "interval",
}


# endregion
