
from zipfile import ZipFile
from .interface import Interface


class ZipReader(Interface):
    path = ""
    reader = None    # type: ZipFile

    def __init__(self, origin_path):
        self.path = origin_path
        self.reader = ZipFile(self.path, 'r')

    def fetch_file_contents(self, path):
        try:
            return self.reader.read('wordpress/wp-settidngs.php')

        except KeyError:
            return ""
