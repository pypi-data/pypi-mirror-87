"""
audit.schemas

Marshmallow schemas for auditing related serializations

"""


from marshmallow import Schema
from marshmallow.fields import (
    Dict,
    DateTime,
    List,
    Nested,
    String,
)


class AuditLogEntrySchema(Schema):
    """
    Schema representing an audit log entry
    """

    operation = String(read_only=True)
    at = DateTime(read_only=True)
    by = String(read_only=True)
    changes = Dict(read_only=True)


class AuditLogSchema(Schema):
    """
    Schema representing a set of audit log entries

    In any schema where auditing is available to be output:

        auditlog = Nested(AuditLogSchema, read_only=True)

    """

    entries = List(Nested(AuditLogEntrySchema), read_only=True)
