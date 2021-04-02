from django import forms

from .models import Recipe, Tag
from .helpers import get_ingredients



class RecipeForm(forms.ModelForm):
    #tags = forms.ModelMultipleChoiceField(
    #Tag.objects.all(), to_field_name='slug', label='Тэги',
    #widget=forms.CheckboxSelectMultiple)
    #cooking_time_minutes = forms.fields.IntegerField(
    #widget=forms.NumberInput(attrs={'class': 'form__input'}), min_value=1)

    class Meta:
        model = Recipe
        fields = ('title', 'image', 'text', 'tag', 'cooking_time')
        widgets = {
            'tag': forms.CheckboxSelectMultiple(),
        }
   
