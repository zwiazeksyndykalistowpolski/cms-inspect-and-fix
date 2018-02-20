
from zipfile import ZipFile
from .interface import Interface


class ZipReader(Interface):
    path = ""
    reader = None    # type: ZipFile
    chdir = ''

    def __init__(self, origin_path: str, chdir = ''):
        self.path = origin_path
        self.reader = ZipFile(self.path, 'r')
        self.chdir = chdir

    def file_exists(self, path: str):
        return any(x.startswith("%s" % self.chdir + path.rstrip("/")) for x in self.reader.namelist())

    def fetch_file_contents(self, path: str):
        return self.reader.read(self.chdir + path).decode('utf-8')
