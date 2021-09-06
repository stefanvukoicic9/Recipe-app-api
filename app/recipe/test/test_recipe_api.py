from rest_framework import status
from rest_framework.test import APIClient

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.models import Recipe, Ingredient

from recipe.serializers import RecipeSerializer, RecipeDitailSerializer

RECIPES_URL = reverse('recipe:recipe-list')
LIST_RECIPES_URL = reverse('recipe:recipe_list')
RECIPE_RATE_URL = reverse('recipe:rate_recipe')

def detail_url(recipe_id):
    return reverse('recipe:recipe-detail', args=[recipe_id])

def sample_recipe(user, **params):
    defaults = {
        'name': "Sample recipe",
        'text': "good recipe",
        'price': 3.4
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)

def sample_ingredient(user, name="Patetos"):
    return Ingredient.objects.create(user=user, name=name)

class PublicRecipeApiTest(TestCase):
    """Test unauthenticated recipe Api access"""
    
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeApiTest(TestCase):
    """Test unauthenticated recipe API access"""    

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            'testtest'
        )
        self.client.force_authenticate(self.user)

    def test_retrive_recipe(self):
        """Test retriving a list of recipes"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by("-id")
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_recipe_limited_to_user(self):
        """Test retriving recipes for user"""
        user2 = get_user_model().objects.create_user(
            "test1@test.com",
            'test1test'
        )

        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serilizer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serilizer.data)
        self.assertEqual(len(res.data), 1)

    def test_view_recipe_detail(self):
        recipe = sample_recipe(user=self.user)
        recipe.ingredients.add(sample_ingredient(user=self.user))

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDitailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_recipe(self):
        """Test creating a recipe"""
        data = {
            'name': 'Chocolate',
            'text': 'cokolate',
            'price': 2,
        }
        res = self.client.post(RECIPES_URL, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id= res.data['id'])
        
        for key in data.keys():
            self.assertEqual(data[key], getattr(recipe, key))

    def test_create_recipe_with_ingredient(self):
        """Test creating a ingredient"""
        ingredient1 = sample_ingredient(user=self.user, name="aaaa")
        ingredient2 = sample_ingredient(user=self.user, name="bbbb")

        data = {
            'name': 'Chocolate',
            'text': 'cokolate',
            'price': 2,
            'ingredients':[ingredient1.id, ingredient2.id]
        }
        res = self.client.post(RECIPES_URL, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data['id'])
        ingredients = recipe.ingredients.all()
        self.assertEqual(len(ingredients), 2)
        self.assertIn(ingredient2, ingredients)
    
    def test_list_recipe(self):
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(LIST_RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_create_rate_recipe_invalid(self):
        """Test create recipe invalid"""
        recipe_obj = sample_recipe(user=self.user)
        
        data = {
            'recipe': recipe_obj.pk,
            'assessment': 5
        }

        res = self.client.post(RECIPE_RATE_URL, data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_rate_recipe_success(self):
        """Test create a recipe  success"""
        user2 = get_user_model().objects.create_user(
            "test2@test.com",
            'test1test'
        )
        recipe_obj = Recipe.objects.create(user=user2, name= 'braba', text ='sssss', price= 2)
        
        data = {
            'recipe': recipe_obj.pk,
            'assessment': 5
        }
        
        res = self.client.post(RECIPE_RATE_URL, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)



