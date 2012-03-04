from django import template
import re

register=template.Library()

def percentage(value):
    """Returns a number as a percentage and rendered to a prescribed (hard coded) number of places"""
    places=1
    if places==0:
        out=int(round(value*100))
    else :
        out=round(value*100,places) if value else "NA"
    out=str(out)+'%'
    return out

def centile(value):
    """Converts a decimal to a centile"""
    return int(value*100)

def addyear(value,year):
    """Frankly a bit of a fudge. Makes the years work on the left side"""
    return re.sub('99$',str(year),value)

register.filter('percentage',percentage)
register.filter('centile',centile)
register.filter('addyear',addyear)

