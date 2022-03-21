from django.test import TestCase
from django.contrib.auth import get_user_model


def sample_user(email='testuser@email.com', password='testCase'):
    return get_user_model().objects.create_user(email=email, password=password)


class AccountsTest(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an emails is successful"""
        email = 'test@gbmsolucoesweb.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalize(self):
        """Test the email for a new user is normalized"""
        email = 'test@GBMSOLUCOESWEB.COM'
        user = get_user_model().objects.create_user(email, 'test123')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """
        Test if an error is raised if a user is createad with an invalid email
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_superuser(self):
        """Test crerating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@gbmsolucoesweb.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
