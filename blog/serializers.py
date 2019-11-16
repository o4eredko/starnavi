from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
	creation_date = serializers.DateTimeField(format='%H:%M:%S %d %b %Y', read_only=True)
	author = serializers.ReadOnlyField(source='author.username')

	class Meta:
		model = Post
		fields = ('author', 'title', 'content', 'creation_date', 'url')


class UserSerializer(serializers.ModelSerializer):
	posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())

	class Meta:
		model = User
		fields = ('id', 'username', 'posts')
