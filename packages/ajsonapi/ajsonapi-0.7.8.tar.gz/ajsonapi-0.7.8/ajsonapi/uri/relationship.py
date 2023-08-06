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
"""Module uri.relationship provides things related to relationship URIs."""

from abc import abstractmethod
from asyncio import Lock, create_task, gather
from itertools import chain
from re import compile as re_compile

from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError

from ajsonapi.conversions import id_number_to_name
from ajsonapi.document import (
    ResourceIdentifierObjectDocument,
    ResourceIdentifierObjectsDocument,
    parse_request_document_data,
)
from ajsonapi.environments import GetObjectIncludedEnvironment
from ajsonapi.errors import (
    DocumentDataNonexistentIdError,
    DocumentDataRelationshipConflictError,
    MethodNotAllowedError,
    ResourceNotFoundError,
    ResourceNotFoundMalformedIdError,
)
from ajsonapi.exceptions import ErrorsException
from ajsonapi.id_value import IdValue
from ajsonapi.logging import log
from ajsonapi.responses import (
    document_response,
    errors_response,
    no_content_response,
)
from ajsonapi.uri.collection import Collection
from ajsonapi.uri.resource import Resource

RE_FOREIGN_KEY_VIOLATION_ERROR_DETAIL = re_compile(
    r'Key \(([^\)]*)\)=\(([^\)]*)\) is not present in table "([^"]*)".')


class Relationship(Resource):
    """Class Relationship represents the relationship URI
    (/{collection}/{id}/relationships/{relationship}).
    """

    def __init__(self, collection, id_, relationship):
        # pylint: disable=too-many-arguments
        self.collection = collection
        self.id = id_  # pylint: disable=invalid-name
        self.relationship = relationship

        self.table = collection.table

    @abstractmethod
    async def parse_document(self, request):
        """Parses the request document for a valid resource object.

        Args:
            request (Request): the request to be parsed.

        Returns:
            A ResourceIdentifierObjectDocument or a
            ResourceIdentifierObjectsDocument (plural).

        Raises:
            ErrorsException with all the errors in case the document does not
            represent a valid resource object.
        """

    async def get(self, query):
        """Produces the response for the GET
        /{collection}/{id}/relationships/{relationship} request.
        """
        links = {
            'self':
                self.path(),
            'related': (f'/{self.collection.name}/{self.id.name}'
                        f'/{self.relationship.name}')
        }
        return document_response(await self.to_document(query=query,
                                                        links=links))

    async def to_document(self, query=None, links=None):
        """Creates the document for the resource objects in this resource
        collection.

        Args:
            links (dict): value for the links field in the response.
        """

        data, included = await self.to_data_included(query)
        document = {'data': data}
        if included is not None:
            document['included'] = included
        if links:
            document['links'] = links
        return document

    async def to_data_included(self, query):
        """Creates the document's data and included member values for this
        collection.
        """
        env = GetRelationshipEnvironment(self, query)
        await env.run()
        return env.data, env.included

    @abstractmethod
    async def get_relationship_data(self, env):
        """Creates the response data member for GET /{collection} responses.

        Specifically, after this function call completes, the env's data
        member contains something like the following object:

        {
            'type': 'centers',
            'id': '1'
        }
        """

    @abstractmethod
    async def patch(self, document, query):
        """Produces the response for the PATCH
        /{collection}/{id}/relationships/{relationship} request.
        """

    @abstractmethod
    async def post(self, document, query):
        """Produces the response for a POST
        /{collection}/{id}/relationships/{relationship} request.
        """

    @abstractmethod
    async def delete(self, document, query):
        """Produces the response for a DELETE
        /{collection}/{id}/relationships/{relationship} request.
        """

    @abstractmethod
    def put(self):
        """Produces the response for a PUT
        /{collection}/{id}/relationships/{relationship} request.
        """

    @abstractmethod
    def options(self):
        """Produces the response for an OPTIONS
        /{collection}/{id}/relationships/{relationship} request.
        """

    async def verify_id_exists(self, connection):
        """Raises an exception in case the id in the URL does not exist."""
        stmt = f'SELECT FROM data.{self.table.name} WHERE id=$1'
        record = await connection.fetchrow(stmt, self.id.number)
        if record is None:
            raise ErrorsException([
                ResourceNotFoundError(f'/{self.collection.name}/{self.id.name}')
            ])

    def path(self):
        """Creates the path to the relationship."""
        return (f'/{self.collection.name}/{self.id.name}/'
                f'relationships/{self.relationship.name}')


