from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

REGISTER_USER_URL = reverse('rest_auth_register')


class PublicAPITeste(TestCase):
    """ Tests for publics endpoints """
    def setUp(self):
        self.client = APIClient()
    

    def test_create_user_with_name_successfuly(self):
        """Test that name is stored when create a user"""
        user_payload = {
            "name": "User Test Name",
            "email": "dumemail@test.com",
            "password1": "testPassword#",
            "password2": "testPassword#"
        }

        res = self.client.post(REGISTER_USER_URL, user_payload)
        user = get_user_model().objects.get(email = user_payload["email"])
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.name, user_payload["name"])
