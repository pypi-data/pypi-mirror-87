# Copyright © 2019-2020 Roel van der Goot
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
"""Module uri.related provides things related to related resource URIs."""

from abc import abstractmethod
from asyncio import Event, Lock, create_task, gather
from itertools import chain
from json import loads

from ajsonapi.conversions import id_number_to_name
from ajsonapi.environments import GetObjectIncludedEnvironment
from ajsonapi.errors import (
    ResourceNotFoundError,
    ResourceNotFoundMalformedIdError,
)
from ajsonapi.exceptions import ErrorsException
from ajsonapi.id_value import IdValue
from ajsonapi.logging import log
from ajsonapi.responses import document_response
from ajsonapi.types import Json
from ajsonapi.uri.collection import Collection
from ajsonapi.uri.resource import Resource


class RelatedResource(Resource):
    """Class RelatedResource represents the related resource URI
    (/{collection}/{id}/{related_resource}).
    """

    def __init__(self, name, collection, id_, relationship):
        self.related_resource_name = name
        self.collection = collection
        self.id = id_  # pylint: disable=invalid-name
        self.relationship = relationship
        self.table = collection.table

    async def get(self, query):
        """Produces the response for the GET
        /{collection}/{id}/{related_resource} request.
        """
        links = {'self': self.path()}
        return document_response(await self.to_document(query=query,
                                                        links=links))

    async def to_document(self, query=None, links=None):
        """Creates the document for the resource object(s) that are part of
        the related resource.
        """

        data, included = await self.to_data_included(query)
        document = {'data': data}
        if included is not None:
            document['included'] = included
        if links:
            document['links'] = links
        return document

    @abstractmethod
    def is_to_many(self):
        """Returns if the related resource is a to-many related resource."""

    @abstractmethod
    async def to_data_included(self, query):
        """Creates the document's data and included member values for this
        related resource.
        """

    @abstractmethod
    async def get_related_data(self, env):
        """Creates the response data member for attributes and local related
        resources.

        Specifically, after this call the environment's data or data_by_lid
        member is updated."""

    async def verify_id_exists(self, env):
        """Raises an exception in case the id in the URL does not exist."""
        stmt = f'SELECT FROM data.{self.table.name} WHERE id = $1'
        record = await env.connection.fetchrow(stmt, self.id.number)
        if record is None:
            env.cancel()
            raise ErrorsException([
                ResourceNotFoundError(f'/{self.collection.name}/{self.id.name}')
            ])

    def path(self):
        """Creates the path to the relationship."""
        return (f'/{self.collection.name}/{self.id.name}/'
                f'{self.related_resource_name}')


class ToOneRelatedResource(RelatedResource):
    """Class ToOneRelatedResource represents the to-one related resource URI
    (/{collection}/{id}/{related_resource}).
    """

    def is_to_many(self):
        return False

    async def to_data_included(self, query):
        """Creates the document's data and included member values for this
        related resources.
        """

        env = GetToOneRelatedResourceEnvironment(self, query)
        await env.run()
        return env.data, env.included

    def record_to_data(self, record):
        """Converts a asyncpg record into a JSON API data member."""
        attributes = {}
        relationships = {}
        for col_name, value in record.items():
            if col_name == 'id':
                id_name = id_number_to_name(value)
            elif col_name in self.relationship.rtable.attributes_by_name:
                col = self.relationship.rtable.attributes_by_name[col_name]
                if col.type_ == Json:  # Should we use a virtual function?
                    attributes[col_name] = loads(value)
                else:
                    attributes[col_name] = value
            else:  # col_name is a lfkey
                rel = self.relationship.rtable.relationship_by_lfkey[col_name]
                relationships[rel.name] = self.to_relationships(rel, value)
        data = {
            'type': self.relationship.rtable.collection.name,
            'id': id_name,
        }
        if attributes:
            data['attributes'] = attributes
        if relationships:
            data['relationships'] = relationships
        return data

    @abstractmethod
    async def get_related_data(self, env):
        pass