class ToOneRelationship(Relationship):
    """Class ToOneRelationship represents the to-one relationship URI
    (/{collection}/{id}/relationships/{relationship}).
    """

    async def parse_document(self, request):
        """Parses the request document for a valid resource object.

        Args:
            request (Request): the request to be parsed.

        Returns:
            A ResourceIdentifierObjectDocument.

        Raises:
            ErrorsException with all the errors in case the document does not
            represent a valid resource object.
        """

        data = await parse_request_document_data(request)
        document = ResourceIdentifierObjectDocument(data)
        document.parse(self.relationship.rtable.collection.name)
        return document

    async def patch(self, document, query):
        if document.data is not None:
            data_id = document.id
        else:
            data_id = None
        await self.patch_execute(data_id)
        return no_content_response()

    @abstractmethod
    async def patch_execute(self, data_id):
        """Updates the database in response to a PATCH
        /{collection}/{id}/relationships/{relationship} request where
        {relationship} is a to-one relationship.
        """

    async def post(self, document, query):
        """Produces the response for a POST
        /{collection}/{id}/relationships/{relationship} request where
        {relationship} is a to-one relationship.
        """
        return errors_response([MethodNotAllowedError()],
                               headers={'Allow': 'GET,HEAD,OPTIONS,PATCH'})

    async def delete(self, document, query):
        """Produces the response for a DELETE
        /{collection}/{id}/relationships/{relationship} request where
        {relationship} is a to-one relationship.
        """
        return errors_response([MethodNotAllowedError()],
                               headers={'Allow': 'GET,HEAD,OPTIONS,PATCH'})

    def put(self):
        """Produces the response for a DELETE
        /{collection}/{id}/relationships/{relationship} request where
        {relationship} is a to-one relationship.
        """
        return errors_response([MethodNotAllowedError()],
                               headers={'Allow': 'GET,HEAD,OPTIONS,PATCH'})

    def options(self):
        """Produces the response for an OPTIONS
        /{collection}/{id}/relationships/{relationship} request where
        {relationship} is a to-one relationship.
        """
        headers = {'Allow': 'GET,OPTIONS,PATCH'}
        return no_content_response(headers=headers)


class OneToOneLocalRelationship(ToOneRelationship):
    """Class OneToOneLocalRelationship represents the URI
    (/{collection}/{id}/relationships/{relationship}) for a one-to-one
    relationship with a local foreign id.
    """

    async def get_relationship_data(self, env):
        stmt = (f'SELECT {self.relationship.lfkey} '
                f'FROM data.{self.table.name} '
                f'WHERE id=$1')
        async with self.table.pool.acquire() as connection:
            log.debug(f'{stmt}: {self.id.number}')
            record = await connection.fetchrow(stmt, self.id.number)
        if record is None:
            raise ErrorsException([
                ResourceNotFoundError(f'/{self.collection.name}/{self.id.name}')
            ])
        record_id = record[0]
        if record_id is None:
            env.data = None
            return
        env.data = {
            'type': self.relationship.rtable.collection.name,
            'id': id_number_to_name(record_id),
        }

    async def patch_execute(self, data_id):
        # Need to remove other lfkeys that point to data_id_number!
        stmt = (f'UPDATE data.{self.relationship.table.name} '
                f'SET {self.relationship.lfkey} = $1 '
                f'WHERE id=$2')
        if data_id is None:
            data_id_number = None
        else:
            data_id_number = data_id.number
        try:
            async with self.table.pool.acquire() as connection:
                log.debug(f'{stmt}: {data_id_number}, {self.id.number}')
                result = await connection.execute(stmt, data_id_number,
                                                  self.id.number)
            if result == 'UPDATE 0':
                raise ErrorsException([
                    ResourceNotFoundError(
                        f'/{self.collection.name}/{self.id.name}')
                ])
        except UniqueViolationError as exc:
            raise ErrorsException([DocumentDataRelationshipConflictError()
                                  ]) from exc
        except ForeignKeyViolationError as exc:
            raise ErrorsException([
                DocumentDataNonexistentIdError(f'/data/id/{data_id.name}')
            ]) from exc


