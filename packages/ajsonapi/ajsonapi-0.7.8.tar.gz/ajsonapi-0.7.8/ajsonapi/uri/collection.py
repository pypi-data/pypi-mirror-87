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
"""Module collection provides class Collection."""

from abc import abstractmethod
from asyncio import Event, Lock, create_task, gather
from itertools import chain
from json import loads
from re import compile as re_compile

from asyncpg.exceptions import (
    CheckViolationError,
    ExclusionViolationError,
    ForeignKeyViolationError,
    NotNullViolationError,
    RestrictViolationError,
    UniqueViolationError,
)

from ajsonapi.conversions import id_number_to_name
from ajsonapi.document import (
    ResourceObjectDocument,
    parse_request_document_data,
)
from ajsonapi.environments import GetCollectionIncludedEnvironment
from ajsonapi.errors import (
    FilterInvalidFieldError,
    IncludeInvalidPathError,
    QueryParameterUnsupportedError,
    ResourceNotFoundError,
    SortInvalidFieldError,
)
from ajsonapi.events import CreateEvent
from ajsonapi.exceptions import ErrorsException, NonexistentRelationshipIdError
from ajsonapi.logging import log
from ajsonapi.postgres import (
    convert_unique_violation_error,
    convert_violation_error,
)
from ajsonapi.query import parse_fields, parse_page, query_has_parameter
from ajsonapi.responses import document_response, no_content_response
from ajsonapi.types import Json
from ajsonapi.uri.resource import Resource

RE_FILTER = re_compile(r'filter\[([^\]]*)\]')


