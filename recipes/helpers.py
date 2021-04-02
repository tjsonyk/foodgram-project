from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model


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