class OneToOneRemoteRelationship(ToOneRelationship):
    """Class OneToOneRemoteRelationship represents the URI
    (/{collection}/{id}/relationships/{relationship}) for a one-to-one
    relationship with a remote foreign id.
    """

    async def get_relationship_data(self, env):
        stmt = (f'SELECT id '
                f'FROM data.{self.relationship.rtable.name} '
                f'WHERE {self.relationship.rfkey}=$1')
        async with self.table.pool.acquire() as connection:
            async with connection.transaction():
                log.debug(f'{stmt}: {self.id.number}')
                record = await connection.fetchrow(stmt, self.id.number)
                if record is None:
                    await self.verify_id_exists(connection)
                    env.data = None
                    return
        env.data = {
            'type': self.relationship.rtable.collection.name,
            'id': id_number_to_name(record[0]),
        }

    async def patch_execute(self, data_id):
        stmt_remove = (f'UPDATE data.{self.relationship.rtable.name} '
                       f'SET {self.relationship.rfkey} = NULL '
                       f'WHERE {self.relationship.rfkey}=$1')
        async with self.table.pool.acquire() as connection:
            async with connection.transaction():
                log.debug(f'{stmt_remove}: {self.id.number}')
                await connection.execute(stmt_remove, self.id.number)
                if data_id:
                    stmt_add = (f'UPDATE data.{self.relationship.rtable.name} '
                                f'SET {self.relationship.rfkey} = $1 '
                                f'WHERE id=$2 AND '
                                f'({self.relationship.rfkey} IS NULL OR '
                                f'{self.relationship.rfkey}=$1)')
                    try:
                        log.debug(f'{stmt_add}: {self.id.number}, '
                                  f'{data_id.number}')
                        result = await connection.execute(
                            stmt_add, self.id.number, data_id.number)
                        if result == 'UPDATE 0':
                            stmt_verify = (
                                f'SELECT '
                                f'FROM'
                                f' data.{self.relationship.rtable.name} '
                                f'WHERE id=$1')
                            log.debug(stmt_verify)
                            records = await connection.fetch(
                                stmt_verify, data_id.number)
                            if records == []:
                                raise ErrorsException([
                                    DocumentDataNonexistentIdError(
                                        f'/data/id/{data_id.name}')
                                ])
                            raise ErrorsException(
                                [DocumentDataRelationshipConflictError()])
                    except ForeignKeyViolationError as exc:
                        raise ErrorsException([
                            ResourceNotFoundError(
                                f'/{self.collection.name}/{self.id.name}')
                        ]) from exc


class ManyToOneRelationship(ToOneRelationship):
    """Class ManyToOneRelationship represents the URI many-to-one relationship
    URI (/{collection}/{id}/relationships/{relationship}).
    """

    async def get_relationship_data(self, env):
        stmt = (f'SELECT {self.relationship.lfkey} '
                f'FROM data.{self.table.name} '
                f'WHERE id=$1')
        async with self.table.pool.acquire() as connection:
            log.debug(f'{stmt}: {self.id.number}')
            record = await connection.fetchrow(stmt, self.id.number)
        if record is None:
            raise ErrorsException([
                ResourceNotFoundError(f'/{self.collection.name}/{self.id.name}')
            ])
        record_id = record[0]
        if record_id is None:
            env.data = None
            return
        env.data = {
            'type': self.relationship.rtable.collection.name,
            'id': id_number_to_name(record_id),
        }

    async def patch_execute(self, data_id):
        stmt = (f'UPDATE data.{self.table.name} '
                f'SET {self.relationship.lfkey} = $1 '
                f'WHERE id=$2')
        if data_id is None:
            data_id_number = None
        else:
            data_id_number = data_id.number
        try:
            async with self.table.pool.acquire() as connection:
                log.debug(f'{stmt}: {data_id_number}, {self.id.number}')
                result = await connection.execute(stmt, data_id_number,
                                                  self.id.number)
            if result == 'UPDATE 0':
                raise ErrorsException([
                    ResourceNotFoundError(
                        f'/{self.collection.name}/{self.id.name}')
                ])
        except ForeignKeyViolationError as exc:
            raise ErrorsException([
                DocumentDataNonexistentIdError(f'/data/id/{data_id.name}')
            ]) from exc


