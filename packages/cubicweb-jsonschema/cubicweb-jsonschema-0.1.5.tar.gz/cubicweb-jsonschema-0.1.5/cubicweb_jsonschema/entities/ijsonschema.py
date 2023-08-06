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
"""cubicweb-jsonschema entity's classes"""

import jsonschema

from logilab.common.registry import objectify_predicate

from cubicweb import ValidationError
from cubicweb.predicates import match_kwargs, non_final_entity
from cubicweb.entity import Adapter, EntityAdapter

from cubicweb_jsonschema import (
    VIEW_ROLE,
    CREATION_ROLE,
    EDITION_ROLE,
    orm_rtype,
    relinfo_for,
)


def jsonschema_adapter(cnx, **ctx):
    """Return a IJSONSchema adapter selected from ``ctx`` information."""
    return cnx.vreg['adapters'].select('IJSONSchema', cnx, **ctx)


def jsonschema_validate(schema, instance, _entity=None):
    """Validate an instance under the JSON schema."""
    try:
        jsonschema.validate(instance, schema)
    except jsonschema.ValidationError as exc:
        raise ValidationError(_entity, {None: exc.message})


def _filter_relinfo(relinfos, relinfo_to_skip):
    for rtype, role, tetypes in relinfos:
        if (rtype, role) == relinfo_to_skip:
            continue
        yield rtype, role, tetypes


class IJSONSchemaMixIn(object):

    def relinfo_for(self, schema_role):
        return relinfo_for(self.entity, schema_role)


class IJSONSchemaETypeAdapter(IJSONSchemaMixIn, Adapter):
    """IJSONSchema adapter for entity creation with `etype` specified in
    selection context.

    Subclasses may refine the selection context using ``match_kwargs``
    predicates (e.g. ``match_kwargs({'etype': 'MyEtype'})`` to override JSON
    Schema generation for a particular etype).
    """
    __regid__ = 'IJSONSchema'
    __select__ = match_kwargs('etype')

    def __repr__(self):
        return ('<{0.__class__.__name__} etype={0.etype}>'.format(self))

    @property
    def etype(self):
        """The entity type bound to this adapter."""
        return str(self.cw_extra_kwargs['etype'])

    @property
    def entity_mapper(self):
        return self._cw.vreg['mappers'].select(
            'jsonschema.entity', self._cw, etype=self.etype)

    def view_schema(self, **kwargs):
        """Return a JSON schema suitable for viewing adapted entity."""
        jsldoc = self.entity_mapper.jsl_document(VIEW_ROLE)
        return jsldoc.get_schema(**kwargs)

    def creation_schema(self, **kwargs):
        """Return a JSON schema suitable for entity creation."""
        jsldoc = self.entity_mapper.jsl_document(CREATION_ROLE)
        return jsldoc.get_schema(**kwargs)

    @property
    def entity(self):
        return self._cw.vreg['etypes'].etype_class(self.etype)(self._cw)

    def create_entity(self, instance):
        """Return a CubicWeb entity built from `instance` data matching this
        JSON schema.
        """
        jsonschema_validate(self.creation_schema(), instance)
        values = self.entity_mapper.values(None, instance)
        return self._cw.create_entity(self.etype, **values)

    def serialize(self, entities):
        """Return `entities` as a collection for JSON serialization."""
        mapper = self._cw.vreg['mappers'].select(
            'jsonschema.collection', self._cw, etype=self.etype)
        return mapper.serialize(entities)


