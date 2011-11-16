from django.db import models
from django_markup.fields import MarkupField

class Category(models.Model):
    name = models.CharField(max_length=512, blank=True)
    details = models.TextField(blank=True)
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    
    def __unicode__(self):
        return self.name

class dClass(models.Model):
    name = models.CharField(max_length=512)
    description = models.CharField(blank=True, max_length=1024)
    details = models.TextField(blank=True)
    visible = models.BooleanField(default=True)
    category = models.ForeignKey(Category, blank=True, null=True)
    
    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
    
    def __unicode__(self):
        return self.name

class dType(models.Model):
    name = models.CharField(blank=True, max_length=256)
    classRef = models.ForeignKey(dClass, blank=True, null=True)
    description = models.CharField(blank=True, max_length=1024)
    class Meta:
        verbose_name = "Type"
        verbose_name_plural = "Types"
    
    def __unicode__(self):
        return self.name

class dAccess(models.Model):
    name = models.CharField(blank=True, max_length=256)
    description = models.CharField(blank=True, max_length=1024)
    class Meta:
        verbose_name = "access"
        verbose_name_plural = "accesses"
    
    def __unicode__(self):
        return self.name
    
class dFunctionBase(models.Model):
    name = models.CharField(max_length=512)
    description = models.CharField(blank=True, max_length=1024)
    details = models.TextField(blank=True)
    visible = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Function"
        verbose_name_plural = "Functions"

    def __unicode__(self):
        return self.name
    
class dFunction(dFunctionBase):
    category = models.ForeignKey(Category, blank=True, null=True)
    
    class Meta:
        verbose_name = "Function"
        verbose_name_plural = "Functions"

class dVariableBase(models.Model):
    typeRef = models.ForeignKey(dType, blank=True, null=True)
    name = models.CharField(blank=True, max_length=256)
    description = models.CharField(blank=True, max_length=1024)
    class Meta:
        verbose_name = "Variable"
        verbose_name_plural = "Variables"
        abstract = True
        
class dClassVariable(dVariableBase):
    classRef = models.ForeignKey(dClass)
    accessRef = models.ForeignKey(dAccess, blank=True, null=True)
    static = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)
    class Meta:
        verbose_name = "Class Variable"
        verbose_name_plural = "Class Variables"
    
    def __unicode__(self):
        return self.classRef.name+"::"+self.name

class dClassFunction(dFunctionBase):
    classRef = models.ForeignKey(dClass)
    accessRef = models.ForeignKey(dAccess, blank=True, null=True)
    static = models.BooleanField(default=False)
    virtual = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Class Function"
        verbose_name_plural = "Class Functions"
    
    def __unicode__(self):
        return str(self.classRef)+"::"+self.name+"()"

class dFunctionParamSet(models.Model):
    functionRef = models.ForeignKey(dFunctionBase)
    returnType = models.ForeignKey(dType)
    returnDescription = models.CharField(blank=True, max_length=1024)
    description = models.CharField(blank=True, max_length=1024)
    class Meta:
        verbose_name = "Function parameter set"
        verbose_name_plural = "Function parameter sets"
    
    def __unicode__(self):
        return "set for "+str(self.functionRef)
    
class dFunctionParam(dVariableBase):
    paramSetRef = models.ForeignKey(dFunctionParamSet, related_name="params")
    position = models.PositiveSmallIntegerField("Position")
    class Meta:
        ordering = ['position']
        verbose_name = "Function parameter"
        verbose_name_plural = "Function parameters"
        
    def __unicode__(self):
        return str(self.typeRef)+" for "+str(self.paramSetRef.functionRef)