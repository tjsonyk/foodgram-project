from django.contrib import admin

from .models import Recipe, Ingredient, Dimension

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author')
    list_filter = ('pub_date')
    empty_value_display = "-empty-"


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'dimension')


class DimensionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'type_of_unit')


admin.site.register([Recipe, Ingredient, Dimension])
