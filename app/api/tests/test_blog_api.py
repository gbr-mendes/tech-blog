from uuid import uuid4
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework.test import APIClient
from rest_framework import status

from blog import models


POSTS_ENDPOINT = reverse('api:posts')
COMMENTS_ENDPOINT = reverse('api:comments')


# Helper Function
def create_posts(posts):
    for post in posts:
        models.Post.objects.create(**post)

def create_comments(comments):
    for comment in comments:
        models.Comment.objects.create(**comment)


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
    
    def test_create_comment(self):
        """Test creating a comment to a post"""
        author = get_user_model().objects.create_user(email='dumemail@test.com', password='password')
        client = APIClient()
        client.force_authenticate(author)
        post = models.Post.objects.create(
            author = get_user_model().objects.create_user(
                email="dumemail2@test.com",
                password="password"
            ),
            title = 'lorem ipsum',
            extract = 'lorem ipsum extract',
            content = 'lorem ipsum content',
        )

        payload = {
            "comment": 'lorem ipsum extract',
        }
        res = client.post(f"{COMMENTS_ENDPOINT}?post_id={post.id}", payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        exists = models.Comment.objects.filter(id=res.data['id']).exists()
        self.assertTrue(exists)
    
    def test_create_comment_unauthorized(self):
        """Test creating a comment with a user unauthenticated"""
        client = APIClient()
        
        post = models.Post.objects.create(
            author = get_user_model().objects.create_user(
                email="dumemail2@test.com",
                password="password"
            ),
            title = 'lorem ipsum',
            extract = 'lorem ipsum extract',
            content = 'lorem ipsum content',
        )

        payload = {
            "comment": 'lorem ipsum extract',
        }
        res = client.post(f"{COMMENTS_ENDPOINT}?post_id={post.id}", payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_comments(self):
        """Test retriving comments"""
        client = APIClient()

        post = models.Post.objects.create(
            author = get_user_model().objects.create_user(
                email="dumemail@test.com",
                password="password"
            ),
            title = 'lorem ipsum',
            extract = 'lorem ipsum extract',
            content = 'lorem ipsum content',
        )
        
        author = get_user_model().objects.create_user(
            email="dumemail2@test.com",
            password="password"
        )

        comments_payload = [
            {
                "author": author,
                "comment": 'lorem ipsum extract',
                "post": post
            },
            {
                "author": author,
                "comment": 'lorem ipsum extract',
                "post": post
            },{
                "author": author,
                "comment": 'lorem ipsum extract',
                "post": post
            },
        ]

        create_comments(comments_payload)

        res = client.get(f"{COMMENTS_ENDPOINT}?post_id={post.id}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        results = res.data["results"]

        self.assertEqual(len(comments_payload), len(results))

        for index, comment in enumerate(comments_payload):
            self.assertEqual(comment["author"].id, results[index]["author"])
            self.assertEqual(comment["comment"], results[index]["comment"])
            self.assertEqual(comment["post"].id, results[index]["post"])

    def test_get_comments_post_unknown(self):
        """Test if a nice message is returned when trying to fetch comments for a post that doesn't exist"""
        client = APIClient()
        post_id = uuid4()
        res = client.get(f"{COMMENTS_ENDPOINT}?post_id={post_id}")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["detail"], "We couldn't find the requested post!")
    
    def test_create_comment_post_unknown(self):
        """Test if a nice message is returned when trying to create a comment for a post that doesn't exist"""
        author = get_user_model().objects.create_user(email='dumemail@test.com', password='password')
        client = APIClient()
        client.force_authenticate(author)
        post_id = uuid4()

        payload = {
            "comment": 'lorem ipsum extract',
        }
        res = client.post(f"{COMMENTS_ENDPOINT}?post_id={post_id}", payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["detail"], "We couldn't find the requested post!")
    
    def test_get_comments_invalid_uuid(self):
        """Test if a nice message is returned when trying to fetch comments for a post passing an invalid uuid"""
        client = APIClient()
        post_id = "dum_id"
        res = client.get(f"{COMMENTS_ENDPOINT}?post_id={post_id}")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["detail"], "UUID passed as parameter is invalid")
    
    def test_create_comment_invalid_uuid(self):
        """Test if a nice message is returned when trying to create a comment for a post passing an invalid uuid"""
        author = get_user_model().objects.create_user(email='dumemail@test.com', password='password')
        client = APIClient()
        client.force_authenticate(author)
        post_id = "dum_id"
        payload = {
            "comment": 'lorem ipsum extract',
        }
        res = client.post(f"{COMMENTS_ENDPOINT}?post_id={post_id}", payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["detail"], "UUID passed as parameter is invalid")