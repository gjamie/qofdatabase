from django import template
import re

register=template.Library()

def percentage(value):
    places=1
    if places==0:
        out=int(round(value*100))
    else :
        out=round(value*100,places)
    out=str(out)+'%'
    return out

def centile(value):
    return int(value*100)

def addyear(value,year):
    return re.sub('99$',str(year),value)

register.filter('percentage',percentage)
register.filter('centile',centile)
register.filter('addyear',addyear)
