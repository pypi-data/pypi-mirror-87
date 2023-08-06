"""Provides enums used to indicate the status and the change in status."""
import typing

from aenum import Enum


class MyEnum(Enum):
    """Extension of the Enum class that allows matching on the name (case insensitive) as well as the value."""

    @classmethod
    def _missing_name_(cls, name: typing.Union[int, str]):
        """Allow matching on the name as well as the value of the enum."""
        if isinstance(name, int):
            return cls(name)
        elif isinstance(name, str):
            for member in cls.__iter__():
                if member.name.lower() == name.lower():
                    return member


class MyOrderedEnum(MyEnum):
    """Extension of the MyEnum class that includes ordering."""

    def __ge__(self, other):
        if not type(self) == type(other):
            return NotImplemented
        return self.value >= other.value

    def __gt__(self, other):
        if not type(self) == type(other):
            return NotImplemented
        return self.value > other.value

    def __le__(self, other):
        if not type(self) == type(other):
            return NotImplemented
        return self.value <= other.value

    def __lt__(self, other):
        if not type(self) == type(other):
            return NotImplemented
        return self.value < other.value


class Status(MyOrderedEnum):
    """Enum which represents the status of the app being monitored."""

    UNKNOWN = 0  # Status of app has not yet been established
    OK = 1  # App is running as expected
    WARNING = (
        2
    )  # Some tests have been failed but not enough to warrant reporting an error
    ERROR = 3  # The app has displayed an issue consistently


class StatusChange(MyEnum):
    """Enum which represents the status transition caused by the last measurement of the app being monitored."""

    INVALID = -1
    NONE = 0
    ERROR_RESOLVED = 1
    WARNING_RESOLVED = 2
    NEW_ERROR = 3
    NEW_WARNING = 4
