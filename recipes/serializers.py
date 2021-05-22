from rest_framework import serializers, validators

from .models import Ingredient, Dimension, Favors


class DimensionSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('title',)
        model = Dimension
    def __str__(self):
        return self.title


class IngredientSerializer(serializers.ModelSerializer):
    dimension = serializers.StringRelatedField(many=False)
    #dimension = serializers.CharField(source='dimension.title', read_only=True)

    class Meta:
        fields = __all__
        model = Ingredient


class FavorsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Favors
        fields = __all__
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Favors.objects.all(),
                fields=['user', 'recipe']
            )
        ]
