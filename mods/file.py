###################################################################################
# @file file.py
# @author Keidan (Kevin Billonneau)
# @par Copyright GNU GENERAL PUBLIC LICENSE Version 3
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
            return 'Untitled'
        index = self.filename.replace('\\', '/').rfind('/') + 1
        return self.filename[index:]

    def read(self):
        file = open(self.filename, 'rb')
        self.data = file.read()
        file.close()

    def write(self):
        file = open(self.filename, 'wb+')
        file.write(self.data)
        file.close()
