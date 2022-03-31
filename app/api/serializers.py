from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from blog.models import Post


class UserSerializer(serializers.ModelSerializer):
    """Serializers for the user object"""
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, set the password and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password',
                                            'trim_whitespace': False})

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs


class PostSerializer(serializers.ModelSerializer):
    """Serialiers to posts model"""
    class Meta:
        model = Post
        fields = ('id', 'title', 'extract', 'author', 'release_date')

    def to_representation(self, instance):
        rep = super(PostSerializer, self).to_representation(instance)
        rep['author'] = instance.author.name
        return rep
