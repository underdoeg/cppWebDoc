from django.template.response import TemplateResponse
from cppdoc.models import *
from django.http import HttpResponse
from django.template import RequestContext, loader

def index(request):
    return listClasses(request)

def listClasses(request):
    c = {}
    c["classes"] = dClass.objects.all().filter(visible=True)
    t = loader.get_template('classList.html')
    rc = RequestContext(request, c)
    return HttpResponse(t.render(rc),
    content_type="application/xhtml+xml")