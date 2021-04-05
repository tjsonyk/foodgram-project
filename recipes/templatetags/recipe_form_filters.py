from django import template
from django.http import QueryDict

from recipes.models import Recipe, Tag

register = template.Library()

@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})

@register.filter(name='get_filter_values')
def get_filter_values(value):
    return value.getlist('filters')

@register.filter(name='get_filter_link')
def get_filter_link(request, tag):
    new_request = request.GET.copy()
    if tag.value in request.GET.getlist('filters'):
        filters = new_request.getlist('filters')
        filters.remove(tag.value)
        new_request.setlist('filters', filters)
    else:
        new_request.appendlist('filters', tag.value)
    
    return new_request.urlencode()