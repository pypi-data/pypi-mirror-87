"""
audit.utils.sqlalchemy

SQLAlchemy/Alembic utilities to be able to have triggers/stored procedures within migrations

Currently only tested with PostgreSQL

"""

from alembic.operations import Operations, MigrateOperation


class ReplaceableObject:
    """A base replaceable object for the database"""

    def __init__(self, name, definition):
        self.name = name
        self.definition = definition


class StoredProcedure(ReplaceableObject):
    '''
    If you want to create a stored procedure, you would do the following:

        from audit.utils.sqlalchemy import StoredProcedure

        users_audit_sp = StoredProcedure(
            "process_users_audit()",
            """
            RETURNS TRIGGER AS $users_audit$
                BEGIN
                    --
                    -- Create a row in the audit table to reflect the operation performed,
                    -- making use of the special variable TG_OP to work out the operation.
                    --
                    IF (TG_OP = 'DELETE') THEN
                        INSERT INTO users_audit SELECT 'DELETE', now(), OLD.*;
                    ELSIF (TG_OP = 'UPDATE') THEN
                        INSERT INTO users_audit SELECT 'UPDATE', now(), NEW.*;
                    ELSIF (TG_OP = 'INSERT') THEN
                        INSERT INTO users_audit SELECT 'INSERT', now(), NEW.*;
                    END IF;
                    RETURN NULL; -- result is ignored since this is an AFTER trigger
                END;
            $users_audit$ LANGUAGE plpgsql;
            """
        )

        def upgrade():
            op.create_procedure(users_audit_sp)

        def downgrade():
            op.drop_procedure(users_audit_sp)

    Note: That the first argument to `StoredProcedure` includes the parameters that the
          procedure accepts.

    Additionally, unlike other ReplaceableObjects, StoredProcedure accepts `is_immutable` to
    change the outputted DDL statement to allow for replacement of this object. This allows for
    in place updates to the procedure using `CREATE OR REPLACE FUNCTION ...`. This is the
    default behaviour.
    '''

    def __init__(self, name_with_args, definition, *, is_immutable=True):

        super().__init__(name_with_args, definition)
        self.is_immutable = is_immutable


class Trigger(ReplaceableObject):
    '''
    If you want to add a trigger, you would do the following:

        from audit.utils.sqlalchemy import Trigger

        users_trigger = Trigger(
            "users_audit_trigger",
            "users",
            """
            FOR EACH ROW EXECUTE FUNCTION process_users_audit();
            """
        )

        def upgrade():
            op.create_trigger(users_trigger)

        def downgrade():
            op.drop_trigger(users_trigger)

    Trigger also accepts three boolean keywords: on_insert, on_update, on_delete
    This allows you to specify that the trigger only runs on certain actions. The
    default is to run on all 3 actions.
    '''

    def __init__(self, name, tablename, definition, *,
                 on_insert=True, on_update=True, on_delete=True):

        super().__init__(name, definition)
        self.tablename = tablename

        if not on_insert and not on_update and not on_delete:
            raise ValueError('You must specify at least one of on_insert, on_update or'
                             ' on_delete to create a trigger.')

        self.on_operations = []
        if on_insert:
            self.on_operations.append('INSERT')
        if on_update:
            self.on_operations.append('UPDATE')
        if on_delete:
            self.on_operations.append('DELETE')


class ReversibleOp(MigrateOperation):
    """A base class for any reversible operation not already handled by Alembic internals"""

    def __init__(self, target):
        self.target = target

    @classmethod
    def invoke_for_target(cls, operations, target):
        """Run this operation"""

        op = cls(target)  # pylint: disable=invalid-name
        return operations.invoke(op)

    def reverse(self):
        """Reverse this operation"""

        raise NotImplementedError()

    @classmethod
    def _get_object_from_version(cls, operations, ident):
        """Get the object from a specific migration version"""

        version, objname = ident.split(".")

        module = operations.get_context().script.get_revision(version).module
        obj = getattr(module, objname)
        return obj

    @classmethod
    def replace(cls, operations, target, replaces=None, replace_with=None):
        """Allow for upgrading an object"""

        if replaces:
            old_obj = cls._get_object_from_version(operations, replaces)
            drop_old = cls(old_obj).reverse()
            create_new = cls(target)
        elif replace_with:
            old_obj = cls._get_object_from_version(operations, replace_with)
            drop_old = cls(target).reverse()
            create_new = cls(old_obj)
        else:
            raise TypeError("replaces or replace_with is required")

        operations.invoke(drop_old)
        operations.invoke(create_new)


@Operations.register_operation("create_trigger", "invoke_for_target")
@Operations.register_operation("replace_trigger", "replace")
class CreateTriggerOp(ReversibleOp):
    """Allow for reversal of this type of operation"""

    def reverse(self):
        """Reverse this operation"""

        return DropTriggerOp(self.target)


@Operations.register_operation("drop_trigger", "invoke_for_target")
class DropTriggerOp(ReversibleOp):
    """Allow for reversal of this type of operation"""

    def reverse(self):
        """Reverse this operation"""

        return CreateTriggerOp(self.target)


@Operations.register_operation("create_procedure", "invoke_for_target")
@Operations.register_operation("replace_procedure", "replace")
class CreateSPOp(ReversibleOp):
    """Allow for reversal of this type of operation"""

    def reverse(self):
        """Reverse this operation"""

        return DropSPOp(self.target)


@Operations.register_operation("drop_procedure", "invoke_for_target")
class DropSPOp(ReversibleOp):
    """Allow for reversal of this type of operation"""

    def reverse(self):
        """Reverse this operation"""

        return CreateSPOp(self.target)


@Operations.implementation_for(CreateSPOp)
def create_procedure(operations, operation):
    """Create the SQL to run from the operation.target"""

    if operation.target.is_immutable:
        create_text = "CREATE FUNCTION"
    else:
        create_text = "CREATE OR REPLACE FUNCTION"

    operations.execute(
        "%s %s %s" % (
            create_text, operation.target.name, operation.target.definition
        )
    )


@Operations.implementation_for(DropSPOp)
def drop_procedure(operations, operation):
    """Create the SQL to run from the operation.target"""

    operations.execute("DROP FUNCTION %s" % operation.target.name)


@Operations.implementation_for(CreateTriggerOp)
def create_trigger(operations, operation):
    """Create the SQL to run from the operation.target"""

    operations.execute(
        "CREATE TRIGGER %s AFTER %s ON %s %s" % (
            operation.target.name,
            ' OR '.join(operation.target.on_operations),
            operation.target.tablename,
            operation.target.definition
        )
    )


@Operations.implementation_for(DropTriggerOp)
def drop_trigger(operations, operation):
    """Create the SQL to run from the operation.target"""

    operations.execute("DROP TRIGGER %s ON %s" % (
        operation.target.name, operation.target.tablename
    ))
