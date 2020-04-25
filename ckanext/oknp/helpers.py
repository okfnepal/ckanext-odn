from ckan.model import Session, Package, Revision
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as h
import ckan.model as model
from six import text_type

import logging


def recent_data():
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


def main_nav(*args):
    home_menu_routes = ['home.index', 'Home']
    datasets_menu_routes = ['search', 'Datasets']
    org_menu_routes = ['organizations_index', 'Organizations']
    output = h.build_nav_main(home_menu_routes,datasets_menu_routes,org_menu_routes)
    # TODO - Add realtime navigation

    return output

def user_counter():
    user_count = model.Session.query(model.User).count()
    return user_count


