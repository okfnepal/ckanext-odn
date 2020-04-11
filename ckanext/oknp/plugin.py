import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.model import Session, Package, Revision


class OknpPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers, inherit=True)


    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'oknp')
    
    def recent_data(self):
        """
        Most recent datasets, based on the metadata_modified attr.
        Return HTML that can be rendered in the templates calling
        {{ h.most_recent() }}
        """
        packages = []
        for package in Session.query(Package).filter(Package.state == 'active',
                Package.private == False).order_by(
                Package.metadata_modified.desc()).limit(4):
            packages.append(package.as_dict())
        data = {'packages': packages, 'list_class': "unstyled dataset-list",
            'item_class': "dataset-item module-content", 'truncate': 120,
            'hide_resources': False}
        return toolkit.render_snippet('snippets/package_list.html',
        data)

    # ITemplateHelpers
    def get_helpers(self):
        return {
                'recent_data': self.recent_data,
            }
