
import os
from .interface import Interface
from .zipreader import ZipReader
from .tarreader import TarReader
from .dirreader import DirectoryReader
from cmsif_package.invalidargumentexception import InvalidArgumentException


class OriginReader(Interface):
    originPath = ""  # type: str
    chdir = ""       # type: str
    reader = None    # type: Interface

    def __init__(self, origin_path: str, chdir: str):
        self.originPath = origin_path
        self.chdir = chdir
        self.__create_proper_reader()

    def __create_proper_reader(self):
        """ Creates a reader that reads from zip/tar/directory """

        if self.originPath[-4:] == ".zip":
            self.reader = ZipReader(self.originPath, self.chdir)
            return

        elif self.originPath[-7:] == ".tar.gz" or self.originPath[:-8] == ".tar.bz2":
            self.reader = TarReader(self.originPath, self.chdir)
            return

        elif os.path.isdir(self.originPath):
            self.reader = DirectoryReader(self.originPath, self.chdir)
            return

        raise InvalidArgumentException('Origin path is not in a recognized format')

    def fetch_file_contents(self, path):
        return self.reader.fetch_file_contents(path)

    def get_file_hash(self, path):
        return self.reader.get_file_hash(path)

    def file_exists(self, path: str):
        return self.reader.file_exists(path)
