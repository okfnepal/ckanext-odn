import logging
import ckan.lib.base as base
import ckan.plugins as p
import ckan.logic as logic
import ckan.model as model
import ckan.lib.captcha as captcha
import ckan.lib.navl.dictization_functions as dictization_functions
import ckan.lib.mailer as mailer
import ckan.lib.helpers as h
import socket
from pylons import config
from ckan.common import _, request, c, response
from ckanext.oknp.interfaces import ISuggestion
log = logging.getLogger(__name__)

render = base.render
abort = base.abort

DataError = dictization_functions.DataError
unflatten = dictization_functions.unflatten

check_access = logic.check_access
get_action = logic.get_action
flatten_to_string_key = logic.flatten_to_string_key

class SuggestionController(base.BaseController):

    def __before__(self, action, **env):

        super(SuggestionController, self).__before__(action, **env)

        try:
            self.context = {'model': model, 'session': model.Session, 'user': base.c.user or base.c.author, 'auth_user_obj': base.c.userobj}
            check_access('send_sugesstion', self.context)
        except logic.NotAuthorized:
            base.abort(401, _('Not authorized to use contact form'))

    @staticmethod
    def _submit(context):
    
        try:
            data_dict = logic.clean_dict(unflatten(logic.tuplize_dict(logic.parse_params(request.params))))
            c.form = data_dict['name']
            captcha.check_recaptcha(request)
        except logic.NotAuthorized:
            base.abort(401, _('Not authorized to see this page'))

        errors = {}
        error_summary = {}

        if data_dict["email"] == '':
            errors['email'] = [u'Missing Value']
            error_summary['Email'] = u'Missing value'

        if data_dict["name"] == '':
            errors['name'] = [u'Missing Value']
            error_summary['Name'] = u'Missing value'

        if data_dict["organzation"] == '':
            errors['organzation'] = [u'Missing Value']
            error_summary['Organization'] = u'Missing value'

        if data_dict["dataset_title"] == '':
            errors['dataset_title'] = [u'Missing Value']
            error_summary['Dataset'] = u'Missing value'

        if data_dict["dataset_owner"] == '':
            errors['dataset_owner'] = [u'Missing Value']
            error_summary['Dataset Owner'] = u'Missing value'

        if data_dict["url"] == '':
            errors['url'] = [u'Missing Value']
            error_summary['Url'] = u'Missing value'

        if len(errors) == 0:

            body = '\n\nOrganization:'+ data_dict["organzation"] +'\n\nData Title:'+ data_dict["dataset_title"] +'\n\nDataset Owner:'+ data_dict["dataset_owner"]+'\n\nDataset url:'+ data_dict["url"] +'%s' % data_dict["content"] 

            body += '\n\nSent by:\nName:%s\nEmail: %s\n' % (data_dict["name"], data_dict["email"])

            mail_dict = {
                'recipient_email': config.get("ckanext.suggestion.mail_to", config.get('email_to')),
                'recipient_name': config.get("ckanext.suggestion.recipient_name", config.get('ckan.site_title')),
                'subject': config.get("ckanext.suggestion.subject", 'Contact/Question from visitor'),
                'body': body,
                'headers': {'reply-to': data_dict["email"]}
            }

            # Allow other plugins to modify the mail_dict
            for plugin in p.PluginImplementations(ISuggestion):
                plugin.mail_alter(mail_dict, data_dict)

            try:
                mailer.mail_recipient(**mail_dict)
            except (mailer.MailerException, socket.error):
 
                h.flash_error(_(u'Sorry, there was an error. Please try again later'))
            else:
                data_dict['success'] = True
                
        return data_dict, errors, error_summary

    def post(self):

        data = {}
        errors = {}
        error_summary = {}

        # Submit the data
        if 'save' in request.params:
            data, errors, error_summary = self._submit(self.context)
        else:
            # Try and use logged in user values for default values
            try:
                data['name'] = base.c.userobj.fullname or base.c.userobj.name
                data['email'] = base.c.userobj.email
            except AttributeError:
                data['name'] = data['email'] = None

        if data.get('success', False):
            return p.toolkit.render('suggestion/success.html')
        else:
            vars = {'data': data, 'errors': errors, 'error_summary': error_summary}
            return p.toolkit.render('suggestion/form.html', extra_vars=vars)
        