class OneToOneLocalRelatedResource(ToOneRelatedResource):
    """Class OneToOneLocalRelatedResource represents the URI
    (/{collection}/{id}/{related_resource}) for a one-to-one related resource
    with a local foreign id.
    """

    async def get_related_data(self, env):
        query_fields = env.query['fields']
        rtable = self.relationship.rtable
        if rtable.collection in query_fields:
            columns = chain(['id'], (str(col)
                                     for col in rtable.columns
                                     if col in query_fields[rtable.collection]))
        else:
            columns = (str(col) for col in rtable.columns)
        stmt = (f'SELECT {", ".join(columns)} '
                f'FROM data.{rtable.name} '
                f'WHERE id = ('
                f' SELECT {self.relationship.lfkey}'
                f' FROM data.{self.table.name}'
                f' WHERE id = $1)')
        async with env.lock:
            log.debug(f'{stmt}: {self.id.number}')
            record = await env.connection.fetchrow(stmt, self.id.number)
            if record is None:
                await self.verify_id_exists(env)
                env.data = None
                env.event.set()
                return
        env.data = self.record_to_data(record)
        env.event.set()


class OneToOneRemoteRelatedResource(ToOneRelatedResource):
    """Class OneToOneRemoteRelatedResource represents the URI
    (/{collection}/{id}/{related_resource}) for a one-to-one related resource
    with a remote foreign id.
    """

    async def get_related_data(self, env):
        query_fields = env.query['fields']
        rtable = self.relationship.rtable
        if rtable.collection in query_fields:
            columns = chain(['id'], (str(col)
                                     for col in rtable.columns
                                     if col in query_fields[rtable.collection]))
        else:
            columns = (str(col) for col in rtable.columns)
        # We could remove rfkey because we know it already.
        stmt = (f'SELECT {", ".join(columns)} '
                f'FROM data.{self.relationship.rtable.name} '
                f'WHERE {self.relationship.rfkey} = $1')
        async with env.lock:
            log.debug(f'{stmt}: {self.id.number}')
            record = await env.connection.fetchrow(stmt, self.id.number)
            if record is None:
                await self.verify_id_exists(env)
                env.data = None
                env.event.set()
                return
        env.data = self.record_to_data(record)
        env.event.set()


class ManyToOneRelatedResource(ToOneRelatedResource):
    """Class ManyToOneRelatedResource represents the URI
    (/{collection}/{id}/{related_resource}) for a many-to-one related
    resource.
    """

    async def get_related_data(self, env):
        query_fields = env.query['fields']
        rtable = self.relationship.rtable
        if rtable.collection in query_fields:
            columns = chain(['id'], (str(col)
                                     for col in rtable.columns
                                     if col in query_fields[rtable.collection]))
        else:
            columns = (str(col) for col in self.relationship.rtable.columns)
        stmt = (f'SELECT {", ".join(columns)} '
                f'FROM data.{self.relationship.rtable.name} '
                f'WHERE id = ('
                f' SELECT {self.relationship.lfkey}'
                f' FROM data.{self.table.name}'
                f' WHERE id = $1)')
        async with env.lock:
            log.debug(f'{stmt}: {self.id.number}')
            record = await env.connection.fetchrow(stmt, self.id.number)
            if record is None:
                await self.verify_id_exists(env)
                env.data = None
                env.event.set()
                return
        env.data = self.record_to_data(record)
        env.event.set()


class ToManyRelatedResource(RelatedResource):
    """Class ToManyRelatedResource represents the to-one related resource URI
    (/{collection}/{id}/{related_resource}).
    """

    def is_to_many(self):
        return True

    async def to_data_included(self, query):
        """Creates the document's data and included member values for this
        related resources.
        """

        env = GetToManyRelatedResourceEnvironment(self, query)
        await env.run()
        return env.data, env.included

    def record_to_data(self, record):
        """Converts a asyncpg record into a JSON API data member."""
        attributes = {}
        relationships = {}
        for col_name, value in record.items():
            if col_name == 'id':
                id_name = id_number_to_name(value)
            elif col_name in self.relationship.rtable.attributes_by_name:
                attributes[col_name] = value
            else:  # col_name is a lfkey
                rel = self.relationship.rtable.relationship_by_lfkey[col_name]
                if value:
                    relationship_data = {
                        'type': rel.rtable.collection.name,
                        'id': id_number_to_name(value)
                    }
                else:
                    relationship_data = None
                relationships[rel.name] = {
                    'data': relationship_data,
                    'links': {
                        'self': (f'/{self.relationship.name}/{id_name}/'
                                 f'relationships/{rel.name}'),
                        'related': (f'/{self.relationship.name}/{id_name}/'
                                    f'{rel.name}'),
                    }
                }
        data = {
            'type': self.relationship.rtable.collection.name,
            'id': id_name,
        }
        if attributes:
            data['attributes'] = attributes
        if relationships:
            data['relationships'] = relationships
        return data

    @abstractmethod
    async def get_related_data(self, env):
        pass


