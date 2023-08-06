# Copyright © 2019-2020 Roel van der Goot
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""Module log provides logging infrastructure."""

from logging import DEBUG, FileHandler, Formatter, StreamHandler, getLogger
from os.path import join
from sys import stdout


class Log():
    """Log is the ajsonapi logger."""

    def __init__(self, file_path='', file_name=''):
        # pylint: disable=invalid-name
        self.logger = getLogger('ajsonapi')
        self.logger.setLevel(DEBUG)

        fm = Formatter(
            '[%(process)d][%(asctime)s.%(msecs)03d] '
            '%(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %T')
        sh = StreamHandler(stdout)
        sh.setLevel(DEBUG)
        sh.setFormatter(fm)
        self.logger.addHandler(sh)

        if file_name:
            fh = FileHandler(join(file_path, file_name))
            fh.setFormatter(fm)
            self.logger.addHandler(fh)

    def debug(self, msg, *args):
        """Log a message at the debug log level."""
        self.logger.debug(msg, *args)

    def info(self, msg, *args):
        """Log a message at the info log level."""
        self.logger.info(msg, *args)

    def warning(self, msg, *args):
        """Log a message at the warning log level."""
        self.logger.warning(msg, *args)

    def error(self, msg, *args):
        """Log a message at the error log level."""
        self.logger.error(msg, *args)

    def critical(self, msg, *args):
        """Log a message at the critical log level."""
        self.logger.critical(msg, *args)


log = Log()  # pylint: disable=invalid-name
