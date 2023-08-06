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
"""Module application provides class Application."""

from asyncio import sleep

from aiohttp import WSMsgType, web
from asyncpg.exceptions import (
    CannotConnectNowError,
    ConnectionDoesNotExistError,
)
from asyncpg.pool import create_pool

from ajsonapi.events import Event
from ajsonapi.exceptions import ErrorsException
from ajsonapi.init import init
from ajsonapi.logging import log
from ajsonapi.requests import (
    parse_collection_document_query,
    parse_collection_query,
    parse_object_document_query,
    parse_object_query,
    parse_related_resource_query,
    parse_relationship_document_query,
    parse_relationship_query,
)
from ajsonapi.responses import errors_response, no_content_response
from ajsonapi.table import create_all as table_create_all
from ajsonapi.table import parse_model
from ajsonapi.uri.relationship import parse as parse_relationship


class Application:
    """JSON API web server.

    Default routes are derived from the specified object model.
    """

    # pylint: disable=too-many-public-methods

    def __init__(self, *args, **kwargs):
        Event.connect(self)
        self.app = web.Application(*args, **kwargs)
        self.ws_list = []
        self.pool = None

    async def connect_database(self, database):
        """Connects to the database.

        Args:
            database (str): URL to Postgres database. For example:
                'postgresql://user:password@localhost:5432/db'.

        Raises:
            NotImplementedError in case database doesn't start with
                'postgresql:'.
        """
        if not database.startswith('postgresql:'):
            raise NotImplementedError('Only postgres is currently supported.')
        while self.pool is None:
            try:
                self.pool = await create_pool(database)
            except (CannotConnectNowError,
                    ConnectionDoesNotExistError):  # pragma: no cover
                self.pool = None
                await sleep(.1)
        init(self.pool)

    async def disconnect_database(self):
        """Disconnects from the database."""
        await self.pool.close()

    def verify_model(self):
        """Parses the model."""
        # pylint: disable=no-self-use
        parse_model()

    async def create_tables(self):
        """Creates all tables in the database."""
        # pylint: disable=no-self-use
        await table_create_all(self.pool)

    def add_json_api_routes(self):
        """Add JSON API routes to the web application."""

        path = r'/{collection:[^/]*}'
        self.app.add_routes([
            web.get(path, self.get_collection),
            web.post(path, self.post_collection),
            web.options(path, self.options_collection),
        ])

        path = r'/{collection:[^/]*}/{id:[0-9A-Fa-f-]*}'
        self.app.add_routes([
            web.get(path, self.get_object),
            web.delete(path, self.delete_object),
            web.patch(path, self.patch_object),
            web.options(path, self.options_object),
        ])

        path = (r'/{collection:[^/]*}/{id:[0-9A-Fa-f-]*}/'
                r'relationships/{relationship:[^/]*}')
        self.app.add_routes([
            web.get(path, self.get_relationship),
            web.patch(path, self.patch_relationship),
            web.post(path, self.post_relationship),
            web.delete(path, self.delete_relationship),
            web.put(path, self.put_relationship),
            web.options(path, self.options_relationship),
        ])

        path = (r'/{collection:[^/]*}/{id:[0-9A-Fa-f-]*}/'
                r'{related_resource:[^/]*}')
        self.app.add_routes([
            web.get(path, self.get_related_resource),
            web.options(path, self.options_related_resource),
        ])

    def add_event_socket_route(self):
        """Add event socket."""

        path = '/event-socket/'
        self.app.add_routes([
            web.get(path, self.get_event_socket),
        ])

    async def get_collection(self, request):
        """Entry point for GET /{collection} requests.

        Args:
            request: The GET /{collection} request.
        """

        try:
            collection, query = parse_collection_query(request,
                                                       allow_include=True,
                                                       allow_fields=True,
                                                       allow_filter=True,
                                                       allow_sort=True,
                                                       allow_page=True)
            return await collection.get(query)
        except ErrorsException as err:
            return errors_response(err.errors)

    async def post_collection(self, request):
        """Entry point for GET /{collection} requests.

        Args:
            request: The POST /{collection} request.
        """

        try:
            collection, document, query = await parse_collection_document_query(
                request)
            return await collection.post(document, query)
        except ErrorsException as err:
            return errors_response(err.errors)

    async def options_collection(self, request):
        """Entry point for OPTIONS /{collection} requests.

        Args:
            request: The OPTIONS /{collection} request.
        """
        # pylint: disable=unused-argument
        return no_content_response(headers={'Allow': 'GET,OPTIONS,POST'})

    async def get_object(self, request):
        """Entry point for GET /{collection}/{id} requests.

        Args:
            request: The GET /{collection}/{id} request.
        """
        try:
            object_, query = await parse_object_query(request,
                                                      allow_include=True,
                                                      allow_fields=True)
            return await object_.get(query)
        except ErrorsException as err:
            return errors_response(err.errors)

    async def delete_object(self, request):
        """Entry point for DELETE /{collection}/{id} requests.

        Args:
            request: The DELETE /{collection}/{id} request.
        """
        try:
            object_, _ = await parse_object_query(request)
            return await object_.delete()
        except ErrorsException as err:
            return errors_response(err.errors)

    async def patch_object(self, request):
        """Entry point for DELETE /{collection}/{id} requests.

        Args:
            request: The DELETE /{collection}/{id} request.
        """
        try:
            object_, document, query = await parse_object_document_query(request
                                                                        )
            return await object_.patch(document, query)
        except ErrorsException as err:
            return errors_response(err.errors)

    async def options_object(self, request):
        """Entry point for OPTIONS /{collection}/{id} requests.

        Args:
            request: The OPTIONS /{collection}/{id} request.
        """
        # pylint: disable=unused-argument
        return no_content_response(
            headers={'Allow': 'DELETE,GET,OPTIONS,PATCH'})

    async def get_relationship(self, request):
        """Entry point for GET /{collection}/{id}/relationships/{relationship}
        requests.

        Args:
            request: The GET /{collection}/{id}/relationships/{relationship}
                request.

        Returns:
            Appropriate response for the request.
        """
        try:
            relationship, query = await parse_relationship_query(
                request, allow_include=True, allow_fields=True)
            return await relationship.get(query)
        except ErrorsException as err:
            return errors_response(err.errors)

    async def patch_relationship(self, request):
        """Entry point for PATCH
        /{collection}/{id}/relationships/{relationship} requests.

        Args:
            request: The PATCH /{collection}/{id}/relationships/{relationship}
                request.

        Returns:
            Appropriate response for the request.
        """
        try:
            relationship, document, query = \
                    await parse_relationship_document_query(request)
            return await relationship.patch(document, query)
        except ErrorsException as err:
            return errors_response(err.errors)

    async def post_relationship(self, request):
        """Entry point for POST
        /{collection}/{id}/relationships/{relationship} requests.

        Args:
            request: The POST /{collection}/{id}/relationships/{relationship}
                request.

        Returns:
            Appropriate response for the request.
        """
        try:
            relationship, document, query = \
                    await parse_relationship_document_query(request)
            return await relationship.post(document, query)
        except ErrorsException as err:
            return errors_response(err.errors)

    async def delete_relationship(self, request):
        """Entry point for DELETE
        /{collection}/{id}/relationships/{relationship} requests.

        Args:
            request: The DELETE /{collection}/{id}/relationships/{relationship}
                request.

        Returns:
            Appropriate response for the request.
        """
        try:
            relationship, document, query = \
                    await parse_relationship_document_query(request)
            return await relationship.delete(document, query)
        except ErrorsException as err:
            return errors_response(err.errors)

    async def put_relationship(self, request):
        """Entry point for PUT /{collection}/{id}/relationships/{relationship}
        requests.

        Args:
            request: The PUT /{collection}/{id}/relationships/{relationship}
                request.

        Returns:
            Appropriate response for the request.
        """
        relationship = parse_relationship(request)
        return relationship.put()

    async def options_relationship(self, request):
        """Entry point for OPTIONS
        /{collection}/{id}/relationships/{relationship} requests.

        Args:
            request: The OPTIONS /{collection}/{id}/relationships/{relationship}
                request.

        Returns:
            Appropriate response for the request.
        """
        relationship = parse_relationship(request)
        return relationship.options()

    async def get_related_resource(self, request):
        """Entry point for GET /{collection}/{id}/{related_resource} requests.

        Args:
            request: The GET /{collection}/{id}/{related_resource} request.

        Returns:
            Appropriate response for the request.
        """
        try:
            related, query = await parse_related_resource_query(
                request,
                allow_include=True,
                allow_fields=True,
                allow_filter=True,
                allow_sort=True,
                allow_page=True)
            return await related.get(query)
        except ErrorsException as err:
            return errors_response(err.errors)

    async def options_related_resource(self, request):
        """Entry point for OPTIONS /{collection}/{id}/{related_resource}
        requests.

        Args:
            request: The OPTIONS /{collection}/{id}/{related_resource} request.

        Returns:
            Appropriate response for the request.
        """
        # pylint: disable=unused-argument
        return no_content_response(headers={'Allow': 'GET,OPTIONS'})

    async def get_event_socket(self, request):
        """Creates a web socket for events."""

        ws = web.WebSocketResponse()  # pylint: disable=invalid-name
        await ws.prepare(request)
        self.ws_list.append(ws)
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                # Eventually: allow clients to register/deregister individual
                # events they are interested in.
            elif msg.type == WSMsgType.ERROR:
                log.debug('websocket connection closed with exception',
                          ws.exception())
        self.ws_list.remove(ws)
        return ws

    async def broadcast(self, event):
        """Broadcasts an event on all event sockets."""

        stream_event = event.stream_event()
        for ws in self.ws_list:  # pylint: disable=invalid-name
            await ws.send_json(stream_event)
