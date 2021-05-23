import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from django_filters import rest_framework as rest_filters, CharFilter
from django.core.paginator import Paginator
from django.views.generic import View

from .models import (
    Recipe,
    User,
    Ingredient,
    Tag,
    Amount,
    Favors,
    ShopList,
    Follow
    )
from .forms import RecipeForm
from .serializers import (
    IngredientSerializer,
    FavorsSerializer
    )
from .helpers import get_ingredients


def tags_values(filter_values):

    if filter_values:
        recipe_list = recipe_list.filter(
            tag__value__in=filter_values).distinct().all()
        )


def index(request):
    title = 'Рецепты'
    tags_values = tags_values(request.GET.getlist('filters'))
    #tags_values = request.GET.getlist('filters')
    recipe_list = Recipe.objects.all()
    tags = Tag.objects.all()
    header = 'Рецепты'

    #if tags_values:
    #    recipe_list = recipe_list.filter(
    #        tag__value__in=tags_values).distinct().all()

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'indexNotAuth.html',
        {'title': title, 'page': page, 'tags': tags, 'header': header}
        )


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
            return redirect('main-page')
    else:
        form = RecipeForm(request.POST or None, files=request.FILES or None)
    return render(request, 'formRecipe.html', {'form': form})


@login_required
def recipe_edit(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, author__username=username, id=recipe_id)

    if request.user != recipe.author:
        return redirect('main-page', username=username, recipe_id=recipe.id)

    ingredients = get_ingredients(request)
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    if form.is_valid():
        Amount.objects.filter(recipe=recipe).delete()
        recipe = form.save(commit=False)
        recipe.save()

        for item in ingredients:
            Amount.objects.create(
                amount=ingredients[item],
                ingredient=Ingredient.objects.get(title=f'{item}'),
                recipe=recipe
                )
        form.save_m2m()
        return redirect('main-page')
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None, instance=recipe
        )
    return render(
        request,
        'formRecipe.html',
        {'form': form, 'recipe': recipe}
    )


@login_required
def recipe_delete(request, recipe_id):

    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user == recipe.author:
        recipe.delete()
    return redirect('main-page')


def recipe_view(request, username, resipe_id):
    recipe = get_object_or_404(
        Recipe,
        author__username=username,
        id=resipe_id
    )
    return render(request, 'singlePage.html', {'recipe': recipe})


class IngredientFilter(rest_filters.FilterSet):
    query = CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ['title', ]


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [rest_filters.DjangoFilterBackend]
    filterset_class = IngredientFilter


class FavorsViewSet(viewsets.ModelViewSet):
    queryset = Favors.objects.all()
    serializer_class = FavorsSerializer

    def get_object(self):
        return get_object_or_404(
            Favors, user=self.request.user, recipe=self.kwargs.get('pk'))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse({'success': True})


def favorites(request):

    tags = Tag.objects.all()
    tags_values = tags_values(request.GET.getlist('filters'))
    #tags_values = request.GET.getlist('filters')

    recipe_list = Recipe.objects.filter(
        favor__user__id=request.user.id).all()

    #if tags_values:
    #    recipe_list = recipe_list.filter(
    #        tag__value__in=tags_values).distinct().all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'favorite.html',
        {'page': page, 'paginator': paginator, 'tags': tags}
        )


class Purchases(View):

    def post(self, request):
        recipe_id = json.loads(request.body)['id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        
        ShopList.objects.get_or_create(
            user=request.user, recipe=recipe)
        return JsonResponse({'success': True})

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = get_object_or_404(User, username=request.user.username)
        obj = get_object_or_404(ShopList, user=user, recipe=recipe)
        obj.delete()
        return JsonResponse({'success': True})


def shop(request):
    shop_list = ShopList.objects.filter(user=request.user).all()
    return render(request, 'shopList.html', {'shop_list': shop_list})


def download_shop_list(request):

    def generate_shop_list(request):
        buyer = get_object_or_404(User, username=request.user.username)
        shop_list = buyer.buyer.all()
        ingredients_dict = {}

        for item in shop_list:
            for amount in item.recipe.amount_set.all():

                name = f'{amount.ingredient.title} ({amount.ingredient.dimension})'
                units = amount.amount

                if name in ingredients_dict.keys():
                    ingredients_dict[name] += units
                else:
                    ingredients_dict[name] = units

        ingredients_list = []

        for key, units in ingredients_dict.items():
            ingredients_list.append(f'{key} - {units}, ')

        return ingredients_list

    result = generate_shop_list(request)
    filename = 'shopping_list.txt'
    response = HttpResponse(result, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response


def profile(request, username):
    tags = Tag.objects.all()
    profile = get_object_or_404(User, username=username)
    tags_values = tags_values(request.GET.getlist('filters'))
    #tags_values = request.GET.getlist('filters')
    recipe_list = Recipe.objects.filter(
        author=profile.pk).all()
    header = get_object_or_404(User, username=username)

    #if tags_values:
    #    recipe_list = recipe_list.filter(tag__value__in=tags_values)

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'indexNotAuth.html',
        {
            'profile': profile,
            'recipe_list': recipe_list,
            'page': page,
            'paginator': paginator,
            'header': header,
            'tags': tags
        }
        )


class Subscription(View):

    def post(self, request):
        author_id = json.loads(request.body)['id']
        author = get_object_or_404(User, id=author_id)

        Follow.objects.get_or_create(
            user=request.user, author=author)
        return JsonResponse({'success': True})

    def delete(self, request, author_id):
        user = get_object_or_404(User, username=request.user.username)
        author = get_object_or_404(User, id=author_id)
        obj = get_object_or_404(Follow, user=user, author=author)
        obj.delete()
        return JsonResponse({'success': True})


@login_required
def subs_view(request, username):
    user = get_object_or_404(User, username=username)
    authors_list = Follow.objects.filter(user=user).all()
    paginator = Paginator(authors_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'myFollow.html',
        {'page': page, 'paginator': paginator, 'authors': authors_list, }
        )
