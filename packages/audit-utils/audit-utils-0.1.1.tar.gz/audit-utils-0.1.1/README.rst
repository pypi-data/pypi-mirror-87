
DB Auditing Utilities
=====================

There comes a time when you require auditing to be present on a database table.
It usually looks like a painful process to implement it due to the vast changes
required to your codebase. Wouldn't it be wonderful if you could implement it,
while changing the minimal amount of lines of code, and even obtain an easy
access to its logged audit data?

*Note: this library is specifically designed to work with SQLAlchemy_ and
Alembic_. It also supports integration with Marshmallow_. If using a different
ORM layer, feel free to use the concepts herein, adapted to your needs.*

A big thanks to the `Alembic cookbook`_, for the majority of the code used in
`audit.utils.alembic`.

Example usage
-------------

Install `audit-utils` as one of your project dependencies::

    pip3 install audit-utils


You will likely want to adjust the model you wish to audit, so that you have a
base model, from which to inherit in both the audited table and the audit table.

Add the appropriate mixins to your DB models and create an audit table model::

    from audit.models import AuditTableMixin, AuditedMixin
    from application import db

    class UserBase:
        username = db.Column(db.String, nullable=False)
        first_name = db.Column(db.String)
        last_name = db.Column(db.String)

    class User(UserBase, AuditedMixin, db.Model):
        id = db.Column(db.String, nullable=False, primary_key=True)

    class UserAudit(UserBase, AuditTableMixin, db.Model):
        # This is equivalent to User.id, but without being part of the
        # primary key. You should create an index for it, for query
        # performance on the audit data.
        audited_id = db.Column(db.String, nullable=False, primary_key=False)


And if you use Marshmallow_ schemas, you can import the provided schemas for
simplicity::

    from audit.schemas import AuditLogSchema
    from application import marshamallow as ma

    class UserSchema(ma.Schema):
        username = ma.String(required=True)
        first_name = ma.String()
        last_name = ma.String()

        auditlog = ma.Nested(AuditLogSchema, dump_only=True)

        
Finally, generate a new Alembic_ migration that includes the audit table
definition, and add the following bits::

    from application.models import User

    user_audit_sp = User().stored_procedure()
    user_trigger = User().trigger()

    def upgrade():
        op.create_procedure(user_audit_sp)
        op.create_trigger(user_trigger)

    def downgrade():
        op.drop_trigger(user_trigger)
        op.drop_procedure(user_audit_sp)


*Note: Before running the database upgrade, ensure that the generated
audit model columns are in the _same_ order as the audited table. The
stored procedure relies on the order being the same to not need updates
every time a column is added to the base table definition.*

Upgrade your database and you should now have auditing on the user table, handled
at the database level, so you don't need to implement all sorts of things in your code.


Implementation Notes
--------------------

It is entirely possible that you have a compound primary key for the table that you
wish to be audited. This can be handled by overriding a couple of extra methods from
the model mixins.

The `id` and `audited_id` columns are not required to be string columns. They can be
numeric, provided that the types match in both models.

The default stored procedure does not include column names for your table, and as
such does not need to be updated when columns are added/removed/changed.

Occasionally, you will also have columns that you do not wish to include in the audit
changeset. While these columns must exist on both the audited table and the audit
table, you can add them to the list of ignored columns by overriding
`audit_ignorable_columns` in your audited model.


.. _SQLAlchemy: https://www.sqlalchemy.org/
.. _Alembic: https://alembic.sqlalchemy.org/en/latest/
.. _`Alembic cookbook`: https://alembic.sqlalchemy.org/en/latest/cookbook.html#replaceable-objects
.. _Marshmallow: https://marshmallow.readthedocs.io/en/stable/
