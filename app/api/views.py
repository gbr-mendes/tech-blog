from django.core.exceptions import ValidationError
from . import serializers
from rest_framework import generics
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView
from rest_auth.registration.serializers import SocialLoginSerializer
from rest_auth.registration.views import RegisterView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .permissions import CreatePostPermissions
from .utils.exceptions import PostNotFound, UUIDInvalid

from blog import models

from .serializers import ListPostSerializer

# View to custom register rest-auth
class RegisterUserView(RegisterView):
  serializer_class = serializers.RegisterUserSerializer

# Social Authientication
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)


# Comumn views
class RetriveCreatePostsAPIView(generics.ListCreateAPIView):
    queryset = models.Post.objects.all()
    parser_classes = (MultiPartParser, FormParser, )
    authentication_classes = (TokenAuthentication,)
    
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (IsAuthenticated, CreatePostPermissions)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreatePostSerializer
        elif self.request.method == 'GET':
            return ListPostSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class EmailAPIView(generics.CreateAPIView):
    serializer_class = serializers.EmailSerializer


class ListCreateCommentAPIView(generics.ListCreateAPIView):
    def get_queryset(self):
        uid = self.request.GET.get('post_id')
        try:
            exists = models.Post.objects.filter(id=uid).exists()
        except ValidationError:
            raise UUIDInvalid
        if not exists:
            raise PostNotFound()
        comments = models.Comment.objects.filter(post=uid)
        return comments

    def get_authenticators(self):
        if self.request.method == 'POST':
            self.authentication_classes = (TokenAuthentication,)
        return super().get_authenticators()

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.RetriveCommentsSerializer
        elif self.request.method == 'POST':
            return serializers.CreateCommentSerializer

    def perform_create(self, serializer):
        uid = self.request.GET.get('post_id')
        try:
            post = models.Post.objects.filter(id=uid)[0]
        except IndexError:
            raise PostNotFound
        except ValidationError:
            raise UUIDInvalid

        return serializer.save(author=self.request.user, post=post)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = {
            'id': comment.id,
            'author': comment.author.name,
            'comment': comment.comment
        }
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)
