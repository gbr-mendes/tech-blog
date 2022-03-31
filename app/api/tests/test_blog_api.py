from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from blog import models


POSTS_ENDPOINT = reverse('api:posts')


# Helper Function
def create_posts(posts):
    for post in posts:
        models.Post.objects.create(**post)


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