class Collection(Resource):
    """Class collection represents a resource collection."""

    # pylint: disable=too-many-public-methods

    by_name = {}

    def __init__(self, name, json_api):
        self.name = name
        self.table = json_api

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
        document.parse(self)
        return document

    def parse_query(self,
                    request,
                    *,
                    allow_include=False,
                    allow_fields=False,
                    allow_filter=False,
                    allow_sort=False,
                    allow_page=False):
        """Parses the query parameters relative to this collection."""

        # pylint: disable=no-self-use,too-many-arguments

        query = {}
        errors = []

        request_query = request.query
        self.parse_include(request_query, query, errors, allow=allow_include)
        parse_fields(request_query, query, errors, allow=allow_fields)
        self.parse_filter(request_query, query, errors, allow=allow_filter)
        self.parse_sort(request_query, query, errors, allow=allow_sort)
        parse_page(request_query, query, errors, allow=allow_page)

        if errors:
            raise ErrorsException(errors)
        return query

    def parse_include(self, request_query, query, errors, allow):
        """Parses the request's include query parameter."""

        if query_has_parameter(request_query, 'include'):
            if allow:
                query['includes'] = self.includes_dict(
                    request_query['include'].split(','), errors, [])
            else:
                errors.append(QueryParameterUnsupportedError('include'))
        else:
            query['includes'] = None

    def parse_filter(self, request_query, query, errors, allow):
        """Parses the request's filter query parameter."""

        if query_has_parameter(request_query, 'filter'):
            if allow:
                query['filters'] = self.filters_list(request_query, errors)
            else:
                errors.append(QueryParameterUnsupportedError('filter'))
        else:
            query['filters'] = None

    def parse_sort(self, request_query, query, errors, allow):
        """Parses the request's sort query parameter."""

        if query_has_parameter(request_query, 'sort'):
            if allow:
                query['sort'] = self.sort_list(request_query, errors)
            else:
                errors.append(QueryParameterUnsupportedError('sort'))
        else:
            query['sort'] = None

    def includes_dict(self, include_parameters, errors, path):
        """Helper function for parsing request query include parameters."""
        return_dict = {}
        for include_parameter in include_parameters:
            include, *sub_includes = include_parameter.split('.', 1)
            path.append(include)
            try:
                relationship = getattr(self.table.___, include)
            except AttributeError:
                errors.append(IncludeInvalidPathError('.'.join(path)))
            else:
                return_dict.setdefault(relationship, {}).update(
                    relationship.rtable.collection.includes_dict(
                        sub_includes, errors, path))
            path.pop()
        return return_dict

    def filters_list(self, request_query, errors):
        """Helper function for parsing request query filter parameters."""

        return_list = []
        for key, value in request_query.items():
            match = RE_FILTER.match(key)
            if match:
                field_name = match.group(1)
                try:
                    field = getattr(self.table.___, field_name)
                    condition = field.filter_condition(value)
                except AttributeError:
                    errors.append(FilterInvalidFieldError(field_name))
                    continue
                return_list.append(condition)
        return return_list

    def sort_list(self, request_query, errors):
        """Helper function for parsing request query sort parameter."""

        return_list = []
        field_names = request_query['sort'].split(',')
        for field_name in field_names:
            if field_name[0] == '-':
                field_name = field_name[1:]
                order = f'{field_name} DESC'
            else:
                order = f'{field_name} ASC'
            try:
                _ = getattr(self.table.___, field_name)
            except AttributeError:
                errors.append(SortInvalidFieldError(field_name))
                continue
            return_list.append(order)
        return return_list

    async def get(self, query):
        """Produces the response for a GET /{collection} request."""

        links = {'self': self.path()}
        return document_response(await self.to_document(query=query,
                                                        links=links))

    async def post(self, document, query):
        """Produces the response for a POST /{collection} request."""

        if document.id_number:
            return await self.post_with_id(document, query)
        return await self.post_without_id(document, query)

    async def post_with_id(self, document, query):
        """Produces the response for a POST /{collection} request where the
        document's resource object contains an id.
        """

        env = PostCollectionWithIdEnvironment(self, document.id_number,
                                              document.attributes,
                                              document.relationships, query)
        await env.run()
        event = CreateEvent(document.data)
        await event.broadcast()
        return no_content_response()

    async def post_without_id(self, document, query):
        """Produces the response for a POST /{collection} request where the
        document's resource object does not contain an id.
        """

        env = PostCollectionWithoutIdEnvironment(self, document.attributes,
                                                 document.relationships, query)
        await env.run()
        id_name = id_number_to_name(env.id_number)
        document.data['id'] = id_name
        for attr_name, value in document.attributes.items():
            attr = self.table.attributes_by_name[attr_name]
            if attr.type_ == Json:
                document.attributes[attr_name] = loads(value)
        path = f'{self.path()}/{id_name}'
        document.data['links'] = {'self': path}
        event = CreateEvent(document.data)
        await event.broadcast()
        return document_response({'data': document.data},
                                 status=201,
                                 headers={'Location': path})

    async def post_with_id_task(self, env):
        """Updates the database collection table based on the POST
        /{collection} request.
        """
        local_relationships = {
            self.table.lfkey_by_relationship_name[name]: value
            for name, value in env.relationships.items()
            if name in self.table.lfkey_by_relationship_name
        }
        lfkeys = local_relationships.keys()
        lfkey_values = [id_.number for id_ in local_relationships.values()]
        column_names = ', '.join(chain(['id'], env.attributes.keys(), lfkeys))
        length = 1 + len(env.attributes) + len(lfkeys)
        column_values = ', '.join(
            [f'${index}' for index in range(1, length + 1)])
        stmt = (f'INSERT INTO data.{self.table.name} ({column_names}) '
                f'VALUES ({column_values})')
        try:
            async with env.lock:
                async with env.connection.transaction():
                    log.debug(f'{stmt}: {env.id_number}, '
                              f'{env.attributes.values()}, {lfkey_values}')
                    await env.connection.execute(stmt, env.id_number,
                                                 *env.attributes.values(),
                                                 *lfkey_values)
        except ForeignKeyViolationError as exc:
            env.cancel()
            raise NonexistentRelationshipIdError() from exc
        except UniqueViolationError as exc:
            env.cancel()
            raise ErrorsException([convert_unique_violation_error(exc)
                                  ]) from exc
        except (CheckViolationError, ExclusionViolationError,
                NotNullViolationError, RestrictViolationError) as exc:
            env.cancel()
            raise ErrorsException([convert_violation_error(exc)]) from exc

    async def post_without_id_task(self, env):
        """Updates the database collection table based on the POST
        /{collection} request.
        """
        local_relationships = {
            self.table.lfkey_by_relationship_name[name]: value
            for name, value in env.relationships.items()
            if name in self.table.lfkey_by_relationship_name
        }
        lfkeys = local_relationships.keys()
        lfkey_values = [id_.number for id_ in local_relationships.values()]
        column_names = ', '.join(chain(env.attributes.keys(), lfkeys))
        length = len(env.attributes) + len(lfkeys)
        column_values = ', '.join(
            [f'${index}' for index in range(1, length + 1)])
        if column_values:
            stmt = (f'INSERT INTO data.{self.table.name} ({column_names}) '
                    f'VALUES ({column_values}) RETURNING id')
        else:
            stmt = (f'INSERT INTO data.{self.table.name} '
                    'DEFAULT VALUES RETURNING id')
        try:
            async with env.lock:
                async with env.connection.transaction():
                    log.debug(f'{stmt}: {env.attributes.values()}, '
                              f'{lfkey_values}')
                    env.id_number = await env.connection.fetchval(
                        stmt, *env.attributes.values(), *lfkey_values)
                    env.event.set()
        except ForeignKeyViolationError as exc:
            env.cancel()
            raise NonexistentRelationshipIdError() from exc
        except (CheckViolationError, ExclusionViolationError,
                NotNullViolationError, RestrictViolationError,
                UniqueViolationError) as exc:
            env.cancel()
            raise ErrorsException([convert_violation_error(exc)]) from exc

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
        """Creates the response document's data and included member values."""

        env = GetCollectionEnvironment(self, query)
        await env.run()
        return env.data, env.included

    async def get_collection_data(self, env):
        """Creates the response data member for attributes and local
        relationships.

        Specifically, after this call the environment's data member contains
        something like the following dictionary (from id to response data for
        that object):

        {
            1: {
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
            },
            2: {
                ...,
            },
            ...
        }
        """
        fields = env.query['fields']
        if self in fields:
            columns = chain(
                ['id'],
                (str(col) for col in self.table.columns if col in fields[self]))
        else:
            columns = (str(col) for col in self.table.columns)
        filters = env.query['filters']
        sort = env.query['sort']
        if filters:
            if sort:
                stmt = (
                    f"SELECT {', '.join(columns)} FROM data.{self.table.name} "
                    f"WHERE {' AND '.join(filters)} "
                    f"ORDER BY {', '.join(sort)}")
            else:
                stmt = (
                    f"SELECT {', '.join(columns)} FROM data.{self.table.name} "
                    f"WHERE {' AND '.join(filters)}")
        else:
            if sort:
                stmt = (
                    f"SELECT {', '.join(columns)} FROM data.{self.table.name} "
                    f"ORDER BY {', '.join(sort)}")
            else:
                stmt = (
                    f"SELECT {', '.join(columns)} FROM data.{self.table.name}")
        page = env.query['page']
        if page:
            limit = page['size']
            offset = page['number'] * limit
            stmt += f' LIMIT {limit} OFFSET {offset}'
        async with env.lock:
            log.debug(stmt)
            records = await env.connection.fetch(stmt)
        env.data_by_lid = {
            record['id']: self.record_to_data(record) for record in records
        }
        env.event.set()

    async def get_collection_included(self, env, ids):
        """Collects part of the 'included' member for a GET
        /{collection}?include response.
        """
        fields = env.query['fields']
        if self in fields:
            columns = chain(
                ['id'],
                (str(col) for col in self.table.columns if col in fields[self]))
        else:
            columns = (str(col) for col in self.table.columns)
        stmt = (f"SELECT {', '.join(columns)} "
                f"FROM data.{self.table.name} WHERE id IN ({ids})")
        ### Optimize the stmt!
        async with env.lock:
            log.debug(stmt)
            records = await env.connection.fetch(stmt)
        env.included_by_id = {
            record['id']: self.record_to_data(record) for record in records
        }
        env.event.set()

    async def get_object_included(self, env, ids):
        """Collects part of the 'included' member for a GET
        /{collection}?include response.
        """
        fields = env.query['fields']
        if self in fields:
            columns = chain(
                ['id'],
                (str(col) for col in self.table.columns if col in fields[self]))
        else:
            columns = (str(col) for col in self.table.columns)
        stmt = (f"SELECT {', '.join(columns)} "
                f"FROM data.{self.table.name} WHERE id IN ({ids})")
        ### Optimize the stmt!
        async with env.lock:
            log.debug(f'{stmt}: {env.object_id}')
            records = await env.connection.fetch(stmt, env.object_id)
        env.included_by_id = {
            record['id']: self.record_to_data(record) for record in records
        }
        env.event.set()

    def record_to_data(self, record):
        """Converts a asyncpg record into a JSON API data member."""
        attributes = {}
        relationships = {}
        for col_name, value in record.items():
            if col_name == 'id':
                id_name = id_number_to_name(value)
            elif col_name in self.table.attributes_by_name:
                col = self.table.attributes_by_name[col_name]
                if col.type_ == Json:  # Should we use a virtual function?
                    attributes[col_name] = loads(value)
                else:
                    attributes[col_name] = value
            else:  # col_name is a lfkey
                rel = self.table.relationship_by_lfkey[col_name]
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
                        'self': (f'/{self.name}/{id_name}/'
                                 f'relationships/{rel.name}'),
                        'related': (f'/{self.name}/{id_name}/'
                                    f'{rel.name}'),
                    }
                }
        data = {
            'type': self.name,
            'id': id_name,
        }
        if attributes:
            data['attributes'] = attributes
        if relationships:
            data['relationships'] = relationships
        return data

    def path(self):
        """Creates the path to the collection."""

        return f'/{self.name}'


