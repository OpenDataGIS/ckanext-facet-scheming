default_facet_operator = 'OR'
icons_dir = 'images/icons'
default_locale = 'es'
organization_custom_facets = False
group_custom_facets = False

#{% set ['ttl', 'rdf', 'xml', 'n3', 'jsonld' ]

data_links={
    'ttl':{
        'name': 'ttl',
        'display_name': 'fichero ttl',
        'image_display_url': None,
        'description': 'Terse RDF Triple Language'
    },
    'rdf':{
        'name': 'rdf',
        'display_name': 'fichero rdf',
        'image_display_url': None,
        'description': 'Resource Description Framework, RDF'
    },
    'xml':{
        'name': 'xml',
        'display_name': 'fichero xml',
        'image_display_url': None,
        'description': 'Extended Markup Language'
    },
    'n3':{
        'name': 'n3',
        'display_name': 'fichero n3',
        'image_display_url': None,
        'description': '''Notation3'''
    },
    'jsonld':{
        'name': 'jsonld',
        'display_name': 'fichero jsonld',
        'image_display_url': None,
        'description': 'JavaScript Object Notation for Linked Data'
    },
}
