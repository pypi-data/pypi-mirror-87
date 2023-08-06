"""
formatting.py

Format-related functionality.

:author:        Stephen Stauts
:created:       09/05/2020   (DD/MM/YYYY)
:copyright:     © 2020 Stephen Stauts. All Rights Reserved.
"""

# Standard Packages
import time
import typing

# Dependency Packages

# Local Packages and Modules
from . import core


# ID for lock used by format modifications
FORMAT_LOCK_ID = '_format'


class FormatStyle(typing.NamedTuple):
    """Valid formatting styles."""
    name: str
    modern: str
    legacy: str

    def __str__(self):
        """String representation of the class."""
        return self.modern


class Formatter:
    """
    Instance governing how record data and text get formatted into logging
    output.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the class attribute(s).

        If no args are given, a format of just the message will be used.
        Otherwise, args should either be a sequence of a single populated
        string, or a sequence of an unpopulated string followed by the
        formatting styles to populate it with, in order, e.g.:
            Formatter('{0}...{n}', MSG, TIME, ...)

        :raise TypeError:   If the format string is not a str type
        """
        datefmt = str(kwargs.get('datefmt', '%Y-%m-%d %H:%M:%S'))
        with_msecs = kwargs.get('with_msecs', True)
        msec_delim = kwargs.get('msec_delim', ',')
        gmtime = kwargs.get('gmtime', False)

        self._datefmt = datefmt
        self._with_msecs = with_msecs
        self._msec_delim = msec_delim
        self._gmtime = gmtime

        with core.get_lock(FORMAT_LOCK_ID):
            self._d_fmts = {x.name:False for x in _l_formats}

        if not args:
            self._format = populate_unformatted('{}', MSG)
            self._d_fmts[MSG.name] = True
            return

        if not isinstance(args[0], str):
            raise TypeError(
                f"Expected format string; got type '{type(args[0])}'")

        if len(args) == 1:
            self._format = modernize_legacy_formats(args[0])
            with core.get_lock(FORMAT_LOCK_ID):
                for fmt in _l_formats:
                    self._d_fmts[fmt.name] = fmt.modern in self._format
        else:
            l_fmts = args[1:]
            raw_format = populate_unformatted(args[0], *l_fmts)
            self._format = modernize_legacy_formats(raw_format)
            self._d_fmts.update({x.name:True for x in l_fmts})

    @property
    def format(self) -> str:
        """Format string to be populated by record text and data."""
        return self._format

    def format_record(self, record:core.LogRecord) -> str:
        """
        Create a formatted string of the record's contents, updated as needed.

        :param record: Record to format into a string.

        :returns: String formatted with formatting and record contents
        """
        d_fmt_content = dict()

        if self._d_fmts[MSG.name]:
            d_fmt_content[MSG.name] = record.text

        if self._d_fmts[LVL.name]:
            d_fmt_content[LVL.name] = core.name_of_level(record.level)

        if self._d_fmts[LVLNO.name]:
            d_fmt_content[LVLNO.name] = record.level

        if self._d_fmts[TIME.name]:
            d_fmt_content[TIME.name] = self.format_time(record)

        if self._d_fmts[CREATED.name]:
            d_fmt_content[CREATED.name] = record.created

        if self._d_fmts[RELCR.name]:
            d_fmt_content[RELCR.name] = record.relative_created_ms

        return self.format.format(**d_fmt_content)

    def format_time(self, record:core.LogRecord, **kwargs) -> str:
        """
        Create a formatted timestamp of the record's creation time.

        Default variables for formatting options can be overwritten at run time,
        OR this whole function can be re-implemented in a subclass of Formatter
        to gain extra specific functionality. See the `time` package
        documentation for specifics about formatting options and the difference
        between local and GM time for creating timestamps.

        :param record: Record to format into a string.

        :kwarg str datefmt:     Format string for the timestamp.
        :kwarg bool with_msecs: Attach milliseconds to the timestamp.
        :kwarg bool gmtime:     Use GM time for the time style.

        :return: Formatted time stamp of record creation time.
        """
        datefmt = kwargs.get('datefmt', self._datefmt)
        with_msecs = kwargs.get('with_msecs', self._with_msecs)
        msec_delim = kwargs.get('msec_delim', self._msec_delim)
        gmtime = kwargs.get('gmtime', self._gmtime)

        if gmtime:
            current_time = time.gmtime(record.created)
        else:
            current_time = time.localtime(record.created)

        formatted_time = time.strftime(datefmt, current_time)
        if with_msecs:
            return f'{formatted_time}{msec_delim}{record.msecs:03}'
        return formatted_time