class OneToManyRelatedResource(ToManyRelatedResource):
    """Class OneToManyRelatedResource represents the URI
    (/{collection}/{id}/{related_resource}) for a one-to-many related
    resource.
    """

    async def get_related_data(self, env):
        query_fields = env.query['fields']
        rtable = self.relationship.rtable
        if rtable.collection in query_fields:
            columns = chain(['id'], (str(col)
                                     for col in rtable.columns
                                     if col in query_fields[rtable.collection]))
        else:
            columns = (str(col) for col in rtable.columns)
        # We could remove rfkey because we know it already
        filters = env.query['filters']
        sort = env.query['sort']
        if filters:
            if sort:
                stmt = (f'SELECT {", ".join(columns)} '
                        f'FROM data.{self.relationship.rtable.name} '
                        f'WHERE {self.relationship.rfkey} = $1 AND '
                        f'{" AND ".join(filters)} '
                        f'ORDER BY {", ".join(sort)}')
            else:
                stmt = (f'SELECT {", ".join(columns)} '
                        f'FROM data.{self.relationship.rtable.name} '
                        f'WHERE {self.relationship.rfkey} = $1 AND '
                        f'{" AND ".join(filters)}')
        else:
            if sort:
                stmt = (f'SELECT {", ".join(columns)} '
                        f'FROM data.{self.relationship.rtable.name} '
                        f'WHERE {self.relationship.rfkey} = $1 '
                        f'ORDER BY {", ".join(sort)}')
            else:
                stmt = (f'SELECT {", ".join(columns)} '
                        f'FROM data.{self.relationship.rtable.name} '
                        f'WHERE {self.relationship.rfkey} = $1')
        async with env.lock:
            log.debug(f'{stmt}: {self.id.number}')
            records = await env.connection.fetch(stmt, self.id.number)
            if records == []:
                await self.verify_id_exists(env)
        env.data_by_lid = {
            record['id']: self.record_to_data(record) for record in records
        }
        env.event.set()


class ManyToManyRelatedResource(ToManyRelatedResource):
    """Class ManyToManyRelatedResource represents the URI
    (/{collection}/{id}/{related_resource}) for a many-to-many related
    resource.
    """

    async def get_related_data(self, env):
        query_fields = env.query['fields']
        rtable = self.relationship.rtable
        if rtable.collection in query_fields:
            columns = chain(['id'], (str(col)
                                     for col in rtable.columns
                                     if col in query_fields[rtable.collection]))
        else:
            columns = (str(col) for col in rtable.columns)
        filters = env.query['filters']
        sort = env.query['sort']
        if filters:
            if sort:
                stmt = (f'SELECT {", ".join(columns)} '
                        f'FROM data.{self.relationship.rtable.name} '
                        f'WHERE id IN ('
                        f' SELECT {self.relationship.rafkey}'
                        f' FROM data.{self.relationship.atable.name}'
                        f' WHERE {self.relationship.lafkey} = $1) AND'
                        f' {" AND ".join(filters)} '
                        f'ORDER BY {", ".join(sort)}')
            else:
                stmt = (f'SELECT {", ".join(columns)} '
                        f'FROM data.{self.relationship.rtable.name} '
                        f'WHERE id IN ('
                        f' SELECT {self.relationship.rafkey}'
                        f' FROM data.{self.relationship.atable.name}'
                        f' WHERE {self.relationship.lafkey} = $1) AND'
                        f' {" AND ".join(filters)}')
        else:
            if sort:
                stmt = (f'SELECT {", ".join(columns)} '
                        f'FROM data.{self.relationship.rtable.name} '
                        f'WHERE id IN ('
                        f' SELECT {self.relationship.rafkey}'
                        f' FROM data.{self.relationship.atable.name}'
                        f' WHERE {self.relationship.lafkey} = $1) '
                        f'ORDER BY {", ".join(sort)}')
            else:
                stmt = (f'SELECT {", ".join(columns)} '
                        f'FROM data.{self.relationship.rtable.name} '
                        f'WHERE id IN ('
                        f' SELECT {self.relationship.rafkey}'
                        f' FROM data.{self.relationship.atable.name}'
                        f' WHERE {self.relationship.lafkey} = $1)')
        async with env.lock:
            log.debug(f'{stmt}: {self.id.number}')
            records = await env.connection.fetch(stmt, self.id.number)
            if records == []:
                await self.verify_id_exists(env)
        env.data_by_lid = {
            record['id']: self.record_to_data(record) for record in records
        }
        env.event.set()


