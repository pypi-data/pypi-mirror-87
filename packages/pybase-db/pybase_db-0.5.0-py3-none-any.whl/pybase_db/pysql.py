#       NTBBloodbath | PyBase v0.4.0       #
############################################
# PyBase is distributed under MIT License. #

# dependencies (packages/modules)
import os
import time
import sqlite3
import pathlib
import itertools
from rich.console import Console
from rich.traceback import install
install() # Use Rich traceback handler as the default error handler

console = Console()

class PySQL:
    """
    PyBase SQL Class

    ...

    Attributes
    ----------

    Methods
    -------
    delete(table: str, objects: dict = None)
        Delete a table or a element from a column (if it was declared) from the database established in PySQL init.
    create(objects: dict)
        Create a table with columns inside the database established in PySQL init.
    """

    def __init__(self,
                 database: str = None,
                 db_path: str = pathlib.Path().absolute(),
                 debug: bool = False):
        """
        Define the SQLite3 database to use and create it if it doesn't exist.

        ...

        Parameters
        ----------
        database : str, optional
            The name of the database without extension.
            Note: If you don't put a name for the db, it will be created directly in memory without consuming disk.
        db_path : str, optional
            The path where the database is located (default is current working directory).
            Example: /home/bloodbath/Desktop/PyBase
            Note: If the name of a db isn't specified in the db parameter, this path will not be used.

        Raises
        ------
        TypeError
            If database isn't a String (if it's declared).
            If debug isn't a Boolean.
        FileNotFoundError
            If the given path wasn't found.
        """

        self.__path = db_path  # private path variable to clean code.
        if isinstance(debug, bool) == False:
            raise TypeError('debug must be a Boolean.')
        else:
            self.__debug = debug   # debug messages

        # If database isn't equal to None or isn't a String, then raise TypeError.
        if type(database) != str and database != None:
            raise TypeError('database must be a String.')
        elif os.path.exists(db_path) != True:
            raise FileNotFoundError(
                f'The path ({self.__path}) wasn\'t found. Please check that the path exists.'
            )
        else:
            if database == None:
                try:
                    self.__conn = sqlite3.connect(':memory:')
                    self.__cursor = self.__conn.cursor()
                    if self.__debug == True:
                        console.log('[DEBUG]: Using a database stored in memory.')
                        time.sleep(1)
                except Exception as err:
                    console.print_exception()
            else:
                self.__DB = (f'{self.__path}/{database}.db')
                try:
                    self.__conn = sqlite3.connect(self.__DB)
                    self.__cursor = self.__conn.cursor()
                    if self.__debug == True:
                        console.log(f'[DEBUG]: using a database stored in disk ({self.__DB}).')
                        time.sleep(1)
                except Exception as err:
                    console.print_exception()
            if self.__debug == True:
                console.log(f'[DEBUG]: Using SQLite3 version v{sqlite3.version}')
                time.sleep(1)


    def delete(self, table: str, objects: dict = None):
        """
        Delete a table or element inside of the given table from the database established in PySQL init.

        ...
        
        Parameters
        ----------
        table : str
            The table which will be deleted from the database.
            Note: If the value parameter isn't None, the table will not be deleted, if not, the element inside it.
        objects : dict, optional
            The column and value to be deleted from the table.
            Example:
                {
                    "column": "username",
                    "value": "bloodbath"
                }

        Raises
        ------
        ValueError
            If table isn't a String or isn't declared or is equal to None.
        KeyError
            If objects doesn't have a value key.
        sqlite3.OperationalError
            If the given table isn't found.
            If the given table doesn't have the given value.
            If the given table doesn't have the given column.
        """

        if type(table) != str:
            # If a table isn't a String or isn't declared or is equal to None, then raise ValueError.
            raise ValueError('table must be a String.')
        elif objects is None or len(objects) == 0:
            # If a element isn't declared, then delete the entire table.
            # Search if the given table exists inside the database.
            self.__cursor.execute(f"""SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'""")
            rows = self.__cursor.fetchone()
            if rows is None:
                raise KeyError("The given table doesn't exists.")
            else:
                self.__cursor.execute(f"""DROP TABLE {table}""")
                if self.__debug == True:
                    time.sleep(0.5)
                    console.log(f"[DEBUG]: Deleting the table {table}...")
                    time.sleep(1.5)
                self.__conn.commit()
                time.sleep(0.5)
                console.log(f"[LOG]: The table {table} has been deleted.")
        else:
            # If there's no value key in objects, then raise error.
            if not "value" in objects:
                raise KeyError(f"[ERROR]: objects must have a value key.")
            else:
                # If a element is declared, then delete it from the table.
                # Search the given element in the given column and if it doesn't exists, raise error
                self.__cursor.execute(f"""SELECT {objects['column']} FROM {table} WHERE {objects['column']} = '{objects['value']}'""")
                rows = self.__cursor.fetchall()
                if len(rows) == 0:
                    raise ValueError("The given element doesn't exists in the given column.")
                else:
                    try:
                        self.__cursor.execute(f"""DELETE FROM {table} WHERE {objects['column']} = '{objects['value']}'""")
                        if self.__debug == True:
                            time.sleep(0.5)
                            console.log(f"[DEBUG]: Deleting the value {objects['value']} from the column {objects['column']} in table {table}...")
                            time.sleep(1)
                        self.__conn.commit()
                        time.sleep(0.5)
                        console.log(f"[LOG]: The element {objects['value']} has been deleted from {objects['column']} in {table}.")
                    except sqlite3.OperationalError as err:
                        console.print_exception()


    def create(self, objects: dict):
        """
        Create a table if not exists and its elements.

        ...

        Parameters
        ----------
        objects : dict
            The dictionary that contains the table and its elements.
            Example:
                {
                    "table": {
                        "name": "example",
                        "columns": {
                            "test": {
                                "type": "integer",
                                "value": 12345 # or [12345, 67890]
                            }
                        }
                    }
                }

        Raises
        ------
        ValueError
            If objects isn't a dict or is empty (equal to zero).
            If table name isn't a String.
            If columns key is empty (is equal to Zero).
            If columns key type isn't text or integer.
        KeyError
            If objects doesn't have a key called name or columns.
            If columns keys doesn't have type/value.
        """

        each_column = []   # Collect each column name and save them inside a list.
        each_type = []     # Collect each column type and save them inside a list.
        each_value = []    # Collect each column value and save them inside a list.

        # If objects isn't a dict or is equal to zero
        if type(objects) != dict or len(objects) == 0:
            raise ValueError('objects must be a dict and cannot be empty.')
        elif "name" in objects["table"] == False:
            raise KeyError('object dict must have a name key inside the table key.')
        # If table name value isn't a String.
        elif isinstance(objects["table"]["name"], str) == False:
            raise ValueError('table name must be a String.')
        # If table doesn't have a columns key.
        elif "columns" in objects["table"] == False:
            raise KeyError('object dict must have a columns key inside the table key.')
        else:
            if len(objects["table"]["columns"]) == 0:
                raise ValueError('columns key cannot be empty.')
            else:
                columns = objects["table"]["columns"]
                # Search in all the columns keys for type and value
                for column in columns:
                    # If type isn't a key inside the column, raise KeyError
                    if "type" in columns[column] == False:
                        raise KeyError(f'{column} must have a type key')
                    # If type value isn't integer or text, raise ValueError
                    elif not columns[column]["type"] in ["text", "integer"]:
                        raise ValueError(f'{column} type must be integer or text')
                    # If value isn't a key inside the element, raise KeyError
                    elif "value" in columns[column] == False:
                        raise KeyError(f'{column} must have a value key')
                    else:
                        # If all is good, then insert each element with
                        # their types and values inside different lists.
                        each_column.append(column)
                        each_type.append(columns[column]["type"])
                        each_value.append(columns[column]["value"])
                # Check if table doesn't exists.
                self.__cursor.execute(f"""SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{objects['table']['name']}'""")
                if not self.__cursor.fetchone()[0] == 1:

                    try:
                        # Initializing the table creation.
                        create_table = f"""CREATE TABLE IF NOT EXISTS {objects["table"]["name"]} (\n"""
                        for c in range(len(each_column)):            
                            create_table += f"""    {'{} {},'.format(each_column[c], each_type[c]) if (c + 1) != len(each_column) else '{} {}'.format(each_column[c], each_type[c])}\n"""
                        create_table += """);"""

                        if self.__debug:
                            console.log(f"[DEBUG]: Creating table {objects['table']['name']}...")
                            time.sleep(0.5)
                            console.log(f"[DEBUG]:", create_table)
                            time.sleep(1.5)
                        self.__cursor.execute(create_table)
                        time.sleep(0.5)
                        console.log(f"[LOG]: The table {objects['table']['name']} has been created successfully.")
                    except Exception as err:
                        console.print_exception()

                # Initializing the insertion
                try:
                    insert_data = f"""INSERT INTO {objects['table']['name']} ("""
                    for c in range(len(each_column)):
                        insert_data += f"""{'{}, '.format(each_column[c]) if (c + 1) != len(each_column) else '{}'.format(each_column[c])}"""
                    insert_data += """) SELECT """
                    for c in range(len(each_column)):
                        insert_data += f"""'{"{}".format(each_value[c]) if isinstance(each_value[c], list) == False else "{}".format(each_value[c][0])}'""" + f"""{", " if (c + 1) != len(each_column) else " "}"""
                    insert_data += f"""WHERE NOT EXISTS (SELECT 1 FROM {objects['table']['name']} WHERE """
                    for c in range(len(each_column)):
                        insert_data += f"""{each_column[c]} = '{"{}".format(each_value[c]) if isinstance(each_value[c], list) == False else "{}".format(each_value[c][0])}'"""
                        insert_data += f"""{ " AND " if (c + 1) != len(each_column) else ''}"""
                    insert_data += """);"""

                    self.__cursor.execute(insert_data)
                    self.__conn.commit()

                    if self.__debug:
                        if any(isinstance(value, list) for value in each_value):
                            console.log(f"[DEBUG]: Inserting the data only with the first arrays value...")
                            console.log("[DEBUG]:", insert_data)
                        else:
                            console.log(f"[DEBUG]: Inserting the data inside the table {objects['table']['name']}...")
                            console.log("[DEBUG]:", insert_data)

                    # Insert the rest of the array data inside the column
                    self.columns = []
                    self.all_values = []
                    self.values = []

                    for c in range(len(each_column)):
                        if isinstance(each_value[c], list):
                            self.columns.append(each_column[c])
                            self.all_values.append(each_value[c])
                    columns_length = 0
                    all_values_length = 0
                    values_length = 0

                    insert_data = ""
                    while 0 <= all_values_length < len(self.all_values):
                        for i, name in enumerate(self.all_values[all_values_length]):
                            if 0 < i:
                                if i == 1:
                                    self.values.append([])
                                    self.values[values_length].append(name)
                                else:
                                    self.values[values_length].append(name)
                        values_length += 1
                        all_values_length += 1

                    self.values = list(zip(*self.values))

                    row = 0
                    values_length = 0
                    while 0 <= values_length < len(self.columns) and 0 <= row <= (len(self.values) - 1):
                        insert_data += f"""INSERT INTO {objects['table']['name']} ("""
                        for c in range(len(self.columns)):
                            insert_data += f"""{'{}, '.format(self.columns[c]) if (c + 1) != len(self.columns) else '{}'.format(self.columns[c])}"""
                        insert_data += """) SELECT """
                        for i in range(len(self.values[row])):
                            insert_data += f"""'{"{}".format(self.values[row][i])}'""" + f"""{", " if (i + 1) != len(self.values[row]) else " "}"""
                        console.log(self.values[row])
                        insert_data += f"""WHERE NOT EXISTS (SELECT 1 FROM {objects['table']['name']} WHERE """
                        for c, i in itertools.zip_longest(range(len(self.columns)), range(len(self.values[row])), fillvalue=None):
                            insert_data += f"""{self.columns[c]} = '{"{}".format(self.values[row][i])}'"""
                            insert_data += f"""{ " AND " if (c + 1) != len(self.columns) else ''}"""
                        insert_data += """);\n\n"""
                        row += 1
                        values_length += 1

                    self.__cursor.executescript(insert_data)
                    self.__conn.commit()

                    if self.__debug:
                        if any(isinstance(value, list) for value in each_value):
                            console.log(f"[DEBUG]: Inserting the rest of the data arrays values inside the table {objects['table']['name']}...")        
                            time.sleep(0.5)
                            console.log(f"[DEBUG]:", insert_data)
                            time.sleep(1)

                    time.sleep(0.5)
                    console.log(f"[LOG]: The data has been inserted successfully inside the table {objects['table']['name']}.")
                except Exception as err:
                    console.print_exception()

    def get(self, table: str, objects: dict = None):
        """
        Get data from the database.

        ...

        Parameters
        ----------
        table : str
            The table where the data will be searched.
        objects : dict, optional
            The column and value that will be searched.
            Note: If the value is not specified, the entire column will be obtained.
            Example: {
                "column": "languages",
                "value": "Python"
            }

        Raises
        ------
        ValueError
            If table isn't a String.
            If objects isn't a dict.
        KeyError
            If the given column doesn't have the given value.
        sqlite3.OperationalError
            If the given table doesn't have the given column.

        Returns
        -------
        list
            A list with tuples that returns all the found values.
        """

        if type(table) != str:
            raise ValueError('table must be a String.')
        elif isinstance(objects, dict) == False:
            raise ValueError('objects must be a dict.')
        else:
            if not "column" in objects:
                try:
                    # Get all the table
                    self.__cursor.execute(f"""SELECT * FROM {table}""")
                    rows = self.__cursor.fetchall()
                except sqlite3.OperationalError as err:
                    console.print_exception()

                if self.__debug:
                    time.sleep(0.5)
                    console.log(f"[DEBUG]: Getting the table {table}...")
                    time.sleep(0.5)
                    console.log(f"[DEBUG]: The table {table} was obtained successfully and saved in rows attribute.")
                    time.sleep(0.5)
                    console.log("[DEBUG]:", rows)

                return rows
            else:
                if not "value" in objects:
                    try:
                        # Get all the column
                        self.__cursor.execute(f"""SELECT {objects['column']} FROM {table}""")
                        rows = self.__cursor.fetchall()
                    except sqlite3.OperationalError as err:
                        console.print_exception()

                    if self.__debug:
                        time.sleep(0.5)
                        console.log(f"[DEBUG]: Getting the column {objects['column']} from {table} table...")
                        time.sleep(0.5)
                        console.log(f"[DEBUG]: The column {objects['column']} was obtained successfully and saved in rows attribute.") 
                        time.sleep(0.5)
                        console.log("[DEBUG]:", rows)

                    return rows
                else:
                    try:
                        # Get the value in the column
                        self.__cursor.execute(f"""SELECT {objects['column']} FROM {table} WHERE {objects['column']} = '{objects['value']}'""")
                        rows = self.__cursor.fetchone()[0]
                    except sqlite3.OperationalError as err:
                        console.print_exception()

                    if self.__debug:
                        time.sleep(0.5)
                        console.log(f"[DEBUG]: Getting the value {objects['value']} from column {objects['column']} in {table} table...")
                        time.sleep(0.5)
                        console.log(f"[DEBUG]: The value {objects['value']} was obtained successfully and saved in rows attribute.")
                        time.sleep(0.5)
                        console.log("[DEBUG]:", rows)

                    return rows
