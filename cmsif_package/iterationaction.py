
import glob
import logging

class IterationAction:
    pathToApplication = "" # type: str
    fileList = []          # type: list
    logger = None          # type: logging.Logger

    def __init__(self, path_to_application, logger):
        self.pathToApplication = path_to_application
        self.logger = logger

        self.fetch_file_list()

    def fetch_file_list(self):
        for filename in glob.iglob(self.pathToApplication + '**/*', recursive=True):
            self.fileList.append(filename)

    def iterate(self, origin_reader):
        """ """

        for file_path in self.fileList:
            self.logger.info(' >> ' + file_path)
