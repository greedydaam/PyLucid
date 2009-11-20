# coding:utf-8

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _

from redirect.models import RedirectModel


def setup_view(request):
    """
    called to setup a page entry
    TODO: This must be implemented in PyLucid, see also:
    http://pylucid.org/phpBB2/viewtopic.php?p=1551&highlight=setup+view#1551 (de)
    """
    pass


def redirect(request):
    pagetree = request.PYLUCID.pagetree
    #lang_entry = request.PYLUCID.language_entry
    
    try:
        redirect_info = RedirectModel.objects.get(pagetree=pagetree)#, language=lang_entry)
    except RedirectModel.DoesNotExist, err:
        # TODO: Don't redirect to admin panel -> Display a own create view!
        request.page_msg(
             _("Redirect entry for page: %s doesn't exist, please create.") % pagetree.get_absolute_url()
        )
        return HttpResponseRedirect(reverse("admin:redirect_redirectmodel_add"))
    
    destination_url = redirect_info.destination_url
    response_data = redirect_info.get_response_data()
    
    response_class = response_data["class"]
    response = response_class(destination_url)
    
    if settings.DEBUG or request.user.is_staff:
        request.page_msg.info(
            "You redirected from %s to %s (%s)" % (request.path, destination_url, response_data["title"])
        )
    
    return response