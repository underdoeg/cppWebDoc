from django import template

register = template.Library()

def emptyText(kind="description"):
    return "no  yet, click to edit"
    
register.tag('emptyText', emptyText)