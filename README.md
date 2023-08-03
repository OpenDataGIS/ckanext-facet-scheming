<h1 align="center">ckanext-scheming_dcat</h1>
<p align="center">

<p align="center">
    <a href="#overview">Overview</a> •
    <a href="#installation">Installation</a> •
    <a href="#configuration">Configuration</a> •
    <a href="#running-the-tests">Running the Tests</a>
</p>

## Overview
This CKAN extension provides functions and templates specifically designed to extend `ckanext-scheming` and includes DCAT enhancements to adapt CKAN Schema to [GeoDCAT-AP](./ckanext/scheming_dcat/schemas/geodcatap/geodcatap_dataset.yaml).

>**Warning**:<br>
> Requires [mjanez/ckanext-dcat](https://github.com/mjanez/ckanext-dcat), [ckan/ckanext-scheming](https://github.com/ckan/ckanext-scheming) and [ckan/ckanext-spatial](https://github.com/ckan/ckanext-spatial) to work properly.


Enhancements:
- Could use schemas for `ckanext-scheming` in the plugin like [CKAN GeoDCAT-AP schema](ckanext/scheming_dcat/schemas/geodcatap/geodcatap_datasets.yaml)
- Improve the search functionality in CKAN for custom schemas. It uses the fields defined in a scheming file to provide a set of tools to use these fields for scheming, and a way to include icons in their labels when displaying them. More info: [`ckanext-`scheming_dcat``](https://github.com/OpenDataGIS/ckanext-`scheming_dcat`)
- Add Metadata downloads for Linked Open Data formats ([`mjanez/ckanext-dcat`](https://github.com/mjanez/ckanext-dcat)) and Geospatial Metadata (ISO 19139, Dublin Core, etc. with [`mjanez/ckan-pycsw`](https://github.com/mjanez/ckanext-pycsw))
- Add i18n translations.
- Add a set of useful helpers and templates to be used with Metadata Schemas.


## Requirements
This plugin is compatible with CKAN 2.9 or later.


## Installation
```sh
cd $CKAN_VENV/src/

pip install -e "git+https://github.com/ckan/ckanext-scheming_dcat.git#egg=ckanext-scheming_dcat"
```


## Configuration
Set the plugin:

  ```ini

  # Each of the plugins is optional depending on your use
  ckan.plugins = ... scheming_dcat
  ```

### Scheming
Set the schemas you want to use with configuration options:

  ```ini

  # Each of the plugins is optional depending on your use
  ckan.plugins = scheming_dcat_datasets scheming_dcat_groups scheming_dcat_organizations
  ```

To use custom schemas in `ckanext-scheming`:

  ```ini
  # module-path:file to schemas being used
  scheming.dataset_schemas = ckanext.`scheming_dcat`:schemas/geodcatap/ckan_geodcatap.yaml
  scheming.group_schemas = ckanext.`scheming_dcat`:schemas/geodcatap/ckan_group_geodcatap.json
  scheming.organization_schemas = ckanext.`scheming_dcat`:schemas/geodcatap/ckan_org_geodcatap.json

  #   URLs may also be used, e.g:
  #
  # scheming.dataset_schemas = http://example.com/spatialx_schema.yaml

  #   Preset files may be included as well. The default preset setting is:
  scheming.presets = ckanext.`scheming_dcat`:schemas/geodcatap/presets.json

  #   The is_fallback setting may be changed as well. Defaults to false:
  scheming.dataset_fallback = false
  ```

### Facet Scheming
To configure facets, there are no mandatory sets in the config file for this extension. The following sets can be used:

  ```ini
  scheming_dcat.facet_list: [list of fields]      # List of fields in scheming file to use to faceting. Use ckan defaults if not provided.
  scheming_dcat.default_facet_operator: [AND|OR]  # OR if not defined
  scheming_dcat.icons_dir: (dir)                  # images/icons if not defined
  ```

As an example for facet list, we could suggest:

  ```ini
  scheming_dcat.facet_list = "theme groups theme_es dcat_type owner_org res_format publisher_name publisher_type frequency tags tag_uri conforms_to spatial_uri"
  ```

The same custom fields for faceting can be used when browsing organizations and groups data:

  ```ini
  scheming_dcat.organization_custom_facets = true
  scheming_dcat.group_custom_facets = true
  ```

This two last settings are not mandatory. You can omit one or both (or set them to `false`), and the default fields for faceting will be used instead.

### Icons
Icons for each field option in the [`scheming file`](ckanext/scheming_dcat/schemas/geodcatap/geodcatap_datasets.yaml) can be set in multiple ways:

- Set a root directory path for icons for each field using the `icons_dir` key in the scheming file.
- If `icons_dir` is not defined, the directory path is guessed starting from the value provided for the `scheming_dcat`.`icons_dir` parameter in the CKAN config file, adding the name of the field as an additional step to the path.
- For each option, use the `icon` setting to provide the last steps of the icon path from the field's root path defined before. This value may be just a file name or include a path to add to the icon's root directory.
- If `icon` is not used, a directory and file name are guessed from the option's value.
- Icons files are tested for existence when using `schemingdct_schema_icon` function to get them. If the file doesn't exist, the function returns `None`. Icons can be provided by any CKAN extension in its `public` directory.
- Set a default icon for a field using the default_icon setting in the scheming file. You can get it using `schemingdct_schema_get_default_icon` function, and it is your duty to decide when and where to get and use it in a template.


## Schema Types
>**Note**<br>
> [`ckanext-scheming`](https://github.com/ckan/ckanext-scheming#common-schema-keys) common schema types.

With this plugin, you can customize the group, organization, and dataset entities in CKAN. Adding and enabling a schema will modify the forms used to update and create each entity, indicated by the respective `type` property at the root level. Such as `group_type`, `organization_type`, and `dataset_type`. Non-default types are supported properly as is indicated throughout the examples.

### Schemas
Are avalaible multiple custom schemas as:

  1. [`schemas/geodcatap`](/ckanext/scheming_dcat/schemas/geodcatap/geodcatap_dataset.yaml) based on: [GeoDCAT-AP](https://inspire.ec.europa.eu/good-practice/geodcat-ap)/[INSPIRE](https://inspire.ec.europa.eu/Technical-Guidelines2/Metadata/6541) for the spanish context ([NTI-RISP](https://datos.gob.es/en/documentacion/guia-de-aplicacion-de-la-norma-tecnica-de-interoperabilidad-de-reutilizacion-de))
  2. [`schemas/dcat`](/ckanext/scheming_dcat/schemas/dcat/dcat_dataset.yaml) based on: [DCAT](https://www.w3.org/TR/vocab-dcat-3/).
  3. [`schemas/dcatap`](/ckanext/scheming_dcat/schemas/dcat/dcat_dataset.yaml) based on: [DCAT-AP](https://op.europa.eu/en/web/eu-vocabularies/dcat-ap) for the european context.

## Running the Tests
To run the tests:

    pytest --ckan-ini=test.ini ckanext/scheming/tests


























------------------------

# ckanext-scheming_dcat
>**Warning**:<br>
> Requires [mjanez/ckanext-dcat](https://github.com/mjanez/ckanext-dcat), [mjanez/ckanext-scheming](https://github.com/mjanez/ckanext-scheming) and [ckan/ckanext-spatial](https://github.com/ckan/ckanext-spatial) to work properly.

`ckanext-scheming_dcat` provides functions and templates specifically designed to extend `ckanext-scheming` and includes DCAT enhancements to adapt CKAN Schema to [GeoDCAT-AP](https://github.com/mjanez/ckanext-dcat/releases/tag/1.0.0-geodcatap).

Particulary:
- The search functionality in CKAN for custom schemas. It uses the fields defined in a scheming file to provide a set of tools to use these fields for scheming, and a way to include icons in their labels when displaying them.
- Could use the schemas for `ckanext-scheming` in the plugin like [CKAN GeoDCAT-AP schema](ckanext/scheming_dcat/schemas/geodcatap/geodcatap_dataset.yaml)
- Add Metadata downloads for Linked Open Data formats ([`mjanez/ckanext-dcat`](https://github.com/mjanez/ckanext-dcat)) and Geospatial Metadata (ISO 19139, Dublin Core, etc. with [`mjanez/ckan-pycsw`](https://github.com/mjanez/ckanext-pycsw))

>**Note**:<br>
> Use a [custom schema](ckanext/scheming_dcat/schemas/geodcatap/geodcatap_dataset.yaml) based on: [GeoDCAT-AP](https://inspire.ec.europa.eu/good-practice/geodcat-ap)/[INSPIRE](https://inspire.ec.europa.eu/Technical-Guidelines2/Metadata/6541) for the spanish context ([NTI-RISP](https://datos.gob.es/en/documentacion/guia-de-aplicacion-de-la-norma-tecnica-de-interoperabilidad-de-reutilizacion-de)).


![image](https://user-images.githubusercontent.com/96422458/235639244-4c2fc026-efec-460c-9800-62d2b5668b4a.png)



## Requirements
`scheming_dcat` is designed to provide templates and functions to be used by other extensions over it. It uses the fields defined in a scheming file to provide a set of tools to use those fields for scheming, and a way to include icons in its labels when displaying them.

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.8 and earlier | not tested    |
| 2.9             | yes           |
| 2.10            | not yet       |

Suggested values:

* "yes"
* "not tested" - I can't think of a reason why it wouldn't work
* "not yet" - there is an intention to get it working
* "no"


## Installation

To install ckanext-scheming_dcat:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

    ```bash 
    git clone https://github.com/opendatagis/ckanext-scheming_dcat.git
    cd ckanext-scheming_dcat
    pip install -e .
    pip install -r requirements.txt
    ```

3. Add `scheming_dcat` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Clear the index in solr:

	`ckan -c [route to your .ini ckan config file] search-index clear`
   
5. Modify the schema file on Solr (schema or managed schema) to add the multivalued fields added in the scheming extension used for faceting. You can add any field defined in the schema file used in the ckanext-scheming extension that you want to use for faceting.
   You must define each field with these parameters:
   - `type: string` - to avoid split the text in tokens, each individually "faceted".
   - `uninvertible: false` - as recomended by solr´s documentation 
   - `docValues: true` - to ease recovering faceted resources
   - `indexed: true` - to let ckan recover resources under this facet 
   - `stored: true` - to let the value to be recovered by queries
   - `multiValued`: well... it depends on if it is a multivalued field (several values for one resource) or a regular field (just one value). Use "true" or "false" respectively. 
   
   E.g. [`ckanext-iepnb`](https://github.com/OpenDataGIS/ckanext-iepnb) extension are ready to use these multivalued fields. You have to add this configuration fragment to solr schema in order to use them:

	
    ```xml
    <!-- Extra fields -->
      <field name="tag_uri" type="string" uninvertible="false" docValues="true" indexed="true" stored="true" multiValued="true"/>
      <field name="conforms_to" type="string" uninvertible="false" docValues="true" indexed="true" stored="true" multiValued="true"/>
      <field name="lineage_source" type="string" uninvertible="false" docValues="true" indexed="true" stored="true" multiValued="true"/>
      <field name="lineage_process_steps" type="string" uninvertible="false" docValues="true" indexed="true" stored="true" multiValued="true"/>
      <field name="reference" type="string" uninvertible="false" docValues="true" indexed="true" stored="true" multiValued="true"/>
      <field name="theme" type="string" uninvertible="false" docValues="true" indexed="true" stored="true" multiValued="true"/>
      <field name="theme_es" type="string" uninvertible="false" docValues="true" multiValued="true" indexed="true" stored="true"/>
      <field name="metadata_profile" type="string" uninvertible="false" docValues="true" multiValued="true" indexed="true" stored="true"/>
      <field name="resource_relation" type="string" uninvertible="false" docValues="true" indexed="true" stored="true" multiValued="true"/>
    ```

    >**Note**<br>
    >You can ommit any field you're not going to use for faceting, but the best policy could be to add all values at the beginning.
   	
	**Be sure to restart Solr after modify the schema.**
	
6. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

     sudo service apache2 reload
     
7. Reindex solr index:

	`ckan -c [route to your .ini ckan config file] search-index rebuild`

	Sometimes solr can issue an error while reindexing. In that case I'd try to restart solr, delete index ("search-index clear"), restart solr, rebuild index, and restart solr again.
	
	Ckan needs to "fix" multivalued fields to be able to recover values correctly for faceting, so this step must be done in order to use faceting with multivalued fields. 

## Config settings
### Config (.ini) file
To use the custom GeoDCAT-AP schema in `ckanext-scheming`:

  ```ini
  scheming.dataset_schemas = ckanext.scheming_dcat:schemas/geodcatap/geodcatap_dataset.yaml
  scheming.group_schemas = ckanext.scheming_dcat:schemas/geodcatap/geodcatap_group.json
  scheming.organization_schemas = ckanext.scheming_dcat:schemas/geodcatap/geodcatap_org.json
  scheming.presets = ckanext.scheming_dcat:schemas/geodcatap/geodcatp_presets.json
  ```

There are not mandatory sets in the config file for this extension. You can use the following sets:

  ```ini
  scheming_dcat.facet_list: [list of fields]      # List of fields in scheming file to use to faceting. Use ckan defaults if not provided.
  scheming_dcat.default_facet_operator: [AND|OR]  # OR if not defined
  scheming_dcat.icons_dir: (dir)                  # images/icons if not defined
  ```

As an example for facet list, we could suggest:

  ```ini
  scheming_dcat.facet_list = "theme groups theme_es dcat_type owner_org res_format publisher_name publisher_type frequency tags tag_uri conforms_to spatial_uri"
  ```

The same custom fields for faceting can be used when browsing organizations and groups data:

  ```ini
  scheming_dcat.organization_custom_facets = true
  scheming_dcat.group_custom_facets = true
  ```

This two last settings are not mandatory. You can omit one or both (or set them to 'false'), and the default fields for faceting will be used instead.

### Icons

Icons' location for each field option in the scheming file can be set in multiple ways:

- You can set a root directory path for icons for each field using the "icons\_dir" key in the scheming file.

- If you don´t define this key, the directory path are guessed starting from the value provided for the 
"facet\_scheming.icons\_dir" parameter ("images/icons" by default if not provided) in CKAN config file, adding the 
name of the field (field\_name) as a additional step to the path.

Having the root path for the icons used by the values for the options of a field, you must define where the 
icons for each option must be, or know where the extension will search for them by default

- For each option you can use a "icon" setting to provide the last steps of the icon path (from the field icons´ 
root path defined before). This value may be just a file name, or include a path to add to the icon´s root 
directory (_some\_name.jpg_ or _some\_dir\_name/some\_name.jpg_).

- If you don't use this setting, a directory and file name are guessed from the option´s value:

  - If the value is a url, the last two steps of the url are used to guess were the icon is. The first is added 
  to the icons' dir path guessed or defined in the previous step as a subdirectory. The second are used to 
  guess the icon's name, adding and testing "svg","png","jpg" or "gif" as possible extensions.
  - If the value is not a url, it is taken as the name of the icon (testing the extensions named before) in the 
  icons root directory for this field.
  
Icons files are tested for existence when using schemingdct\_schema\_icon function to get them. If the file doesn't exist, the 
function returns `None`. Icons can be provided by any ckan extension, in its `public` directory.

You can set a default icon for a field using the _default\_icon_ setting in the scheming file. You can get it using 
schemingdct\_schema\_get\_default\_icon function, and is your duty do decide when and where get and use it in 
a template.

Examples:

We have set `facet\_scheming.icons\_dir: images/icons` in .ini CKAN config file (or not set this parameter at all,
because this is the default value)

Defining icons in a schema file:

  ```yml
  - field_name: strange_field
  ...
    icons_dir: icons/for/strange/field
  ...
    choices:
    - value: http://some_domain.fake/level1/level2/strange_value
      label:
        en: Strange Value
        es: Valor Extraño
      description:
        en: ''
        es: 'Valor extraño para un campo extraño'
      icon: strange_value_icon.gif
      ...
  ```
    
    
Icons file for "strange_field" field will be searched in public/icons/for/strange/field directory in all CKAN extensions. Url will be
icons/for/strange/field/strange\_value\_icon.gif if file was found in any extension.

The value provided in facet\_scheming.icons\_dir (images/icons) will NOT be used to compose the url, because you have provided icons\_dir in the scheming file for this field.

Using icons not defined in the schema file:

  ```yml
  - field_name: strange_field
  ...
    choices:
    - value: http://some_domain.fake/level1/level2/strange_value
      label:
        en: Strange Value
        es: Valor Extraño
      description:
        en: ''
        es: 'Valor extraño para un campo extraño'
      ...
  ```

Directory for icons will be taken from facet\_scheming.icons\_dir, bacause you not provide a 

Directory for icons will be taken from facet\_scheming.icons\_dir, bacause you not provide a 

Url for this option will be _images/icons/strange\_field/level2/strange\_value.[ext]_,
 beeing [ext] any extension in svg, png, jpg or gif (searched in this order). 

## Developer installation

To install ckanext-scheming_dcat for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/dsanjurj/ckanext-scheming_dcat.git
    cd ckanext-scheming_dcat
    python setup.py develop
    pip install -r dev-requirements.txt


### Helpers

`scheming_dcat` provides a set of useful helpers to be used in templates

- **schemingdct\_default\_facet\_search\_operator**(): Returns the default 
facet search operator: AND/OR (string)
- **schemingdct\_decode\_json**( json\_text ): Converts a JSON formatted text
 in a python object using ckan.common.json
- **schemingdct\_organization\_name**( id ): Returns the name of the organization
 given its id. Returns None if not found
- **schemingdct\_get_facet\_label**( facet ): Returns the label of a facet as
 defined in the scheming file
- **schemingdct\_get\_facet\_items\_dict**( facet, search\_facets=None, limit=None,
 exclude\_active=False, scheming\_choices=None): Returns the list of unselected 
 facet items (objects) for the given facet, sorted by the field indicated in the request.
        Arguments:
  - facet -- the name of the facet to filter.
  - search\_facets -- dict with search facets. Taken from c.search_facets if not
   defined
  - limit -- the max. number of facet items to return. Taken from 
  c.search\_facets_limits if not defined
  - exclude\_active -- only return unselected facets.
  - scheming\_choices -- scheming choices to use to get labels from values.
   If not provided takes `display\_name` field provided by Solr
- **schemingdct\_new\_order\_url**(name, concept): Returns a url with the order
 parameter for the given facet and concept to use.  
    Based in the actual order it rotates ciclically from
     \[no order\]->[direct order]->[inverse order] for the given concept \(name or count\)
- **schemingdct\_schema\_get\_icons\_dir**(field): Gets the icons' directory
 for the given field. It can be obtained (in order of preference) from the 
 _icons\_dir_ property for the given field in the scheming file, from the 
 _facet\_scheming.icons\_dir_ value  given in CKAN configuration file, plus
  the name of the field, or from the directory named after the field name 
  in `images/icons` dir.
- **schemingdct\_schema\_get\_default\_icon**(field): Gets the default 
 icon for the given field, defined in the schemig file, o `None` if not defined.
- **schemingdct\_schema\_icon**(choice, dir=None): Search for the icon path for 
 the especified choice beside the given dir (if any). If the scheming file include a _icon_ 
 setting for the choice, this is returned (beside the given _dir_).
  If not, it takes the last fragment of the value url for the icon name, and 
  the next two fragments of the url as two steps from _dir_ to the icon file.  
  It locates the file searching for svg, png, jpeg or gif extensions in all 
  the _public_ dirs of the ckan configured extensions. If the file could be 
  located, it returns the relative url. If not, it returns `None`.
- **schemingdct\_get\_choice\_dic**(field, value): Gets the choice item for the 
  given value in field of the scheming file. 

### Templates

Also a set of useful templates and snippets are provided

- **schemingdct\_facet\_list.html** Extending ckan original facet list 
snippet, provides a way to show facet labels instead of values (which is what 
Solr provides), prepending an icon if provided. To call you must extend the template 
`package/search.html`.

- **schemingdct\_facet_search\_operator** Gives the control to select the operator used to
combine facets. 

- **multiple\_choice\_icon** Display snippet to use instead the original _multiple\_choice_ snippet
provided by the scheming extension. It adds an icon before the label of the value.

- **select\_icon** Display snippet to use instead the original _select_ snippet
provided by the scheming extension. It adds an icon before the label of the value.

- **multiple\_select-icon** Form snipet to use instead the original multiple_select to show icons 
in multiple options fileds when adding or editing a resource


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## Releasing a new version of ckanext-scheming_dcat

If ckanext-scheming_dcat should be available on PyPI you can follow these steps to publish a new version:

1. Update the version number in the `setup.py` file. See [PEP 440](http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers) for how to choose version numbers.

2. Make sure you have the latest version of necessary packages:

    pip install --upgrade setuptools wheel twine

3. Create a source and binary distributions of the new version:

       python setup.py sdist bdist_wheel && twine check dist/*

   Fix any errors you get.

4. Upload the source distribution to PyPI:

       twine upload dist/*

5. Commit any outstanding changes:

       git commit -a
       git push

6. Tag the new release of the project on GitHub with the version number from
   the `setup.py` file. For example if the version number in `setup.py` is
   0.0.1 then do:

       git tag 0.0.1
       git push --tags

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
