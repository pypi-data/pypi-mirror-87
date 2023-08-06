# copyright 2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-jsonschema Pyramid "schema" resources definitions."""

from pyramid.decorator import reify

from . import (
    _RelationshipProxyResource
)


class ApplicationSchema(object):
    """The root schema resource, describing the application schema."""
    __name__ = ''
    __parent__ = None

    def __init__(self, request):
        self.request = request

    def __getitem__(self, value):
        vreg = self.request.registry['cubicweb.registry']
        try:
            etype = vreg.case_insensitive_etypes[value.lower()]
        except KeyError:
            raise KeyError(value)
        return ETypeSchema(self.request, etype, self)

    @reify
    def described_resource(self):
        """The resource described by the schema bound to this resource."""
        from .entities import RootResource  # avoid circular import
        return RootResource(self.request)


class _SchemaResource(object):

    @reify
    def rset(self):
        return self.described_resource.rset

    @property
    def __name__(self):
        return self.described_resource.__name__

    def __repr__(self):
        return ('<{module}.{self.__class__.__name__} describing '
                '{self.described_resource}>'.format(
                    self=self, module=__name__))


class ETypeSchema(_SchemaResource):
    """Schema resource for an entity type."""

    def __init__(self, request, etype, parent):
        self.request = request
        self.etype = etype
        self.__parent__ = parent

    def __getitem__(self, value):
        if value == 'relationships':
            return _RelationshipProxyResource(
                self.request, self.etype, parent=self)
        entity_resource = self.described_resource[value]
        entity_resource.__parent__ = self.described_resource
        entity_resource.__name__ = value
        return EntitySchema(self.request, entity_resource, self)

    @reify
    def described_resource(self):
        """The resource described by the schema bound to this resource."""
        from .entities import ETypeResource  # avoid circular import
        return ETypeResource(self.request, self.etype)


class EntitySchema(_SchemaResource):
    """Schema resource for an entity."""

    def __init__(self, request, entity_resource, parent):
        self.request = request
        self.described_resource = entity_resource
        self.__parent__ = parent

    def __getitem__(self, value):
        # we should not traverse this way (FIXME)
        assert value != 'relationships'
        try:
            relatedentities_resource = self.described_resource[value]
        except KeyError:
            raise KeyError(value)
        return RelatedEntitiesSchema(self.request, relatedentities_resource,
                                     parent=self)


class RelatedEntitiesSchema(_SchemaResource):
    """Schema resource for related entities."""

    def __init__(self, request, entity_resource, parent):
        self.request = request
        self.described_resource = entity_resource
        self.rtype = entity_resource.rtype
        self.role = entity_resource.role
        self.__parent__ = parent
