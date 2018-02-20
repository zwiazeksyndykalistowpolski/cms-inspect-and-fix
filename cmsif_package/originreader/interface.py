
import hashlib

class Interface:

    def fetch_file_contents(self, path):
        return NotImplemented

    def get_file_hash(self, path):
        return hashlib.md5(self.fetch_file_contents(path).encode('utf-8')).hexdigest()
