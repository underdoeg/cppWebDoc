from django.contrib import admin
from cppdoc.models import *

admin.site.register(Category)
admin.site.register(dClass)
admin.site.register(dFunction)
admin.site.register(dClassFunction)
admin.site.register(dClassVariable)
admin.site.register(dType)
admin.site.register(dFunctionParamSet)
admin.site.register(dFunctionParam)