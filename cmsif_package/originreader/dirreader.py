
import os
from .interface import Interface


class DirectoryReader(Interface):
    path = ""

    def __init__(self, path):
        self.directory = path

    def fetch_file_contents(self, path):
        if not os.path.isfile(self.directory + '/' + path):
            return ""

        handle = open(self.directory + '/' + path, 'r')
        content = handle.read()
        handle.close()

        return content
