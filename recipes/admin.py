from django.contrib import admin

from .models import Recipe, Ingredient, Dimension, Tag, Amount, Favors, Follow, ShopList


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'get_ingredients')
    list_filter = ('pub_date', 'title')
    search_fields = ("text",)
    empty_value_display = "-empty-"


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'dimension')
    list_filter = ('title',)


class DimensionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'type_of_unit')


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'value', 'name')
    search_fields = ['title']


class AmountAdmin(admin.ModelAdmin):
    list_display = ('amount', 'ingredient', 'recipe')


class FavorsAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


class ShopListAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Dimension, DimensionAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Amount, AmountAdmin)
admin.site.register(Favors, FavorsAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(ShopList, ShopListAdmin)
