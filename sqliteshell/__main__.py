#  Barrowcroft, 2024

#  A simple SQLite shell.

NAME = "SQLiteShell"
VERSION ="v.1.0.0"
DATE ="2024"

import os
import subprocess
import sys

from cli.commandline import CLI  # Command line interface.
from clp.commandprocessor import CLP  # Command line processor.
from sqli.sqli import SQLI  # SQLite interface.


class SQLITESHELL:
    def __init__(self)-> None:
        """__init__

        Initialises the SQLiteSHell.

        """
        #  Initialise the SQLite interface.

        self.sqli:SQLI = SQLI()

        #  Initialise the command line processor, and add commands to the list of recognised commands.

        self.clp: CLP = CLP()
        self.clp.add("close", "Closes the current database.", self.close, [])
        self.clp.add("create", "Create and opens a database.", self.create, [("database","The name of the database to create.")])
        self.clp.add("describe", "Describes a table, view, index or trigger.", self.sqli.describe, [("name","The name of the item to describe.")])
        self.clp.add("edit", "Edit a file / script.", self.edit,  [("filename","The name of the file / script to edit.")])
        self.clp.add("exit", "Exits the program.", self.exit, [])
        self.clp.add("help", "Shows this list of recognisable commands.", self.help, [])
        self.clp.add("indices", "Prints a list of indices in the database.", self.sqli.indices, [])
        self.clp.add("open", "Opens a database.", self.open, [("database","The name of the database to open.")])
        self.clp.add("schema", "Prints the database schema.", self.sqli.schema, [])
        self.clp.add("script", "Runs a query from a script file.", self.sqli.script, [("filename","The name of the file containing the query to execute."),("[...]","Parameters as required by the script.")], True)
        self.clp.add("tables", "Prints a list of tables in the database.", self.sqli.tables, [])
        self.clp.add("triggers", "Prints a list of triggers in the database.", self.sqli.triggers, [])
        self.clp.add("views", "Prints a list of views in the database.", self.sqli.views, [])

       #  Initialise the command line interface.

        self.cli: CLI = CLI(self.clp.parse, self.sqli.execute,header=f"{NAME}, {VERSION}, {DATE}.",instructions="Enter '.help' for a list of commands.",trailer="Thank you for using SQLiteShell.")

    def start(self)-> None:
        """start

        Starts the command line interface.

        """
        self.cli.start()

    def exit(self, _: dict[str, str]) -> None:
        """exit

        Exits the program.

        Args:
            _ (dict[str, str]): ignored!
        """
        self.cli.stop()


    def help(self, _: dict[str, str]) -> None:
        """help

        Prints a list of recognised commands.

        Args:
            _ (dict[str, str]): ignored!
        """
        self.clp.list()


    def create(self, parms: dict[str, str]) -> None:
        """create

        Creates a new database using the sqli interface, and updates the cli prompt.

        Args:
            parms (dict[str, str]): paramters
                "database" = name of database to create.
        """
        if self.sqli.create(parms["database"]):
            self.cli.set_prompt(f"{parms["database"]} >")


    def open(self, parms: dict[str, str]) -> None:
        """open

        OPens a database using the sqli interface, and updates the cli prompt.

        Args:
            parms (dict[str, str]): paramters
                "database" = name of database to open.
        """
        if self.sqli.open(parms["database"]):
            self.cli.set_prompt(f"{parms["database"]} >")


    def close(self, _: dict[str, str]) -> None:
        """close

        Closes a database using the sqli interface, and updates the cli prompt.

        Args:
            parms (dict[str, str]): ignored!
        """
        if self.sqli.close():
            self.cli.set_prompt(">")

    def edit(self, parms: dict[str, str]) -> None:
        """
        Opens the default text editor for the specified file.

        Args:
            parms (dict[str, str]): paramters
                "filename" = name of database to open.
        """
        _filename = parms["filename"]
        
        # Create an empty file if it doesn't exist

        if not os.path.exists(_filename):
            with open(_filename, 'w') as _:
                pass

        #  Start editor.
            
        try:
            if sys.platform.startswith('win'):
                # Windows
                os.system(f'start {_filename}')
            elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
                # Linux or macOS
                subprocess.Popen(['xdg-open', _filename])
            else:
                print(f"Unsupported platform: {sys.platform}")
        except Exception as e:
            print(f"Error - could not open editor - {e}")


def main()-> None:
    """main

    Creates and starts the sqlite shell.
    
    """
    sqliteshell: SQLITESHELL = SQLITESHELL()
    sqliteshell.start()

if __name__ == "__main__":
    main()

