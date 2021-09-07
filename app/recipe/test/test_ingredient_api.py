from rest_framework import status
from rest_framework.test import APIClient

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.models import Ingredient
from django.db.models import Count
from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse('recipe:ingredient-list')

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

    # def test_retrive_ingredient_list(self):
    #     """Test Retrive ingredient list"""
    #     Ingredient.objects.create(user=self.user, name="Kale")
    #     Ingredient.objects.create(user=self.user, name="Salt")
        
    #     res = self.client.get(INGREDIENT_URL)

    #     ingredients = Ingredient.objects.all().values('name').annotate(jobtitle_count=Count('name')).order_by('-jobtitle_count')[:5]
    #     seralizer = IngredientSerializer(ingredients, many=True)
        
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data, seralizer.data)
    

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