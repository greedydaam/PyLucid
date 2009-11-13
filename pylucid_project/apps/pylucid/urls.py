# coding: utf-8

"""
    PyLucid app url patterns
    ~~~~~~~~~~~~~~~~~~~~~~~~

    examples for the <url_lang_code> part:
        'de'
        'de-at'
        'de_at'
    Every lang part must have a length of 2 characters.

    Last commit info:
    ~~~~~~~~~~~~~~~~~
    $LastChangedDate$
    $Rev$
    $Author:$

    :copyleft: 2009 by the PyLucid team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""
from django.conf import settings
from django.conf.urls.defaults import patterns, url

from pylucid_project.apps.pylucid import views

urlpatterns = patterns('',
    url(r'^$', views.root_page, name='PyLucid-root_page'),

    url(r'^%s/(?P<page_id>\d+)?/(?P<url_rest>.*?)$' % settings.PYLUCID.PERMALINK_URL_PREFIX, views.permalink,
        name='PyLucid-permalink'
    ),

    url(r'^%s/(?P<filepath>[\w/\.]{4,})?$' % settings.PYLUCID.HEAD_FILES_URL_PREFIX, views.send_head_file,
        name='PyLucid-send_head_file'
    ),

    url(r'^(?P<url_lang_code>[a-zA-Z]{2}([-_][a-zA-Z]{2})*?)/$',
        views.lang_root_page, name='PyLucid-lang_root_page'
    ),

    url(r'^(?P<url_lang_code>[a-zA-Z]{2}([-_][a-zA-Z]{2})*?)/(?P<url_path>[\w/-]+?)/$',
        views.resolve_url, name='PyLucid-resolve_url'
    ),

    url(r'^(?P<url_path>[\w/-]{3,}?)/$',
        views.page_without_lang, name='PyLucid-page_without_lang'
    ),
)
