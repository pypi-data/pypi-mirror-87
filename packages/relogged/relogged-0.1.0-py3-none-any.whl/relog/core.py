"""
core.py

Core functionality of the logging module.

:author:        Stephen Stauts
:created:       09/05/2020   (DD/MM/YYYY)
:copyright:     © 2020 Stephen Stauts. All Rights Reserved.
"""

# Standard Packages
import sys
import time
import threading
import typing

# Dependency Packages

# Local Packages and Modules


class LogLevel:
    """
    Simple logging level object. This seeks to imitate a named tuple but with
    better type safety.
    """

    __slots__ = ['_name', '_weight']

    def __init__(self, name:str='', weight:int=0):
        """
        Initialize the class attribute(s).

        :kwarg str name:    Name of the level.
        :kwarg int weight:  Weight (priority) of the level.
        """
        self._weight = 0
        self._name = ''

        self.name = name
        self.weight = weight

    def __str__(self) -> str:
        """String representation of the level, uppercase for consistency."""
        return self.name

    def __int__(self) -> int:
        """Integer representation of the level's weighted value."""
        return self.weight

    def __iter__(self) -> typing.Sequence:
        """Iterable representation of the class."""
        return iter((self.name, self.weight))

    @property
    def name(self) -> str:
        """Name of the level."""
        return self._name

    @name.setter
    def name(self, name:str):
        """
        Value and type setter for the name property.

        :raise TypeError:   If the given name is not a str type
        :raise ValueError:  If the name is empty
        """
        if not isinstance(name, str):
            raise TypeError(f'Expected type str; got {type(name)}')
        if not name:
            raise ValueError('Level names cannot be empty.')
        self._name = str(name).upper()

    @property
    def weight(self) -> int:
        """Weight (priority) of the level."""
        return self._weight

    @weight.setter
    def weight(self, weight:int):
        """Value and type setter for the weight property."""
        if not isinstance(weight, int):
            raise TypeError('Invalid weight; must be an integer')
        self._weight = int(weight)


class LogRecord:
    """
    Log record that contains information for what is to be, or can be, printed
    as a logged message.
    """

    __slots__ = ['_text', '_level', '_created', '_relcr_ms', '_msecs']

    def __init__(self, level:int, text:str):
        """
        Initialize the class attribute(s).

        Attributes that are calculation-based are calculated once at this point
        (unless otherwise not applicable) to reduce processing overhead by
        repeated calls to attributes that always should return the same
        number.

        :param level:   Logging level.
        :param text:    Message text of the record

        :raise ValueError: If the logging level is not a valid level
        """
        if level is None or not is_log_level_used(level):
            raise ValueError(
                f'Cannot create record with non-existent level: {level}')

        self._text = text
        self._level = level
        self._created = time.time()
        self._relcr_ms = int((self._created - _START_TIME) * 1000)
        self._msecs = int((self._created - int(self._created)) * 1000)

    @property
    def text(self) -> str:
        """Message text of the record."""
        return self._text

    @property
    def level(self) -> int:
        """Logging level weight."""
        return self._level

    @property
    def created(self) -> float:
        """Time the record was created."""
        return self._created

    @property
    def relative_created_ms(self) -> float:
        """
        Time the record was created relative to the program's start
        [milliseconds].
        """
        return self._relcr_ms

    @property
    def msecs(self) -> int:
        """Millisecond portion of the time of the record's creation."""
        return self._msecs


# Initial time of import & setup
_START_TIME = time.time()

# ID for lock used by level modifications
LEVEL_LOCK_ID = '_level'


# Track locks used by each module log. Prevents multiple logs using the same
# name/resource from having individual locks and bypassing thread-safe resource
# accesses. This attempts to apply re-entrant locks to all log cases by default
# when used with this module. Internal use only.
#
_d_log_locks = {
    LEVEL_LOCK_ID   : threading.RLock(),
    'stdout'        : threading.RLock(),
    'stderr'        : threading.RLock(),
}

# Create global ints of levels, like the `logging` package
NOTSET = 0
DEBUG = 20
INFO = 40
WARNING = 60
ERROR = 80
FATAL = 100

# Default logging level for the module
DEFAULT_LVL = INFO

# List of logging levels known by the system. Internal use only.
_l_log_levels = [
    LogLevel('NOTSET', NOTSET),
    LogLevel('DEBUG', DEBUG),
    LogLevel('INFO', INFO),
    LogLevel('WARNING', WARNING),
    LogLevel('ERROR', ERROR),
    LogLevel('FATAL', FATAL)
]

# List of logging level integers known by the system, used to reduce the
# overhead of repeatedly casting a list of LogLevels to a list of ints to check
# if an int is a registered level. Internal use only.
_l_log_level_ints = [int(x) for x in _l_log_levels]

# Dict of logging level names known by the system. Internal use only.
#
# FIXME: There is probably a better way of doing this list/dict things with
# levels. Look into it.
_d_log_level_names = {x.weight:x.name for x in _l_log_levels}


def get_lock(lock_id:str) -> threading.RLock:
    """
    Return the lock associated to a log id, such as a name or stream. This
    ensures that logs sharing the file/stream resource do not compete for access
    to their resource and are thread-safe.

    :param lock_id: ID key for the lock

    :return: Re-entract lock associated to the ID.
    """
    global _d_log_locks
    if lock_id not in _d_log_locks:
        _d_log_locks[lock_id] = threading.RLock()
    return _d_log_locks[lock_id]


def add_log_level(name:str='', weight:int=0, level:LogLevel=None):
    """
    Add a logging level to the list of known levels. This can be specified from
    either a LogLevel class or parameters to construct one. Specifying a level
    class ignores all other arguments.

    :kwarg str name:        Name of the level
    :kwarg int weight:      Weight of the level
    :kwarg LogLevel level:  LogLevel class to add

    :raise TypeError:   If the level kwarg is not a LogLevel object.
    :raise ValueError:  For bad parameters.
    """
    if level:
        if not isinstance(level, LogLevel):
            raise TypeError(
                f"'level' keyword must be a LogLevel, not {type(level)}")
        new_level = level
    else:
        if not weight:
            raise ValueError('Weight must be a non-zero integer.')
        new_level = LogLevel(name, weight)

    for lvl in _l_log_levels:
        if new_level.weight == lvl.weight:
            raise ValueError(
                f"Level weight '{new_level.weight}' is already in use for "
                f"{str(lvl)}")
        elif new_level.name == lvl.name:
            raise ValueError(f"Level name '{lvl.name}' is already in use.")

    with get_lock(LEVEL_LOCK_ID):
        _l_log_levels.append(new_level)
        _l_log_levels.sort(key=lambda x: x.weight)
        _l_log_level_ints.append(int(new_level))
        _l_log_level_ints.sort()


def is_log_level_used(level:int) -> bool:
    """
    Returns true if the given level integer is used for a known logging level.
    """
    with get_lock(LEVEL_LOCK_ID):
        return level in _l_log_level_ints


def name_of_level(level:int) -> str:
    """
    Get the name of the given logging level, or None if it is not tracked.
    """
    with get_lock(LEVEL_LOCK_ID):
        return _d_log_level_names.get(level)


def get_log_levels() -> typing.List[int]:
    """
    Return a list containing the registered logging level integers.
    """
    with get_lock(LEVEL_LOCK_ID):
        return _l_log_level_ints[:]
