
import glob
import logging
from .originreader.dirreader import DirectoryReader

class IterationAction:
    pathToApplication = "" # type: str
    fileList = {}          # type: hash
    logger = None          # type: logging.Logger
    appReader = None       # type: DirectoryReader

    def __init__(self, path_to_application, logger):
        self.pathToApplication = path_to_application
        self.logger = logger

        self.appReader = DirectoryReader(self.pathToApplication)
        self.fetch_file_list()

    def fetch_file_list(self):
        base_path_len = len(self.pathToApplication)

        for filename in glob.iglob(self.pathToApplication + '**/*', recursive=True):
            # add only relative paths
            relative_path = filename[base_path_len + 1:]

            self.fileList[relative_path] = {
                'path': relative_path,
                'sum': self.appReader.get_file_hash(relative_path)
            }

    def iterate(self, origin_reader):
        """ """

        for file_path, data in self.fileList.items():
            self.logger.info(' >> ' + file_path + ', md5: ' + data['sum'])

