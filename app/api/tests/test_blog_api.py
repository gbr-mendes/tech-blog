from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework.test import APIClient
from rest_framework import status

from blog import models


POSTS_ENDPOINT = reverse('api:posts')


# Helper Function
def create_posts(posts):
    for post in posts:
        models.Post.objects.create(**post)


def sample_category(name):
    """Create and return a sample category"""
    return models.Category.objects.create(name=name)


def sample_tag(name):
    """Create and return a sample tag"""
    return models.Tag.objects.create(name=name)


def create_group(name):
    return Group.objects.create(name=name)


class TestBlogPublicEndpoints(TestCase):
    """Test for public endpoints of the blog api"""

    def setUp(self):
        self.client = APIClient()
        self.author = get_user_model().objects.create_user(
            email="test@email.com", password="password", name="Test User"
        )
        self.postsPayload = [{
                "author": self.author,
                "title": "Lorem Ipsum",
                "extract": "Lorem ipsum do...",
                "content": "Lorem ipsum dolor sit amet,consectetur..."
            },
            {
                "author": self.author,
                "title": "Lorem Ipsum",
                "extract": "Lorem ipsum do...",
                "content": "Lorem ipsum dolor sit amet,consectetur..."
            },
            {
                "author": self.author,
                "title": "Lorem Ipsum",
                "extract": "Lorem ipsum do...",
                "content": "Lorem ipsum dolor sit amet,consectetur..."
            }
        ]

    def test_get_posts(self):
        """ Test public endpoint to get posts """
        create_posts(self.postsPayload)
        resp = self.client.get(POSTS_ENDPOINT)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        for i in range(0, len(self.postsPayload)):
            self.assertEqual(
                self.postsPayload[i]["author"].name,
                resp.data["results"][i]["author"]
            )
            self.assertEqual(
                self.postsPayload[i]["title"],
                resp.data["results"][i]["title"]
            )
            self.assertEqual(
                self.postsPayload[i]["extract"],
                resp.data["results"][i]["extract"]
            )

    def test_login_required(self):
        """Test that login is required  to create a post"""
        payload = {
            'title': 'lorem ipsum',
            'extract': 'lorem ipsum extract',
            'content': 'lorem ipsum content',
        }
        res = self.client.post(POSTS_ENDPOINT, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class TestBlogPrivateEndpoints(TestCase):
    """Test for private endpoints of the blog api"""
    def setUp(self):
        self.client = APIClient()
        self.author = get_user_model().objects.create_user(
            email="test@email.com", password="password", name="Test User"
        )
        self.client.force_authenticate(self.author)
        self.group = create_group('BlogStaff')
        self.group.user_set.add(self.author)
    
    def test_create_basic_post(self):
        """Test creating posts api method"""
        payload = {
            'title': 'lorem ipsum',
            'extract': 'lorem ipsum extract',
            'content': 'lorem ipsum content',
        }
        res = self.client.post(POSTS_ENDPOINT, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        post = models.Post.objects.get(id=res.data['id'])
        for key in payload.keys():
            if key == 'author':
                author = get_user_model().objects.get(id=payload[key])
                self.assertEqual(str(author), res.data['author'])
            else:
                self.assertEqual(payload[key], getattr(post, key))
    
    def test_create_post_with_categories(self):
        """Testing create post with categories"""
        category1 = sample_category(name='category1')
        category2 = sample_category(name='category2')

        payload = {
            'title': 'lorem ipsum',
            'extract': 'lorem ipsum extract',
            'content': 'lorem ipsum content',
            'categories': [category1.id, category2.id]
        }
        res = self.client.post(POSTS_ENDPOINT, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        post = models.Post.objects.get(id=res.data['id'])
        categories = post.categories.all()
        self.assertIn(category1, categories)
        self.assertIn(category2, categories)
    
    def test_create_post_with_tags(self):
        """Testing create post with tags"""
        tag1 = sample_tag(name='tag1')
        tag2 = sample_tag(name='tag2')

        payload = {
            'title': 'lorem ipsum',
            'extract': 'lorem ipsum extract',
            'content': 'lorem ipsum content',
            'tags': [tag1.id, tag2.id]
        }
        res = self.client.post(POSTS_ENDPOINT, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        post = models.Post.objects.get(id=res.data['id'])
        tags = post.tags.all()
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)
    
    def test_create_post_user_not_allowed(self):
        """ Test that a post is not created with a user that not satisfy the role (BlogStaff)"""
        author = get_user_model().objects.create_user(email='dumemail@test.com', password='password')
        client = APIClient()
        client.force_authenticate(author)

        payload = {
            'title': 'lorem ipsum',
            'extract': 'lorem ipsum extract',
            'content': 'lorem ipsum content',
        }

        res = client.post(POSTS_ENDPOINT, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)