#!/usr/bin/env python

import argparse
import sys
import os

t = sys.argv[0].replace(os.path.basename(sys.argv[0]), "") + "/../"

if os.path.isdir(t):
    sys.path.append(t)

from cmsif_package import Application
from cmsif_package.invalidargumentexception import InvalidArgumentException

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--origin', help='An origin tarball/zipball path', default='')
    parser.add_argument('--application', help='Application path, defaults to current directory', default='./')
    parsed = parser.parse_args()

    app = Application(
        origin_path=parsed.origin,
        app_path=parsed.application
    )

    try:
        app.main()
    except InvalidArgumentException as e:
        print(e)
        sys.exit(1)
