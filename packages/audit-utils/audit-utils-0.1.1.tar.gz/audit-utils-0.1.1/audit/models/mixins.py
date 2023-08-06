"""
audit.models.mixins

Auditing related mixins
"""


import importlib

import sqlalchemy as sa

from .core import (
    AuditLog,
    AuditLogEntry,
)
from .utils import (
    AuditStoredProcedure,
    AuditTrigger,
)


class AuditTableMixin:
    """
    Adds appropriate columns to a model for creation of an auditing table
    """

    operation = sa.Column(sa.String(), nullable=False, primary_key=True)
    operation_at = sa.Column(sa.DateTime(), nullable=False, primary_key=True)
    updated_by = sa.Column(sa.String(), nullable=False)


class AuditedMixin:
    """
    Add auditing data output to a model that has an associated audit table setup
    """

    __audit_class__ = None

    def trigger(self, *, audit_table=None, **kwargs):
        """Returns the DB trigger definition for the audited table"""

        if not audit_table:
            audit_table = self.audit_class.__tablename__

        return AuditTrigger(
            self.__tablename__,
            audit_table=audit_table,
            **kwargs
        )

    def stored_procedure(self, *, audit_table=None, **kwargs):
        """Returns the DB stored procedure definition for the audited table"""

        if not audit_table:
            audit_table = self.audit_class.__tablename__

        return AuditStoredProcedure(
            self.__tablename__,
            audit_table=audit_table,
            **kwargs
        )

    @property
    def audit_class(self):
        """
        Returns the appropriate audit class for this object
        """

        if not self.__audit_class__:
            self.__audit_class__ = f'{self.__class__}Audit'

        if isinstance(self.__audit_class__, str):

            if '.' in self.__audit_class__:
                audit_module = importlib.import_module(self.__audit_class__.split('.')[:-1])
                self.__audit_class__ = getattr(audit_module, self.__audit_class__.split('.')[-1])

            else:
                self.__audit_class__ = globals().get(self.__audit_class__)

        if self.__audit_class__ is None:
            raise NameError('Cannot find the appropriate audit class. Please specifically'
                            ' define __audit_class__ on %s' % self.__class__)

        return self.__audit_class__

    @property
    def audit_id_filter(self):
        """
        Returns a query filter to use in retrieving rows related to this object

        Override this if you are using a compound primary key or desired specific
        column names, remebering that it is defined as a property
        """

        return (self.audit_class.audited_id == self.id)  # pylint: disable=superfluous-parens

    @property
    def audit_ignorable_columns(self):
        """
        Returns a list of keys that should be ignored from the audit comparison

        Override this to specify other columns that you would like to ignore,
        remebering that it is defined as a property
        """

        return ['audited_id']

    @property
    def auditlog(self):
        """
        Returns the audit log for this object
        """

        entries = self.audit_class.query.filter(self.audit_id_filter) \
            .options(sa.orm.lazyload('*')) \
            .order_by(self.audit_class.operation_at.asc()) \
            .group_by(self.audit_class.audited_id, self.audit_class.operation_at)

        log = AuditLog()
        last = {}

        for entry in entries.all():
            entry_dict = entry.as_dict if hasattr(entry, 'as_dict') else entry.__dict__

            # Pop off audit meta columns from the audit entry record
            operation = entry_dict.pop('operation')
            at = entry_dict.pop('operation_at')  # pylint: disable=invalid-name
            by = entry_dict.get('updated_by')    # pylint: disable=invalid-name

            # Pop off any user-defined columns to ignore
            for key in self.audit_ignorable_columns:
                entry_dict.pop(key, None)

            log.append(AuditLogEntry(operation, at, by, last, entry_dict))
            last = entry_dict

        return log
