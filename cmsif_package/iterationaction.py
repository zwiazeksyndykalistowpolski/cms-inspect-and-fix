
import logging
import os

from .originreader.interface import Interface as OriginReaderInterface
from .originreader.dirreader import DirectoryReader
from .suspiciouschecker import SuspiciousChecker
from .decision import DecisionMaker


class IterationAction:
    pathToApplication = ""  # type: str
    fileList = {}           # type: hash
    logger = None           # type: logging.Logger
    appReader = None        # type: DirectoryReader
    mrSuspicious = None     # type: SuspiciousChecker
    decisionMaker = None    # type: DecisionMaker

    def __init__(self, path_to_application, logger):
        self.pathToApplication = path_to_application
        self.logger = logger
        self.mrSuspicious = SuspiciousChecker()
        self.decisionMaker = DecisionMaker(path_to_application=path_to_application, logger=logger)
        self.appReader = DirectoryReader(self.pathToApplication)
        self.fetch_file_list()

    def find_all_files(self):
        results = []
        for base, dirs, files in os.walk(self.pathToApplication):
            results.extend(os.path.join(base, f) for f in files)
        return results

    def fetch_file_list(self):
        base_path_len = len(self.pathToApplication)

        for filename in self.find_all_files():
            # add only relative paths
            relative_path = filename[base_path_len + 1:]

            if os.path.isdir(filename):
                continue

            self.fileList[relative_path] = {
                'path': relative_path,
                'sum': self.appReader.get_file_hash(relative_path)
            }

    def iterate(self, origin_reader: OriginReaderInterface):
        """
        :param origin_reader OriginReaderInterface
        """

        # iterate over application files and compare with origin
        # as we look for modifications, not for missing files
        for file_path, data in self.fileList.items():
            self.logger.info(' >> Checking ' + file_path + ', md5: ' + data['sum'])

            results = [
                self.compare_app_file_with_origin(origin_reader, file_path),
                self.check_if_file_is_not_suspected(file_path)
            ]

            self.decisionMaker.decide_about_file(
                file_path=file_path,
                results=results,
                origin_reader=origin_reader
            )

    def check_if_file_is_not_suspected(self, file_path: str):
        """ Uses a SuspiciousChecker service that compares files content with known patterns used by malware """

        is_suspected = self.mrSuspicious.is_file_containing_malicious_content(
            content=self.appReader.fetch_file_contents(file_path),
            file_name=file_path
        )

        if is_suspected:
            self.logger.error('!!! FILE at "' + file_path + '" is suspected to have a MALICIOUS CONTENT')

        return not is_suspected

    def compare_app_file_with_origin(self, origin_reader: OriginReaderInterface, file_path: str):
        """ Compares application files with source files eg. cms or backup files """

        if not origin_reader.file_exists(file_path):
            return

        checksum = origin_reader.get_file_hash(file_path)
        comparison = self.fileList[file_path]['sum']

        if checksum != comparison:
            self.logger.warning('Checksum does not match for ' + file_path + ', sum=' + checksum + ', app_sum=' + comparison)
            return False

        return True
