from rest_framework import serializers, validators

from .models import Ingredient, Dimension, Favors


class DimensionSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('title',)
        model = Dimension


class IngredientSerializer(serializers.ModelSerializer):
    dimension = serializers.CharField(source='dimension.title', read_only=True)

    class Meta:
        fields = ('title', 'dimension')
        model = Ingredient


class FavorsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Favors
        fields = ['user', 'recipe']
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Favors.objects.all(),
                fields=['user', 'recipe']
            )
        ]
