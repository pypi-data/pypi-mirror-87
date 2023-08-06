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
"""Module document deals with anything related to request documents."""

from json import JSONDecodeError, dumps

from ajsonapi.conversions import id_name_to_number, uuid_name_to_number
from ajsonapi.errors import (
    DocumentDataInvalidAttributeError,
    DocumentDataInvalidIdError,
    DocumentDataInvalidRelationshipError,
    DocumentDataInvalidTypeError,
    DocumentDataMalformedError,
    DocumentDataMalformedIdError,
    DocumentDataMalformedRelationshipError,
    DocumentDataMalformedUuidError,
    DocumentDataMissingError,
    DocumentDataMissingIdError,
    DocumentDataMissingTypeError,
    DocumentNotJsonError,
)
from ajsonapi.exceptions import ErrorsException, TypeNameError
from ajsonapi.id_value import IdValue
from ajsonapi.types import Json


class Document:
    """Representation of a request document."""

    # pylint: disable=too-few-public-methods

    def __init__(self, data):
        self.data = data

    def parse_type(self, expected_type_name, errors):
        """Verifies that the document's resource object contains the correct
        type.

        Args:
            expected_type_name (str): expected type of the resource (identifier)
                object in the document.
            errors (list): list of errors found so far verifying the document
                describes a valid resourse (identifier) object.
        """

        try:
            type_name = self.data['type']
            if type_name != expected_type_name:
                errors.append(
                    DocumentDataInvalidTypeError(f'/data/type/{type_name}'))
        except TypeError as exc:
            raise ErrorsException([DocumentDataMalformedError()]) from exc
        except KeyError:
            errors.append(DocumentDataMissingTypeError('/data'))


class ResourceObjectDocument(Document):
    """Representation of a request document with a resource object."""

    def __init__(self, data):
        super().__init__(data)
        self.id_number = None
        self.attributes = None
        self.relationships = None

    def parse(self, collection, id_name=None):
        """Parses the document for a valid resource object.

        Args:
            collection (Collection): collection from which the resource object
                should be a member.
            id_name (str): valid id name for the resource object.

        Raises:
            ErrorsException with all the errors in case the document does not
            represent a valid resource object.
        """

        errors = []
        self.parse_type(collection.name, errors)
        self.parse_id(id_name, errors)
        self.parse_attributes(collection, errors)
        self.parse_relationships(collection, errors)
        if errors:
            raise ErrorsException(errors)

    def parse_id(self, expected_id_name, errors):
        """Parses the document's resource object for a valid id.

        Args:
            expected_id_name (str): expected id of the resource object in the
                document.
            errors (list): list of errors found so far verifying the document
                describes a valid resourse object.
        """

        if 'id' in self.data:
            id_name = self.data['id']
            try:
                if expected_id_name:
                    if id_name != expected_id_name:
                        errors.append(
                            DocumentDataInvalidIdError(
                                'Invalid resource object.',
                                f'/data/id/{id_name}'))
                    self.id_number = id_name_to_number(id_name)
                else:
                    self.id_number = uuid_name_to_number(id_name)
            except ValueError:
                errors.append(
                    DocumentDataMalformedUuidError(f'/data/id/{id_name}'))
        else:
            if expected_id_name:
                errors.append(DocumentDataMissingIdError())
            self.id_number = None

    def parse_attributes(self, collection, errors):
        """Parses the document's resource object for valid attributes.

        Args:
            collection (Collection): collection of which the resource object
                should be a member.
            errors (list): list of errors found so far verifying the document
                describes a valid resourse object.
        """

        self.attributes = self.data.get('attributes', {})
        invalid_attribute_names = (
            set(self.attributes.keys()) -
            set(collection.table.attributes_by_name.keys()))
        if invalid_attribute_names:
            errors.extend([
                DocumentDataInvalidAttributeError(
                    f'/data/attributes/{attribute_name}')
                for attribute_name in invalid_attribute_names
            ])
            return

        for attr_name, value in self.attributes.items():
            attr = collection.table.attributes_by_name[attr_name]
            if attr.type_ == Json:
                self.attributes[attr_name] = dumps(value)

    def parse_relationships(self, collection, errors):
        """Parses the document's resource object for valid relationships.

        Args:
            collection (Collection): collection from which the resource object
                should be a member.
            errors (list): list of errors found so far verifying the document
                describes a valid resourse object.
        """

        data_relationships = self.data.get('relationships', {})
        invalid_data_relationship_names = (
            set(data_relationships.keys()) -
            {rel.name for rel in collection.table.relationships})
        if invalid_data_relationship_names:
            errors.extend([
                DocumentDataInvalidRelationshipError(
                    f'/data/relationships/{data_relationship_name}')
                for data_relationship_name in invalid_data_relationship_names
            ])
        self.relationships = {}
        for relationship_name, value in data_relationships.items():
            if relationship_name in invalid_data_relationship_names:
                continue
            relationship = getattr(collection.table.___, relationship_name)
            try:
                relationship_data = value['data']
            except TypeError:
                errors.append(
                    DocumentDataMalformedRelationshipError(
                        f'/data/relationships/{relationship_name}'))
                continue
            data_rio_ids = relationship.verify_data_rios(
                relationship_name, relationship_data, errors)
            self.relationships[relationship_name] = data_rio_ids


