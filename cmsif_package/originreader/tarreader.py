
from tarfile import TarFile
from .interface import Interface

class TarReader(Interface):
    """ """

    def __init__(self, origin_path: str, chdir = ''):
        self.path = origin_path
        self.reader = TarFile(self.path, 'r')
        self.chdir = chdir

    def file_exists(self, path: str):
        return any(x.startswith("%s" % self.chdir + path.rstrip("/")) for x in self.reader.getnames())

    def fetch_file_contents(self, path: str):
        return self.reader.rea(self.chdir + path).decode('utf-8')
