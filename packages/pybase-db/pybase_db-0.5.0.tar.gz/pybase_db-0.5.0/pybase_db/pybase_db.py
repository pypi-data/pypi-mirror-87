#       NTBBloodbath | PyBase v0.4.0       #
############################################
# PyBase is distributed under MIT License. #

# dependencies (packages/modules)
import os
import yaml
import json
import pickle
import pathlib
from rich.console import Console
from rich.traceback import install
install() # Use Rich traceback handler as the default error handler

console = Console()

class PyBase:
    """
    PyBase Main Class

    ...

    Attributes
    ----------

    Methods
    -------
    delete(obj)
        Delete a object from the database established in PyBase init.
    exists(database: str, db_type: str)
        Fetch if the given database exists.
    fetch(obj: str, sub=None)
        Fetch an object and its sub_objects inside the database established in PyBase init.
    insert(content: dict)
        Insert a dictionary content inside the given database file.
    get(key: str=None)
        Read the database file established in PyBase init to to access its objects.
    has(key: str=None)
        Read the database file established in PyBase init to to check availability of its objects.
            
    TODO:
        Add more useful methods.
    """
    def __init__(self,
                 database: str,
                 db_type: str,
                 db_path: str = pathlib.Path().absolute()):
        """
        Define the database to use and create it if it doesn't exist.

        ...

        Parameters
        ----------
        database : str
            The name of the database without extension.
        db_type : str
            The database type.
            Available types: yaml, json, bytes
            Note: To use SQLite3, use the PySQL module.
        db_path : str
            The path where the database is located (default is current working directory).
            Example: /home/bloodbath/Desktop/PyBase

        Raises
        ------
        TypeError
            If database or db_type isn't a String.
        ValueError
            If the given db_type isn't a valid type (JSON, YAML, Bytes).
        FileNotFoundError
            If the given path wasn't found.
        """

        self.__path = db_path  # private path variable to clean code.

        if type(database) != str:
            raise TypeError('database must be a String.')
        elif type(db_type) != str:
            raise TypeError('db_type must be a String.')
        elif os.path.exists(db_path) != True:
            raise FileNotFoundError(
                f'The path ({self.__path}) wasn\'t found. Please check that the path exists.'
            )
        elif type(db_type) == str:
            self.__EXTENSION = '.' + db_type.lower()
            self.__DB = (f'{self.__path}/{database}{self.__EXTENSION}')
            if db_type.lower() == 'json':
                if os.path.exists(self.__DB) == False:
                    try:
                        with open(self.__DB, mode='w+',
                                  encoding='utf-8') as json_file:
                            json.dump({}, json_file)
                    except Exception as err:
                        console.print_exception()
            elif db_type.lower() == 'yaml':
                if os.path.exists(self.__DB) == False:
                    try:
                        with open(self.__DB, mode='w+',
                                  encoding='utf-8') as yaml_file:
                            yaml.dump({}, yaml_file)
                    except Exception as err:
                        console.print_exception()
            elif db_type.lower() == "bytes":
                if not os.path.exists(self.__DB):
                    try:
                        with open(self.__DB, mode="wb") as bytes_file:
                            pickle.dump({}, bytes_file)
                    except Exception as err:
                        console.print_exception()
            else:
                raise ValueError('db_type must be JSON, YAML or Bytes.')

    def delete(self, obj):
        """
        Delete a object from the database established in PyBase init.

        ...
        
        Parameters
        ----------
        obj
            The object which will be deleted from the database.

        Raises
        ------
        KeyError
            If key isn't found.
        ValueError
            If obj doesn't have a value (is equal to zero or None).
        """

        if len(obj) == 0 or obj is None:
            raise ValueError('obj must have a value (str, int, float, bool).')
        else:
            if self.__EXTENSION == '.json':
                try:
                    with open(self.__DB, encoding='utf-8') as json_file:
                        data = json.load(
                            json_file)  # Pass JSON to Python objects.
                        data.pop(obj)  # Delete the given object.
                    with open(self.__DB, mode='w',
                              encoding='utf-8') as json_file:
                        json.dump(data, json_file, indent=4,
                                  sort_keys=True)  # Save
                except KeyError as err:
                    console.print_exception()
            elif self.__EXTENSION == '.yaml':
                try:
                    with open(self.__DB, encoding='utf-8') as yaml_file:
                        data = yaml.load(yaml_file, Loader=yaml.FullLoader)
                        data.pop(obj)
                    with open(self.__DB, mode='w',
                              encoding='utf-8') as yaml_file:
                        yaml.dump(data, yaml_file, sort_keys=True)
                except KeyError as err:
                    console.print_exception()
            elif self.__EXTENSION == '.bytes':
                try:
                    with open(self.__DB, mode="rb") as bytes_file:
                        data = pickle.load(bytes_file)
                        data.pop(obj)
                    with open(self.__DB, mode="wb") as bytes_file:
                        pickle.dump(data, bytes_file)
                except KeyError as err:
                    console.print_exception()

    def exists(self, database: str, db_path: str = pathlib.Path().absolute()):
        """
        Fetch if the given database exists.

        ...

        Parameters
        ----------
        database : str
            The name of the database with extension.

        db_path : str
           The path where the database is located (default is current working directory).
           Example: /home/bloodbath/Desktop/PyBase

        Raises
        ------
        TypeError
            If database or db_path isn't a String.

        Returns
        -------
        bool
            Returns True or False depending on if the database given exists in the given path.
        """

        if type(database) != str:
            raise TypeError('database must be a String.')
        elif type(db_path) != str:
            raise TypeError('db_path must be a String.')
        else:
            if os.path.exists(f'{db_path}/{database}'):
                return True
            else:
                return False

    def fetch(self, obj: str, sub: dict = None):
        """
        Fetch an object and its sub_objects inside the database established in PyBase init.

        ...

        Parameters
        ----------
        obj : str
            The object which will be fetched inside the database.
        sub : dict, optional
            The sub_object(s) of the object which will be fetched inside the database.

        Raises
        ------
        TypeError
            If obj isn't a String or if sub isn't a list.
        ValueError
            If sub have more than 5 objects inside.
        KeyError
            If sub doesn't exist in the database.

        Returns
        -------
        str
            If the object or sub_objects are a String.
        int
            If the object or sub_objects are a Integer.
        float
            If the object or sub_objects are a Float.
        bool
            If the object or sub_objects are a Boolean.

        TODO:
            Add support for more objects inside the lists.
        """
        if type(obj) != str:
            raise TypeError('obj must be a String.')
        elif sub != None and type(sub) != dict:
            raise TypeError('sub must be a dict.')
        elif sub != None and len(sub) > 5:
            raise ValueError('sub can\'t have more than 5 objects inside.')
        else:
            obj = dict({obj: sub}) if sub != None and len(sub) >= 1 else {
                obj: ''
            }
            if self.__EXTENSION == '.json':
                with open(self.__DB, mode='r', encoding='utf-8') as json_file:
                    data = json.load(json_file)
                    for key in list(obj):
                        if key in data and sub != None and len(sub) != 0:
                            try:
                                # Establish the maximum deep of the fetch to 5 objects.
                                if len(sub) == 1 and list(
                                        sub)[0] in data[key].keys():
                                    return type(data[key][list(sub)[0]])
                                elif len(sub) == 2 and list(
                                        sub)[1] in data[key].keys():
                                    return type(data[key][list(sub)[1]])
                                elif len(sub) == 3 and list(
                                        sub)[2] in data[key].keys():
                                    return type(data[key][list(sub)[2]])
                                elif len(sub) == 4 and list(
                                        sub)[3] in data[key].keys():
                                    return type(data[key][list(sub)[3]])
                                elif len(sub) == 5 and list(
                                        sub)[4] in data[key].keys():
                                    return type(data[key][list(sub)[4]])
                            except KeyError as err:
                                console.print_exception()
                        else:
                            try:
                                return type(data[key])
                            except KeyError as e:
                                console.print_exception()
            elif self.__EXTENSION == '.yaml':
                with open(self.__DB, mode='r', encoding='utf-8') as yaml_file:
                    data = yaml.load(yaml_file, Loader=yaml.FullLoader)
                    for key in list(obj):
                        if key in data and sub != None and len(sub) != 0:
                            try:
                                # Establish the maximum deep of the fetch to 5 objects.
                                if len(sub) == 1 and list(
                                        sub)[0] in data[key].keys():
                                    return type(data[key][list(sub)[0]])
                                elif len(sub) == 2 and list(
                                        sub)[1] in data[key].keys():
                                    return type(data[key][list(sub)[1]])
                                elif len(sub) == 3 and list(
                                        sub)[2] in data[key].keys():
                                    return type(data[key][list(sub)[2]])
                                elif len(sub) == 4 and list(
                                        sub)[3] in data[key].keys():
                                    return type(data[key][list(sub)[3]])
                                elif len(sub) == 5 and list(
                                        sub)[4] in data[key].keys():
                                    return type(data[key][list(sub)[4]])
                            except KeyError as err:
                                console.print_exception()
                        else:
                            try:
                                return type(data[key])
                            except KeyError as e:
                                console.print_exception()
            elif self.__EXTENSION == '.bytes':
                with open(self.__DB, mode='rb') as bytes_file:
                    data = pickle.load(bytes_file)
                    for key in list(obj):
                        if key in data and sub != None and len(sub) != 0:
                            try:
                                # Establish the maximum deep of the fetch to 5 objects.
                                if len(sub) == 1 and list(
                                        sub)[0] in data[key].keys():
                                    return type(data[key][list(sub)[0]])
                                elif len(sub) == 2 and list(
                                        sub)[1] in data[key].keys():
                                    return type(data[key][list(sub)[1]])
                                elif len(sub) == 3 and list(
                                        sub)[2] in data[key].keys():
                                    return type(data[key][list(sub)[2]])
                                elif len(sub) == 4 and list(
                                        sub)[3] in data[key].keys():
                                    return type(data[key][list(sub)[3]])
                                elif len(sub) == 5 and list(
                                        sub)[4] in data[key].keys():
                                    return type(data[key][list(sub)[4]])
                            except KeyError as err:
                                console.print_exception()
                        else:
                            try:
                                return type(data[key])
                            except KeyError as err:
                                console.print_exception()
            
    def insert(self, content: dict):
        """
        Insert a dictionary content inside the database file established in PyBase init.
        
        ...

        Parameters
        ----------
        content : dict
            The content which will be inserted inside the database.
            
        Raises
        ------
        TypeError
            If content isn't a dictionary.
        """

        if type(content) != dict:
            raise TypeError('content must be a dictionary.')
        else:
            if self.__EXTENSION == '.json':
                try:
                    with open(self.__DB, encoding='utf-8') as json_file:
                        data = json.load(json_file)
                        data.append(content)
                    with open(self.__DB, mode='w',
                              encoding='utf-8') as json_file:
                        json.dump(data, json_file, indent=4, sort_keys=True)
                except Exception as err:
                    console.print_exception()
            elif self.__EXTENSION == '.yaml':
                try:
                    with open(self.__DB, encoding='utf-8') as yaml_file:
                        data = yaml.load(yaml_file, Loader=yaml.FullLoader)
                        data.update(content)
                    with open(self.__DB, mode='w',
                              encoding='utf-8') as yaml_file:
                        yaml.dump(data, yaml_file, sort_keys=True)
                except Exception as err:
                    console.print_exception()

            elif self.__EXTENSION == '.bytes':
                try:
                    with open(self.__DB, mode="rb") as bytes_file:
                        data = pickle.load(bytes_file) or {}
                        data.update(content)
                    with open(self.__DB, mode='wb') as bytes_file:
                        pickle.dump(data, bytes_file)
                except Exception as err:
                    console.print_exception()

    def get(self, key: str = None):

        """
        Read the database file established in PyBase init to access its objects or values ​​using the key.

        ...

        Parameters
        ----------
        key : str
            The key of the first value of the dictionary
            Default: None

        Raises
        ------
        KeyError
            When the key does not exist in the specified file type

        Returns
        -------
        dict 
            A dictionary which contains all the database objects.
        """
        try:
            if self.__EXTENSION == ".json":
                if key is None:
                    with open(self.__DB, mode="r+", encoding="utf-8") as json_file:
                        data = json.load(json_file) or {}
                        self.__close_file_delete(json_file)
                        return data
                else:
                    with open(self.__DB, mode="r+", encoding="utf-8") as json_file:
                        data = json.load(json_file) or {}
                        self.__close_file_delete(json_file)
                        if self.__util_split(key, data): return self.__util_split(key, data)
                        else:
                            raise KeyError(f"\"{key}\" Does not exist in the file")
            elif self.__EXTENSION == ".yaml":
                if key is None:
                    with open(self.__DB, mode='r+', encoding='utf-8') as yaml_file:
                        data = yaml.load(yaml_file, Loader=yaml.FullLoader) or {}
                        self.__close_file_delete(yaml_file)
                        return data
                else:
                    with open(self.__DB, mode='r+', encoding='utf-8') as yaml_file:
                        data = yaml.load(yaml_file, Loader=yaml.FullLoader) or {}
                        self.__close_file_delete(yaml_file)
                        if self.__util_split(key, data): return self.__util_split(key, data)
                        else:
                            raise KeyError(f"\"{key}\" Does not exist in the file")
            elif self.__EXTENSION == ".bytes":
                if key is None:
                    with open(self.__DB, mode="rb") as bytes_file:
                        data = pickle.load(bytes_file)
                        self.__close_file_delete(bytes_file)
                        return data
                else:        
                    with open(self.__DB, mode='rb') as bytes_file:
                        data = pickle.load(bytes_file) or {}
                        self.__close_file_delete(bytes_file)
                        if self.__util_split(key, data): return self.__util_split(key, data)
                        else:
                            raise KeyError(f"\"{key}\" Does not exist in the file")
        except Exception as err:
            console.print_exception()
    
    def has(self, key: str = None):
        
        """
        Read the database file established in PyBase init to check availability of its objects or values ••using the key.

        ...
        Parameters
        ----------
        key : str
            The key of the first value of the dictionary
            Default: None

        Returns
        -------
        bool 
            A value that indicates whether the data is found or not
        """

        try:
            self.get(key)
            return True
        except Exception as err:
            return False
    
    def __close_file_delete(self, file):
        """   
        Method only for the class, close the open file and erase it from memory (slightly better performance)
        ...

        Parameters
        ----------
        file
            an open (or closed) file

        Raises
        ------
        """
        try:
            close_file = file.close()
            if close_file is None:
                del (file)
        except Exception as err:
            console.print_exception()

    def __util_split(self, key: str, data: dict):
        """
        Method only for the class, split dict from key specific
        ...

        Parameters
        ----------
        key : str
            The key of the dictionary
        data : dict
            The content.

        Raises
        ------
        TypeError
            key is not a str or data is not a dict

        """
        if type(key) != str:
            raise TypeError(f"the type of {key} is invalid.")
        elif type(data) != dict:
            raise TypeError(f'data "{data}" must be a dictionary.')

        args = key.split(".")
        dataObject = data
        for keys in args:
            if not keys in dataObject.keys(): return False
            if keys == args[len(args) - 1]: return dataObject[keys]
            else: dataObject = dataObject[keys]
