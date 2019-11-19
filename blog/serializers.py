from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import Post, Like


class UserSerializer(serializers.HyperlinkedModelSerializer):
	posts = serializers.HyperlinkedRelatedField(many=True, view_name='post-detail', read_only=True)

	class Meta:
		model = User
		fields = ('url', 'id', 'username', 'posts')


class RegistrationSerializer(serializers.ModelSerializer):
	password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
	password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
	email = serializers.EmailField(label='Email address', max_length=254, required=True)

	class Meta:
		model = User
		fields = ('username', 'email', 'password', 'password2')

	def save(self):
		if User.objects.filter(email=self.validated_data['email']).exists():
			raise serializers.ValidationError('User with this e-mail already exists')
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
		if not user.is_authenticated:
			return False
		obj_type = ContentType.objects.get_for_model(obj)
		likes = Like.objects.filter(content_type=obj_type, object_id=obj.id, user=user)
		return likes.exists()
