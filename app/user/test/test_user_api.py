from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

SIGN_IN_USER_URL = reverse('user:signin')
TOKEN_URL = reverse('user:login')

def sigin_in_user(**param):
    return get_user_model().objects.create_user(**param)

class SiginUserApiTest(TestCase):
    """Test the sigin user"""

    def setUp(self):
        self.client = APIClient()

    def test_sigin_user_success(self):
        """Test create user with valid payload is successful"""
        data = {
            'email': 'test@test.com',
            'password': 'testtest',
            'first_name': 'Test test',
            'last_name': 'Test'
        }    

        res = self.client.post(SIGN_IN_USER_URL, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(data['password']))
        self.assertNotIn('password', res.data)

    def test_user_exist(self):
        """Test create user that already exsist failse"""
        data = {
            'email': 'test@test.com',
            'password': 'testtest',
            'first_name': 'Test test',
            'last_name': 'Test'
        }  
        sigin_in_user(**data)
        res = self.client.post(SIGN_IN_USER_URL, data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_short(self):
        """Test that the password must be more then 7 characters"""
        data = {
            'email': 'test@test.com',
            'password': 'test',
            'first_name': 'Test test',
            'last_name': 'Test'
        }  
        res = self.client.post(SIGN_IN_USER_URL, data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=data['email']
        ).exists()
        self.assertFalse(user_exists)
    
    def test_create_token(self):
        """Test that a token is created"""
        data = {'email': 'test@test.com', 'password': 'testtest'}
        sigin_in_user(**data)
        payload = {
            'username': 'test@test.com',
            'password': 'testtest'
        }
        res = self.client.post(TOKEN_URL, payload)
        
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        sigin_in_user(email='test@test.com', password="hellohello")
        data = {
            'email': 'test@test.com', 
            'password': "testtest"
        }
        res = self.client.post(TOKEN_URL, data)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_to_user(self):
        """Test that token is not create if user doesn't exist"""
        data = {
            'email': 'test@test.com', 
            'password': "testtest"
        }
        res = self.client.post(TOKEN_URL, data)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email':'', 'password':""})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

