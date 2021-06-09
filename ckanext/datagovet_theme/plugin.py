from ckan.common import config

import ckan.lib.helpers as h
import ckan.model as model
import ckan.logic as logic
from ckan.lib.plugins import DefaultTranslation
import ckan.plugins as plugins
from ckan.common import _
import ckan.plugins.toolkit as toolkit
import os
from ckan.common import request
from routes.mapper import SubMapper
import mimetypes

def get_number_of_files():
    return model.Session.execute("select count(*) from resource where state = 'active'").first()[0]


def get_number_of_external_links():
    return model.Session.execute("select count(*) from resource where state = 'active' and url not LIKE '%data.gov.et%'").first()[0]


def most_popular_groups():
    '''Return a sorted list of the groups with the most datasets.'''

    # Get a list of all the site's groups from CKAN, sorted by number of datasets.
    groups = toolkit.get_action('group_list')(
        data_dict={'sort': 'package_count desc', 'all_fields': True})

    # Truncate the list to the 20 most popular groups only.
    groups = groups[:20]

    return groups


def groups():
    '''Return the groups sorted by name.'''

    # Get a list of all the site's groups from CKAN, sorted by number of datasets.
    groups = toolkit.get_action('group_list')(
        data_dict={'sort': 'name desc', 'all_fields': True})

    # Truncate the list to the 20 most popular groups only.
    groups = groups[:20]

    return groups


def get_group_select_list():
    result = []
    user = toolkit.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    groups = logic.get_action('group_list')(context, {})

    for group in groups:
        result.append({'value': group})
    return result


def group_id():
    id = request.params.get('grp') or request.params.get('groups__0__id')
    return id

class DatagovetThemePlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IResourceController, inherit=True)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.ITranslation)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'datagovet_theme')

    # Make groups mandatory. valid for API calls
    # def validate(self, context, data_dict, schema, action):
    #     # first, run the schema-based validation to get that out of the way:
    #     (data_dict, errors) = toolkit.navl_validate(data_dict, schema, context)
    #     # we're only interested if this is a create or update action:
    #     if action in [ 'package_create', 'package_update' ]:
    #         # now comes the actual validation:
    #         if 'groups' not in data_dict:
    #             errors['groups'] = errors.get('groups', []) + [ _("Required field \'groups\' not set.") ]
    #         else:
    #             if len(data_dict['groups'] < 1):
    #                 errors['groups'] = errors.get('groups', []) + [ _('\'groups\' property has no value.') ]
    #         # we should probably also check if the group exists, etc.

    #     return (data_dict, errors)

    # IRoutes
    # def after_map(self, mapping):
    #     GA_CONTROLLER = """
    #         ckanext.datagovet_theme.controllers.gacontroller:GAController"""
    #     with SubMapper(mapping, controller=GA_CONTROLLER) as m:
    #         m.connect('ga_index',
    #                   '/datagovet_theme/ga',
    #                   action='index')
    #     return mapping

    def get_helpers(self):
        return {
            'get_number_of_files': get_number_of_files,
            'get_number_of_external_links': get_number_of_external_links,
            'datagovet_theme_most_popular_groups': most_popular_groups,
            'get_group_select_list': get_group_select_list,
            'groups': groups,
            'group_id': group_id
        }

    def update_config_schema(self, schema):
        ignore_missing = toolkit.get_validator('ignore_missing')
        not_empty = toolkit.get_validator('not_empty')

        schema.update({
            'ckanext.datagovet_theme.disallowed_extensions': [ignore_missing, str],
            'ckanext.datagovet_theme.allowed_extensions': [ignore_missing, str],
            # 'groups': [not_empty],
        })

        return schema

    # IResourceController
    def before_create(self, context, resource):
        disallowed_extensions = toolkit.aslist(config.get('ckanext.datagovet_theme.disallowed_extensions',[]))
        disallowed_mimetypes = [mimetypes.types_map["." + x] for x in disallowed_extensions]

        allowed_extensions = toolkit.aslist(config.get('ckanext.datagovet_theme.allowed_extensions',[]))
        allowed_mimetypes = [mimetypes.types_map["." + x] for x in allowed_extensions]

        is_resource_extension_allowed = False
        error_message = ''
        if (type(resource['upload']) is not str):
            if allowed_mimetypes:
                if resource['upload'].type in allowed_mimetypes:
                    is_resource_extension_allowed = True
                else:
                    error_message="Doar urmatoarele extensii sunt permise: " + ", ".join(allowed_extensions) + "."
            else:
                if resource['upload'].type not in disallowed_mimetypes:
                    is_resource_extension_allowed = True
                else:
                    error_message= "Urmatoarele extensii sunt nepermise: " + ", ".join(disallowed_extensions) + "."

        # is_resource_extension_allowed = True
        if ('upload' in resource) and (type(resource['upload']) is not str) and not is_resource_extension_allowed:
            # If we did not do this, the URL field would contain the filename
            # and people can press finalize afterwards.
            resource['url'] = ''

            raise toolkit.ValidationError(['Fisierul are o extensie nepermisa! ' + error_message])
            is_resource_extension_allowed = False
        

    def before_show(context, resource_dict):
        custom_url = config.get('datagovet_theme.custom_resource_download_url')

        if custom_url:
            # We should probably treat this exception. But let it fail here. You should add ckan.site_url to the config
            old_url = config['ckan.site_url']
            resource_dict['datagovet_download_url'] = resource_dict['url'].replace(old_url, custom_url)
        else:
            resource_dict['datagovet_download_url'] = resource_dict['url']
        return resource_dict
