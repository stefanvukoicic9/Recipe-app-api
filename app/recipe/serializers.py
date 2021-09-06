from rest_framework import serializers
from django.db.models import Avg
from core.models import Ingredient, Recipe, RateRecipe

class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',) 


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer a recipe"""

    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )

    avg_rate = serializers.SerializerMethodField()

    def get_avg_rate(self, obj):
        avg = RateRecipe.objects.filter(recipe__id = obj.id).aggregate(Avg('assessment'))['assessment__avg']
        return avg

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'text', 'price', 'ingredients', 'avg_rate')
        read_only_fields = ('id', 'avg_rate', )

class RecipeDitailSerializer(RecipeSerializer):
    """Serialize a recipe detail"""

    ingredients = IngredientSerializer(many=True, read_only=True)

class RateRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = RateRecipe
        fields = ('id', 'recipe', 'assessment',)
        read_only_fields = ('id',)