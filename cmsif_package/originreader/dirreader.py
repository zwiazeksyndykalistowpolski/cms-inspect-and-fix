
import os
from .interface import Interface


class DirectoryReader(Interface):
    path = ""
    chdir = ""

    def __init__(self, path, chdir = ''):
        self.directory = path
        self.chdir = chdir

    def file_exists(self, path: str):
        return os.path.isfile(self.directory + '/' + self.chdir + path)

    def fetch_file_contents(self, path):
        if not self.file_exists(path):
            raise FileNotFoundError('Cannot find file "' + path + '"')

        try:
            handle = open(self.directory + '/' + self.chdir + path, 'r')
            content = handle.read()
            handle.close()
        except UnicodeDecodeError:
            content = ""

        return content
