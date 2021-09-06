from core import models
from django.test import TestCase
from django.contrib.auth import  get_user_model
from core.functions import create_owner

def sample_user(email="test@test.com", password="testtest"):
    """create a user"""
    return get_user_model().objects.create_user(email, password)

def sample_recipe(user):
    return models.Recipe.objects.create(
            user = user,
            name = 'lepa hrana',
            text = 'Steak and mushroom sauce',
            price = 2.45
        )

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        '''Test creating a new user with an email is successful'''
        email = 'test@stefan.com'
        password = 'stefan123'
        
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_owner(self):
        '''Test creating a new owner is successful'''
        email = 'stefan@hireapp.me'
        password = 'stefan123'
        
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        
        owner = create_owner(user, email)
        owner_obj = models.Owner.objects.get(user=user)

        self.assertEqual(owner.city, owner_obj.city)
        self.assertEqual(owner.state, owner_obj.state)


    def test_new_user_email_normalized(self):
        '''Test the email for a new user is nnormalized'''

        email =  'test@STEFAN.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def  test_new_user_invalid_email(self):
        """Test creating user with mo email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')
    
    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@test.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
    
    def test_ingredient_str(self):
        """Test the Ingredient  string representatnin"""

        ingredient = models.Ingredient.objects.create(
            user = sample_user(),
            name = "Cauliflower"
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        recipe = models.Recipe.objects.create(
            user = sample_user(),
            name = 'lepa hrana',
            text = 'Steak and mushroom sauce',
            price = 2.45
        )

        self.assertEqual(str(recipe), recipe.name)

    def test_rate_recipe(self):
        user = sample_user()
        user2 = get_user_model().objects.create_superuser(
            'test1@test.com',
            'test123'
        )
        recipe = sample_recipe(user2)

        
        rate_recipe = models.RateRecipe(
            user=user,
            recipe=recipe,
            assessment=int(5)
        )

        self.assertEqual(rate_recipe.assessment, int(5)) 