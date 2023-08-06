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
"""Module uri.resrouce provides the Resource base class."""

from abc import ABC

from ajsonapi.conversions import id_number_to_name


class Resource(ABC):
    """Class Resource is the base for all uri resource objects."""

    # pylint: disable=too-few-public-methods

    def to_relationships(self, rel, value):
        """Converts a relationship and its record value into a JSON API
        relationships member.
        """

        # pylint: disable=no-member
        if value is None:
            relationship_data = None
        else:
            relationship_data = {
                'type': rel.rtable.collection.name,
                'id': id_number_to_name(value)
            }
        return {
            'data': relationship_data,
            'links': {
                'self': (f'/{self.collection.name}/{self.id.name}/'
                         f'relationships/{rel.name}'),
                'related': (f'/{self.collection.name}/{self.id.name}/'
                            f'{rel.name}'),
            }
        }
