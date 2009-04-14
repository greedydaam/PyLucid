

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response

#from pylucid_project.apps.pylucid.models import Page08


def root_page(request):
    """
    Display a root page with some usefull links 
    XXX: Only for developing
    """
    context = {
        "admin_url": "/%s/" % settings.ADMIN_URL_PREFIX,
    }
    return render_to_response('pylucid/root_page.html', context)

def lang_root_page(request, lang_code):
    return HttpResponse("root page for lang: %r" % lang_code)

def resolve_url(request, lang_code, url_path):
    """ get a page """
    return HttpResponse("lang: %r path: %r" % (lang_code, url_path))



#def get_page(request, page_id):
#    page = Page08.objects.get(id=page_id)
#    context = {
#        "page": page,
#    }
#    return render_to_response('pylucid/test.html', context)
