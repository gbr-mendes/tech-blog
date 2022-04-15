from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.registration.views import RegisterView
from rest_framework import serializers

from blog.models import Email, Post, Comment


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


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'comment')


class RetriveCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'author', 'comment', 'post')

        def to_representation(self, instance):
            rep = super(CreatePostSerializer, self).to_representation(instance)
            rep['author'] = instance.author.name
            return rep


class EmailSerializer(serializers.ModelSerializer):
    """ Serializer to email model """
    class Meta:
        model = Email
        fields = ('name', 'email', 'message')


class RegisterUserSerializer(RegisterSerializer):
    """Custom serializer for rest-auth endpoint to create user"""
    name = serializers.CharField()
    
    def custom_signup(self, request, user):
        user.name = self.validated_data.get('name', '')
        user.save(update_fields=['name'])
