#this is based on https://github.com/arturoc/new-OF-site/blob/master/_tools/docs_update.py

from django.core.management.base import BaseCommand, CommandError
from cppdoc.models import *
from configobj import ConfigObj
import os.path
from lxml import etree
from lxml import objectify

def getType(name):
    if not name:
        name = ""
    typeInst, created = dType.objects.get_or_create(name=name)
    if created:
        print("NEW TYPE "+name)
    return typeInst

def getAccess(name):
    if not name:
        name = ""
    typeInst, created = dAccess.objects.get_or_create(name=name)
    if created:
        print("NEW ACCESS "+name)
    return typeInst

def serialize_class(filename):
    xml = objectify.parse(filename)
    doxygen = xml.getroot()

    clazz = doxygen.compounddef

    classname = clazz.compoundname.text

    #store the class in django if necessary
    classInst, created = dClass.objects.get_or_create(name=classname)
    
    if created:
        print("NEW CLASS "+classname)
    
    if clazz.find('sectiondef')!=None:
        for section in clazz.sectiondef:
            for member in section.memberdef:
                if member.get("kind") == 'enum':
                    pass
                else:
                    if member.get("kind") == 'variable':
                        varInst, created = dClassVariable.objects.get_or_create(name=member.name.text, classRef=classInst)
                        if created:
                            print("NEW VARIABLE "+member.name.text+" in "+classname)
                        varInst.typeRef = getType(member.type.text)
                        varInst.accessRef = getAccess(member.get("prot"))
                        if created and varInst.accessRef.name == "private":
                            varInst.visible = False
                        if member.get("static") == 'yes':
                            varInst.static = True
                        else:
                            varInst.static = False
                        varInst.save()
                    if member.get("kind") == 'function':
                        funcInst, created = dClassFunction.objects.get_or_create(name=member.name.text, classRef=classInst)
                        if created:
                            print("NEW FUNCTION "+member.name.text+" in "+classname)
                            
                        paramTypes = []
                        if member.find('param') is not None:
                            for param in member.param:
                                mType = param.type
                                if mType.find("ref"):
                                    mType = mType.ref
                                paramTypes.append(getType(mType.text))
                        
                        #check if this array of paramTypes already exists for the function
                        #is there a more django native way to do this?
                        paramSets = dFunctionParamSet.objects.all().filter(functionRef=funcInst)
                        paramSet = None
                        
                        if paramSets:
                            for set in paramSets:
                                sParams = set.params.all()
                                pLen = len(sParams)
                                if pLen == 0 and len(paramTypes) == 0:
                                    paramSet = set
                                elif pLen == len(paramTypes):
                                    for i in range(0, pLen):
                                        if not sParams[i].typeRef == getType(paramTypes[i]):
                                            break

                                        if i is pLen -1:
                                            paramSet = set
                                        pass
                                
                                if paramSet is not None:
                                    break
                                
                        if not paramSet:
                            print("NEW PARAM SET "+str(member.argsstring.text))
                            paramSet = dFunctionParamSet(functionRef=funcInst, returnType=getType(member.get("type")))
                            paramSet.save()
                            for i in range(0, len(paramTypes)):
                                param = dFunctionParam(paramSetRef = paramSet, typeRef=getType(paramTypes[i]), position=i)
                                param.save()
                        
                        paramSet.returnType = getType(member.get('type'))
                        paramSet.save()
                        
                        #print(len(paramTypes))
                        #print(str(member.argsstring.text))
                        #print(member.name.text)
                        #f.write( str(member.type.text) + " " + str(member.name.text) + str(member.argsstring.text) + "\n" )
                    #f.write( "$$/code\n\n\n\n" )
    
    '''
    f = open('docs/' + classname + ".html.mako",'w')
    
    index.write("[" + classname + "](" + classname + ".html)\n\n")
    
    f.write( '<%inherit file="_templates/docs.mako" />\n' )
    f.write( '___' + classname + "___\n" )
    
    inheritsfrom = []
    if clazz.find('derivedcompoundref')!=None:
        inheritsfrom = clazz.derivedcompoundref

    variables = []
    functions = []
    enums     = []

    if clazz.find('sectiondef')!=None:
        for section in clazz.sectiondef:
            for member in section.memberdef:
                #if section.get("kind") == public TODO: access, virtual, pure virtual
                if member.get("kind") == 'enum':
                    pass
                else:
                    f.write( "$$code(lang=c++)\n" )
                    if member.get("kind") == 'variable':
                        f.write( str(member.type.text) + " " + str(member.name.text) + "\n" )
                    if member.get("kind") == 'function':
                        f.write( str(member.type.text) + " " + str(member.name.text) + str(member.argsstring.text) + "\n" )
                    f.write( "$$/code\n\n\n\n" )
    
    f.close()
    '''


class Command(BaseCommand):
    args = '<xmlFolder>'
    help = "parse a doxygen file and sync the result with the db"
    
    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError('no doxyfile specified')
        
        doxyfolderPath = args[0]
        if not os.path.isdir(doxyfolderPath):
            raise CommandError('doxygen xml folder "%s" does not exist' % doxyfolderPath)
        
        for root, dirs, files in os.walk(doxyfolderPath):
            for name in files:       
                filename = os.path.join(root, name)
                if name.find('class')==0:
                    serialize_class(filename)