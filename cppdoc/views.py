from django.template.response import TemplateResponse
from cppdoc.models import *
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404

def index(request):
    return listClasses(request)

def listClasses(request):
    c = {}
    c["classes"] = dClass.objects.all().filter(visible=True)
    t = loader.get_template('base.html')
    rc = RequestContext(request, c)
    return HttpResponse(t.render(rc), content_type="application/xhtml+xml")
    
def classDetails(request, classname=""):
    c = {}
    c["classes"] = dClass.objects.all().filter(visible=True)
    c["activeClass"] = get_object_or_404(dClass, name=classname)

    t = loader.get_template('base.html')
    rc = RequestContext(request, c)
    return HttpResponse(t.render(rc), content_type="application/xhtml+xml")
    
def classFunctionDetail(request, classname="", functionname=""):
    c = {}
    c["classes"] = dClass.objects.all().filter(visible=True)
    c["activeClass"] = get_object_or_404(dClass, name=classname)
    c["activeClassFunction"] = get_object_or_404(dClassFunction, name=functionname, classRef=c["activeClass"])

    t = loader.get_template('base.html')
    rc = RequestContext(request, c)
    return HttpResponse(t.render(rc), content_type="application/xhtml+xml")