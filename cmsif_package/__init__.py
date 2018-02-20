
import logging
import sys
import os

from .coloredformatter import ColoredFormatter
from .iterationaction import IterationAction
from .invalidargumentexception import InvalidArgumentException
from .originreader import OriginReader


class Application:
    pathToOrigin = ""         # type: str
    chdir = ""                # type: str
    pathToApplication = ""    # type: str
    originReader = None       # type: OriginReader
    logger = None             # type: logging.Logger

    def __init__(self, origin_path: str, app_path: str, chdir: str):
        self.pathToOrigin = origin_path
        self.pathToApplication = app_path
        self.chdir = chdir

        self.setup_logger()

    def setup_logger(self):
        """ Constructs the logger """

        self.logger = logging.getLogger('cmsif')
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = ColoredFormatter("[%(asctime)s][%(name)s][%(levelname)s]: %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def validate(self):
        """ Validates user typed arguments and raises an exception that is catchable at upper level """

        if not os.path.isdir(self.pathToApplication):
            raise InvalidArgumentException('Path to application is invalid')

        if not os.path.exists(self.pathToOrigin):
            raise InvalidArgumentException('Origin tarball/zipball/directory does not exists, please provide an ' +
                                           'archived backup or cms original files')

    def setup_origin_reader(self):
        """ Creates an instance of a origin reader """

        self.originReader = OriginReader(
            origin_path=self.pathToOrigin,
            chdir=self.chdir
        )

    def main(self):
        self.validate()
        self.setup_origin_reader()

        action = IterationAction(
            path_to_application=self.pathToApplication,
            logger=self.logger
        )

        action.iterate(origin_reader=self.originReader)