class ToManyRelationship(Relationship):
    """Class ToOneRelationship represents the to-many relationship URI
    (/{collection}/{id}/relationships/{relationship}).
    """

    async def parse_document(self, request):
        """Parses the request document for a valid resource object.

        Args:
            request (Request): the request to be parsed.

        Returns:
            A ResourceIdentifierObjectsDocument.

        Raises:
            ErrorsException with all the errors in case the document does not
            represent a valid resource object.
        """

        data = await parse_request_document_data(request)
        document = ResourceIdentifierObjectsDocument(data)
        document.parse(self.relationship.rtable.collection.name)
        return document

    async def patch(self, document, query):
        await self.patch_execute(document.ids)
        return no_content_response()

    @abstractmethod
    async def patch_execute(self, data_ids):
        """Updates the database in response to a PATCH
        /{collection}/{id}/relationships/{relationship} request where
        {relationship} is a to-many relationship.
        """

    async def post(self, document, query):
        """Produces the response for a POST
        /{collection}/{id}/relationships/{relationship} request where
        {relationship} is a to-many relationship.
        """
        await self.post_execute(document.ids)
        return no_content_response()

    @abstractmethod
    async def post_execute(self, data_ids):
        """Updates the database in response to a POST
        /{collection}/{id}/relationships/{relationship} request where
        {relationship} is a to-many relationship.
        """

    async def delete(self, document, query):
        """Produces the response for a POST
        /{collection}/{id}/relationships/{relationship} request where
        {relationship} is a to-many relationship.
        """
        await self.delete_execute(document.ids)
        return no_content_response()

    def put(self):
        """Produces the response for a DELETE
        /{collection}/{id}/relationships/{relationship} request where
        {relationship} is a to-one relationship.
        """
        return errors_response(
            [MethodNotAllowedError()],
            headers={'Allow': 'DELETE,GET,HEAD,OPTIONS,PATCH,POST'})

    def options(self):
        """Produces the response for an OPTIONS
        /{collection}/{id}/relationships/{relationship} request where
        {relationship} is a to-one relationship.
        """
        headers = {'Allow': 'DELETE,GET,OPTIONS,PATCH,POST'}
        return no_content_response(headers=headers)

    @abstractmethod
    async def delete_execute(self, data_ids):
        """Updates the database in response to a POST
        /{collection}/{id}/relationships/{relationship} request where
        {relationship} is a to-many relationship.
        """


