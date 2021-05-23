from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ('title', 'image', 'text', 'tags', 'cooking_time')
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
