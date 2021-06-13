from django.contrib.auth import get_user_model

from .models import Recipe

User = get_user_model()


def get_ingredients(request):
    ingredients = {}

    for key, name in request.POST.items():
        if key.startswith('nameIngredient'):
            num = key.split('_')[1]
            ingredients[name] = request.POST[
                f'valueIngredient_{num}'
            ]
    return ingredients

def tags_values(filter_values, recipe_list):

    if filter_values:
        recipe_list = recipe_list.filter(
            tags__value__in=filter_values).distinct().all()
    return recipe_list