# coding: utf-8

"""
    PyLucid.admin
    ~~~~~~~~~~~~~~

    Register all PyLucid model in django admin interface.

    Last commit info:
    ~~~~~~~~~~~~~~~~~
    $LastChangedDate$
    $Rev$
    $Author$

    :copyleft: 2008 by the PyLucid team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from django.contrib import admin
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from reversion.admin import VersionAdmin

from pylucid import models
from pylucid.system.auto_model_info import UpdateInfoBaseAdmin

#_____________________________________________________________________________
# Some work-a-rounds for django bugs :(

# Quick work-a-round for http://code.djangoproject.com/ticket/10061
admin.site.root_path = "/%s/" % settings.ADMIN_URL_PREFIX

#-----------------------------------------------------------------------------
# add user brocken, if TEMPLATE_STRING_IF_INVALID != ""
# http://code.djangoproject.com/ticket/11176
from django.contrib.auth.admin import UserAdmin

org_add_view = UserAdmin.add_view
def ugly_patched_add_view(*args, **kwargs):
    old = settings.TEMPLATE_STRING_IF_INVALID
    settings.TEMPLATE_STRING_IF_INVALID = ""
    result = org_add_view(*args, **kwargs)
    settings.TEMPLATE_STRING_IF_INVALID = old
    return result

UserAdmin.add_view = ugly_patched_add_view
    

#------------------------------------------------------------------------------


class PageTreeAdmin(UpdateInfoBaseAdmin, VersionAdmin):
    #prepopulated_fields = {"slug": ("title",)}    

    list_display = (
        "slug", "site", "get_absolute_url", "description",
        "lastupdatetime", "lastupdateby"
    )
    list_display_links = ("slug", "get_absolute_url")
    list_filter = ("site", "type", "design", "createby", "lastupdateby", )
    date_hierarchy = 'lastupdatetime'
    search_fields = ("slug", "description")

admin.site.register(models.PageTree, PageTreeAdmin)


class LanguageAdmin(VersionAdmin):
    pass

admin.site.register(models.Language, LanguageAdmin)


class PageMetaAdmin(UpdateInfoBaseAdmin, VersionAdmin):
    list_display = ("title_or_slug", "get_absolute_url", "get_site", "lastupdatetime", "lastupdateby",)
    list_display_links = ("title_or_slug", "get_absolute_url")
    list_filter = ("lang", "keywords", "createby", "lastupdateby")
    date_hierarchy = 'lastupdatetime'
    search_fields = ("description", "keywords")

admin.site.register(models.PageMeta, PageMetaAdmin)


class PageContentAdmin(UpdateInfoBaseAdmin, VersionAdmin):
    list_display = ("title_or_slug", "get_absolute_url", "get_site", "lastupdatetime", "lastupdateby",)
    list_display_links = ("title_or_slug", "get_absolute_url")
    list_filter = ("lang", "markup", "createby", "lastupdateby",)
    date_hierarchy = 'lastupdatetime'
    search_fields = ("content", "title_or_slug", "get_absolute_url")

admin.site.register(models.PageContent, PageContentAdmin)


class PluginPageAdmin(UpdateInfoBaseAdmin, VersionAdmin):
    list_display = (
        "get_plugin_name", "get_absolute_url", "app_label", "get_site", "lastupdatetime", "lastupdateby",
    )
    list_display_links = ("get_plugin_name", "app_label")
    list_filter = ("createby", "lastupdateby",)
    date_hierarchy = 'lastupdatetime'
    search_fields = ("app_label",)

admin.site.register(models.PluginPage, PluginPageAdmin)


class DesignAdmin(UpdateInfoBaseAdmin, VersionAdmin):    
    list_display = ("name", "template", "lastupdatetime", "lastupdateby")
    list_display_links = ("name",)
    list_filter = ("site", "template", "createby", "lastupdateby")
    search_fields = ("name", "template")

admin.site.register(models.Design, DesignAdmin)


class EditableHtmlHeadFileAdmin(UpdateInfoBaseAdmin, VersionAdmin):
    list_display = ("filename", "description", "lastupdatetime", "lastupdateby")
    list_display_links = ("filename", "description")
    list_filter = ("site",)

admin.site.register(models.EditableHtmlHeadFile, EditableHtmlHeadFileAdmin)


#------------------------------------------------------------------------------


class PyLucidUserAdmin(UserAdmin):
    """
    extended version of User Model Admin class.
    Add hooks for creating/deleting UserProfile model entries.
    
    We can use signals for this. But in singals handler, we get no request object.
    Here we can give the request object into UserProfile methods for sending
    feedback to the user and we need it for UpdateInfoBaseModel.
    """
    def log_addition(self, request, object):
        """ called, after a new user created -> Create the UserProfile entry """
        super(PyLucidUserAdmin, self).log_addition(request, object)
        models.UserProfile.objects.create_user_profile(request, object)
        
    def log_deletion(self, request, object, object_repr):
        """ called, after a user was deleted -> Delete the UserProfile entry """
        super(PyLucidUserAdmin, self).log_deletion(request, object, object_repr)
        models.UserProfile.objects.delete(request, object)
        
# Change the User Admin class with our externed version 
admin.site.unregister([User])
admin.site.register(User, PyLucidUserAdmin)


class UserProfileAdmin(UpdateInfoBaseAdmin, VersionAdmin):
    list_display = ("user", "site_info", "lastupdatetime", "lastupdateby")
    list_display_links = ("user",)
    list_filter = ("site",)

admin.site.register(models.UserProfile, UserProfileAdmin)