# List of format styles. Internal use only.
_l_formats = [
    FormatStyle(name='time',    modern='{time}',    legacy='%(asctime)s'),
    FormatStyle(name='created', modern='{created}', legacy='%(created)f'),
    FormatStyle(name='file',    modern='{file}',    legacy='%(filename)s'),
    FormatStyle(name='func',    modern='{func}',    legacy='%(funcName)s'),
    FormatStyle(name='lvl',     modern='{lvl}',     legacy='%(levelname)s'),
    FormatStyle(name='lvlno',   modern='{lvlno}',   legacy='%(levelno)s'),
    FormatStyle(name='line',    modern='{line}',    legacy='%(lineno)d'),
    FormatStyle(name='msg',     modern='{msg}',     legacy='%(message)s'),
    FormatStyle(name='module',  modern='{module}',  legacy='%(module)s'),
    FormatStyle(name='msecs',   modern='{msecs}',   legacy='%(msecs)d'),
    FormatStyle(name='name',    modern='{name}',    legacy='%(name)s'),
    FormatStyle(name='path',    modern='{path}',    legacy='%(pathname)s'),
    FormatStyle(name='pid',     modern='{pid}',     legacy='%(process)d'),
    FormatStyle(name='proc',    modern='{proc}',    legacy='%(processName)s'),
    FormatStyle(name='relcr',   modern='{relcr}',   legacy='%(relativeCreated)d'),
    FormatStyle(name='thid',    modern='{thid}',    legacy='%(thread)d'),
    FormatStyle(name='thread',  modern='{thread}',  legacy='%(threadName)s'),
]


# Global shorthand references to format styles.
TIME    = [x for x in _l_formats if x.name == 'time'    ][0]
CREATED = [x for x in _l_formats if x.name == 'created' ][0]
FILE    = [x for x in _l_formats if x.name == 'file'    ][0]
FUNC    = [x for x in _l_formats if x.name == 'func'    ][0]
LVL     = [x for x in _l_formats if x.name == 'lvl'     ][0]
LVLNO   = [x for x in _l_formats if x.name == 'lvlno'   ][0]
LINE    = [x for x in _l_formats if x.name == 'line'    ][0]
MSG     = [x for x in _l_formats if x.name == 'msg'     ][0]
MODULE  = [x for x in _l_formats if x.name == 'module'  ][0]
MSECS   = [x for x in _l_formats if x.name == 'msecs'   ][0]
NAME    = [x for x in _l_formats if x.name == 'name'    ][0]
PATH    = [x for x in _l_formats if x.name == 'path'    ][0]
PID     = [x for x in _l_formats if x.name == 'pid'     ][0]
PROC    = [x for x in _l_formats if x.name == 'proc'    ][0]
RELCR   = [x for x in _l_formats if x.name == 'relcr'   ][0]
THID    = [x for x in _l_formats if x.name == 'thid'    ][0]
THREAD  = [x for x in _l_formats if x.name == 'thread'  ][0]


def populate_unformatted(unformatted_str:str, *args) -> str:
    """
    Format a given string with a list of FormatStyle objects and return the
    result. This assumes that the unformatted string is a string like those
    used with the `format` function, such as `'{} | {}'`, `'{0} | {1}'`, etc.

    :param unformatted_str: Desired format string containing format
                            characters to be populated by the args iterable.
    :param args:            Sequence of FormatStyle objects.

    :raise TypeError:   If any arg is not the expected object.

    :returns: Formatted string
    """
    if any(not isinstance(fmt_arg, FormatStyle) for fmt_arg in args):
        raise TypeError('Format arguments must be FormatStyle enumerations; '
                        f'got {tuple(type(arg) for arg in args)}')
    return unformatted_str.format(*(x.modern for x in args))


def modernize_legacy_formats(format_str:str) -> str:
    """
    Replace any legacy format strings with this lib's "modern" versions.

    :param format_str:  Format string to parse and replace.

    :returns: String re-formatted with modern format tags.
    """
    with core.get_lock(FORMAT_LOCK_ID):
        for fmt in _l_formats:
            format_str = format_str.replace(fmt.legacy, fmt.modern)
    return format_str
