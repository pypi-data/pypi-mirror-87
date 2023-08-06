# Copyright © 2020 Roel van der Goot
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
"""Module postgres deals with postgres interactions."""

from re import compile as re_compile

from asyncpg.exceptions import CheckViolationError, UniqueViolationError

from ajsonapi.errors import (
    DocumentDataDuplicateIdError,
    DocumentDataViolationError,
    DocumentError,
)

RE_UNIQUE_VIOLATION_ERROR_DETAIL = re_compile(
    r'Key \(([^)]*)\)=\(([^)]*)\) already exists.')


def convert_unique_violation_error(exc: UniqueViolationError) -> DocumentError:
    """Converts a Postgres UniqueViolationError into a JSON:API error."""
    match = RE_UNIQUE_VIOLATION_ERROR_DETAIL.match(exc.detail)
    cols = match.group(1).split(', ')
    if len(cols) == 1 and cols[0] == 'id':
        return DocumentDataDuplicateIdError(f'/data/id/{match.group(2)}')
    return DocumentDataViolationError('/data', exc.detail)


def convert_violation_error(exc: CheckViolationError) -> DocumentError:
    """Converts a Postgres ViolationError into a JSON:API error."""
    return DocumentDataViolationError('/data', exc.detail)
