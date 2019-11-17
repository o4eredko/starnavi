from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Post
from . import services as likes_services


class UserSerializer(serializers.HyperlinkedModelSerializer):
	posts = serializers.HyperlinkedRelatedField(many=True, view_name='post-detail', read_only=True)

	class Meta:
		model = User
		fields = ('url', 'id', 'username', 'posts')


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
