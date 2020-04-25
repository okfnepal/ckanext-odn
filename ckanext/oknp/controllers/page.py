import ckan.lib.base as base
import ckan.plugins as p
import ckan.plugins.toolkit as toolkit

_ = toolkit._ 

class FaqController(base.BaseController):
    def get(self):
        return p.toolkit.render('static_page/faq.html')

class ConditionPageController(base.BaseController):
    def get(self):
        return p.toolkit.render('static_page/condition.html')

class Group(base.BaseController):
    def redirect(self):
        p.toolkit.abort(404, _('Page not found'))