class GetCollectionEnvironment:
    """Class GetCollectionEnvironment is the execution environment for a
    GET /{collection} request.
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, collection, query):
        self.collection = collection
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
        /{collection} response.
        """
        self.data_environment = GetCollectionDataEnvironment(self)

    def create_included_environments(self, ids, includes):
        """Creates the environment for collecting the included member of the
        GET /{collection} response.
        """
        if includes is None:
            return
        for relationship, remote_includes in includes.items():
            remote_collection = relationship.rtable.collection
            remote_ids = relationship.collection_remote_ids(self.query, ids)
            self.included_environments.append(
                GetCollectionIncludedEnvironment(remote_collection, remote_ids,
                                                 self))
            if remote_includes:
                self.create_included_environments(remote_ids, remote_includes)

    def create_tasks(self):
        """Create all tasks for querying the database to create a GET
        /{collection} response.
        """

        self.create_data_environment()
        self.create_included_environments(None, self.query['includes'])
        self.tasks = [
            create_task(env.run()) for env in chain([self.data_environment],
                                                    self.included_environments)
        ]

    async def run(self):
        """Executes the GET /{collection} tasks."""

        async with self.collection.table.pool.acquire() as self.connection:
            async with self.connection.transaction():
                self.create_tasks()
                await gather(*self.tasks)
        self.data = list(self.data_environment.data_by_lid.values())
        if self.query['includes']:
            self.included = list(
                chain.from_iterable(env.included_by_id.values()
                                    for env in self.included_environments))


