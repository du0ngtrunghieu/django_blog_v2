from django import template

register = template.Library()

@register.filter(name='ifinlist')
def ifinlist(value,array):
    arr=[]
    for c in array.all():
        arr.append(c.user.id)
    if value in arr:
        return True
    else:
        return False
def class_icons(icon):
    if icon is "DW":
        return "fas fa-download"
    else:
        return "fas fa-location-arrow"