class GetRelatedResourceEnvironment:
    """Class GetRelatedResourceEnvironment is the execution environment
    for a GET /{collection}/{id}/{related_resource} request.
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, related, query):
        self.related = related
        self.query = query
        self.tasks = []
        self.connection = None
        self.lock = Lock()
        self.data_environment = None
        self.data = None
        self.included_environments = []
        self.included = None

    @abstractmethod
    def create_data_environment(self):
        """Creates the environment for collecting the data member of a GET
        /{collection}/{id}/{related_resource} response.
        """

    def create_included_environments(self, ids, includes):
        """Creates the environment for collecting the included member of the
        GET /{collection}/{id}/{related_resource} response.
        """
        if includes is None:
            return
        for relationship, remote_includes in includes.items():
            remote_collection = relationship.rtable.collection
            remote_ids = relationship.object_remote_ids(ids)
            self.included_environments.append(
                GetObjectIncludedEnvironment(self.related.id.number,
                                             remote_collection, remote_ids,
                                             self))
            if remote_includes:
                self.create_included_environments(remote_ids, remote_includes)

    def create_tasks(self):
        """Create all tasks for querying the database to create a GET
        /{collection}/{id}/{related_resource} response.
        """
        self.create_data_environment()
        relationship = self.related.relationship
        self.create_included_environments(relationship.object_remote_ids(),
                                          self.query['includes'])
        self.tasks = [
            create_task(env.run()) for env in chain([self.data_environment],
                                                    self.included_environments)
        ]

    async def run(self):
        """Executes the GET /{collection}/{id}/{related_resource} tasks."""

        async with self.related.table.pool.acquire() as self.connection:
            async with self.connection.transaction():
                self.create_tasks()
                await gather(*self.tasks)
        self.data = self.data_environment.get_data()
        if self.query['includes']:
            self.included = list(
                chain.from_iterable(env.included_by_id.values()
                                    for env in self.included_environments))


class GetToOneRelatedResourceEnvironment(GetRelatedResourceEnvironment):
    """Class GetToOneRelatedResourceEnvironment is the execution environment
    for a GET /{collection}/{id}/{related_resource} request where
    related_resource corresponds to a to-one relationship.
    """

    def create_data_environment(self):
        self.data_environment = GetToOneRelatedResourceDataEnvironment(self)


class GetToManyRelatedResourceEnvironment(GetRelatedResourceEnvironment):
    """Class GetToManyRelatedResourceEnvironment is the execution environment
    for a GET /{collection}/{id}/{related_resource} request where
    related_resource corresponds to a to-many relationship.
    """

    def create_data_environment(self):
        self.data_environment = GetToManyRelatedResourceDataEnvironment(self)


class GetRelatedResourceDataEnvironment:
    """Class GetRelatedResourceDataEnvironment is the execution environment
    for a GET /{collection}/{id}/{related_resource} request.
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, env):
        self.related = env.related
        self.query = env.query
        self.tasks = []
        self.gather_future = None
        self.connection = env.connection
        self.lock = env.lock
        self.event = Event()

    @abstractmethod
    def create_tasks(self):
        """Create all tasks for querying the database to create the data
        member of a GET /{collection}/{id}/{related_resource} response.
        """

    async def run(self):
        """Executes the GET /{collection}/{id}/{related_resource} tasks."""

        self.create_tasks()
        self.gather_future = gather(*self.tasks)
        await self.gather_future

    def cancel(self):
        """Cancels the environment."""

        self.gather_future.cancel()


