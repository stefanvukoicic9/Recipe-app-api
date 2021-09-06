from django.http.response import Http404
from rest_framework import viewsets, mixins
from rest_framework import generics
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db.models import Count

from core.models import Ingredient, Recipe, RateRecipe

from recipe import serializers


class IngrediendViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Menage Ingredient in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

    def get_queryset(self):
        """Return top 5  objects """
        
        return self.queryset.values('name').annotate(jobtitle_count=Count('name')).order_by('-jobtitle_count')[:5]

    def perform_create(self, serializer):
        """Create a new Ingredient"""

        serializer.save(user=self.request.user)

class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    serializer_class = serializers.RecipeSerializer
    queryset= Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrive the recipes for the authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.RecipeDitailSerializer
        
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)

class RecipeList(generics.ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeDitailSerializer
    permission_classes = [IsAuthenticated,]




class RateRecipeView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        """Rate Recipe"""
        if Recipe.objects.filter(user=self.request.user, pk=request.data['recipe']).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        if RateRecipe.objects.filter(user = request.user, recipe__id=request.data['recipe']).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        recipe_rate = RateRecipe.objects.create(user= request.user, recipe_id=request.data['recipe'], assessment=request.data['assessment'])
        serializer = serializers.RateRecipeSerializer(recipe_rate)
        
        return Response(serializer.data,status=status.HTTP_201_CREATED)