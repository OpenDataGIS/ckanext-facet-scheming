default_facet_operator = 'OR'
icons_dir = 'images/icons'
default_locale = 'es'
organization_custom_facets = False
group_custom_facets = False

#{% set ['ttl', 'rdf', 'xml', 'n3', 'jsonld' ]

data_links=[
    {
        'name': 'ttl',
        'display_name': 'fichero ttl',
        'image_display_url': None,
        'description': 'Descripción ttl'
    },
    {
        'name': 'rdf',
        'display_name': 'fichero rdf',
        'image_display_url': None,
        'description': 'Descripción rdf'
    },
    {
        'name': 'xml',
        'display_name': 'fichero xml',
        'image_display_url': None,
        'description': 'Descripción xml'
    },
    {
        'name': 'n3',
        'display_name': 'fichero n3',
        'image_display_url': None,
        'description': '''Notation3 o N3, como se conoce más comúnmente,
         es una forma abreviada de serialización no-XML de modelos en RDF, 
         diseñado pensando en la legibilidad por parte de humanos: N3 es 
         mucho más compacto y fácil de leer que la notación RDF/XML.'''
    },
    {
        'name': 'jsonld',
        'display_name': 'fichero jsonld',
        'image_display_url': None,
        'description': 'Descripción jsonld'
    },
]
