################################################################################
#                                                                              #
#  This file is part of DeltaPD.                                               #
#                                                                              #
#  DeltaPD is free software: you can redistribute it and/or modify             #
#  it under the terms of the GNU Affero General Public License as published by #
#  the Free Software Foundation, either version 3 of the License, or           #
#  (at your option) any later version.                                         #
#                                                                              #
#  DeltaPD is distributed in the hope that it will be useful,                  #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
#  GNU Affero General Public License for more details.                         #
#                                                                              #
#  You should have received a copy of the GNU Affero General Public License    #
#  along with DeltaPD.  If not, see <https://www.gnu.org/licenses/>.           #
#                                                                              #
################################################################################

import logging
import ntpath
import os
import re
import sys

from deltapd.common import assert_path_exists


def supports_colour():
    """Check that the current terminal supports colour.

    Returns
    -------
    bool
        True if the terminal supports colour, False otherwise.

    References
    ----------
        https://github.com/django/django/blob/master/django/core/management/color.py

    """
    supported_platform = sys.platform != 'win32' or 'ANSICON' in os.environ
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    return supported_platform and is_a_tty


def colour(to_fmt, attr=None, fg=None, bg=None):
    """Format a string using ANSI colour encoding, if the terminal supports it.

    Parameters
    ----------
    to_fmt : str
        The string to be formatted.
    attr : list
        A list of attributes to be applied.
    fg : str
        The foreground colour to apply.
    bg : str
        The background colour to apply.

    Returns
    -------
    str
        A string formatted according to the specifications.
    """
    if not supports_colour():
        return to_fmt
    else:
        options_attr = {'reset': 0, 'bright': 1, 'dim': 2, 'underscore': 4,
                        'blink': 5, 'reverse': 7, 'hidden': 8}
        options_col = {'black': 0, 'red': 1, 'green': 2, 'yellow': 3, 'blue': 4,
                       'magenta': 5, 'cyan': 6, 'white': 7}
        options = list() if not attr else [str(options_attr[x]) for x in attr]
        if fg:
            options.append(str(30 + options_col[fg]))
        if bg:
            options.append(str(40 + options_col[bg]))
        return '\x1b[{}m{}\x1b[0m'.format(';'.join(options), to_fmt)


def logger_setup(log_dir, log_file, program_name, version, silent, debug=False):
    """Setup loggers.

    Two logger are setup which both print to the stdout and a
    log file when the log_dir is not None. The first logger is
    named 'timestamp' and provides a timestamp with each call,
    while the other is named 'no_timestamp' and does not prepend
    any information. The attribution 'is_silent' is also added
    to each logger to indicate if the silent flag is thrown.

    Parameters
    ----------
    log_dir : str
        Output directory for log file.
    log_file : str
        Desired name of log file.
    program_name : str
        Name of program.
    version : str
        Program version number.
    silent : bool
        Flag indicating if output to stdout should be suppressed.
    debug : bool
        True if debug messages should be displayed, False otherwise.
    """

    class SpecialFormatter(logging.Formatter):
        """Terminal output rules"""
        ts_i = colour('[%(asctime)s]', ['bright'], 'blue')
        lvl_i = colour('INFO:', ['bright'], 'blue')

        ts_d = colour('[%(asctime)s]', ['bright'], 'green')
        lvl_d = colour('DEBUG:', ['bright'], 'green')

        ts_w = colour('[%(asctime)s]', ['bright'], 'yellow')
        lvl_w = colour('WARN:', ['bright'], 'yellow')

        ts_e = colour('[%(asctime)s]', ['bright'], 'red')
        lvl_e = colour('ERROR:', ['bright'], 'red')

        msg = '%(message)s'

        default_fmt = logging.Formatter(fmt=f'{ts_i} {lvl_i} {msg}',
                                        datefmt="%Y-%m-%d %H:%M:%S")
        debug_fmt = logging.Formatter(fmt=f'{ts_d} {lvl_d} {msg}',
                                      datefmt="%Y-%m-%d %H:%M:%S")
        info_fmt = logging.Formatter(fmt=f'{ts_i} {lvl_i} {msg}',
                                     datefmt="%Y-%m-%d %H:%M:%S")
        warn_fmt = logging.Formatter(fmt=f'{ts_w} {lvl_w} {msg}',
                                     datefmt="%Y-%m-%d %H:%M:%S")
        err_fmt = logging.Formatter(fmt=f'{ts_e} {lvl_e} {msg}',
                                    datefmt="%Y-%m-%d %H:%M:%S")

        def format(self, record):
            if record.levelno >= logging.ERROR:
                return self.err_fmt.format(record)
            elif record.levelno >= logging.WARNING:
                return self.warn_fmt.format(record)
            elif record.levelno >= logging.INFO:
                return self.info_fmt.format(record)
            elif record.levelno >= logging.DEBUG:
                return self.debug_fmt.format(record)
            else:
                return self.default_fmt.format(record)

    class ColourlessFormatter(SpecialFormatter):
        """Log file output rules (removes all colour characters)."""
        ansi_escape = re.compile(r'\x1b[^m]*m')
        fmt = logging.Formatter(fmt="[%(asctime)s] %(levelname)s: %(message)s",
                                datefmt="%Y-%m-%d %H:%M:%S")

        def format(self, record):
            record.msg = self.ansi_escape.sub('', record.msg)
            return self.fmt.format(record)

    # setup general properties of loggers
    timestamp_logger = logging.getLogger('default')
    timestamp_logger.setLevel(logging.DEBUG if debug else logging.INFO)

    no_timestamp_logger = logging.getLogger('no_timestamp')
    no_timestamp_logger.setLevel(logging.DEBUG if debug else logging.INFO)

    warning_logger = logging.getLogger('warnings')
    warning_logger.setLevel(logging.DEBUG if debug else logging.INFO)

    # setup logging to console
    timestamp_stream_logger = logging.StreamHandler(sys.stdout)
    timestamp_stream_logger.setFormatter(SpecialFormatter())
    timestamp_logger.addHandler(timestamp_stream_logger)

    no_timestamp_stream_logger = logging.StreamHandler(sys.stdout)
    no_timestamp_stream_logger.setFormatter(None)
    no_timestamp_logger.addHandler(no_timestamp_stream_logger)

    timestamp_logger.is_silent = False
    no_timestamp_stream_logger.is_silent = False
    if silent:
        timestamp_logger.is_silent = True
        timestamp_stream_logger.setLevel(logging.ERROR)
        no_timestamp_stream_logger.is_silent = True

    if log_dir:
        assert_path_exists(log_dir)
        timestamp_file_logger = logging.FileHandler(os.path.join(log_dir,
                                                                 log_file), 'a')
        timestamp_file_logger.setFormatter(ColourlessFormatter())
        timestamp_logger.addHandler(timestamp_file_logger)

        no_timestamp_file_logger = logging.FileHandler(os.path.join(log_dir,
                                                                    log_file), 'a')
        no_timestamp_file_logger.setFormatter(None)
        no_timestamp_logger.addHandler(no_timestamp_file_logger)

        warning_fh = logging.FileHandler(os.path.join(log_dir,
                                                      log_file.replace('.log', '.warnings.log')), 'a')
        warning_fh.setFormatter(ColourlessFormatter())
        warning_logger.addHandler(warning_fh)

    timestamp_logger.info('%s v%s' % (program_name, version))
    base_name = ntpath.basename(sys.argv[0])
    if base_name == '__main__.py':
        prog_name = __name__.split('.')[0]
    else:
        prog_name = base_name
    timestamp_logger.info(f'{prog_name} {" ".join(sys.argv[1:])}')