class GetCollectionDataEnvironment:
    """Class GetCollectionDataEnvironment is the execution environment for the
    data part of the GET /{collection} response.
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, env):
        self.collection = env.collection
        self.query = env.query
        self.tasks = []
        self.connection = env.connection
        self.lock = env.lock
        self.data_by_lid = {}
        self.event = Event()

    def create_tasks(self):
        """Create all tasks for querying the database to create the data part
        of a GET /{collection} response.
        """
        self.tasks = [create_task(self.collection.get_collection_data(self))]
        query_fields = self.query['fields']
        if self.collection in query_fields:
            self.tasks.extend([
                create_task(rel.get_collection_data(self))
                for rel in query_fields[self.collection]
                if rel in self.collection.table.remote_relationships
            ])
        else:
            self.tasks.extend([
                create_task(rel.get_collection_data(self))
                for rel in self.collection.table.remote_relationships
            ])

    async def run(self):
        """Executes the GET /{collection} data tasks."""
        self.create_tasks()
        await gather(*self.tasks)


class PostCollectionEnvironment:
    """Class PostCollectionEnvironment is the execution environment for a POST
    /{collection} request.
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, collection, id_number, attributes, relationships, query):
        # pylint: disable=too-many-arguments

        self.collection = collection
        self.id_number = id_number
        self.attributes = attributes
        self.relationships = relationships
        self.query = query
        self.connection = None
        self.lock = Lock()
        self.tasks = []
        self.gather_future = None
        self.event = Event()  # To indicate that self.id_number exists

    @abstractmethod
    def create_tasks(self):
        """Create all tasks for updating the database in response to a POST
        /{collection} request.
        """

    async def run(self):
        """Executes the POST /{collection} tasks."""
        async with self.collection.table.pool.acquire() as self.connection:
            async with self.connection.transaction():
                try:
                    async with self.connection.transaction():
                        self.create_tasks()
                        self.gather_future = gather(*self.tasks)
                        await self.gather_future
                except NonexistentRelationshipIdError:
                    env = VerifyRelationshipIdsEnvironment(
                        self.collection.table, self.relationships,
                        self.connection)
                    await env.run()

    def cancel(self):
        """Cancels the environment."""

        self.gather_future.cancel()


