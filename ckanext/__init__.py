# encoding: utf-8

# this is a namespace package
try:
    import pkg_resources
    pkg_resources.declare_namespace(__name__)
except ImportError:
    import pkgutil
    __path__ = pkgutil.extend_path(__path__, __name__)

    
/Users/sagarg/Documents/oknp/odn/ckanext/ckanext-odn/ckanext/odn/assets/main.scss 
/Users/sagarg/Documents/oknp/odn/ckanext/ckanext-odn/ckanext/odn/public/scss/main.scss