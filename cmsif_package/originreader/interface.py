
import hashlib

class Interface:

    def fetch_file_contents(self, path: str):
        return NotImplemented

    def file_exists(self, path: str):
        return NotImplemented

    def get_file_hash(self, path: str):
        raw_contents = self.fetch_file_contents(path)

        if isinstance(raw_contents, bytes):
            return hashlib.md5(raw_contents).hexdigest()

        return hashlib.md5(raw_contents.encode('utf-8')).hexdigest()
