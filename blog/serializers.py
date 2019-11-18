from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import Post
from . import services as likes_services


class UserSerializer(serializers.HyperlinkedModelSerializer):
	posts = serializers.HyperlinkedRelatedField(many=True, view_name='post-detail', read_only=True)

	class Meta:
		model = User
		fields = ('url', 'id', 'username', 'posts')


class RegistrationSerializer(serializers.ModelSerializer):
	password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
	password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

	class Meta:
		model = User
		fields = ('username', 'email', 'password', 'password2')

	def save(self):
		user = User(email=self.validated_data['email'], username=self.validated_data['username'])
		password = self.validated_data['password']
		try:
			validate_password(password)
		except ValidationError as e:
			raise serializers.ValidationError({'password': str(e)})
		password2 = self.validated_data['password2']
		if password != password2:
			raise serializers.ValidationError({'password': 'Passwords must match'})
		user.set_password(password)
		user.save()
		return user


class PostSerializer(serializers.HyperlinkedModelSerializer):
	author = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)
	author_username = serializers.ReadOnlyField(source='author.username')
	created = serializers.DateTimeField(format='%H:%M:%S %d %b %Y', read_only=True)
	is_fan = serializers.SerializerMethodField()

	class Meta:
		model = Post
		fields = ('url', 'id', 'title', 'content', 'created',
				  'author', 'author_username', 'total_likes', 'is_fan')

	def get_is_fan(self, obj) -> bool:
		user = self.context.get('request').user
		return likes_services.is_fan(obj, user)
