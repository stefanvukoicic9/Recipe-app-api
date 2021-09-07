from rest_framework import status
from rest_framework.test import APIClient

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.models import Ingredient, Recipe
from django.db.models import Count

from recipe import serializers

INGREDIENT_URL = reverse('recipe:ingredient-list')
INGREDIENT_TOP5_URL = reverse('recipe:topingredients')
def sample_recipe(user, **params):
    defaults = {
        'name': "Sample recipe",
        'text': "good recipe",
        'price': 3.4
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)

class PublicIngredientApiTest(TestCase):
    
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access to endpoint """
        
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateIngredientsApiTest(TestCase):
    
    def setUp(self) :
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'testtest'
        )
        self.client.force_authenticate(self.user)

    def test_retrive_ingredient_list(self):
        """Test Retrive ingredient list"""
        recipe = sample_recipe(user= self.user, name="test1test")
        recipe2 = sample_recipe(user= self.user, name="test2test")
        recipe3 = sample_recipe(user= self.user, name="test3test")
        recipe4 = sample_recipe(user= self.user, name="test4test")
        recipe5 = sample_recipe(user= self.user, name="test5test")

        ingredient1 = Ingredient.objects.create(user=self.user, name="Kale")
        ingredient2 = Ingredient.objects.create(user=self.user, name="Salt")
        ingredient3 = Ingredient.objects.create(user=self.user, name="egg")
        ingredient4 = Ingredient.objects.create(user=self.user, name="aa")
        ingredient5 = Ingredient.objects.create(user=self.user, name="sdas")
        ingredient6 = Ingredient.objects.create(user=self.user, name="asdf")
        ingredient7 = Ingredient.objects.create(user=self.user, name="asxx")
        ingredient8 = Ingredient.objects.create(user=self.user, name="ccc")
        ingredient9 = Ingredient.objects.create(user=self.user, name="www")
        ingredient10 = Ingredient.objects.create(user=self.user, name="aaeew")
        ingredient11 = Ingredient.objects.create(user=self.user, name="asdas")
        
        recipe.ingredients.add(ingredient1.pk, ingredient2.pk, ingredient3.pk, ingredient5.pk,ingredient8.pk,ingredient10.pk)
        recipe2.ingredients.add(ingredient1.pk, ingredient4.pk, ingredient3.pk, ingredient6.pk,ingredient8.pk,ingredient7.pk)
        recipe3.ingredients.add(ingredient9.pk, ingredient2.pk, ingredient3.pk, ingredient5.pk,ingredient8.pk,ingredient10.pk)
        recipe4.ingredients.add(ingredient11.pk, ingredient2.pk, ingredient3.pk, ingredient5.pk,ingredient8.pk,ingredient10.pk)
        recipe5.ingredients.add(ingredient1.pk, ingredient2.pk, ingredient3.pk, ingredient5.pk,ingredient8.pk,ingredient10.pk)
        
        array_ingredients =  recipe.ingredients.all() | recipe2.ingredients.all() |  recipe3.ingredients.all() | recipe4.ingredients.all()  | recipe5.ingredients.all()

        array_ingredients = array_ingredients.values('name').annotate(jobtitle_count=Count('name')).order_by('-jobtitle_count')[:5]

        serializer = serializers.IngredientSerializer(array_ingredients, many=True)
        res = self.client.get(INGREDIENT_TOP5_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)
    

    def test_create_ingredient_successful(self):
        """Test create a new ingrediant successful"""
        data = {'name': 'Cabbage'}

        self.client.post(INGREDIENT_URL, data)

        exists = Ingredient.objects.filter(user = self.user, name= data['name']).exists()

        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """Test """
        data = {'name':''}
        res = self.client.post(INGREDIENT_URL, data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)