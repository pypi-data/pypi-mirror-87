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
"""Module id provides class Id."""

from ajsonapi.types import Uuid


class Id:
    """Class representing the "id" column in JSON_API classes."""

    def __init__(self, type_):
        self.type_ = type_
        self.table_name = None  # Overriden in JSON_API.__init_subclass__

    def sql(self):
        """Returns the column definition for the "id" field."""
        # pylint: disable=no-self-use

        if self.type_ == Uuid:
            return "id UUID DEFAULT data.uuid_generate_v4()"
        # self.type_ == Int64
        return (f"id UUID DEFAULT CAST ("
                f"LPAD(TO_HEX(nextval('data.seq_{self.table_name}')), 32, '0')"
                f" AS UUID)")

    def sql_constraints(self):
        """Returns the constraints for the "id" field."""
        # pylint: disable=no-self-use
        return ['PRIMARY KEY (id)']

    def __str__(self):
        return 'id'
