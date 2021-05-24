from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(
    r'ingredients',
    views.IngredientViewSet,
    basename='ingredients'
    )
router.register('favorites', views.FavorsViewSet, basename='favorites')

urlpatterns = [
    path('', views.index, name='main-page'),
    path('', include(router.urls)),
    path("recipe/<str:username>/", views.profile, name='profile'),
    path('favorite/', views.favorites, name='favorite'),
    path('subscription/<str:username>/', views.subs_view, name='subscription'),
    path('subscriptions/', views.Subscription.as_view(), name='add_subs'),
    path(
        'subscriptions/<int:author_id>/',
        views.Subscription.as_view(),
        name='remove_subs'
        ),
    path(
        'recipe/<int:recipe_id>/delete/',
        views.recipe_delete,
        name='recipe_delete'
        ),
    path('<str:username>/<int:recipe_id>/', views.recipe_view, name='recipe'),
    path('new/', views.new_recipe, name='new-recipe'),
    path(
        '<str:username>/<int:recipe_id>/edit/',
        views.recipe_edit,
        name='recipe_edit'
        ),
    path('shop/', views.shop, name='shop'),
    path('shop/download/', views.download_shop_list, name='download'),
    path('purchases/', views.Purchases.as_view(), name='add_to_shop'),
    path(
        'purchases/<int:recipe_id>/',
        views.Purchases.as_view(),
        name='remove_from_shop'
        ),

]
