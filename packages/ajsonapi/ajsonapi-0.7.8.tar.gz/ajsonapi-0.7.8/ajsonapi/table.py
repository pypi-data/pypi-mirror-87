# Copyright © 2018-2020 Roel van der Goot
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""Module table provides class Table."""

from itertools import chain

from ajsonapi.attribute import Attribute
from ajsonapi.conversions import pascal_to_snake
from ajsonapi.exceptions import ModelError
from ajsonapi.logging import log
# pylint: disable=unused-import
from ajsonapi.relationships import (
    LocalRelationship,
    ManyToManyRelationship,
    ManyToOneRelationship,
    Relationship,
)
from ajsonapi.toposort import CircularDependencyError, toposort
from ajsonapi.types import Int64
from ajsonapi.uri.collection import Collection


class Original:
    """Class to store the original Table attributes and relationships."""

    # pylint: disable=too-few-public-methods

    def _pylint(self):
        """Method to stop pylint from complaining about too-few-public-methods
        in an empty class with a disable=too-few-public-methods directive
        (PyCQA/pylint issue #2913).
        """


class Table:
    """Class Table is the Python representation of an SQL table."""
    # pylint: disable=too-few-public-methods

    by_class_name = {}
    atable_def_by_class_name = {}

    @classmethod
    def __init_subclass__(cls):
        # pylint: disable=too-many-statements,too-many-branches,too-many-nested-blocks
        if cls.__name__ in ['JSON_API', 'AssociationTable']:
            return

        # To prevent ajsonapi's attributes and relationships from overriding the
        # user's attributes and relationships, move the user's attributes and
        # relationships to ___.
        cls.___ = Original()
        for name, col in cls.__dict__.items():
            if isinstance(col, (Attribute, Relationship)):
                setattr(cls.___, name, col)
        for name, col in cls.___.__dict__.items():
            if isinstance(col, (Attribute, Relationship)):
                delattr(cls, name)

        cls.name = cls.__name__
        collection_name = pascal_to_snake(cls.__name__)
        cls.collection = Collection(collection_name, cls)
        Collection.by_name[collection_name] = cls.collection
        cls.attributes_by_name = {}
        cls.relationships = []
        cls.local_relationships = []
        cls.remote_relationships = []
        cls.lfkey_by_relationship_name = {}
        cls.relationship_by_lfkey = {}
        cls.columns = []
        cls.constraints = []
        cls.pool = None

        # Update relationships to class 'cls' for classes in cls.by_class_name.
        for table in Table.by_class_name.values():
            for col in table.___.__dict__.values():
                if isinstance(col, Relationship):
                    if col.rtable == cls.__name__:
                        col.rtable = cls
                    if isinstance(col, ManyToManyRelationship):
                        if col.atable == cls.__name__:
                            col.atable = cls

        # Now insert cls in by_class_name in case it contains a relationship to
        # itself. That way the next code section resolves the circular
        # dependency.
        Table.by_class_name[cls.name] = cls

        # Update attributes and relationships in cls.
        for name, col in cls.___.__dict__.items():
            if isinstance(col, Attribute):
                col.name = name
                cls.columns.append(col)
                cls.attributes_by_name[col.name] = col
            elif isinstance(col, Relationship):
                col.name = name
                cls.relationships.append(col)
                col.table = cls
                col.collection = cls.collection
                if isinstance(col, LocalRelationship):
                    cls.local_relationships.append(col)
                    cls.lfkey_by_relationship_name[col.name] = col.lfkey
                    cls.relationship_by_lfkey[col.lfkey] = col
                    cls.columns.append(col)
                    cls.constraints.append(col)
                else:
                    cls.remote_relationships.append(col)
                    if (isinstance(col, ManyToManyRelationship) and
                            isinstance(col.atable, str)):
                        if col.atable in Table.by_class_name:
                            col.atable = Table.by_class_name[col.atable]
                        else:
                            lclassname = cls.__name__
                            if isinstance(col.rtable, str):
                                rclassname = col.rtable
                            else:
                                rclassname = col.rtable.__name__
                            if col.atable not in cls.atable_def_by_class_name:
                                cls.atable_def_by_class_name[col.atable] = (
                                    f"class {col.atable}(AssociationTable):\n"
                                    f"    rel0 = ManyToOneRelationship"
                                    f"('{lclassname}', lfkey='{col.lafkey}')\n"
                                    f"    rel1 = ManyToOneRelationship"
                                    f"('{rclassname}', lfkey='{col.rafkey}')\n")
                if (isinstance(col.rtable, str) and
                        col.rtable in Table.by_class_name):
                    col.rtable = Table.by_class_name[col.rtable]
                    for rel in col.rtable.relationships:
                        if col.is_reverse(rel):
                            rel.reverse = col
                            col.reverse = rel
                            break

    @classmethod
    def sql_statements(cls, exclude_classes=None):
        """Creates the sql statements for this table.

        Returns:
            stmt_table: The SQL statement to create the table.
            stmts_fk: List of SQL statements for foreign key constraints that
                are removed from the stmt_table.
        """
        if exclude_classes is None:
            exclude_classes = set()
        columns_now, columns_later = [], []
        for col in cls.columns:
            if col in cls.local_relationships:
                if col.rtable in exclude_classes:
                    columns_later.append(col)
                else:
                    columns_now.append(col)
            else:
                columns_now.append(col)
        table_fields = ',\n   '.join(
            chain((col.sql() for col in cls.columns),
                  chain.from_iterable(col.sql_constraints()
                                      for col in cls.constraints
                                      if col in columns_now)))
        # pylint: disable=no-member
        if hasattr(cls, 'id') and cls.id.type_ == Int64:
            stmt_table = (
                f'CREATE SEQUENCE IF NOT EXISTS data.seq_{cls.name};\n'
                f'CREATE TABLE IF NOT EXISTS data.{cls.name} (\n   '
                f'{table_fields}\n);')
        else:
            stmt_table = (f'CREATE TABLE IF NOT EXISTS data.{cls.name} (\n   '
                          f'{table_fields}\n);')
        stmts_fk = [
            f'ALTER TABLE data.{cls.name} ADD {constraint}'
            for col in cls.constraints if col in columns_later
            for constraint in col.sql_constraints()
        ]
        return stmt_table, stmts_fk

    @classmethod
    def _dependencies(cls):
        """Fetches the creation dependencies for this class.

        Returns:
            A set of classes whose tables must be created before this class's
            table.
        """
        return {rel.rtable for rel in cls.local_relationships}


class AssociationTable(Table):
    """Class AssociationTable is the Python representation of an SQL
    association table.
    """
    # pylint: disable=too-few-public-methods

    @classmethod
    def __init_subclass__(cls):
        super().__init_subclass__()
        cls.constraints.append(cls)

    @classmethod
    def sql_constraints(cls):
        """Returns the constraints for classes derived from AssociationTable."""
        return [
            "UNIQUE "
            f"({', '.join(rel.lfkey for rel in cls.local_relationships)})"
        ]


def parse_model():
    """Parse the provided model for failures."""

    errors = []
    for class_name, table in Table.by_class_name.items():
        for rel in table.relationships:
            if isinstance(rel.table, str):
                error = (f'Relationship {class_name}.{rel.name}: '
                         f'remote table {rel.table} does not exist.')
                errors.append(error)
    if errors:
        raise ModelError(errors)


async def db_execute(pool, stmt):
    """Execute statement."""

    async with pool.acquire() as connection:
        log.debug(stmt)
        return await connection.execute(stmt)


async def create_all(pool):
    """Creates the SQL tables for the classes in the object model.

    Args:
        pool: Connection pool to the database in which to create the SQL tables.
    """

    await db_execute(pool, 'CREATE SCHEMA data;')
    await db_execute(
        pool, 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'
        ' WITH SCHEMA data;')

    # pylint: disable=protected-access
    stmts_delayed = []  # Delayed foreign key constraints

    for class_name, stmt in Table.atable_def_by_class_name.items():
        if class_name not in Table.by_class_name:
            # pylint: disable=exec-used
            exec(compile(stmt, '<string>', 'exec'))
    dependencies = {
        table: table._dependencies() for table in Table.by_class_name.values()
    }
    while True:
        try:
            for tables in toposort(dependencies):
                for table in tables:
                    stmt_table, _ = table.sql_statements()
                    await db_execute(pool, stmt_table)
            break
        except CircularDependencyError as exc:
            dependencies = exc.data
            itr = iter(dependencies.items())
            table, deps = next(itr)
            stmt_table, stmts_fk = table.sql_statements(deps)
            await db_execute(pool, stmt_table)
            stmts_delayed.extend(stmts_fk)
            dependencies = {
                item: (dep - {table})
                for item, dep in dependencies.items()
                if item != table
            }
    for stmt in stmts_delayed:
        await db_execute(pool, stmt)


def init(pool):
    """Initializes all user Table subclasses."""

    for table in Table.__subclasses__():
        if table.__name__ != 'JSON_API':
            table.pool = pool
    for table in AssociationTable.__subclasses__():
        table.pool = pool
