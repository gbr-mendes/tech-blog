from.serializers import EmailSerializer
from rest_framework import generics
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView
from rest_auth.registration.serializers import SocialLoginSerializer


from blog import models

from .serializers import PostSerializer

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
class RetrivePostsAPIView(generics.ListAPIView):
    queryset = models.Post.objects.all()
    serializer_class = PostSerializer


class EmailAPIView(generics.CreateAPIView):
    serializer_class = EmailSerializer
