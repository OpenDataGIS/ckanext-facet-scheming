import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import ckanext.facet_scheming.helpers as helpers
import ckanext.facet_scheming.validators as validators
import ckanext.facet_scheming.config as fs_config
from ckanext.scheming.plugins import SchemingDatasetsPlugin, SchemingGroupsPlugin, SchemingOrganizationsPlugin
from ckanext.facet_scheming.faceted import Faceted
from ckanext.facet_scheming.utils import init_config
from ckanext.facet_scheming import blueprint
from ckanext.facet_scheming.package_controller import PackageController
from ckan.lib.plugins import DefaultTranslation

import logging

logger = logging.getLogger(__name__)


class FacetSchemingPlugin(plugins.SingletonPlugin,
                           Faceted, 
                           PackageController, 
                           DefaultTranslation):

    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IFacets)
    plugins.implements(plugins.IPackageController)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IValidators)
    plugins.implements(plugins.IBlueprint)


# IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')

        #toolkit.add_resource('fanstatic',
        #                     'facet_scheming')

        toolkit.add_resource('assets',
                             'ckanext-facet_scheming')

        fs_config.default_locale = config_.get('ckan.locale_default',
                                               fs_config.default_locale
                                               )

        fs_config.default_facet_operator = config_.get(
            'facet_scheming.default_facet_operator',
            fs_config.default_facet_operator
            )

        fs_config.icons_dir = config_.get(
            'facet_scheming.icons_dir',
            fs_config.icons_dir
            )

        fs_config.organization_custom_facets = toolkit.asbool(
            config_.get('facet_scheming.organization_custom_facets',
                        fs_config.organization_custom_facets)
            )

        fs_config.group_custom_facets = toolkit.asbool(
            config_.get('facet_scheming.group_custom_facets',
                        fs_config.group_custom_facets
                        )
            )
        
        fs_config.debug = toolkit.asbool(
            config_.get('debug',
                        fs_config.debug
                        )
            )
        
        #Load yamls config files, if not in debug mode
        if not fs_config.debug:
            init_config()

        #configure Faceted class (parent of this)
        self.facet_load_config(config_.get(
            'facet_scheming.facet_list',
            '').split())
        
        
    def get_helpers(self):
        respuesta = dict(helpers.all_helpers)
        return respuesta
    
    def get_validators(self):
        logger.debug("Validadores: {0}".format(dict(validators.all_validators)))
        return dict(validators.all_validators)

    #IBlueprint
    def get_blueprint(self):
        return blueprint.fscheming


class FacetSchemingDatasetsPlugin(SchemingDatasetsPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IDatasetForm, inherit=True)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IValidators)

    def read_template(self):
        return 'facet_scheming/package/read.html'
    
    def resource_template(self):
        return 'facet_scheming/package/resource_read.html'

class FacetSchemingGroupsPlugin(SchemingGroupsPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IGroupForm, inherit=True)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IValidators)

    def about_template(self):
        return 'facet_scheming/group/about.html'

class SchemingOrganizationsPlugin(SchemingOrganizationsPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IGroupForm, inherit=True)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IValidators)
    
    def about_template(self):
        return 'facet_scheming/organization/about.html'

    