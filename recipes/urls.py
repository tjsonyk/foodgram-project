from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'ingredients', views.IngredientViewSet, basename='ingredients')
router.register(r'tag', views.TagViewSet)
router.register(r'dimension', views.DimensionViewSet)

urlpatterns = [
    path('', views.index, name='main-page'),
    path('new/', views.new_recipe, name='new-recipe'),
    path('', include(router.urls)),
]
