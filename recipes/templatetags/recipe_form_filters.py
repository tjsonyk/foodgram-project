from django import template

from recipes.models import Favors, ShopList, Follow

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


@register.filter
def favorites(user, recipe):
    return Favors.objects.filter(user=user, recipe=recipe).exists()


@register.filter
def purchases(user, recipe):
    return ShopList.objects.filter(user=user, recipe=recipe).exists()


@register.filter(name='is_follow')
def is_follow(author, user):
    return Follow.objects.filter(user=user, author=author).exists()
