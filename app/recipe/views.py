from django.db.models.query import QuerySet
from django.http.response import Http404
from rest_framework import viewsets, mixins
from rest_framework import generics
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
        """Get all ingredients"""
        return self.queryset

    def perform_create(self, serializer):
        """Create a new Ingredient"""
        serializer.save(user=self.request.user)


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    serializer_class = serializers.RecipeSerializer
    queryset= Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_ints(self, qs):
        return [int(i) for i in qs.split(',')]

    def get_queryset(self):
        """Retrive the recipes for the authenticated user"""
        queryset = self.queryset
        
        ingredients = self.request.query_params.get('ingredients')
        name = self.request.query_params.get('name')
        text = self.request.query_params.get('text')
        
        if ingredients:
            queryset = queryset.filter(ingredients__id__in=self._params_to_ints(ingredients))
        
        if name:
            queryset = queryset.filter(name=name)
        
        if text:
            queryset = queryset.filter(text__contains=text)


        return queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        
        if self.action == 'retrieve' :
            return serializers.RecipeDitailSerializer
        
        if  self.action == 'list':
            return serializers.RecipeDitailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)


class RecipeList(generics.ListAPIView):
    serializer_class = serializers.RecipeDitailSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated,]

    def _params_to_ints(self, qs):
        return [int(i) for i in qs.split(',')]

    def get_queryset(self):
        """Retrive the recipes for the authenticated user"""
        queryset = Recipe.objects.all()
        
        ingredients = self.request.query_params.get('ingredients')
        name = self.request.query_params.get('name')
        text = self.request.query_params.get('text')
        
        if ingredients:
            queryset = queryset.filter(ingredients__id__in=self._params_to_ints(ingredients))
        
        if name:
            queryset = queryset.filter(name=name)
        
        if text:
            queryset = queryset.filter(text__contains=text)


        return queryset

class RateRecipeView(generics.GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.RateRecipeSerializer

    def post(self, request, format=None):
        """Rate Recipe"""
        if Recipe.objects.filter(user=self.request.user, pk=request.data['recipe']).exists():
            return Response({'error': 'recipe is user created'},status=status.HTTP_400_BAD_REQUEST)
        
        if RateRecipe.objects.filter(user = request.user, recipe__id=request.data['recipe']).exists():
            return Response({'error': 'recipe is rated'},status=status.HTTP_400_BAD_REQUEST)
        
        if  int(request.data['assessment']) < 1 or int(request.data['assessment']) > 5:
            return Response({'error': 'assessment is not vaild'},status=status.HTTP_400_BAD_REQUEST)

        recipe_rate = RateRecipe.objects.create(user= request.user, recipe_id=request.data['recipe'], assessment=request.data['assessment'])
        serializer = serializers.RateRecipeSerializer(recipe_rate)
        
        return Response(serializer.data,status=status.HTTP_201_CREATED)



class GetMoseUsedIngredientsTop(generics.ListAPIView):
    serializer_class = serializers.IngredientSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        data = Recipe.objects.all()
        i = 1
        n = len(data)
        if n >0:
            data_qs = data[0].ingredients.all() 
        while i < n:
            data_qs |= data[i].ingredients.all()
            i +=1
            
        return data_qs.values('name').annotate(jobtitle_count=Count('name')).order_by('-jobtitle_count')[:5]