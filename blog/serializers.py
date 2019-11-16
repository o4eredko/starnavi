from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
	creation_date = serializers.DateTimeField(format='%H:%M:%S %d %b %Y', read_only=True)
	author_id = serializers.ReadOnlyField(source='author.id')
	author_username = serializers.ReadOnlyField(source='author.username')

	class Meta:
		model = Post
		fields = ('author_id', 'author_username', 'title', 'content', 'creation_date', 'url')


class UserSerializer(serializers.HyperlinkedModelSerializer):
	posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

	class Meta:
		model = User
		fields = ('id', 'username', 'posts', 'url')
