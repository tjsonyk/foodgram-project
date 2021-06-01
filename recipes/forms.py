from django import forms
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
        recipe = super().save(commit=False)
        recipe.author = request.user
        recipe.save()

        if ingredients == None:
            self.add_error(None, 'Добавьте ингредиенты')

        for item in ingredients:
            Amount.objects.create(
                amount=abs(int(ingredients[item])),
                ingredient=get_object_or_404(Ingredient, title=f'{item}'),
                recipe=recipe
                )
        
        self.save_m2m()
