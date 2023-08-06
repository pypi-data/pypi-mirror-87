"""Contains the StatusEntry class which represents an measurement in the MongoDB database."""
from mongoengine import Document, DateTimeField, BooleanField, StringField

from monitor_common.status import Status, StatusChange


class StatusEntry(Document):
    """
    A Mongo document for a status entry.

    This entry should represent a single test and it's outcome.
    """

    time = DateTimeField(required=True)
    result = BooleanField(required=True)
    _status = StringField(required=True, db_field="status")
    _status_change = StringField(required=True, db_field="status_change")

    meta = {"db_alias": "monitor", "collection": "status_entry"}

    def __init__(self, *args, **kwargs):
        """
        Init which behaves the same as the default init for MongoEngine documents.

        Handles the special behaviour to store the status and status_change parameters in the form of Status and
        StatusChange objects (instead of the base strings accepted normally).
        """

        def retrieve_from_kwargs(prop: str):
            to_return = None
            if prop in kwargs:
                to_return = kwargs[prop]
                del kwargs[prop]
            return to_return

        status = retrieve_from_kwargs("status")
        status_change = retrieve_from_kwargs("status_change")

        super(StatusEntry, self).__init__(*args, **kwargs)

        if status:
            self.status = status
        if status_change:
            self.status_change = status_change

    @property
    def status(self):
        """Return the status stored in the entry as a Status enum."""
        return Status[self._status] if self._status else None

    @status.setter
    def status(self, status: Status):
        """Set the status, takes a Status enum and stores it as a string."""
        self._status = status.name

    @property
    def status_change(self):
        """Return the status_change stored in the entry as a StatusChange enum."""
        return StatusChange[self._status_change] if self._status_change else None

    @status_change.setter
    def status_change(self, status_change: StatusChange):
        """Set the status_change, takes a StatusChange enum and stores it as a string."""
        self._status_change = status_change.name

    def to_dict(self):
        """Return the StatusEntry as a dictionary."""
        json_dict = {
            "time": str(self.time),
            "result": self.result,
            "status": self.status.name if self.status else None,
            "status_change": self.status_change.name if self.status_change else None,
        }

        return json_dict

    def __eq__(self, other):
        """Compare two StatusEntry objects, they are considered equivalent if all their properties are the same."""
        return (
            (isinstance(other, StatusEntry))
            and (self.time == other.time)
            and (self.result == other.result)
            and (self._status == other._status)
            and (self._status_change == other._status_change)
        )

    def __repr__(self):
        """
        Return a unique representation based on the properties of the entry.

        Creates a hash of all the properties that will be unique to each entry. Note that the hash is not guaranteed to
        be the same between different distributions.
        """
        cls_name = self.__class__.__name__
        cls_hash = hash(frozenset(self.to_dict().items()))
        return "{0}({1})".format(cls_name, cls_hash)

    def __str__(self):
        """Return a string representation of the StatusEntry. This is a Json dictionary of it's parameters."""
        return str(self.to_dict())
