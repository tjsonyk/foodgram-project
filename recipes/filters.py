from django_filters import rest_framework as rest_filters, CharFilter


class IngredientFilter(rest_filters.FilterSet):
    query = CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ['title', ]