class ResourceIdentifierObjectDocument(Document):
    """Representation of a request document with a resource identification
    object.
    """

    def __init__(self, data):
        super().__init__(data)
        self.id = None  # pylint: disable=invalid-name

    def parse(self, expected_type_name):
        """Parses the document for a valid resource identifier object.

        Args:
            expected_type_name (str): expected type name of the resource
                identifier object.

        Raises:
            ErrorsException with all the errors in case the document does not
            represent a valid resource identifier object.
        """

        errors = []
        if self.data is not None:
            self.parse_type(expected_type_name, errors)
            self.parse_id(errors)
            if errors:
                raise ErrorsException(errors)

    def parse_id(self, errors):
        """Verifies that the document's resource identifier object contains a
        valid id.

        Args:
            errors (list): list of errors found so far verifying the document
                describes a valid resourse object.
        """
        try:
            id_name = self.data['id']
            try:
                self.id = IdValue(id_name)
            except ValueError:
                errors.append(
                    DocumentDataMalformedIdError(
                        'Invalid resource identifier object.',
                        f'/data/id/{id_name}'))
        except KeyError:
            errors.append(DocumentDataMissingIdError('/data'))


def parse_roi_type(roi, index, expected_type_name, errors):
    """Parses the resource object indetifier for an invalid type."""

    try:
        roi_type_name = roi['type']
        if roi_type_name != expected_type_name:
            errors.append(
                DocumentDataInvalidTypeError(
                    f'/data/{index}/type/{roi_type_name}'))
    except KeyError:
        errors.append(DocumentDataMissingTypeError(f'/data/{index}'))


def parse_roi_id(roi, index, errors):
    """Parses the resource object indentier for an invalid id."""

    try:
        roi_id_name = roi['id']
        try:
            id_name_to_number(roi_id_name)
        except ValueError:
            errors.append(
                DocumentDataMalformedIdError(
                    'Invalid resource identifier object.',
                    f'/data/{index}/id/{roi_id_name}'))
    except KeyError:
        errors.append(DocumentDataMissingIdError(f'/data/{index}'))


class ResourceIdentifierObjectsDocument(Document):
    """Representation of a request document with a list of resource
    identification objects.
    """

    def __init__(self, data):
        super().__init__(data)
        self.ids = None

    def parse(self, expected_type_name):
        """Parses the document for a valid resource identifier objects.

        Args:
            expected_type_name (str): expected type name of the resource
                identifier object.

        Raises:
            ErrorsException with all the errors in case the document does not
            represent a valid resource identifier object.
        """

        if not isinstance(self.data, list):
            raise ErrorsException([DocumentDataMalformedError()])

        try:
            obj_type_names = {obj['type'] for obj in self.data}
            if not obj_type_names <= {expected_type_name}:
                raise TypeNameError()
            self.ids = [IdValue(obj['id']) for obj in self.data]
        except (KeyError, ValueError, TypeNameError) as exc:
            errors = []
            for index, roi in enumerate(self.data):
                parse_roi_type(roi, index, expected_type_name, errors)
                parse_roi_id(roi, index, errors)
            raise ErrorsException(errors) from exc


async def parse_request_document_data(request):
    """Parses the request document for a valid data member.

    Args:
        request (Request): the request to be parsed.

    Returns:
        The data member of the request document.

    Raises:
        ErrorsException with an error in case the request document is
        malformed.
    """

    try:
        document = await request.json()
    except JSONDecodeError as exc:
        raise ErrorsException([DocumentNotJsonError()]) from exc
    try:
        data = document['data']
    except KeyError as exc:
        raise ErrorsException([DocumentDataMissingError()]) from exc
    return data
