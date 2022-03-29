from rest_framework import serializers

from blog.models import Post


class PostSerializer(serializers.ModelSerializer):
    """Serialiers to posts model"""
    class Meta:
        model = Post
        fields = ('id', 'title', 'extract', 'author', 'release_date')
