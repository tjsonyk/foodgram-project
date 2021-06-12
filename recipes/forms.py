from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from .models import Recipe, Amount, Ingredient


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ('title', 'image', 'text', 'tags', 'cooking_time')
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
    
    def save(self, request, commit=True, ingredients=None):
        #if not ingredients:
        #    self.add_error(None, 'Добавьте ингредиенты')
        recipe = super().save(commit=False)
        recipe.author = request.user
        recipe.save(commit=False)

        for item in ingredients:
            Amount.objects.create(
                amount=ingredients[item],
                ingredient=get_object_or_404(Ingredient, title=f'{item}'),
                recipe=recipe
                )
        
        self.save_m2m()
