# -*- coding: utf-8 -*-

# gms_preprocessing, spatial and spectral homogenization of satellite remote sensing data
#
# Copyright (C) 2020  Daniel Scheffler (GFZ Potsdam, daniel.scheffler@gfz-potsdam.de)
#
# This software was developed within the context of the GeoMultiSens project funded
# by the German Federal Ministry of Education and Research
# (project grant code: 01 IS 14 010 A-C).
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
# Please note the following exception: `gms_preprocessing` depends on tqdm, which
# is distributed under the Mozilla Public Licence (MPL) v2.0 except for the files
# "tqdm/_tqdm.py", "setup.py", "README.rst", "MANIFEST.in" and ".gitignore".
# Details can be found here: https://github.com/tqdm/tqdm/blob/master/LICENCE.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = 'Daniel Scheffler'

import sys
import warnings
import logging
import os

from ..options.config import GMS_config as CFG

# try:
#     # noinspection PyCompatibility
#     from StringIO import StringIO  # Python 2
# except ImportError:
#     from io import StringIO  # Python 3


class GMS_logger(logging.Logger):
    def __init__(self, name_logfile, fmt_suffix=None, path_logfile=None, log_level='INFO', append=True,
                 log_to_joblog=True):
        # type: (str, any, str, any, bool, bool) -> None
        """Returns a logging.logger instance pointing to the given logfile path.
        :param name_logfile:
        :param fmt_suffix:      if given, it will be included into log formatter
        :param path_logfile:    if no path is given, only a StreamHandler is created
        :param log_level:       the logging level to be used (choices: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL';
                                default: 'INFO')
        :param append:          <bool> whether to append the log message to an existing logfile (1)
                                or to create a new logfile (0); default=1
        :param log_to_joblog:   whether to additionally log all messages to the logfile of the GMS job (default=1)
        """

        # private attributes
        self._captured_stream = ''

        # attributes that need to be present in order to unpickle the logger via __setstate_
        self.name_logfile = name_logfile
        self.fmt_suffix = fmt_suffix
        self.path_logfile = path_logfile
        self.log_level = log_level
        self.appendMode = append

        super(GMS_logger, self).__init__(name_logfile)

        self.path_logfile = path_logfile
        self.formatter_fileH = logging.Formatter('%(asctime)s' + (' [%s]' % fmt_suffix if fmt_suffix else '') +
                                                 ' %(levelname)s:   %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
        self.formatter_ConsoleH = logging.Formatter('%(asctime)s' + (' [%s]' % fmt_suffix if fmt_suffix else '') +
                                                    ':   %(message)s', datefmt='%Y/%m/%d %H:%M:%S')

        from ..misc.helper_functions import silentmkdir

        # set fileHandler
        if path_logfile:
            # create output directory
            silentmkdir(path_logfile)

            # create FileHandler
            fileHandler = logging.FileHandler(path_logfile, mode='a' if append else 'w')
            fileHandler.setFormatter(self.formatter_fileH)
            fileHandler.setLevel(log_level)
        else:
            fileHandler = None

        # set fileHandler for job logfile
        if log_to_joblog:
            job_logfile = os.path.join(CFG.path_job_logs, '%s.log' % CFG.ID)

            # create output directory
            silentmkdir(job_logfile)

            # create FileHandler
            joblog_Handler = logging.FileHandler(job_logfile, mode='a' if append else 'w')
            joblog_Handler.setFormatter(self.formatter_fileH)
            joblog_Handler.setLevel(log_level)

            # create SocketHandler
            # joblog_Handler = SocketHandler('localhost', DEFAULT_TCP_LOGGING_PORT)  # FIXME static host
            # joblog_Handler.setFormatter(self.formatter_fileH)
            # joblog_Handler.setLevel(log_level)

        else:
            joblog_Handler = None

        # create StreamHandler # TODO add a StringIO handler
        # self.streamObj     = StringIO()
        # self.streamHandler = logging.StreamHandler(stream=self.streamObj)
        # self.streamHandler.setFormatter(formatter)
        # self.streamHandler.set_name('StringIO handler')

        # create ConsoleHandler for logging levels DEGUG and INFO -> logging to sys.stdout
        consoleHandler_out = logging.StreamHandler(stream=sys.stdout)  # by default it would go to sys.stderr
        consoleHandler_out.setFormatter(self.formatter_ConsoleH)
        consoleHandler_out.set_name('console handler stdout')
        consoleHandler_out.setLevel(log_level)
        consoleHandler_out.addFilter(LessThanFilter(logging.WARNING))

        # create ConsoleHandler for logging levels WARNING, ERROR, CRITICAL -> logging to sys.stderr
        consoleHandler_err = logging.StreamHandler(stream=sys.stderr)
        consoleHandler_err.setFormatter(self.formatter_ConsoleH)
        consoleHandler_err.setLevel(logging.WARNING)
        consoleHandler_err.set_name('console handler stderr')

        self.setLevel(log_level)

        if not self.handlers:
            if fileHandler:
                self.addHandler(fileHandler)
            if joblog_Handler:
                self.addHandler(joblog_Handler)
            # self.addHandler(self.streamHandler)
            self.addHandler(consoleHandler_out)
            self.addHandler(consoleHandler_err)

    def __getstate__(self):
        self.close()
        return self.__dict__

    def __setstate__(self, ObjDict):
        """Defines how the attributes of GMS object are unpickled."""
        self.__init__(ObjDict['name_logfile'], fmt_suffix=ObjDict['fmt_suffix'], path_logfile=ObjDict['path_logfile'],
                      log_level=ObjDict['log_level'], append=True)
        ObjDict = self.__dict__
        return ObjDict

    @property
    def captured_stream(self):
        if not self._captured_stream:
            self._captured_stream = self.streamObj.getvalue()

        return self._captured_stream

    @captured_stream.setter
    def captured_stream(self, string):
        assert isinstance(string, str), "'captured_stream' can only be set to a string. Got %s." % type(string)
        self._captured_stream = string

    def close(self):
        # update captured_stream and flush stream
        # self.captured_stream += self.streamObj.getvalue()
        # print(self.handlers[:])

        # self.removeHandler(self.streamHandler)
        # print(dir(self.streamHandler))
        # self.streamHandler = None

        for handler in self.handlers[:]:
            if handler:
                try:
                    # if handler.get_name()=='StringIO handler':
                    # self.streamObj.flush()
                    # self.streamHandler.flush()
                    self.removeHandler(handler)  # if not called with '[:]' the StreamHandlers are left open
                    handler.flush()
                    handler.close()
                except PermissionError:
                    warnings.warn('Could not properly close logfile due to a PermissionError: %s' % sys.exc_info()[1])

        if self.handlers[:]:
            warnings.warn('Not all logging handlers could be closed. Remaining handlers: %s' % self.handlers[:])

            # print('sh', self.streamHandler)

    def view_logfile(self):
        with open(self.path_logfile) as inF:
            print(inF.read())

    def __del__(self):
        try:
            self.close()
        except ValueError as e:
            if str(e) == 'I/O operation on closed file':
                pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return True if exc_type is None else False


def close_logger(logger):
    if logger and hasattr(logger, 'handlers'):
        for handler in logger.handlers[:]:  # if not called with '[:]' the StreamHandlers are left open
            if handler:
                try:
                    logger.removeHandler(handler)
                    handler.flush()
                    handler.close()
                except PermissionError:
                    warnings.warn('Could not properly close logfile due to a PermissionError: %s' % sys.exc_info()[1])

        if logger.handlers[:]:
            warnings.warn('Not all logging handlers could be closed. Remaining handlers: %s' % logger.handlers[:])


def shutdown_loggers():
    logging.shutdown()


class LessThanFilter(logging.Filter):
    """Filter class to filter log messages by a maximum log level.

    Based on http://stackoverflow.com/questions/2302315/
        how-can-info-and-debug-logging-message-be-sent-to-stdout-and-higher-level-messag
    """
    def __init__(self, exclusive_maximum, name=""):
        """Get an instance of LessThanFilter.

        :param exclusive_maximum:  maximum log level, e.g., logger.WARNING
        :param name:
        """
        super(LessThanFilter, self).__init__(name)
        self.max_level = exclusive_maximum

    def filter(self, record):
        """Filter funtion.

        NOTE: Returns True if logging level of the given record is below the maximum log level.

        :param record:
        :return: bool
        """
        # non-zero return means we log this message
        return True if record.levelno < self.max_level else False
