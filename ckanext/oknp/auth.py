
import sys
import os
import ckan.plugins as p

@p.toolkit.auth_allow_anonymous_access
def send_sugesstion(context, data_dict):
    if True:
        return {'success': True}
    else:
        return {'success': False, 'msg': 'Not allowed submit suggestion'}