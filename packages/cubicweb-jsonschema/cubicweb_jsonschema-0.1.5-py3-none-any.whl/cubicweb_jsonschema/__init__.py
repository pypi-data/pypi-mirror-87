"""cubicweb-jsonschema application package

JSON Schema for CubicWeb
"""

VIEW_ROLE = 'view'
CREATION_ROLE = 'creation'
EDITION_ROLE = 'edition'

JSONSCHEMA_MEDIA_TYPE = 'application/schema+json'


def orm_rtype(rtype, role):
    if role == 'object':
        return 'reverse_' + rtype
    return rtype


def relinfo_for(entity, schema_role):
    """Return a generator of relation information tuple (rtype, role,
    targettypes) for given schema role.
    """
    try:
        permission = {
            VIEW_ROLE: 'read',
            CREATION_ROLE: 'add',
            EDITION_ROLE: 'update',
        }[schema_role]
    except KeyError:
        raise ValueError('unhandled schema role "{0}" in {1}'.format(
            schema_role, entity))
    rsection = entity._cw.vreg['uicfg'].select(
        'jsonschema', entity._cw, entity=entity)
    return rsection.relations_by_section(entity, 'inlined', permission)
