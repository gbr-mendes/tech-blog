from.serializers import EmailSerializer, CreatePostSerializer, ListPostSerializer
from rest_framework import generics
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView
from rest_auth.registration.serializers import SocialLoginSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser


from blog import models

from .serializers import ListPostSerializer

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
    
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()
    
    def get_authenticators(self):
        if self.request.method == 'POST':
            self.authentication_classes = (TokenAuthentication,)
        return super().get_authenticators()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreatePostSerializer
        elif self.request.method == 'GET':
            return ListPostSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class EmailAPIView(generics.CreateAPIView):
    serializer_class = EmailSerializer
