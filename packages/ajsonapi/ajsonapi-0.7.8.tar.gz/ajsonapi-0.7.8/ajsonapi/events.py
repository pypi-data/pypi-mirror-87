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
"""Module events provides events for changes to resource objects in the object
model."""

from abc import abstractmethod


class Event:
    """Base class for events"""

    # pylint: disable=too-few-public-methods

    app = None

    @classmethod
    def connect(cls, app):
        """Connects events to the app."""
        cls.app = app

    def __init__(self, data):
        self.data = data

    @abstractmethod
    def stream_event(self):
        """Converts the journal event into a stream event."""

    async def publish(self):
        """Publishes the event on the event jounal."""

    async def broadcast(self):
        """Tells the application to broadcast the event."""
        await self.app.broadcast(self)


class CreateEvent(Event):
    """Event to signal the creation of a resource object"""

    # pylint: disable=too-few-public-methods

    def stream_event(self):
        return {
            'op': 'create',
            'data': self.data,
        }


class UpdateEvent(Event):
    """Event to signal a change of a resource object"""

    # pylint: disable=too-few-public-methods

    def stream_event(self):
        return {
            'op': 'update',
            'data': self.data,
        }


class DeleteEvent(Event):
    """Event to signal the deletion of a resource object"""

    # pylint: disable=too-few-public-methods

    def stream_event(self):
        return {
            'op': 'delete',
            'data': self.data,
        }
