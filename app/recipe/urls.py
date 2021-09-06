from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views

router = DefaultRouter()
router.register('ingredients', views.IngrediendViewSet)
router.register('recipe', views.RecipeViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
    path('recipe_list/', views.RecipeList.as_view(), name='recipe_list'),
    path('rate_recipe/', views.RateRecipeView.as_view(), name='rate_recipe')
]