from rest_framework import serializers

from .models import Ingredient, Tag, Dimension


class DimensionSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ('title',)
        model = Dimension


class IngredientSerializer(serializers.ModelSerializer):
    dimension = serializers.CharField(source='dimension.title', read_only=True)
    class Meta:
        fields = ('title', 'dimension')
        model = Ingredient


class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ('value', 'name')
        model = Tag
