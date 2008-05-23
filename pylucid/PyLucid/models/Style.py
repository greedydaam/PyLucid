# -*- coding: utf-8 -*-
"""
    PyLucid.models.Style
    ~~~~~~~~~~~~~~~~~~~~

    Model for stylesheets.

    Last commit info:
    ~~~~~~~~~~~~~~~~~
    $LastChangedDate$
    $Rev$
    $Author$

    :copyright: 2007 by the PyLucid team.
    :license: GNU GPL v3, see LICENSE.txt for more details.
"""

import os, posixpath

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Style(models.Model):
    """
    The global stylesheet.

    On save() we try to store the CSS content into a local cache file in the
    media path. This only works, if the process has the writeability.
    In a simple shared web hosting environment, the http server runs the web
    app with the user 'nobody', so he has not the writeability. In this case,
    the stylesheet must be request via a _command url.
    Important: The method get_absolute_url() doesn't check if the local cache
    file was written succsessfully in the past! This it the job for the
    page_style plugin. The method returns allways the url to the locale cache
    file.
    """
    name = models.CharField(unique=True, max_length=150)

    createtime = models.DateTimeField(auto_now_add=True)
    lastupdatetime = models.DateTimeField(auto_now=True)

    createby = models.ForeignKey(User, related_name="style_createby",
        null=True, blank=True
    )
    lastupdateby = models.ForeignKey(User, related_name="style_lastupdateby",
        null=True, blank=True
    )

    description = models.TextField(null=True, blank=True)
    content = models.TextField()

    class Admin:
        list_display = (
            "id", "name", "description", "createtime", "lastupdatetime"
        )
        list_display_links = ("name",)
        js = ['tiny_mce/tiny_mce.js', 'js/textareas_raw.js']

    def __unicode__(self):
        return self.name

    def get_filename(self):
        """
        How to make it URL and filesystem save?
        """
        return self.name + ".css"

    def get_absolute_url(self):
        """
        Get the absolute url (without the domain/host part) for the stylesheet
        file stored in the media path.
        Important: Returns allways a link to the locale cache file, it doesn't
        check if the file exists!
        """
        filename = self.get_filename()
        url = posixpath.join(
            "",
            settings.MEDIA_URL,
            settings.PYLUCID_MEDIA_DIR,
            filename, # FIXME: url save?
        )
        return url

    def get_filepath(self):
        """
        Get the file path to the local stylesheet file.
        Important: It is not tested if the file exists!
        FIXME: How to handle special characters?
        """
        filename = self.get_filename()
        filepath = os.path.join(
            settings.MEDIA_ROOT,
            settings.PYLUCID_MEDIA_DIR,
            filename
        )
        # FIXME: Should we use os.path.abspath() ?
        return filepath

    def save(self):
        """
        Save a new or updated stylesheet.
        try to store the content into the cache file in the media path.
        """
        from PyLucid.system.utils import delete_page_cache
        filepath = self.get_filepath()
        try:
            f = file(filepath, "w") # FIXME: Encoding?
            content = self.content.encode(settings.FILE_CHARSET)
            f.write(content)
            f.close()
        except Exception, e:
            # FIXME: How can we give feedback?
#            print "Style save error:", e # Olny for dev server
            pass

        #Delete the page cache if a stylesheet was edited.
        delete_page_cache()

        super(Style, self).save() # Call the "real" save() method

    class Meta:
        db_table = 'PyLucid_style'
        app_label = 'PyLucid'