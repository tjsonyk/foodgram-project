from django import forms

from .models import Recipe, Amount


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ('title', 'image', 'text', 'tags', 'cooking_time')
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
    
    def add_ingredients(self, ingredients=None):
        if ingredients == None:
            self.add_error(None, 'Добавьте ингредиенты')

        for item in ingredients:
            Amount.objects.create(
                amount=ingredients[item],
                ingredient=get_object_or_404(Ingredient, title=f'{item}'),
                recipe=recipe
                )if not ingredients:
            form.add_error(None, 'Добавьте ингредиенты')

        for item in ingredients:
            Amount.objects.create(
                amount=ingredients[item],
                ingredient=get_object_or_404(Ingredient, title=f'{item}'),
                recipe=recipe
                )
