from django.test import TestCase
from core.functions import check


class TestCheckEmailAddress(TestCase):
    
    def setUp(self) -> None:
        self.email = 'vukoicicstefan@gmail.com'
        self.email1 = 'vulestefan@gmailcom'

    def test_check_email_valid(self):
        """Test function check  email is valid"""
        res = check(self.email)
        self.assertTrue(res)

    def test_check_email_invalid(self):
        """Test function check email is invalid"""
        res = check(self.email1)
        self.assertFalse(res)
