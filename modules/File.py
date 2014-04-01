###################################################################################
# @file File.py
# @author Keidan
# @date 01/04/2014
# @par Project
# gtkhex
# @par Copyright
# Copyright 2014 Keidan, all right reserved
# This software is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY.
# 
# Licence summary : 
#    You can modify and redistribute the sources code and binaries.
#    You can send me the bug-fix
# Term of the licence in in the file licence.txt.
#
###################################################################################

class File:
    def __init__(self, filename=None):
        self.filename = filename
        self.data = None

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def set_filename(self, filename):
        self.filename = filename

    def get_filename(self):
        return self.filename

    def get_simple_name(self):
        if not self.filename:
            return "Untitled"
        index = self.filename.replace("\\","/").rfind("/") + 1
        return self.filename[index:]

    def read(self):
        file = open(self.filename, "r")
        self.data = file.read()
        file.close()

    def write(self):
        file = open(self.filename, "w+")
        file.write(self.data)
        file.close()