class OneToManyRelationship(ToManyRelationship):
    """Class OneToManyRelationship represents the URI one-to-many relationship
    URI (/{collection}/{id}/relationships/{relationship}).
    """

    async def get_relationship_data(self, env):
        stmt = (f'SELECT id '
                f'FROM data.{self.relationship.rtable.name} '
                f'WHERE {self.relationship.rfkey}=$1')
        async with self.table.pool.acquire() as connection:
            async with connection.transaction():
                log.debug(f'{stmt}: {self.id.number}')
                records = await connection.fetch(stmt, self.id.number)
                if records == []:
                    await self.verify_id_exists(connection)
                    env.data = []
                    return
        env.data = [{
            'type': self.relationship.rtable.collection.name,
            'id': id_number_to_name(record[0]),
        } for record in records]

    async def patch_execute(self, data_ids):
        stmt_remove = (f'UPDATE data.{self.relationship.rtable.name} '
                       f'SET {self.relationship.rfkey} = NULL '
                       f'WHERE {self.relationship.rfkey}=$1')
        async with self.table.pool.acquire() as connection:
            async with connection.transaction():
                log.debug(f'{stmt_remove}: {self.id.number}')
                await connection.execute(stmt_remove, self.id.number)
                if data_ids:
                    stmt_add = (f'UPDATE data.{self.relationship.rtable.name} '
                                f'SET {self.relationship.rfkey} = $1 '
                                f'WHERE id=any($2::UUID[])')
                    data_id_numbers = [data_id.number for data_id in data_ids]
                    try:
                        log.debug(f'{stmt_add}: {self.id.number}, '
                                  f'{data_id_numbers}')
                        result = await connection.execute(
                            stmt_add, self.id.number, data_id_numbers)
                        if result != f'UPDATE {len(data_ids)}':
                            stmt_verify = (
                                f'SELECT id '
                                f'FROM'
                                f' data.{self.relationship.rtable.name} '
                                f'WHERE id=ANY($1::UUID[])')
                            log.debug(stmt_verify)
                            records = await connection.fetch(
                                stmt_verify, data_id_numbers)
                            records_set = set(records)
                            errors = [
                                DocumentDataNonexistentIdError(
                                    f'/data/{index}/id/{data_id.name}')
                                for index, data_id in enumerate(data_ids)
                                if data_id.number not in records_set
                            ]
                            raise ErrorsException(errors)
                    except ForeignKeyViolationError as exc:
                        raise ErrorsException([
                            ResourceNotFoundError(
                                f'/{self.collection.name}/{self.id.name}')
                        ]) from exc
                else:
                    await self.verify_id_exists(connection)

    async def post_execute(self, data_ids):
        if data_ids:
            stmt = (f'UPDATE data.{self.relationship.rtable.name} '
                    f'SET {self.relationship.rfkey} = $1 '
                    f'WHERE id=ANY($2::UUID[])')
            data_id_numbers = [data_id.number for data_id in data_ids]
            async with self.table.pool.acquire() as connection:
                async with connection.transaction():
                    try:
                        log.debug(f'{stmt}: {self.id.number}, '
                                  f'{data_id_numbers}')
                        result = await connection.execute(
                            stmt, self.id.number, data_id_numbers)
                    except ForeignKeyViolationError as exc:
                        raise ErrorsException([
                            ResourceNotFoundError(
                                f'/{self.collection.name}/{self.id.name}')
                        ]) from exc
                    if result != f'UPDATE {len(data_ids)}':
                        stmt_verify = (
                            f'SELECT id '
                            f'FROM data.{self.relationship.rtable.name} '
                            f'WHERE id=ANY($1::UUID[])')
                        log.debug(f'{stmt_verify}: {data_id_numbers}')
                        records = await connection.fetch(
                            stmt_verify, data_id_numbers)
                        records_set = set(records)
                        errors = [
                            DocumentDataNonexistentIdError(
                                f'/data/{index}/id/{data_id.name}')
                            for index, data_id in enumerate(data_ids)
                            if data_id.number not in records_set
                        ]
                        raise ErrorsException(errors)
        else:
            async with self.table.pool.acquire() as connection:
                await self.verify_id_exists(connection)

    async def delete_execute(self, data_ids):
        if data_ids:
            stmt = (f'UPDATE data.{self.relationship.rtable.name} '
                    f'SET {self.relationship.rfkey} = NULL '
                    f'WHERE {self.relationship.rfkey}=$1 AND '
                    f'id=ANY($2::UUID[])')
            data_id_numbers = [data_id.number for data_id in data_ids]
            async with self.table.pool.acquire() as connection:
                async with connection.transaction():
                    log.debug(f'{stmt}: {self.id.number}, {data_id_numbers}')
                    result = await connection.execute(stmt, self.id.number,
                                                      data_id_numbers)
                    if result == 'UPDATE 0':
                        await self.verify_id_exists(connection)
        else:
            async with self.table.pool.acquire() as connection:
                await self.verify_id_exists(connection)


