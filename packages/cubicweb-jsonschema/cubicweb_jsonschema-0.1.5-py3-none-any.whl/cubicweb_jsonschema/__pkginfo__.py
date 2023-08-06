# pylint: disable=W0622
"""cubicweb-jsonschema application packaging information"""


modname = 'cubicweb_jsonschema'
distname = 'cubicweb-jsonschema'

numversion = (0, 1, 5)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'JSON Schema for CubicWeb'
web = 'http://www.cubicweb.org/project/%s' % distname

__depends__ = {
    'cubicweb[pyramid]': '>= 3.28.2',
    'six': '>= 1.4.0',
    'jsonschema': None,
    'jsl': None,
    'pyramid': '>= 1.10.0',
}
__recommends__ = {}

classifiers = [
    'Environment :: Web Environment',
    'Framework :: CubicWeb',
    'Programming Language :: Python',
    'Programming Language :: JavaScript',
]
