from django.test import TestCase
from django.contrib.auth import get_user_model

from blog import models


class TestBlogModels(TestCase):
    """Tests for blog models"""
    def test_str_category(self):
        """Test that category is returned as a string"""
        CATEGORY_NAME = 'Test'
        category = models.Category.objects.create(
            name=CATEGORY_NAME
        )
        self.assertEqual(str(category), category.name)

    def test_str_tag(self):
        """Test that tag is returned as a string"""
        TAG_NAME = 'Test'
        tag = models.Tag.objects.create(
            name=TAG_NAME
        )
        self.assertEqual(str(tag), tag.name)

    def test_str_post(self):
        """Test that post is returned as a string"""
        author = get_user_model().objects.create_user(
            email="test@user.com", password="password"
        )
        post_pyload = {
            "author": author,
            "title": "Test Title Post"
        }
        post = models.Post.objects.create(**post_pyload)
        self.assertEqual(str(post), post.title)
    
    def test_str_email(self):
        """Test that email is returned as a string"""
        email = models.Email.objects.create(
            name='Test Sender',
            email='test@email.com',
            message='lorem ipsum'
        )
        self.assertEqual(str(email), email.name)
