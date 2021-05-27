from django.contrib.auth import get_user_model

from .models import Recipe

User = get_user_model()


def get_ingredients(request):

    ingredients = {}
    for key in request.POST:
        if key.startswith('nameIngredient'):
            value_ingredient = key[15:]
            ingredients[request.POST[key]] = request.POST[
                'valueIngredient_' + value_ingredient
            ]

    return ingredients

def tags_values(filter_values):
    recipe_list = Recipe.objects.all()

    if filter_values:
        recipe_list = recipe_list.filter(
            tags__value__in=filter_values).distinct().all()
    return recipe_list