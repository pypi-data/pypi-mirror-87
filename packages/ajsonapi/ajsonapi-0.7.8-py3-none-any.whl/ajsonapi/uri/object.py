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
"""Module object provides class Object."""

from asyncio import Event, Lock, create_task, gather
from itertools import chain
from json import loads

from asyncpg.exceptions import (
    CheckViolationError,
    ExclusionViolationError,
    ForeignKeyViolationError,
    NotNullViolationError,
    RestrictViolationError,
    UniqueViolationError,
)

from ajsonapi.conversions import id_number_to_name
from ajsonapi.document import ResourceObjectDocument
from ajsonapi.environments import GetObjectIncludedEnvironment
from ajsonapi.errors import (
    DeleteObjectRemotelyRelatedError,
    ResourceNotFoundError,
    ResourceNotFoundMalformedIdError,
)
from ajsonapi.events import DeleteEvent, UpdateEvent
from ajsonapi.exceptions import ErrorsException, NonexistentRelationshipIdError
from ajsonapi.id_value import IdValue
from ajsonapi.logging import log
from ajsonapi.postgres import convert_violation_error
from ajsonapi.responses import document_response, no_content_response
from ajsonapi.types import Json
from ajsonapi.uri.collection import (
    Collection,
    VerifyRelationshipIdsEnvironment,
    parse_request_document_data,
)
from ajsonapi.uri.resource import Resource


