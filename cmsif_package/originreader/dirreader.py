
from .interface import Interface


class DirectoryReader(Interface):
    path = ""

    def __init__(self, path):
        self.directory = path
