from rest_framework import generics
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

from blog import models

from .serializers import PostSerializer

# Social Authientication
class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

class RetrivePostsAPIView(generics.ListAPIView):
    queryset = models.Post.objects.all()
    serializer_class = PostSerializer
