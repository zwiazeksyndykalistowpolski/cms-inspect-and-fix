
import glob
import logging
import os
import sys
import subprocess

from .originreader.interface import Interface as OriginReaderInterface
from .originreader.dirreader import DirectoryReader
from .suspiciouschecker import SuspiciousChecker


class IterationAction:
    pathToApplication = ""  # type: str
    fileList = {}           # type: hash
    logger = None           # type: logging.Logger
    appReader = None        # type: DirectoryReader
    mrSuspicious = None     # type: SuspiciousChecker

    def __init__(self, path_to_application, logger):
        self.pathToApplication = path_to_application
        self.logger = logger
        self.mrSuspicious = SuspiciousChecker()

        self.appReader = DirectoryReader(self.pathToApplication)
        self.fetch_file_list()

    def fetch_file_list(self):
        base_path_len = len(self.pathToApplication)

        for filename in glob.iglob(self.pathToApplication + '**/*', recursive=True):
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

            self.decide_about_file(
                file_path=file_path,
                results=results,
                origin_reader=origin_reader
            )

    def decide_about_file(self, file_path: str, results: list, origin_reader: OriginReaderInterface):
        """ Allows user to take an action """

        if len([x for x in results if x is False]) == 0:
            return

        answer = input("\n  >> !!! " + file_path + ": Action required. \n[p] Preview file \
                         \n[b] Restore from backup/origin \
                         \n[e] Edit \
                         \n[f] OK, its fine now, go to next file \
                         \n[c] Change ownership of a file to root:root to prevent file modifications \
                         \n[q] Interrupt\n\nWhat to do? ")

        if answer == 'f':
            return True

        elif answer == 'b':
            self.restore_from_backup(file_path, origin_reader)

        elif answer == 'q':
            sys.exit(0)

        elif answer == 'e':
            subprocess.call(['nano', self.pathToApplication + '/' + file_path])

        elif answer == "c":
            self.set_root_permissions(file_path)

        elif answer == 'p':
            self.preview_file(file_path)

        self.decide_about_file(file_path=file_path, results=results, origin_reader=origin_reader)

    def preview_file(self, file_path):
        """ Preview a file using Unix/Linux 'less' """
        os.system('less "' + self.pathToApplication + '/' + file_path + '"')

    def restore_from_backup(self, file_path: str, origin_reader: OriginReaderInterface):
        """ Restore a file from origin """

        if not origin_reader.file_exists(file_path):
            self.logger.warning('File "' + file_path + '" does not have a backup in the origin/backup!')
            return

        content = origin_reader.fetch_file_contents(file_path)
        self.logger.info('Restoring ' + str(len(content)) + ' bytes for "' + file_path + '"')

        handle = open(self.pathToApplication + '/' + file_path, 'w')
        handle.write(content)
        handle.close()

    def check_if_file_is_not_suspected(self, file_path: str):
        """ Uses a SuspiciousChecker service that compares files content with known patterns used by malware """

        is_suspected = self.mrSuspicious.is_file_containing_malicious_content(
            content=self.appReader.fetch_file_contents(file_path),
            file_name=file_path
        )

        if is_suspected:
            self.logger.error('!!! FILE at "' + file_path + '" is suspected to have a MALICIOUS CONTENT')

        return not is_suspected

    def set_root_permissions(self, file_path):
        """ Sets root user and root group as owner on the file to prevent file modifications by the malware
            that works on web server permissions """

        self.logger.info('Setting root:root permissions on a file "' + file_path + '"')
        os.system('sudo chown root:root "' + self.pathToApplication + '/' + file_path + '"')

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
