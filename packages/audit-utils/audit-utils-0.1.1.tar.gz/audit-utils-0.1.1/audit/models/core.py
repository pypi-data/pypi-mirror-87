"""
audit.models

Auditing related models
"""

import json

try:
    from audit.schemas import AuditLogSchema, AuditLogEntrySchema
    NO_MARSHMALLOW = False
except ImportError:
    NO_MARSHMALLOW = True
    pass


class AuditLog:
    """
    A set of Audit Log Entries
    """

    entries = []

    def __init__(self, entries=None):
        if entries:
            if not isinstance(entries, list):
                entries = [entries]

            for entry in entries:
                self.append(entry)

    def append(self, value):
        """Append a log entry, ensuring that it _is_ a log entry"""

        if not isinstance(value, AuditLogEntry):
            raise ValueError(
                'AuditLog objects can only contain AuditLogEntry objects, not %s' % type(value))

        self.entries.append(value)

    def to_json(self, *args, **kwargs):
        """Output this object to JSON"""

        return json.dumps({'entries': self.entries}, *args, **kwargs)

    def dump(self, **kwargs):
        """Marshmallow interface"""

        return self.to_json() if NO_MARSHMALLOW else AuditLogSchema(**kwargs).dump(self)


class AuditLogEntry:
    """
    An Audit Log Entry represents a change that occurred between 2 database rows.

    `operation` is one of `INSERT`, `UPDATE`, `DELETE`, according to which action was taken
    `at` is the time the change occurred
    `by` is an identifier of the initiator of the change. This value is completely arbitrary

    """

    operation = None
    at = None
    by = None
    raw_old = {}
    raw_new = {}

    def __init__(self, operation, at, by, old=None, new=None):  # pylint: disable=too-many-arguments
        self.operation = operation
        self.at = at  # pylint: disable=invalid-name
        self.by = by  # pylint: disable=invalid-name

        if not old and not new:
            raise ValueError('Both old and new cannot be empty.')

        self.raw_old = old if old else {}
        self.raw_new = new if new else {}

    @property
    def changes(self):
        """Build changes list"""

        types_to_leave = (str, int, float, bool,)
        chgs = []
        new_keys = sorted(self.raw_new.keys())

        for key,value in self.raw_old.items():
            if value is not None and not isinstance(value, types_to_leave):
                value = str(value)

            if key not in self.raw_new:
                chgs.append({key: {'old': value, 'new': None}})

            else:
                new_value = self.raw_new.get(key)
                if new_value is not None and not isinstance(new_value, types_to_leave):
                    new_value = str(new_value)

                if new_value != value:
                    chgs.append({key: {'old': value, 'new': new_value}})

                new_keys.remove(key)

        for key in new_keys:
            if self.raw_new[key] is not None:
                if not isinstance(self.raw_new[key], types_to_leave):
                    new_value = str(self.raw_new[key])
                else:
                    new_value = self.raw_new[key]

                chgs.append({key: {'old': None, 'new': new_value}})

        return chgs

    def to_json(self, *args, **kwargs):
        """Output this object to JSON"""

        return json.dumps(
            {
                'operation': self.operation,
                'at': self.at,
                'by': self.by,
                'changes': self.changes,
            },
            *args, **kwargs)

    def dump(self, **kwargs):
        """Marshmallow interface"""

        return self.to_json() if NO_MARSHMALLOW else AuditLogEntrySchema(**kwargs).dump(self)
