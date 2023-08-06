"""
handler.py

Handler functionality.

:author:        Stephen Stauts
:created:       09/05/2020   (DD/MM/YYYY)
:copyright:     © 2020 Stephen Stauts. All Rights Reserved.
"""

# Standard Packages
from abc import ABC, abstractmethod
import sys
import threading
import typing

# Dependency Packages

# Local Packages and Modules
from . import core
from . import formatting


class Filter(typing.NamedTuple):
    """
    Named tuple structure for Filter components.

    A filter function must return True or False to determine pass or fail,
    respectively. Passing on True prevents filter functions with no return
    value (i.e. `None`) from being considered a pass.
    """
    func:typing.Callable[..., typing.Any]
    args:tuple = tuple()
    kwargs:dict = dict()


class BaseHandler(ABC):
    """Base handler class."""

    def __init__(self, **kwargs):
        """
        Initialize the class attribute(s). Specifying a format string with
        or without format arguments will take precedence over specifying a
        formatter object. If none are specified, the handler will create a
        formatter using just the message output.

        :kwarg str name:            Specific identifier for the handler
        :kwarg Formatter formatter: Specific formatter instance to use
        :kwarg str format_str:      Format string, populated or unpopulated.
        :kwarg tuple format_args:   Formatting arguments for the format string
        """
        name = kwargs.get('name', '')
        formatter = kwargs.get('formatter')
        format_str = kwargs.get('format', '')
        format_args = kwargs.get('format_args', tuple())

        if format_str and format_args:
            formatter = formatting.Formatter(format_str, *format_args)
        elif format_str and not format_args:
            formatter = formatting.Formatter(format_str)
        elif not formatter:
            formatter = formatting.Formatter('{}', formatting.MSG)

        self._name = name if name else id(self)
        self._lock = None
        self._l_filters = list()
        self.formatter = formatter

    def __repr__(self) -> str:
        """Representation of the class."""
        return f'<{self.__class__.__name__} {self.name}>'

    @property
    @abstractmethod
    def lock_id(self) -> str:
        """
        Specific ID of the threading lock to use for the handler.

        This should be implemented by a handler sub-class for its own needs.
        """
        pass

    @property
    def lock(self) -> threading.RLock:
        """Threading lock used by the handler."""
        if not self._lock:
            self._lock = core.get_lock(self.lock_id)
        return self._lock

    @property
    def name(self) -> str:
        """Specific identifier for the handler."""
        return self._name

    @property
    def formatter(self) -> str:
        """Formatter instance that formats record text."""
        return self._formatter

    @formatter.setter
    def formatter(self, formatter:formatting.Formatter):
        """
        Value and type setter for the formatter property.

        :raise TypeError: If the given value is not of the correct type.
        """
        if not isinstance(formatter, formatting.Formatter):
            raise TypeError(
                'Can only assign Formatter objects to formatter attribute')
        self._formatter = formatter

    @property
    def format(self) -> str:
        """Format string used by the handler."""
        return self._formatter.format

    @abstractmethod
    def emit(self, record:core.LogRecord):
        """
        Emit a log record to its destination. This is the actual "logging"
        function that sends the formatted record to its IO destination. It
        should be called by `handle` instead of directly by other sources.

        This should be implemented by a handler sub-class for its own needs.

        :param record:  Record to emit
        """
        pass

    @abstractmethod
    def flush(self):
        """
        Flush all logging output. This should be implemented by a handler for
        its own needs.
        """
        pass

    def format_record(self, record:core.LogRecord) -> str:
        """
        Create a formatted string of the record's contents, updated as needed.

        :param record: Record to format into a string.

        :returns: String formatted with formatting and record contents
        """
        return self.formatter.format_record(record)

    def handle(self, record:core.LogRecord):
        """
        Handle a log record by filtering it to determine whether or not it meets
        emission criteria.

        Emission criteria always consitutes all filters passing in order to
        emit the record.

        :param record:  Record to handle.
        """
        for nt_filter in self._l_filters:
            if not nt_filter.func(record, *nt_filter.args, **nt_filter.kwargs):
                return

        with self.lock:
            self.emit(record)

    def add_filter(self, new_filter:Filter):
        """
        Add a record filter to the handler.

        :param new_filter:  A function or Filter object to do the filtering.

        :raise TypeError: For an invalid filter argument.
        """
        if not isinstance(new_filter, Filter):
            raise TypeError('Can only add Filter objects.')
        self._l_filters.append(new_filter)

    def remove_filter(self, old_filter:Filter):
        """
        Remove a filter from the handler.

        :param old_filter:  A function or Filter object to do the filtering.
        """
        try:
            self._l_filters.remove(old_filter)
        except ValueError:
            pass


class StreamHandler(BaseHandler):
    """
    Handler class that logs records to an IO stream.

    :note:  This class does not close the stream, as `sys.stdout`
            `sys.stderr` may be used.
    """

    def __init__(self, **kwargs):
        """
        Initialize the class attribute(s).

        :kwarg TextIOWrapper stream:    IO stream used for the handler
        :kwarg str name:                Custom name for the handler; otherwise
                                        `<stream>-<object ID>`.

        :raise ValueError: Invalid stream specified
        """
        stream = kwargs.pop('stream', sys.stderr)
        name = kwargs.get('name')   # Not unique to this init; check only

        if not self.is_valid_stream(stream):
            raise ValueError(f'Invalid IO stream: {stream}')

        super().__init__(**kwargs)

        self._stream = stream
        if not name:
            # Stream + id differentiates multiple stream handlers
            self._name = f'{self.name_for_stream(self.stream)}-{id(self)}'

    @property
    def lock_id(self) -> str:
        """Specific ID of the threading lock to use for the handler."""
        return 'stdout' if self.stream == sys.stdout else 'stderr'

    @property
    def stream(self) -> str:
        """Stream used by the handler."""
        return self._stream

    @staticmethod
    def is_valid_stream(stream) -> str:
        """Given stream is a valid stream source for the handler."""
        return any(stream == x for x in [sys.stderr, sys.stdout])

    @staticmethod
    def name_for_stream(stream) -> str:
        """Shorthand name for a given stream."""
        if stream == sys.stdout:
            return 'stdout'
        elif stream == sys.stderr:
            return 'stderr'
        else:
            return 'unknown'

    def flush(self):
        """Flush the stream."""
        with self.lock:
            if self.stream and hasattr(self.stream, 'flush'):
                self.stream.flush()

    def emit(self, record:core.LogRecord):
        """
        Emit (print) a log record to its destination.

        :param record:  Record to emit
        """
        with self.lock:
            self.stream.write(f'{self.format_record(record)}\n')
            self.flush()
