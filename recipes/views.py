from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import filters, mixins, serializers, viewsets
from django_filters import rest_framework as rest_filters, NumberFilter, CharFilter
import django_filters
from django.core.paginator import Paginator

from .models import Recipe, User, Ingredient, Tag, Dimension, Amount
from .forms import RecipeForm
from .serializers import IngredientSerializer, TagSerializer, DimensionSerializer
from .helpers import get_ingredients

def index(request):
    title = 'Рецепты'
    tags_values = request.GET.getlist('filters')
    recipe_list = Recipe.objects.all()
    tags = Tag.objects.all()

    if tags_values:
        recipe_list = recipe_list.filter(
            tag__value__in=tags_values).distinct().all()

    paginator = Paginator(recipe_list, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'indexNotAuth.html', {'title': title, 'page': page, 'tags': tags})

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