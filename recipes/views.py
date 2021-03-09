from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Recipe, User

def index(request):
    title = 'Рецепты'
    recipe_list = Recipe.objects.all()
    return render(request, 'indexNotAuth.html', {'title': title, 'recipe_list': recipe_list})
