
import sys
import os
import logging
import subprocess
from .originreader.interface import Interface as OriginReaderInterface


class DecisionMaker:
    pathToApplication = ""  # type: str
    logger = None           # type: logging.Logger

    def __init__(self, path_to_application: str, logger: logging.Logger):
        self.pathToApplication = path_to_application
        self.logger = logger

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

    def set_root_permissions(self, file_path):
        """ Sets root user and root group as owner on the file to prevent file modifications by the malware
            that works on web server permissions """

        self.logger.info('Setting root:root permissions on a file "' + file_path + '"')
        os.system('sudo chown root:root "' + self.pathToApplication + '/' + file_path + '"')