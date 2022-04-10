from dataclasses import fields
from rest_framework import serializers

from blog.models import Email, Post


class ListPostSerializer(serializers.ModelSerializer):
    """Serialiers to posts model"""
    class Meta:
        model = Post
        fields = ('id', 'title', 'extract', 'author', 'release_date')

    def to_representation(self, instance):
        rep = super(ListPostSerializer, self).to_representation(instance)
        rep['author'] = instance.author.name
        return rep

class CreatePostSerializer(serializers.ModelSerializer):
    """Serialiers to posts model"""
    class Meta:
        model = Post
        fields = ('id', 'title', 'extract', 'content', 'main_image', 'release_date', 'categories', 'tags')

    def to_representation(self, instance):
        rep = super(CreatePostSerializer, self).to_representation(instance)
        rep['author'] = instance.author.name
        return rep


class EmailSerializer(serializers.ModelSerializer):
    """ Serializer to email model """
    class Meta:
        model = Email
        fields = ('name', 'email', 'message')