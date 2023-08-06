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

"""cubicweb-jsonschema Pyramid resources definitions."""

from functools import wraps


def parent(init_method):
    """Decorator for resource class's __init__ method to bind the __parent__
    attribute to instance.
    """
    @wraps(init_method)
    def wrapper(self, *args, **kwargs):
        parent = kwargs.pop('parent', None)
        init_method(self, *args, **kwargs)
        self.__parent__ = parent

    return wrapper


def find_relationship(schema, etype, rtype):
    """Return (`rtype`, `role`) if `etype` has a relationship `rtype` else
    raise a ValueError.
    """
    eschema = schema[etype]
    for relinfo in eschema.relation_definitions():
        rschema, __, role = relinfo
        if rschema.final or rschema.meta:
            continue
        if rschema.type == rtype:
            return relinfo
    raise ValueError(rtype)


class _RelationshipProxyResource(object):
    """A "proxy" resource allowing to pass through the "relationships" segment
    of path during traversal.
    """

    @parent
    def __init__(self, request, etype=None, **kwargs):
        self.request = request
        self.etype = etype

    def __getitem__(self, value):
        vreg = self.request.registry['cubicweb.registry']
        schema = vreg.schema
        if self.etype:
            etype = self.etype
        elif hasattr(self, '__parent__'):
            etype = self.__parent__.entity.cw_etype
        else:
            raise AssertionError('neither etype nor __parent__ got specified')
        try:
            relinfo = find_relationship(schema, etype, value)
        except ValueError:
            raise KeyError(value)
        else:
            parent = getattr(self, '__parent__', None)
            return RelationshipResource(self.request, *relinfo, parent=parent)


class RelationshipResource(object):
    """A resource to manipulate a relationship `rtype` with __parent__ as
    `role`.

    This can be used for both "schema" and "entities" resources.
    """

    @parent
    def __init__(self, request, rschema, target_schemas, role, **kwargs):
        self.request = request
        self.rtype = rschema.type
        self.target_schemas = target_schemas
        self.role = role

    @property
    def target_type(self):
        """Target entity type of relationship."""
        if len(self.target_schemas) > 1:
            target = self.request.params.get('target_type')
            if target and target in {s.type for s in self.target_schemas}:
                return target
            raise NotImplementedError()
        return self.target_schemas[0].type
