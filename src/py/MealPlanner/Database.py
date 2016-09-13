# -*- coding: utf-8 -*-
"""
Created on Mon Aug 01 09:11:52 2016

@author: mike
"""

import json
import re
import os


class DatabaseMixin(object):

    """ Generic database methods based on a directory database"""

    def __init__(self, database_directory):
        self.database = database_directory
        self.database_length = self._get_length()

    def __str__(self):
        pass

    def __repr__(self):
        pass


    def _get_length(self):
        return len(os.listdir(self.database))



    def _write_entry(self, fname, entry):

        """ Write .json to directory"""

        json_entry = json.dumps(entry, indent=4)
        new_file = self.database + "/" + fname
        with open(new_file, "w") as file_open:
            file_open.write(json_entry)

        self.database_length = self._get_length()
        print fname, "written to ", new_file


    def _find_entry(self, *args):

        """ Returns list of matched files in a
        directory by index (int) or keyword (str)
        """

        args = args[0]
        results = []
        entries = os.listdir(self.database)

        if isinstance(args, str):
            for f in entries:
                if re.search(args, f):
                    results.append(f)
        elif isinstance(args, int)and args < self.database_length:
            results.append(entries[args])
        else:
            pass

        return results


    def _read_entry(self, fname):

        """ takes string of file name and returns
         contents of .json from a directory
        """

        if ".json" in fname:
            with open(self.database + "/" + fname) as entry:
                loaded = json.load(entry)
        else:
            loaded = "file is not .json"

        return loaded


    def _delete_entry(self, fname):

        """ Deletes file from directory """

        os.remove(self.database + "/" + fname)
        print "deleted " + fname


    def _edit_entry(self, fname, method_to_run):

        """ Edit a file by copying its original contents,
        modifiying it, deleting the file then save the
        modified version as the old file name.
        """

        entry = self._read_entry(fname)

        new_entry = method_to_run(entry)

        self._delete_entry(fname)
        self._write_entry(fname, new_entry)