class ManyToManyRelationship(ToManyRelationship):
    """Class ManyToManyRelationship represents the URI many-to-many relationship
    URI (/{collection}/{id}/relationships/{relationship}).
    """

    async def get_relationship_data(self, env):
        stmt = (f'SELECT {self.relationship.rafkey} '
                f'FROM data.{self.relationship.atable.name} '
                f'WHERE {self.relationship.lafkey}=$1')
        async with self.table.pool.acquire() as connection:
            async with connection.transaction():
                log.debug(f'{stmt}: {self.id.number}')
                records = await connection.fetch(stmt, self.id.number)
                if records == []:
                    await self.verify_id_exists(connection)
                    env.data = []
                    return
        env.data = [{
            'type': self.relationship.rtable.collection.name,
            'id': id_number_to_name(record[0]),
        } for record in records]

    async def patch_execute(self, data_ids):
        stmt_remove = (f'DELETE FROM data.{self.relationship.atable.name} '
                       f'WHERE {self.relationship.lafkey}=$1')
        stmt_add = (f'INSERT INTO data.{self.relationship.atable.name} '
                    f'({self.relationship.lafkey}, '
                    f'{self.relationship.rafkey}) '
                    f'VALUES ($1, $2)')
        values = [(self.id.number, data_id.number) for data_id in data_ids]
        async with self.table.pool.acquire() as connection:
            async with connection.transaction():
                try:
                    async with connection.transaction():
                        log.debug(f'{stmt_remove}: {self.id.number}')
                        await connection.execute(stmt_remove, self.id.number)
                        log.debug(f'{stmt_add}: {values}')
                        await connection.executemany(stmt_add, values)
                except ForeignKeyViolationError as exc:
                    async with connection.transaction():
                        await self.on_foreign_key_violation_error(
                            connection, exc, data_ids)

    async def post_execute(self, data_ids):
        if data_ids:
            # To prevent duplicates, we first remove any existing associations
            stmt_remove = (f'DELETE FROM data.{self.relationship.atable.name} '
                           f'WHERE {self.relationship.lafkey}=$1 AND '
                           f'{self.relationship.rafkey}=ANY($2::UUID[])')
            stmt_add = (f'INSERT INTO data.{self.relationship.atable.name} '
                        f'({self.relationship.lafkey}, '
                        f'{self.relationship.rafkey}) '
                        f'VALUES ($1, $2)')
            data_id_numbers = [data_id.number for data_id in data_ids]
            values = [(self.id.number, data_id.number) for data_id in data_ids]
            async with self.table.pool.acquire() as connection:
                async with connection.transaction():
                    try:
                        async with connection.transaction():
                            log.debug(f'{stmt_remove}: {self.id.number}, '
                                      f'{data_id_numbers}')
                            await connection.execute(stmt_remove,
                                                     self.id.number,
                                                     data_id_numbers)
                            log.debug(f'{stmt_add}: {values}')
                            await connection.executemany(stmt_add, values)
                    except ForeignKeyViolationError as exc:
                        async with connection.transaction():
                            await self.on_foreign_key_violation_error(
                                connection, exc, data_ids)
        else:
            async with self.table.pool.acquire() as connection:
                await self.verify_id_exists(connection)

    async def delete_execute(self, data_ids):
        if data_ids:
            stmt = (f'DELETE FROM data.{self.relationship.atable.name} '
                    f'WHERE {self.relationship.lafkey}=$1 AND '
                    f'{self.relationship.rafkey}=ANY($2::UUID[])')
            data_id_numbers = [data_id.number for data_id in data_ids]
            async with self.table.pool.acquire() as connection:
                async with connection.transaction():
                    log.debug(f'{stmt}: {self.id.number}, {data_id_numbers}')
                    result = await connection.execute(stmt, self.id.number,
                                                      data_id_numbers)
                    if result == 'DELETE 0':
                        await self.verify_id_exists(connection)
        else:
            async with self.table.pool.acquire() as connection:
                await self.verify_id_exists(connection)

    async def on_foreign_key_violation_error(self, connection, exc, data_ids):
        """Handles a ForeignKeyViolationError on changing the association
        table.
        """
        detail = exc.detail  # pylint: disable=no-member
        groups = RE_FOREIGN_KEY_VIOLATION_ERROR_DETAIL.match(detail).groups()
        if groups[0] == self.relationship.lafkey:
            raise ErrorsException([
                ResourceNotFoundError(f'/{self.collection.name}/{self.id.name}')
            ])
        # groups[0] == self.relationship.rafkey

        stmt_verify = (f'SELECT {self.relationship.rafkey} '
                       f'FROM data.{self.relationship.atable.name} '
                       f'WHERE {self.relationship.lafkey}=$1')
        log.debug(f'{stmt_verify}: {self.id.number}')
        records = await connection.fetch(stmt_verify, self.id.number)
        errors = [
            DocumentDataNonexistentIdError(f'/data/{index}/id/{data_id.name}')
            for index, data_id in enumerate(data_ids)
            if data_id.number not in set(records)
        ]
        raise ErrorsException(errors)