class PostCollectionWithIdEnvironment(PostCollectionEnvironment):
    """Class PostCollectionWithIdEnvironment is the execution environment for
    a POST /{collection} request where the requests document's data contains
    an id.
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, collection, id_number, attributes, relationships, query):
        # pylint: disable=too-many-arguments

        super().__init__(collection, id_number, attributes, relationships,
                         query)
        self.event.set()

    def create_tasks(self):
        """Create all tasks for updating the database in response to a POST
        /{collection} request where the request document's data contains an
        id.
        """
        self.tasks = [create_task(self.collection.post_with_id_task(self))]
        self.tasks.extend([
            create_task(rel.post_collection_task(self))
            for rel in self.collection.table.remote_relationships
            if rel.name in self.relationships
        ])


class PostCollectionWithoutIdEnvironment(PostCollectionEnvironment):
    """Class PostCollectionWithoutIdEnvironment is the execution environment
    for a POST /{collection} request where the request document's data does
    not contain an id.
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, collection, attributes, relationships, query):
        # pylint: disable=too-many-arguments
        super().__init__(collection, None, attributes, relationships, query)

    def create_tasks(self):
        """Create all tasks for updating the database in response to a POST
        /{collection} request where the request document's data does not
        contain an id.
        """
        self.tasks = [create_task(self.collection.post_without_id_task(self))]
        self.tasks.extend([
            create_task(rel.post_collection_task(self))
            for rel in self.collection.table.remote_relationships
            if rel.name in self.relationships
        ])


class VerifyRelationshipIdsEnvironment:
    """Class VerifyRelationshipIdsEnvironment is the execution environment for
    verifying the existence of relationship ids.
    """

    def __init__(self, table, relationships, connection):
        self.table = table
        self.ids_by_relationship = {
            getattr(table.___, name): ids
            for name, ids in relationships.items()
        }
        self.connection = connection
        self.lock = Lock()
        self.tasks = []
        self.errors = []

    def create_tasks(self):
        """Create all tasks for verifying the document's data/id members for
        existence.
        """
        self.tasks = [
            create_task(relationship.verify_data_ids_exist(self, ids))
            for relationship, ids in self.ids_by_relationship.items()
        ]

    async def run(self):
        """Raises ErrorsException with errors for all the document's
        nonexistent relationship ids.
        """
        async with self.connection.transaction():
            self.create_tasks()
            await gather(*self.tasks)
            raise ErrorsException(self.errors)


def parse_collection(request):
    """Gets a collection associated with a request.

    Args:
        request: Incoming Http(s) request.

    Exceptions:
        ErrorsException: Exception containing a 'resource not found' error.
    """

    collection_name = request.match_info['collection']
    try:
        return Collection.by_name[collection_name]
    except KeyError as exc:
        raise ErrorsException([ResourceNotFoundError(f'/{collection_name}')
                              ]) from exc
