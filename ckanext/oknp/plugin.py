import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.model import Session, Package, Revision
import logging

import ckanext.oknp.helpers as h
import ckanext.oknp.auth as auth

_ = toolkit._ 

class OknpPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers, inherit=True)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IFacets)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'oknp')

    def _facets(self, facets_dict):
        if 'groups' in facets_dict:
            del facets_dict['groups']
        return facets_dict

    def dataset_facets(self, facets_dict, package_type):
        return self._facets(facets_dict)

    def organization_facets(self, facets_dict, organization_type,
            package_type):
        return self._facets(facets_dict)


    # ITemplateHelpers
    def get_helpers(self):
        return {
                'recent_data': h.recent_data,
                'build_nav_main': h.main_nav
            }

    ## IRoutes
    def before_map(self, map):

        map.connect('suggestion_form', '/suggest-dataset',
                    controller='ckanext.oknp.controllers.suggestion:SuggestionController',
                    action='post')
                    
        map.connect('FaqController', '/faq',
                    controller='ckanext.oknp.controllers.page:FaqController',
                    action='get')

        map.connect('page', '/terms-condition',
                    controller='ckanext.oknp.controllers.page:ConditionPageController',
                    action='get')

        map.connect('group', '/group',
                    controller='ckanext.oknp.controllers.page:Group',
                    action='redirect')

        return map
    
    def get_auth_functions(self):
        return {'send_sugesstion': auth.send_sugesstion}