class GetToOneRelatedResourceDataEnvironment(GetRelatedResourceDataEnvironment):
    """Class GetToOneRelatedResourceDataEnvironment is the execution
    environment for the data part of a GET
    /{collection}/{id}/{related_resource} response where related_resource
    corresponds to a to-one relationship.
    """

    def __init__(self, env):
        super().__init__(env)
        self.data = None

    def create_tasks(self):
        """Create all tasks for querying the database to create the data
        member of a GET /{collection}/{id}/{related_resource} response where
        related_resource corresponds to a to-one relationship.
        """
        self.tasks = [create_task(self.related.get_related_data(self))]
        query_fields = self.query['fields']
        if self.related.relationship.rtable.collection in query_fields:
            self.tasks.extend([
                create_task(rel.get_to_one_related_data(self))
                for rel in query_fields[
                    self.related.relationship.rtable.collection]
                if rel in self.related.relationship.rtable.remote_relationships
            ])
        else:
            self.tasks.extend([
                create_task(rel.get_to_one_related_data(self))
                for rel in self.related.relationship.rtable.remote_relationships
            ])

    def get_data(self):
        """Returns the data collected by executing the environment."""
        return self.data


class GetToManyRelatedResourceDataEnvironment(GetRelatedResourceDataEnvironment
                                             ):
    """Class GetToManyRelatedResourceDataEnvironment is the execution
    environment for the data part of a GET
    /{collection}/{id}/{related_resource} response where related_resource
    corresponds to a to-many relationship.
    """

    def __init__(self, env):
        super().__init__(env)
        self.data_by_lid = {}

    def create_tasks(self):
        """Create all tasks for querying the database to create the data
        member of a GET /{collection}/{id}/{related_resource} response where
        related_resource corresponds to a to-many relationship.
        """
        self.tasks = [create_task(self.related.get_related_data(self))]
        query_fields = self.query['fields']
        if self.related.relationship.rtable.collection in query_fields:
            self.tasks.extend([
                create_task(rel.get_to_many_related_data(self))
                for rel in query_fields[
                    self.related.relationship.rtable.collection]
                if rel in self.related.relationship.rtable.remote_relationships
            ])
        else:
            self.tasks.extend([
                create_task(rel.get_to_many_related_data(self))
                for rel in self.related.relationship.rtable.remote_relationships
            ])

    def get_data(self):
        """Returns the data collected by executing the environment."""
        return list(self.data_by_lid.values())


def make_related_resource(collection_name, id_name, related_resource_name):
    """Returns the related resource URI
    (/{collection}/{id}/{related_resource}) corresponding to the user provided
    model relationships.

    Args:
        collection_name (str): Name of the collection.
        id_name (str): Name of the id.
        related_resource_name (str): Name of the related resource.

    Returns:
        An instantiated object of the correct derived class of RelatedResource.
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
        relationship = getattr(collection.table.___, related_resource_name)
    except AttributeError as exc:
        raise ErrorsException([
            ResourceNotFoundError(f'/{collection_name}/{id_name}/'
                                  f'{related_resource_name}')
        ]) from exc

    return relationship.make_uri_related_resource(related_resource_name,
                                                  collection, id_)


def parse(request):
    """Gets a related resource associated with a request.

    Args:
        request: Incoming Http(s) request.

    Returns:
        A URI related resource.

    Exceptions:
        ErrorsException: Exception containing a 'resource not found' error.
    """

    collection_name = request.match_info['collection']
    id_name = request.match_info['id']
    related_resource_name = request.match_info['related_resource']
    return make_related_resource(collection_name, id_name,
                                 related_resource_name)
