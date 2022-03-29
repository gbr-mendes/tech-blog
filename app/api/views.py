from rest_framework.generics import ListAPIView
from . import serializers

from blog import models


class RetrivePostsAPIView(ListAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
