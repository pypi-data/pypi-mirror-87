"""
audit.models.utils

Auditing related utilities
"""

from audit.utils.sqlalchemy import (
    StoredProcedure,
    Trigger,
)


class AuditStoredProcedure(StoredProcedure):
    """
    An auditing specific stored procedure
    """

    def __init__(self, audited_table, *, audit_table=None, procedure_name=None, **kwargs):
        self.audited_table = audited_table

        if not audit_table:
            audit_table = f'{audited_table}_audit'
        self.audit_table = audit_table

        if not procedure_name:
            procedure_name = f'process_{audit_table}'

        if not procedure_name.endswith(')'):
            procedure_name += '()'

        self.procedure_name = procedure_name

        super().__init__(procedure_name, self.build_definition(), **kwargs)

    def build_definition(self):
        """Creates the definition for this stored procedure"""

        return f"""
            RETURNS TRIGGER AS ${self.audit_table}$
                BEGIN
                    --
                    -- Create a row in the audit table to reflect the operation performed,
                    -- making use of the special variable TG_OP to work out the operation.
                    --
                    IF (TG_OP = 'DELETE') THEN
                        INSERT INTO {self.audit_table} SELECT 'DELETE', now(), OLD.*;
                    ELSIF (TG_OP = 'UPDATE') THEN
                        INSERT INTO {self.audit_table} SELECT 'UPDATE', now(), NEW.*;
                    ELSIF (TG_OP = 'INSERT') THEN
                        INSERT INTO {self.audit_table} SELECT 'INSERT', now(), NEW.*;
                    END IF;
                    RETURN NULL; -- result is ignored since this is an AFTER trigger
                END;
            ${self.audit_table}$ LANGUAGE plpgsql;
        """

class AuditTrigger(Trigger):
    """
    An auditing trigger
    """

    def __init__(self, audited_table, *, audit_table=None, procedure_name=None, **kwargs):
        self.audited_table = audited_table

        if not audit_table:
            audit_table = f'{audited_table}_audit'
        self.audit_table = audit_table

        if not procedure_name:
            procedure_name = f'process_{audit_table}'

        if not procedure_name.endswith(')'):
            procedure_name += '()'

        self.procedure_name = procedure_name

        super().__init__(f'{audit_table}_trigger', audited_table, self.build_definition(), **kwargs)

    def build_definition(self):
        """Creates the definition for this trigger"""

        return f'FOR EACH ROW EXECUTE FUNCTION {self.procedure_name}'