class GetRelationshipEnvironment:
    """Class GetRelatedResourceEnvironment is the execution environment
    for a generating a GET /{collection}/{id}/relationships/{relationship}
    response.
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, relationship, query):
        self.relationship = relationship
        self.query = query
        self.tasks = []
        self.connection = None
        self.lock = Lock()
        self.data_environment = None
        self.data = None
        self.included_environments = []
        self.included = None

    def create_data_environment(self):
        """Creates the environment for collecting the data member of a GET
        /{collection}/{id}/relationships/{relationship} response.
        """
        self.data_environment = GetRelationshipDataEnvironment(self)

    def create_included_environments(self, ids, includes):
        """Creates the environment for collecting the included member of a
        GET /{collection}/{id}/relationships/{relationships} response.
        """
        if includes is None:
            return
        for relationship, remote_includes in includes.items():
            remote_collection = relationship.rtable.collection
            remote_ids = relationship.object_remote_ids(ids)
            self.included_environments.append(
                GetObjectIncludedEnvironment(self.relationship.id.number,
                                             remote_collection, remote_ids,
                                             self))
            if remote_includes:
                self.create_included_environments(remote_ids, remote_includes)

    def create_tasks(self):
        """Create all tasks for querying the database to create a GET
        /{collection}/{id}/relationships/{relationship} response.
        """
        self.create_data_environment()
        self.create_included_environments(None, self.query['includes'])
        self.tasks = [
            create_task(env.run()) for env in chain([self.data_environment],
                                                    self.included_environments)
        ]

    async def run(self):
        """Executes the GET /{collection}/{id}/relationships/{relationship}
        tasks.
        """

        async with self.relationship.table.pool.acquire() as self.connection:
            async with self.connection.transaction():
                self.create_tasks()
                await gather(*self.tasks)
        self.data = self.data_environment.data
        if self.query['includes']:
            self.included = list(
                chain.from_iterable(env.included_by_id.values()
                                    for env in self.included_environments))


class GetRelationshipDataEnvironment:
    """Class GetRelationshipDataEnvironment is the execution environment for
    the data part of the GET /{collection}/{id}/relationships/{relationship}
    response.
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, env):
        self.relationship = env.relationship
        self.query = env.query
        self.tasks = []
        self.connection = env.connection
        self.lock = env.lock
        self.data = None

    def create_tasks(self):
        """Create all tasks for querying the database to create a GET
        /{collection}/{id}/relationships/{relationship} response.
        """
        self.tasks = [
            create_task(self.relationship.get_relationship_data(self))
        ]

    async def run(self):
        """Executes the environment to generate the data member of the GET
        /{collection}/{id}/relationships/{relationship} response.
        """
        self.create_tasks()
        await gather(*self.tasks)


def make_relationship(collection_name, id_name, relationship_name):
    """Returns the relationship URI
    (/{collection}/{id}/relationships/{relationship}) corresponding to the user
    provided model relationships.

    Args:
        collection_name (str): Name of the collection.
        id_name (str): Name of the id.
        relationship_name (str): Name of the relationship.

    Returns:
        An instantiated object of the correct derived class of Relationship.
    """

    try:
        collection = Collection.by_name[collection_name]
    except KeyError as exc:
        raise ErrorsException([ResourceNotFoundError(f'/{collection_name}')
                              ]) from exc

    try:
        id_ = IdValue(id_name)
    except ValueError as exc:
        raise ErrorsException([
            ResourceNotFoundMalformedIdError(f'/{collection_name}/{id_name}')
        ]) from exc

    try:
        relationship = getattr(collection.table.___, relationship_name)
    except AttributeError as exc:
        raise ErrorsException([
            ResourceNotFoundError(f'/{collection_name}/{id_name}/'
                                  f'relationships/{relationship_name}')
        ]) from exc

    return relationship.make_uri_relationship(collection, id_)


def parse(request):
    """Gets a relationship URI associated with a request.

    Args:
        request: Incoming Http(s) request.

    Returns:
        A URI relationship.

    Exceptions:
        ErrorsException: Exception containing a 'resource not found' error.
    """

    collection_name = request.match_info['collection']
    id_name = request.match_info['id']
    relationship_name = request.match_info['relationship']
    return make_relationship(collection_name, id_name, relationship_name)
