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

"""cubicweb-jsonschema Pyramid "entities" resources definitions."""

from six import text_type

from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPNotFound

from rql import nodes

from cubicweb.pyramid import resources as cw_resources

from . import (
    find_relationship,
    parent,
    _RelationshipProxyResource,
    schema as schema_resources,
)


class RootResource(object):
    """Root resources for entities."""
    __parent__ = None
    __name__ = ''

    def __init__(self, request):
        self.request = request

    @reify
    def described_by(self):
        return schema_resources.ApplicationSchema(self.request)


class ETypeResource(cw_resources.ETypeResource):
    """Specialize cubicweb.pyramid.resources.ETypeResource with a
    "relationships" traversal key and `__parent__`/`__name__` attributes.
    """
    def __init__(self, *args, **kwargs):
        super(ETypeResource, self).__init__(*args, **kwargs)
        self.__parent__ = RootResource(self.request)
        self.__name__ = self.etype.lower()

    def __getitem__(self, value):
        if value == 'relationships':
            return _RelationshipProxyResource(self.request, self.etype)
        # Copy from parent's class method.
        for attrname in ('eid', self.cls.cw_rest_attr_info()[0]):
            resource = EntityResource(self.request, self.cls, attrname, value)
            try:
                rset = resource.rset
            except HTTPNotFound:
                continue
            if rset.rowcount:
                resource.__name__ = value
                resource.__parent__ = self
                return resource
        raise KeyError(value)

    @reify
    def described_by(self):
        return schema_resources.ETypeSchema(
            self.request, self.etype, self.__parent__.described_by)


class EntityResource(cw_resources.EntityResource):
    """Specialize cubicweb.pyramid.resources.EntityResource to add a
    __getitem__ method.
    """

    def __getitem__(self, value):
        # Make sure parent class has no __getitem__ as we do not call it here.
        # If it happens, we'll need to call it here.
        assert not hasattr(super(EntityResource, self), '__getitem__')
        etype = self.cls.cw_etype
        if value == 'relationships':
            return _RelationshipProxyResource(self.request, etype, parent=self)
        vreg = self.request.registry['cubicweb.registry']
        schema = vreg.schema
        try:
            rschema, __, role = find_relationship(schema, etype, value)
        except ValueError:
            raise KeyError(value)
        else:
            return RelatedEntitiesResource(
                self.request, rschema.type, role, parent=self)

    @reify
    def described_by(self):
        return schema_resources.EntitySchema(
            self.request, self, self.__parent__.described_by)


class RelatedEntitiesResource(object):
    """A resource wrapping entities related to the entity bound to
    `entity_resource` through `rtype`/`role`.
    """

    @parent
    def __init__(self, request, rtype, role, **kwargs):
        self.request = request
        self.rtype = rtype
        self.role = role
        self.__name__ = rtype

    @reify
    def rset(self):
        # May raise HTTPNotFound, this is probably fine (isn't it?)
        entity = self.__parent__.rset.one()
        vreg = self.request.registry['cubicweb.registry']
        # XXX Until https://www.cubicweb.org/ticket/12306543 gets done.
        rql = entity.cw_related_rql(self.rtype, role=self.role)
        args = {'x': entity.eid}
        select = vreg.parse(entity._cw, rql, args).children[0]
        sortterms = self.request.params.get('sort')
        if sortterms:
            select.remove_sort_terms()
            mainvar = select.get_variable('X')
            for term in sortterms.split(','):
                if term.startswith('-'):
                    asc = False
                    term = term[1:]
                else:
                    asc = True
                mdvar = select.make_variable()
                rel = nodes.make_relation(mainvar, term,
                                          (mdvar,), nodes.VariableRef)
                select.add_restriction(rel)
                select.add_sort_var(mdvar, asc=asc)
        rql = select.as_string()
        return entity._cw.execute(rql, args)

    @reify
    def described_by(self):
        return schema_resources.RelatedEntitiesSchema(
            self.request, self, self.__parent__.described_by)

    def __getitem__(self, value):
        if self.role != 'subject':
            # We only handle subject-relation in traversal.
            raise KeyError(value)
        entity = self.__parent__.rset.one()
        rset = self.request.cw_cnx.execute(
            'Any O WHERE O eid %(o)s, S {rtype} O, S eid %(s)s'.format(
                rtype=self.rtype),
            {'o': value, 's': entity.eid})
        if not rset:
            raise KeyError(value)
        return RelatedEntityResource(
            self.request, rset.one(), rtype=self.rtype, role=self.role,
            parent=self)


class RelatedEntityResource(object):
    """A resource an entity related to another one."""

    def __init__(self, request, entity, rtype, role, parent):
        self.request = request
        self.entity = entity
        self.rtype = rtype
        self.role = role
        self.__parent__ = parent
        self.__name__ = text_type(entity.eid)

    @reify
    def described_by(self):
        raise NotImplementedError()
