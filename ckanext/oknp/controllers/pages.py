import ckan.lib.base as base
import ckan.plugins as p

class FaqController(base.BaseController):

   return p.toolkit.render('/faq.html')

class ConditionPageController(base.BaseController):


   return p.toolkit.render('/condition.html')
    """
    Controller for displaying a contact form
    """
class SitemapController(BaseController):
	response.headers['Content-type'] = 'text/plain'
	return p.toolkit.render('/robots.txt')
