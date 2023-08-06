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
"""Module jsonapi provides class JSON_API."""

from ajsonapi.id import Id
from ajsonapi.table import Table
from ajsonapi.types import Int64


class JSON_API(Table):
    """JSON_API is the base class from which users derive object model
    classes. Classes that derive from JSON_API will result in URLs and methods
    in the web server through which to manipulate the object model.
    """
    # pylint: disable=invalid-name, too-few-public-methods

    @classmethod
    def __init_subclass__(cls):
        super().__init_subclass__()
        if not hasattr(cls, 'id'):
            cls.id = Id(Int64)
        cls.id.table_name = cls.name
        cls.columns.insert(0, cls.id)
        cls.constraints.insert(0, cls.id)


def init(pool):
    """Initializes all JSON_API subclasses."""

    for json_api in JSON_API.__subclasses__():
        json_api.pool = pool