class Object(Resource):
    """Class object represents a resource object."""

    def __init__(self, collection, id_):
        self.collection = collection
        self.id = id_  # pylint: disable=invalid-name
        self.table = collection.table
        self.pool = self.table.pool

    async def parse_document(self, request):
        """Parses the request document for a valid resource object.

        Args:
            request (Request): the request to be parsed.

        Returns:
            A ResourceObjectDocument.

        Raises:
            ErrorsException with all the errors in case the document does not
            represent a valid resource object.
        """

        data = await parse_request_document_data(request)
        document = ResourceObjectDocument(data)
        document.parse(self.collection, self.id.name)  # Needs an id_name
        return document

    async def get(self, query):
        """Produces the response for a GET /{collection}/{id} request."""

        links = {'self': self.path()}
        return document_response(await self.to_document(query=query,
                                                        links=links))

    async def delete(self):
        """Removes the object from the database and produces the response for
        a DELETE /{collection}/{id} request.
        """

        stmt = f'DELETE FROM data.{self.table.name} WHERE id = $1'
        try:
            async with self.table.pool.acquire() as connection:
                log.debug(f'{stmt}: {self.id.number}')
                result = await connection.execute(stmt, self.id.number)
        except ForeignKeyViolationError as exc:
            raise ErrorsException(
                [DeleteObjectRemotelyRelatedError(self.path())]) from exc
        if result == 'DELETE 0':
            raise ErrorsException([ResourceNotFoundError(self.path())])
        event = DeleteEvent({
            'type': self.collection.name,
            'id': id_number_to_name(self.id.number),
        })
        await event.broadcast()
        return no_content_response()

    async def patch(self, document, query):
        """Patches the object in the database and produces the response for a
        PATCH /{collection}/{id} request.
        """

        if document.attributes or document.relationships:
            env = PatchObjectEnvironment(self, document.attributes,
                                         document.relationships, query)
            await env.run()
        links = {'self': self.path()}
        document = await self.to_document(query=query, links=links)
        event = UpdateEvent(document['data'])
        await event.broadcast()
        return document_response(document)

    async def patch_task(self, env):
        """Update the database collection table based on the PATCH
        /{collection}/{id} request.
        """
        local_relationships = {
            self.table.lfkey_by_relationship_name[name]: value
            for name, value in env.relationships.items()
            if name in self.table.lfkey_by_relationship_name
        }
        lfkeys = local_relationships.keys()
        lfkey_values = [id_.number for id_ in local_relationships.values()]
        column_names = chain(env.attributes.keys(), lfkeys)
        column_values = ', '.join(
            f'{col} = ${index+2}' for index, col in enumerate(column_names))
        stmt = (f'UPDATE data.{self.table.name} '
                f'SET {column_values} '
                f'WHERE id = $1')
        try:
            async with env.lock:
                async with env.connection.transaction():
                    log.debug(f'{stmt}: {env.attributes.values()}, '
                              f'{self.id.number}')
                    result = await env.connection.execute(
                        stmt, env.obj.id.number, *env.attributes.values(),
                        *lfkey_values)
            if result == 'UPDATE 0':
                env.cancel()
                raise ErrorsException([ResourceNotFoundError(self.path())])
        except ForeignKeyViolationError as exc:
            env.cancel()
            raise NonexistentRelationshipIdError() from exc
        except (CheckViolationError, ExclusionViolationError,
                NotNullViolationError, RestrictViolationError,
                UniqueViolationError) as exc:
            env.cancel()
            raise ErrorsException([convert_violation_error(exc)]) from exc

    async def to_document(self, query=None, links=None):
        """Creates the document for this resource object.

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
        """Creates the response document's data and included member values."""

        env = GetObjectEnvironment(self, query)
        await env.run()
        return env.data, env.included

    async def get_object_data(self, env):
        """Creates the response data member for attributes and local
        relationships.

        Specifically, after this function call completes, the environment's
        data member contains something like the following object:

        {
            'type': 'centers',
            'id': '1',
            'attributes': {
                'attr_int': 1,
                'attr_str': 'one',
            },
            'relationships': {
                'one_one_local': {
                    'data': {
                        'type': 'one_one_locals',
                        'id': UUID_11,
                    },
                    'links': {
                        'self': '/centers/1/relationships/one_one_local',
                        'related': '/centers/1/one_one_local',
                    },
                },
                'many_one': {
                    'data': {
                        'type': 'many_ones',
                        'id': UUID_31,
                    },
                    'links': {
                        'self': '/centers/1/relationships/many_ones',
                        'related': '/centers/1/many_ones',
                    },
                },
            },
            'links': {
                'self': '/centers/1',
            },
        }
        """
        fields = env.query['fields']
        if self.collection in fields:
            columns = chain(['id'], (str(col)
                                     for col in self.table.columns
                                     if col in fields[self.collection]))
        else:
            columns = (str(col) for col in self.table.columns)
        # We could remove 'id' because we know it already.
        stmt = (f"SELECT {', '.join(columns)} "
                f"FROM data.{self.table.name} WHERE id = $1")
        async with env.lock:
            log.debug(f'{stmt}: {self.id.number}')
            record = await env.connection.fetchrow(stmt, self.id.number)
            if not record:
                env.cancel()
                raise ErrorsException([ResourceNotFoundError(self.path())])
        env.data = self.record_to_data(record)
        env.event.set()

    def record_to_data(self, record):
        """Converts a asyncpg record into a JSON API data member."""
        attributes = {}
        relationships = {}
        for col_name, value in record.items():
            if col_name == 'id':
                continue
            if col_name in self.table.attributes_by_name:
                col = self.table.attributes_by_name[col_name]
                if col.type_ == Json:  # Should we use a virtual function?
                    attributes[col_name] = loads(value)
                else:
                    attributes[col_name] = value
            else:  # col_name is a lfkey
                rel = self.table.relationship_by_lfkey[col_name]
                relationships[rel.name] = self.to_relationships(rel, value)
        data = {
            'type': self.collection.name,
            'id': self.id.name,
        }
        if attributes:
            data['attributes'] = attributes
        if relationships:
            data['relationships'] = relationships
        return data

    def path(self):
        """Creates the path to the collection."""

        return f'/{self.collection.name}/{self.id.name}'


