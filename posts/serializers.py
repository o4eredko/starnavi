from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Post


class UserSerializer(serializers.HyperlinkedModelSerializer):
	posts = serializers.HyperlinkedRelatedField(many=True, view_name='post-detail', read_only=True)

	class Meta:
		model = User
		fields = ('url', 'id', 'username', 'posts')


class PostSerializer(serializers.HyperlinkedModelSerializer):
	author = serializers.ReadOnlyField(source='author.username')
	created = serializers.DateTimeField(format='%H:%M:%S %d %b %Y', read_only=True)

	class Meta:
		model = Post
		fields = ('url', 'id', 'title', 'content', 'created', 'author')

