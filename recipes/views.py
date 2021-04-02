from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, serializers, viewsets
from django_filters import rest_framework as rest_filters, NumberFilter, CharFilter
import django_filters

from .models import Recipe, User, Ingredient, Tag, Dimension, Amount
from .forms import RecipeForm
from .serializers import IngredientSerializer, TagSerializer, DimensionSerializer
from .helpers import get_ingredients

def index(request):
    title = 'Рецепты'
    recipe_list = Recipe.objects.all()
    return render(request, 'indexNotAuth.html', {'title': title, 'recipe_list': recipe_list})

@login_required
def new_recipe(request):
    if request.method == 'POST':
        ingredients = get_ingredients(request)
        form = RecipeForm(data=request.POST, files=request.FILES)
        if not ingredients:
            form.add_error(None, 'Добавьте ингредиенты')
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            for item in ingredients:
                Amount.objects.create(
                    amount=ingredients[item],
                    ingredient=Ingredient.objects.get(title=f'{item}'),
                    recipe=recipe)
            form.save_m2m()
            return redirect('/new/')
    else:
        form = RecipeForm(request.POST, files=request.FILES)
    return render(request, 'formRecipe.html', {'form': form})


class IngredientFilter(rest_filters.FilterSet):
    query = CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ['title',]

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [rest_filters.DjangoFilterBackend]
    filterset_class = IngredientFilter


class DimensionViewSet(viewsets.ModelViewSet):
    queryset = Dimension.objects.all()
    serializer_class = DimensionSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Ingredient
        fields = ['title',]