class GetObjectEnvironment:
    """Class GetObjectEnvironment is the execution environment for a GET
    /{collection}/{id} request.
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, obj, query):
        self.obj = obj
        self.query = query
        self.tasks = []
        self.connection = None
        self.lock = Lock()
        self.data_environment = None
        self.data = None
        self.included_environments = []
        self.included = None

    def create_data_environment(self):
        """Creates the environment for collecting the data member of the GET
        /{collection}/{id} response.
        """
        self.data_environment = GetObjectDataEnvironment(self)

    def create_included_environments(self, ids, includes):
        """Creates the environment for collecting the included member of the
        GET /{collection}/{id} response.
        """
        if includes is None:
            return
        for relationship, remote_includes in includes.items():
            remote_collection = relationship.rtable.collection
            remote_ids = relationship.object_remote_ids(ids)
            self.included_environments.append(
                GetObjectIncludedEnvironment(self.obj.id.number,
                                             remote_collection, remote_ids,
                                             self))
            if remote_includes:
                self.create_included_environments(remote_ids, remote_includes)

    def create_tasks(self):
        """Creates all the tasks to generate the GET /{collection}/{id}
        response.
        """

        self.create_data_environment()
        self.create_included_environments(None, self.query['includes'])
        self.tasks = [
            create_task(env.run()) for env in chain([self.data_environment],
                                                    self.included_environments)
        ]

    async def run(self):
        """Executes the GET /{collection}/{id} tasks."""

        async with self.obj.table.pool.acquire() as self.connection:
            async with self.connection.transaction():
                self.create_tasks()
                await gather(*self.tasks)
        self.data = self.data_environment.data
        if self.query['includes']:
            self.included = list(
                chain.from_iterable(env.included_by_id.values()
                                    for env in self.included_environments))


class GetObjectDataEnvironment:
    """Class GetCollectionDataEnvironment is the execution environment for the
    data part of the GET /{collection}/{id} response.
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, env):
        self.obj = env.obj
        self.query = env.query
        self.tasks = []
        self.gather_future = None
        self.connection = env.connection
        self.lock = env.lock
        self.data = None
        self.event = Event()

    def create_tasks(self):
        """Creates all the tasks for querying the database to generate the
        data part of a GET /{collection}/{id} response.
        """

        self.tasks = [create_task(self.obj.get_object_data(self))]
        query_fields = self.query['fields']
        if self.obj.collection in query_fields:
            self.tasks.extend([
                create_task(rel.get_object_data(self))
                for rel in query_fields[self.obj.collection]
                if rel in self.obj.table.remote_relationships
            ])
        else:
            self.tasks.extend([
                create_task(rel.get_object_data(self))
                for rel in self.obj.table.remote_relationships
            ])

    async def run(self):
        """Executes the GET /{collection}/{id} tasks."""

        self.create_tasks()
        self.gather_future = gather(*self.tasks)
        await self.gather_future

    def cancel(self):
        """Cancels the environment."""

        self.gather_future.cancel()


class PatchObjectEnvironment:
    """Class PatchObjectEnvironment is the execution environment for a PATCH
    /{collection}/{id} request.
    """

    # pylint: disable=too-many-instance-attributes
    def __init__(self, obj, attributes, relationships, query):
        self.obj = obj
        self.attributes = attributes
        self.relationships = relationships
        self.query = query
        self.connection = None
        self.lock = Lock()
        self.tasks = []
        self.gather_future = None

    def create_tasks(self):
        """Creates all the tasks to execute the PATCH /{collection}/{id}
        request.
        """
        self.tasks = [create_task(self.obj.patch_task(self))]
        self.tasks.extend([
            create_task(rel.patch_object_task(self))
            for rel in self.obj.table.remote_relationships
            if rel.name in self.relationships
        ])

    async def run(self):
        """Executes the PATCH /{collection}/{id} tasks."""

        async with self.obj.table.pool.acquire() as self.connection:
            async with self.connection.transaction():
                try:
                    async with self.connection.transaction():
                        self.create_tasks()
                        self.gather_future = gather(*self.tasks)
                        await self.gather_future
                except NonexistentRelationshipIdError:
                    env = VerifyRelationshipIdsEnvironment(
                        self.obj.table, self.relationships, self.connection)
                    await env.run()

    def cancel(self):
        """Cancels the environment."""

        self.gather_future.cancel()


def parse(request):
    """Gets an object associated with the request.

    Args:
        request: Incoming Http(s) request.

    Exceptions:
        ErrorsException: Exception containing a 'resource not found' error.
    """

    collection_name = request.match_info['collection']
    id_name = request.match_info['id']

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

    return Object(collection, id_)
