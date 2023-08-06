"""
logger.py

Logger implementations and related functionality.

:author:        Stephen Stauts
:created:       24/10/2020   (DD/MM/YYYY)
:copyright:     © 2020 Stephen Stauts. All Rights Reserved.
"""

# Standard Packages
from abc import ABC, abstractmethod
from collections import defaultdict
from pprint import pformat
import threading
import typing
import weakref

# Dependency Packages

# Local Packages and Modules
from . import core
from . import formatting
from . import handler


class BaseLogger(ABC):
    """
    Abstract base class for Logger objects.

    A logger that performs logging operations across its assigned handlers.
    """

    def __init__(self, name:str, level:int=core.NOTSET):
        """
        Initialize the class attribute(s).

        :param name:    Unique identifier for the instance.

        :kwarg int level:   Output logging level.
        """
        self._name = str(name)
        self._level = int(level)
        self._lock = None
        self._d_handlers = defaultdict(list)
        self._disabled = False

    def __repr__(self) -> str:
        """Representation of the class."""
        return f'<{self.__class__.__name__} {id(self)} "{self.name}"">'

    @property
    def name(self) -> str:
        """Unique identifier for the instance."""
        return self._name

    @property
    def level(self) -> int:
        """
        Output logging level. Only handlers associated to this logging level
        will log output.
        """
        return self._level

    @level.setter
    def level(self, level:int):
        """
        Value and type setter for the level property.

        :raise ValueError: If the given value is not valid.
        """
        if not core.is_log_level_used(level):
            raise ValueError(f'Unknown logging level: {level}')
        with self.lock:
            self._level = level

    @property
    @abstractmethod
    def lock_id(self) -> str:
        """
        Specific ID of the threading lock to use for the logger.

        This should be implemented by a logger sub-class for its own needs.
        """
        pass

    @property
    def lock(self) -> threading.RLock:
        """Threading lock used by the logger."""
        if not self._lock:
            self._lock = core.get_lock(self.lock_id)
        return self._lock

    @property
    def disabled(self) -> bool:
        """All logging output for the instance is disabled."""
        return self._disabled or self.level == core.NOTSET

    @disabled.setter
    def disabled(self, disabled:bool):
        """Value and type setter for the disabled property."""
        with self.lock:
            self._disabled = bool(disabled)

    def _log(self, msg, level, *args, **kwargs):
        """
        Low-level routine that creates the LogRecord and actually forwards it
        to the handlers associated to logging level.

        :param level:   Logging level of the message.
        :param msg:     Message to log.

        :kwarg bool pretty: Use pretty formatting for the message.
        """
        if not self.is_enabled_for(level):
            return

        pretty = kwargs.get('pretty')

        record = core.LogRecord(level, pformat(msg) if pretty else msg)
        with self.lock:
            for handler_ in self._d_handlers[level]:
                handler_.handle(record)

    def is_enabled_for(self, level:int) -> bool:
        """
        A logger is not disabled and has handlers associated to at least the
        specified level.
        """
        return (not self._disabled
            and level != core.NOTSET
            and level >= self.level
        )

    def log(self, msg, *args, **kwargs):
        """
        Log a message. If a level is not specified, this will use the instance's
        level.
        """
        level = kwargs.pop('level', self.level)
        self._log(msg, level, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        """
        Log a debugging message.

        :param msg: Message to log.
        """
        self._log(msg, core.DEBUG, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """
        Log a informational (typical print statement) message.

        :param msg: Message to log.
        """
        self._log(msg, core.INFO, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """
        Log a warning message.

        :param msg: Message to log.
        """
        self._log(msg, core.WARNING, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """
        Log an error message.

        :param msg: Message to log.
        """
        self._log(msg, core.ERROR, *args, **kwargs)

    def fatal(self, msg, *args, **kwargs):
        """
        Log a fatal error message.

        :param msg: Message to log.
        """
        self._log(msg, core.FATAL, *args, **kwargs)

    def has_handlers(self) -> bool:
        """True if the instance has any handler registered to a level."""
        return any(len(x) for x in self._d_handlers.values())

    def add_handler(self, handler_:handler.BaseHandler, level:int, **kwargs):
        """
        Add a handler registered at a logging level. The handler will be
        available to all levels above the given level threshold.

        :param handler: Handler to use
        :param level:   Level at which the handler should be registered.

        :kwarg bool level_only:     Assign the handler only to the given level.

        :raise TypeError:   For an invalid handler object.
        :raise ValueError:  For invalid levels.
        """
        level_only = kwargs.get('level_only')

        if not isinstance(handler_, handler.BaseHandler):
            raise TypeError('Argument must be a derivative of BaseHandler; '
                            f' got {type(handler_)}')

        if not core.is_log_level_used(level):
            raise ValueError(f'Unknown logging level: {level}')

        if level == core.NOTSET:
            raise ValueError('Cannot assign a handlers to NOTSET.')

        l_relevant_levels = [x for x in core.get_log_levels() if x >= level]

        with self.lock:
            if level_only:
                self._d_handlers[level].append(handler_)
            else:
                for lvl in l_relevant_levels:
                    self._d_handlers[lvl].append(handler_)

    def remove_handler(self, handler_:handler.BaseHandler, **kwargs):
        """
        Remove a handler from all levels it is relevant to for the instance.

        :param handler: Handler to remove

        :kwarg int level:   Specific level from which to remove the handler.

        :raise TypeError:  For handler arguments that are not valid objects.
        """
        level = kwargs.get('level')

        if not isinstance(handler_, handler.BaseHandler):
            raise TypeError('Argument must be a derivative of BaseHandler; '
                            f'got {type(handler_)}')

        with self.lock:
            if level and handler_ in self._d_handlers[level]:
                self._d_handlers[level].remove(handler_)
            else:
                for lvl, l_handlers in self._d_handlers.copy().items():
                    if handler_ in l_handlers:
                        self._d_handlers[lvl].remove(handler_)

    def remove_handlers(self, level:int=core.NOTSET):
        """
        Remove all handlers from the instance or from a particular logging
        level.

        kwarg int level:    Specific level to remove handlers from, or all
                            levels if not given.

        :raise ValueError:  For invalid level parameter.
        """
        if not core.is_log_level_used(level):
            raise ValueError(f'Unknown logging level: {level}')

        with self.lock:
            if not level:
                self._d_handlers = defaultdict(list)
            else:
                self._d_handlers[level] = list()


class _RootLogger(BaseLogger):
    """
    Default logger that is used for module-level logging operations when no
    other logger has been created or prioritized. This logger will output to
    a standard output stream in the same manner as `print` calls.

    This class is intended for internal use only.
    """

    def __init__(self):
        """Initialize the class attribute(s)."""
        super().__init__(self.__class__.__name__, level=core.INFO)

    @property
    def lock_id(self) -> str:
        """Specific ID of the threading lock to use for the handler."""
        return self.name


# ID for lock used by logger modifications
LOGGER_LOCK_ID = '_logger'

# Root logger instance. Internal use only.
_root_logger = _RootLogger()
_root_logger.add_handler(handler.StreamHandler(), core.INFO)

DEFAULT_ROOT_ID = _root_logger.name
_custom_root_id = None

# Tracked logger objects. Internal use only.
_wvd_loggers = weakref.WeakValueDictionary()
_wvd_loggers[_root_logger.name] = _root_logger


def get_logger(name=None) -> BaseLogger:
    """
    Return a specific logger, or the root logger if no name is given.

    :kwarg str name:    Name of the logger to retrieve.

    :raise ValueError: If the logger does not exist.
    """
    global _custom_root_id

    if not name:
        name = _custom_root_id if _custom_root_id else DEFAULT_ROOT_ID

    with core.get_lock(LOGGER_LOCK_ID):
        try:
            _logger = _wvd_loggers[name]
        except KeyError as key_err:
            if _custom_root_id and key_err.args[0] == _custom_root_id:
                _custom_root_id = None
                _logger = _wvd_loggers[DEFAULT_ROOT_ID]
            else:
                raise ValueError(f'No such logger: {name}')

    return _logger


def register_logger(new_logger:BaseLogger, as_root=False):
    """
    Register a new logger with the module, allowing it to be retrievable with
    `get_logger`.

    :param new_logger:  Logger instance to register.

    :kwarg bool as_root:    Register the new logger as the logger to use for
                            root logging calls instead of the module default.

    :raise TypeError:  If the logger parameter is invalid.
    """
    if not isinstance(new_logger, BaseLogger):
        raise TypeError(f'Not a sub-class of BaseLogger: {type(new_logger)}')

    global _custom_root_id

    with core.get_lock(LOGGER_LOCK_ID):
        if as_root:
            _custom_root_id = new_logger.name
        _wvd_loggers[new_logger.name] = new_logger


def log(msg, level, *args, **kwargs):
    """
    Log a message using the root logger. A level given as a keyword argument
    will be overwritten by the level argument.

    :param msg:     Message to log.
    :param level:   Logging level of the message.
    """
    kwargs['level'] = level
    root_logger = get_logger()
    root_logger.log(msg, *args, **kwargs)


def debug(msg, *args, **kwargs):
    """
    Log a debugging message using the root logger.

    :param msg: Message to log.
    """
    root_logger = get_logger()
    root_logger.debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    """
    Log a informational (typical print statement) message using the root logger.

    :param msg: Message to log.
    """
    root_logger = get_logger()
    root_logger.info(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    """
    Log a warning message using the root logger.

    :param msg: Message to log.
    """
    root_logger = get_logger()
    root_logger.warning(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    """
    Log an error message using the root logger.

    :param msg: Message to log.
    """
    root_logger = get_logger()
    root_logger.error(msg, *args, **kwargs)


def fatal(msg, *args, **kwargs):
    """
    Log a fatal error message using the root logger.

    :param msg: Message to log.
    """
    root_logger = get_logger()
    root_logger.fatal(msg, *args, **kwargs)
