import ckan.lib.base as base
import ckan.plugins as p

class FaqController(base.BaseController):
    def get(self):
        return p.toolkit.render('static_page/faq.html')

class ConditionPageController(base.BaseController):
    def get(self):
        return p.toolkit.render('static_page/condition.html')
