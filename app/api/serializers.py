from rest_framework import serializers

from blog.models import Post


class PostSerializer(serializers.ModelSerializer):
    """Serialiers to posts model"""
    class Meta:
        model = Post
        fields = ('id', 'title', 'extract', 'author', 'release_date')

    def to_representation(self, instance):
        rep = super(PostSerializer, self).to_representation(instance)
        rep['author'] = instance.author.name
        return rep
