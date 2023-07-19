default_facet_operator = 'OR'
icons_dir = 'images/icons'
default_locale = 'es'
organization_custom_facets = False
group_custom_facets = False
debug = False

#{% set ['ttl', 'rdf', 'xml', 'n3', 'jsonld' ]

data_links=None
inspire_links=None
inspire_link="/csw/?service=CSW&version=2.0.2&request=GetRecordById&id={id}&elementSetName=full&outputSchema={schema}"

inspire_formats=[
    {
        'name':'ISO/TC 211',
        'display_name':'ISO/TC 211',
        'outputSchema':'http://www.isotc211.org/2005/gmd',
        'image_display_url': None,
        'description': 'ISO/TC 211 xml formated data',
    }
]

        
    