class IJSONSchemaRelationTargetETypeAdapter(IJSONSchemaETypeAdapter):
    """IJSONSchema adapter for entity creation of an entity of `etype` related
    through `rtype` and `role` specified in selection context.
    """
    __select__ = match_kwargs('etype', 'rtype', 'role')

    def __repr__(self):
        return ('<{0.__class__.__name__} etype={0.etype} rtype={0.rtype} '
                'role={0.role}>'.format(self))

    @property
    def rtype(self):
        return self.cw_extra_kwargs['rtype']

    @property
    def role(self):
        return self.cw_extra_kwargs['role']

    def relinfo_for(self, schema_role):
        relinfo = super(IJSONSchemaRelationTargetETypeAdapter,
                        self).relinfo_for(schema_role)
        if schema_role == CREATION_ROLE:
            relinfo = _filter_relinfo(relinfo, (self.rtype, self.role))
        return relinfo

    @property
    def entity_mapper(self):
        return self._cw.vreg['mappers'].select(
            'jsonschema.entity', self._cw,
            etype=self.etype, rtype=self.rtype, role=self.role,
        )

    def create_entity(self, instance, target=None):
        """Return a CubicWeb entity related to `target` through relation
        information from selection context.
        """
        entity = super(IJSONSchemaRelationTargetETypeAdapter,
                       self).create_entity(instance)
        if target is not None:
            entity.cw_set(**{orm_rtype(self.rtype, self.role): target})
        return entity


class IJSONSchemaEntityAdapter(IJSONSchemaMixIn, EntityAdapter):
    """IJSONSchema adapter for live entities."""
    __regid__ = 'IJSONSchema'
    # Prevent this adapter from being selected in place of
    # IJSONSchemaRelatedEntityAdapter in case one picks a bad rtype/role.
    __select__ = non_final_entity() & ~match_kwargs('rtype', 'role')

    def __repr__(self):
        return ('<{0.__class__.__name__} entity={0.entity}>'.format(self))

    @property
    def etype(self):
        return self.entity.cw_etype

    @property
    def entity_mapper(self):
        return self._cw.vreg['mappers'].select(
            'jsonschema.entity', self._cw, entity=self.entity)

    def view_schema(self, **kwargs):
        """Return a JSON schema suitable for viewing adapted entity."""
        jsldoc = self.entity_mapper.jsl_document(VIEW_ROLE)
        return jsldoc.get_schema(**kwargs)

    def edition_schema(self, **kwargs):
        """Return a JSON schema suitable for editing adapted entity."""
        jsldoc = self.entity_mapper.jsl_document(EDITION_ROLE)
        return jsldoc.get_schema(**kwargs)

    def relations(self):
        """Yield (rtype, role, targettypes) for non-final relations."""
        rsection = self._cw.vreg['uicfg'].select(
            'jsonschema', self._cw, entity=self.entity)
        return rsection.relations_by_section(self.entity, 'related', 'read')

    def edit_entity(self, instance):
        """Return a CubicWeb entity built from `instance` data matching this
        JSON schema.
        """
        jsonschema_validate(self.edition_schema(), instance)
        values = {}
        values = self.entity_mapper.values(self.entity, instance)
        return self.entity.cw_set(**values)

    def serialize(self):
        """Return a dictionary of entity's data suitable for JSON
        serialization.
        """
        relinfo = self.relinfo_for(VIEW_ROLE)
        return self.entity_mapper.serialize(relinfo)


@objectify_predicate
def relation_for_entity(cls, cnx, entity, rtype, role):
    """Return 1 if `entity` has an `(rtype, role)` relation."""
    return 1 if entity.e_schema.has_relation(rtype, role) else 0


class IJSONSchemaRelatedEntityAdapter(IJSONSchemaEntityAdapter):
    """IJSONSchema adapter for entities in the context of a relation."""
    __select__ = (non_final_entity()
                  & match_kwargs('rtype', 'role') & relation_for_entity())

    def __repr__(self):
        return ('<{0.__class__.__name__} entity={0.entity} '
                'rtype={0.rtype} role={0.role}>'.format(self))

    @property
    def rtype(self):
        return self.cw_extra_kwargs['rtype']

    @property
    def role(self):
        return self.cw_extra_kwargs['role']

    def relinfo_for(self, schema_role):
        relinfo = super(IJSONSchemaRelatedEntityAdapter,
                        self).relinfo_for(schema_role)
        return _filter_relinfo(relinfo, (self.rtype, self.role))
